#!/usr/bin/env python3
"""Validate the repository collaboration contract."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

REQUIRED_FILES = (
    "README.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "project-configuration.md",
    "repository-settings.md",
    ".github/project-contract.json",
    ".github/pull_request_template.md",
    ".github/ISSUE_TEMPLATE/task.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/repository-contract.yml",
    "Makefile",
    "requirements-dev.txt",
)

PR_TEMPLATE_SECTIONS = (
    "## 왜 바꾸나요?",
    "## 다른 부분에 미치는 영향",
    "## 어떻게 확인했나요?",
    "## 아직 확인하지 못한 것과 다음 할 일",
    "## 문제가 생겼을 때 되돌리는 방법",
    "## 올리기 전 확인",
)

ISSUE_FIELDS = (
    "purpose",
    "type",
    "subsystem",
    "priority",
    "gate",
    "acceptance",
    "verification",
    "dependencies",
)

DROPDOWN_FIELDS = {
    "type": "유형",
    "subsystem": "Subsystem",
    "priority": "Priority",
    "gate": "Gate",
}

ISSUE_FIELD_TYPES = {
    "purpose": "textarea",
    "type": "dropdown",
    "subsystem": "dropdown",
    "priority": "dropdown",
    "gate": "dropdown",
    "acceptance": "textarea",
    "verification": "textarea",
    "dependencies": "textarea",
}

ACTION_SHA = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")


class GitHubLoader(yaml.SafeLoader):
    """YAML loader that follows YAML 1.2 booleans for GitHub's `on` key."""


for first_character, resolvers in list(GitHubLoader.yaml_implicit_resolvers.items()):
    GitHubLoader.yaml_implicit_resolvers[first_character] = [
        resolver for resolver in resolvers if resolver[0] != "tag:yaml.org,2002:bool"
    ]
GitHubLoader.add_implicit_resolver(
    "tag:yaml.org,2002:bool",
    re.compile(r"^(?:true|false)$", re.IGNORECASE),
    list("tTfF"),
)


def load_yaml(path: Path, errors: list[str]) -> Any | None:
    try:
        return yaml.load(path.read_text(encoding="utf-8"), Loader=GitHubLoader)
    except (OSError, yaml.YAMLError) as error:
        errors.append(f"invalid YAML in {path.as_posix()}: {error}")
        return None


def load_project_contract(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid project contract JSON: {error}")
        return None
    if not isinstance(data, dict) or not isinstance(data.get("fields"), dict):
        errors.append("project contract must define a fields object")
        return None
    return data


def validate_issue_form(
    form: Any, contract: dict[str, Any], errors: list[str]
) -> None:
    if not isinstance(form, dict) or not isinstance(form.get("body"), list):
        errors.append("Issue Form must define a body list")
        return

    for key in ("name", "description", "title"):
        value = form.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Issue Form {key} must be a non-empty string")

    field_items = [
        item
        for item in form["body"]
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]
    field_ids = [item["id"] for item in field_items]
    if len(field_ids) != len(set(field_ids)):
        errors.append("Issue Form field IDs must be unique")
    fields = {item["id"]: item for item in field_items}

    for field_id in ISSUE_FIELDS:
        field = fields.get(field_id)
        if field is None:
            errors.append(f"Issue Form is missing field: {field_id}")
            continue
        expected_type = ISSUE_FIELD_TYPES[field_id]
        if field.get("type") != expected_type:
            errors.append(
                f"Issue Form field {field_id} must use type {expected_type}"
            )
        attributes = field.get("attributes")
        label = attributes.get("label") if isinstance(attributes, dict) else None
        if not isinstance(label, str) or not label.strip():
            errors.append(f"Issue Form field {field_id} must define a label")
        validations = field.get("validations")
        if not isinstance(validations, dict) or validations.get("required") is not True:
            errors.append(f"Issue Form field {field_id} must be required")

    project_fields = contract["fields"]
    for form_id, project_name in DROPDOWN_FIELDS.items():
        field = fields.get(form_id)
        if field is None:
            continue
        attributes = field.get("attributes")
        options = attributes.get("options") if isinstance(attributes, dict) else None
        if options != project_fields.get(project_name):
            errors.append(
                f"Issue Form options for {project_name} do not match project contract"
            )


def validate_issue_config(
    config: Any, contract: dict[str, Any], errors: list[str]
) -> None:
    if not isinstance(config, dict):
        errors.append("Issue template config must be an object")
        return
    if config.get("blank_issues_enabled") is not False:
        errors.append("blank issues must remain disabled")
    links = config.get("contact_links")
    urls = [link.get("url") for link in links or [] if isinstance(link, dict)]
    if contract.get("project_url") not in urls:
        errors.append("Issue template config must link the live Project")


def validate_workflow(workflow: Any, errors: list[str]) -> None:
    if not isinstance(workflow, dict):
        errors.append("repository-contract workflow must be an object")
        return

    events = workflow.get("on")
    if not isinstance(events, dict) or "pull_request" not in events:
        errors.append("repository-contract workflow must run on pull_request")
    push = events.get("push") if isinstance(events, dict) else None
    branches = push.get("branches") if isinstance(push, dict) else None
    if not isinstance(branches, list) or "main" not in branches:
        errors.append("repository-contract workflow must run on pushes to main")

    permissions = workflow.get("permissions")
    if not isinstance(permissions, dict) or permissions.get("contents") != "read":
        errors.append("repository-contract workflow permissions must be contents: read")

    jobs = workflow.get("jobs")
    job = jobs.get("repository-contract") if isinstance(jobs, dict) else None
    if not isinstance(job, dict):
        errors.append(
            "repository-contract workflow must define the repository-contract job"
        )
        return

    steps = job.get("steps")
    if not isinstance(steps, list):
        errors.append("repository-contract job must define steps")
        return

    if job.get("runs-on") != "ubuntu-latest":
        errors.append("repository-contract job must run on ubuntu-latest")
    if "if" in job:
        errors.append("repository-contract job must not be conditionally disabled")

    action_uses = [
        step.get("uses")
        for step in steps
        if isinstance(step, dict) and step.get("uses")
    ]
    for action in action_uses:
        if not isinstance(action, str) or not ACTION_SHA.fullmatch(action):
            errors.append(f"workflow action must be pinned to a full commit SHA: {action}")

    action_names = {
        action.split("@", 1)[0]
        for action in action_uses
        if isinstance(action, str) and "@" in action
    }
    for required_action in ("actions/checkout", "actions/setup-python"):
        if required_action not in action_names:
            errors.append(f"workflow must use {required_action} pinned to a SHA")

    if any(isinstance(step, dict) and "if" in step for step in steps):
        errors.append("repository-contract steps must not be conditionally disabled")

    commands = [
        step["run"].strip()
        for step in steps
        if isinstance(step, dict) and isinstance(step.get("run"), str)
    ]
    install_command = "python -m pip install --require-hashes -r requirements-dev.txt"
    validate_command = "make validate PYTHON=python"
    if install_command not in commands:
        errors.append("workflow must install hash-locked validation dependencies")
    if validate_command not in commands:
        errors.append("workflow must run the exact repository validation command")


def validate_project_document(
    document: str, contract: dict[str, Any], errors: list[str]
) -> None:
    required_values: list[str] = [str(contract.get("project_url", ""))]
    for field, options in contract["fields"].items():
        required_values.append(field)
        required_values.extend(options)
    for view in contract.get("views", []):
        required_values.append(view["name"])
        if view.get("filter"):
            required_values.append(view["filter"])
    required_values.extend(contract.get("workflows", []))

    for value in required_values:
        if value and value not in document:
            errors.append(f"project document is missing live baseline value: {value}")


def validate(root: Path) -> list[str]:
    """Return every repository-contract violation found under *root*."""
    errors: list[str] = []

    for relative_path in REQUIRED_FILES:
        if not (root / relative_path).is_file():
            errors.append(f"missing required file: {relative_path}")

    contract_path = root / ".github/project-contract.json"
    contract = (
        load_project_contract(contract_path, errors) if contract_path.is_file() else None
    )

    pr_template = root / ".github/pull_request_template.md"
    if pr_template.is_file():
        content = pr_template.read_text(encoding="utf-8")
        for section in PR_TEMPLATE_SECTIONS:
            if section not in content:
                errors.append(f"missing PR template section: {section}")
        if "Refs #" not in content or "Closes #" in content:
            errors.append("PR template must use Refs # and must not auto-close the Issue")

    task_form_path = root / ".github/ISSUE_TEMPLATE/task.yml"
    if task_form_path.is_file() and contract is not None:
        form = load_yaml(task_form_path, errors)
        if form is not None:
            validate_issue_form(form, contract, errors)

    config_path = root / ".github/ISSUE_TEMPLATE/config.yml"
    if config_path.is_file() and contract is not None:
        config = load_yaml(config_path, errors)
        if config is not None:
            validate_issue_config(config, contract, errors)

    workflow_path = root / ".github/workflows/repository-contract.yml"
    if workflow_path.is_file():
        workflow = load_yaml(workflow_path, errors)
        if workflow is not None:
            validate_workflow(workflow, errors)

    document_path = root / "project-configuration.md"
    if document_path.is_file() and contract is not None:
        validate_project_document(
            document_path.read_text(encoding="utf-8"), contract, errors
        )

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("repository contract: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
