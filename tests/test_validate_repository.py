import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_repository import validate


PROJECT_CONTRACT = {
    "project_url": "https://github.com/orgs/TUSI-KHU/projects/1",
    "fields": {
        "Status": ["Backlog", "In Progress", "Review", "Done", "Canceled"],
        "Priority": ["P0", "P1", "P2"],
        "유형": [
            "Feature",
            "Change",
            "Defect",
            "Research",
            "Test",
            "Risk",
            "Anomaly",
        ],
        "Subsystem": ["SYS", "HW", "FSW", "GNC", "RF", "GS", "TEST"],
        "Gate": ["G0", "G1", "G2", "G3", "Post-flight"],
    },
    "views": [
        {"name": "Board", "filter": "-status:Done,Canceled"},
        {"name": "My Review", "filter": "status:Review"},
    ],
    "workflows": ["Item added to project", "Item closed"],
}

TASK_FORM = """\
name: Task
description: Project Task
title: "[Task] "
body:
  - type: textarea
    id: purpose
    attributes: {label: 목적}
    validations: {required: true}
  - type: dropdown
    id: type
    attributes:
      label: 유형
      options: [Feature, Change, Defect, Research, Test, Risk, Anomaly]
    validations: {required: true}
  - type: dropdown
    id: subsystem
    attributes:
      label: Subsystem
      options: [SYS, HW, FSW, GNC, RF, GS, TEST]
    validations: {required: true}
  - type: dropdown
    id: priority
    attributes:
      label: Priority
      options: [P0, P1, P2]
    validations: {required: true}
  - type: dropdown
    id: gate
    attributes:
      label: Gate
      options: [G0, G1, G2, G3, Post-flight]
    validations: {required: true}
  - type: textarea
    id: acceptance
    attributes: {label: 완료 조건}
    validations: {required: true}
  - type: textarea
    id: verification
    attributes: {label: 검증 방법}
    validations: {required: true}
  - type: textarea
    id: dependencies
    attributes: {label: 의존성}
    validations: {required: true}
"""

WORKFLOW = """\
name: repository-contract
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
jobs:
  repository-contract:
    name: repository-contract
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
      - uses: actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065
      - run: python -m pip install --require-hashes -r requirements-dev.txt
      - run: make validate PYTHON=python
"""

PROJECT_SYNC_WORKFLOW = """\
name: sync-issue-project
on:
  issues:
    types: [opened, edited, reopened]
permissions:
  contents: read
  issues: read
jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
      - run: python scripts/sync_issue_to_project.py
        env:
          PROJECT_TOKEN: ${{ secrets.PROJECT_TOKEN }}
          PROJECT_OWNER: TUSI-KHU
          PROJECT_NUMBER: "1"
"""

PR_TEMPLATE = """\
## 왜 바꾸나요?
Refs #1
## 다른 부분에 미치는 영향
## 어떻게 확인했나요?
## 아직 확인하지 못한 것과 다음 할 일
## 문제가 생겼을 때 되돌리는 방법
## 올리기 전 확인
"""


class RepositoryContractTest(unittest.TestCase):
    def write_contract(self, root: Path) -> None:
        files = {
            "README.md": "# Project\n",
            "CONTRIBUTING.md": "Issue -> branch -> PR\n",
            "LICENSE": "MIT License\n",
            "project-configuration.md": json.dumps(
                PROJECT_CONTRACT, ensure_ascii=False
            ),
            "repository-settings.md": "# 저장소 설정\n",
            ".github/project-contract.json": json.dumps(
                PROJECT_CONTRACT, ensure_ascii=False
            ),
            ".github/pull_request_template.md": PR_TEMPLATE,
            ".github/ISSUE_TEMPLATE/task.yml": TASK_FORM,
            ".github/ISSUE_TEMPLATE/config.yml": (
                "blank_issues_enabled: false\n"
                "contact_links:\n"
                "  - name: Project\n"
                f"    url: {PROJECT_CONTRACT['project_url']}\n"
                "    about: Project board\n"
            ),
            ".github/workflows/repository-contract.yml": WORKFLOW,
            ".github/workflows/sync-issue-project.yml": PROJECT_SYNC_WORKFLOW,
            "Makefile": "validate:\n\tpython scripts/validate_repository.py\n",
            "requirements-dev.txt": "pyyaml==6.0.2\n",
        }
        for relative_path, content in files.items():
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    def test_complete_contract_passes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            self.assertEqual([], validate(root))

    def test_missing_issue_config_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            (root / ".github/ISSUE_TEMPLATE/config.yml").unlink()
            self.assertIn(
                "missing required file: .github/ISSUE_TEMPLATE/config.yml",
                validate(root),
            )

    def test_missing_project_sync_workflow_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            (root / ".github/workflows/sync-issue-project.yml").unlink()
            self.assertIn(
                "missing required file: .github/workflows/sync-issue-project.yml",
                validate(root),
            )

    def test_project_sync_workflow_must_run_on_issue_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            workflow = root / ".github/workflows/sync-issue-project.yml"
            workflow.write_text(
                PROJECT_SYNC_WORKFLOW.replace("opened, edited, reopened", "opened"),
                encoding="utf-8",
            )
            self.assertIn(
                "project sync workflow must handle opened, edited, and reopened Issues",
                validate(root),
            )

    def test_project_sync_workflow_requires_repository_secret(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            workflow = root / ".github/workflows/sync-issue-project.yml"
            workflow.write_text(
                PROJECT_SYNC_WORKFLOW.replace(
                    "PROJECT_TOKEN: ${{ secrets.PROJECT_TOKEN }}",
                    "PROJECT_TOKEN: token-in-file",
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "project sync workflow must read PROJECT_TOKEN from repository secrets",
                validate(root),
            )

    def test_malformed_yaml_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            form = root / ".github/ISSUE_TEMPLATE/task.yml"
            form.write_text("body: [\n", encoding="utf-8")
            self.assertTrue(
                any("invalid YAML" in error for error in validate(root)),
                validate(root),
            )

    def test_project_dropdown_drift_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            form = root / ".github/ISSUE_TEMPLATE/task.yml"
            form.write_text(TASK_FORM.replace(", Post-flight", ""), encoding="utf-8")
            self.assertIn(
                "Issue Form options for Gate do not match project contract",
                validate(root),
            )

    def test_required_issue_field_is_enforced(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            form = root / ".github/ISSUE_TEMPLATE/task.yml"
            form.write_text(
                TASK_FORM.replace(
                    "id: verification\n    attributes: {label: 검증 방법}\n"
                    "    validations: {required: true}",
                    "id: verification\n    attributes: {label: 검증 방법}",
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "Issue Form field verification must be required", validate(root)
            )

    def test_invalid_issue_component_and_metadata_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            form = root / ".github/ISSUE_TEMPLATE/task.yml"
            invalid = TASK_FORM.replace("name: Task", "name: ''").replace(
                "description: Project Task", "description: ''"
            ).replace("- type: textarea\n    id: purpose", "- type: markdown\n    id: purpose")
            form.write_text(invalid, encoding="utf-8")

            errors = validate(root)
            self.assertIn("Issue Form name must be a non-empty string", errors)
            self.assertIn("Issue Form description must be a non-empty string", errors)
            self.assertIn("Issue Form field purpose must use type textarea", errors)

    def test_nonexecuting_workflow_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            workflow = root / ".github/workflows/repository-contract.yml"
            workflow.write_text(
                """\
name: repository-contract
on:
  pull_request:
  push: {branches: [main]}
permissions: {contents: read}
jobs:
  repository-contract:
    steps:
      - run: echo 'python -m pip install --require-hashes -r requirements-dev.txt'
      - run: echo 'make validate PYTHON=python'
""",
                encoding="utf-8",
            )

            errors = validate(root)
            self.assertIn("repository-contract job must run on ubuntu-latest", errors)
            self.assertIn("workflow must use actions/checkout pinned to a SHA", errors)
            self.assertIn("workflow must run the exact repository validation command", errors)

    def test_duplicate_issue_field_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            form = root / ".github/ISSUE_TEMPLATE/task.yml"
            form.write_text(
                TASK_FORM.replace("id: dependencies", "id: verification"),
                encoding="utf-8",
            )
            self.assertIn("Issue Form field IDs must be unique", validate(root))

    def test_conditionally_disabled_workflow_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            workflow = root / ".github/workflows/repository-contract.yml"
            workflow.write_text(
                WORKFLOW.replace(
                    "  repository-contract:\n    name:",
                    "  repository-contract:\n    if: false\n    name:",
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "repository-contract job must not be conditionally disabled",
                validate(root),
            )

    def test_mutable_action_tag_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            workflow = root / ".github/workflows/repository-contract.yml"
            workflow.write_text(
                WORKFLOW.replace(
                    "actions/checkout@11d5960a326750d5838078e36cf38b85af677262",
                    "actions/checkout@v4",
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "workflow action must be pinned to a full commit SHA: actions/checkout@v4",
                validate(root),
            )

    def test_pr_must_reference_issue_without_auto_close(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            template = root / ".github/pull_request_template.md"
            template.write_text(
                PR_TEMPLATE.replace("Refs #1", "Closes #1"), encoding="utf-8"
            )
            self.assertIn(
                "PR template must use Refs # and must not auto-close the Issue",
                validate(root),
            )

    def test_documented_project_option_drift_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_contract(root)
            document = root / "project-configuration.md"
            document.write_text("# missing baseline\n", encoding="utf-8")
            self.assertTrue(
                any("project document" in error for error in validate(root)),
                validate(root),
            )


if __name__ == "__main__":
    unittest.main()
