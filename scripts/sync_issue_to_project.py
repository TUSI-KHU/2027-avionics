#!/usr/bin/env python3
"""Add Issue Form submissions to the organization Project and sync select fields."""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

FORM_LABELS = {
    "작업 종류": "유형",
    "담당 분야": "Subsystem",
    "중요도": "Priority",
    "개발 단계": "Gate",
}

PROJECT_QUERY = """
query($owner: String!, $number: Int!, $after: String) {
  organization(login: $owner) {
    projectV2(number: $number) {
      id
      fields(first: 50, after: $after) {
        nodes {
          ... on ProjectV2SingleSelectField {
            id
            name
            options { id name }
          }
        }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""

ISSUE_ITEMS_QUERY = """
query($issueId: ID!, $after: String) {
  node(id: $issueId) {
    ... on Issue {
      projectItems(first: 50, after: $after) {
        nodes { id project { id } }
        pageInfo { hasNextPage endCursor }
      }
    }
  }
}
"""

ADD_ITEM_MUTATION = """
mutation($projectId: ID!, $contentId: ID!) {
  addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
    item { id }
  }
}
"""

UPDATE_FIELD_MUTATION = """
mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
  updateProjectV2ItemFieldValue(
    input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: {singleSelectOptionId: $optionId}
    }
  ) {
    projectV2Item { id }
  }
}
"""


class FormValueError(ValueError):
    """Raised when form values cannot be mapped safely to the live Project."""


def parse_issue_form(body: str) -> dict[str, str]:
    """Extract Project values from the Markdown produced by the Issue Form."""
    headings = list(re.finditer(r"^###\s+(.+?)\s*$", body, flags=re.MULTILINE))
    sections: dict[str, str] = {}
    for index, heading in enumerate(headings):
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        value = body[start:end].strip()
        sections[heading.group(1).strip()] = value

    present_labels = FORM_LABELS.keys() & sections.keys()
    if not present_labels:
        return {}

    missing = [label for label in FORM_LABELS if not sections.get(label, "").strip()]
    if missing:
        raise FormValueError(
            "Issue Form is missing Project selections: " + ", ".join(missing)
        )

    return {
        project_field: sections[form_label].splitlines()[0].strip()
        for form_label, project_field in FORM_LABELS.items()
    }


def build_field_updates(
    values: dict[str, str],
    project_fields: list[dict[str, Any]],
    contract: dict[str, Any],
) -> list[tuple[str, str]]:
    """Resolve form values to live Project field and option IDs."""
    contract_fields = contract.get("fields")
    if not isinstance(contract_fields, dict):
        raise FormValueError("Project contract does not define fields")

    fields_by_name = {
        field.get("name"): field
        for field in project_fields
        if isinstance(field, dict) and isinstance(field.get("name"), str)
    }
    updates: list[tuple[str, str]] = []

    for field_name, value in values.items():
        allowed = contract_fields.get(field_name)
        if not isinstance(allowed, list) or value not in allowed:
            raise FormValueError(f"{field_name} has unsupported value: {value}")

        field = fields_by_name.get(field_name)
        if not field or not isinstance(field.get("id"), str):
            raise FormValueError(f"Project field is missing: {field_name}")

        options = field.get("options")
        option_ids = {
            option.get("name"): option.get("id")
            for option in options or []
            if isinstance(option, dict)
        }
        option_id = option_ids.get(value)
        if not isinstance(option_id, str):
            raise FormValueError(
                f"Project field {field_name} does not contain option: {value}"
            )
        updates.append((field["id"], option_id))

    return updates


def graphql(token: str, query: str, variables: dict[str, Any]) -> dict[str, Any]:
    """Run one authenticated GitHub GraphQL request without logging the token."""
    payload = json.dumps({"query": query, "variables": variables}).encode("utf-8")
    request = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "2027-avionics-project-sync",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub GraphQL HTTP {error.code}: {detail}") from error
    except urllib.error.URLError as error:
        raise RuntimeError(f"GitHub GraphQL request failed: {error.reason}") from error

    if result.get("errors"):
        messages = "; ".join(
            str(item.get("message", item)) for item in result["errors"]
        )
        raise RuntimeError(f"GitHub GraphQL error: {messages}")
    data = result.get("data")
    if not isinstance(data, dict):
        raise RuntimeError("GitHub GraphQL response did not contain data")
    return data


def next_page_cursor(
    connection: dict[str, Any],
    current: str | None,
    seen: set[str],
    context: str,
) -> str | None:
    """Return the next cursor, failing closed on malformed or stalled pages."""
    page_info = connection.get("pageInfo")
    if not isinstance(page_info, dict):
        raise RuntimeError(f"{context} pagination did not return pageInfo")
    has_next_page = page_info.get("hasNextPage")
    if not isinstance(has_next_page, bool):
        raise RuntimeError(f"{context} pagination did not return hasNextPage")
    if not has_next_page:
        return None

    cursor = page_info.get("endCursor")
    if not isinstance(cursor, str) or not cursor:
        raise RuntimeError(f"{context} pagination did not return an end cursor")
    if cursor == current or cursor in seen:
        raise RuntimeError(f"{context} pagination cursor did not advance")
    seen.add(cursor)
    return cursor


def load_project(
    token: str, owner: str, number: int
) -> tuple[str, list[dict[str, Any]]]:
    """Load the Project ID and all fields across every GraphQL page."""
    cursor: str | None = None
    seen_cursors: set[str] = set()
    project_id: str | None = None
    fields: list[dict[str, Any]] = []

    while True:
        data = graphql(
            token,
            PROJECT_QUERY,
            {"owner": owner, "number": number, "after": cursor},
        )
        organization = data.get("organization")
        project = organization.get("projectV2") if isinstance(organization, dict) else None
        if not isinstance(project, dict) or not isinstance(project.get("id"), str):
            raise RuntimeError(f"Project was not found: {owner}/{number}")
        project_id = project["id"]

        connection = project.get("fields")
        if not isinstance(connection, dict):
            raise RuntimeError("Project fields connection was not returned")
        nodes = connection.get("nodes")
        if not isinstance(nodes, list):
            raise RuntimeError("Project fields page did not contain nodes")
        fields.extend(field for field in nodes if isinstance(field, dict))

        next_cursor = next_page_cursor(
            connection, cursor, seen_cursors, "Project field"
        )
        if next_cursor is None:
            break
        cursor = next_cursor

    if project_id is None:
        raise RuntimeError(f"Project was not found: {owner}/{number}")
    return project_id, fields


def find_or_add_item(token: str, issue_id: str, project_id: str) -> str:
    """Return the existing Project item ID, adding the Issue when necessary."""
    cursor: str | None = None
    seen_cursors: set[str] = set()
    while True:
        data = graphql(
            token, ISSUE_ITEMS_QUERY, {"issueId": issue_id, "after": cursor}
        )
        node = data.get("node")
        if not isinstance(node, dict):
            raise RuntimeError("Issue Project items query did not return a node")
        connection = node.get("projectItems")
        if not isinstance(connection, dict):
            raise RuntimeError("Issue node did not return projectItems")
        items = connection.get("nodes")
        if not isinstance(items, list):
            raise RuntimeError("Issue projectItems page did not contain nodes")
        for item in items:
            if (
                isinstance(item, dict)
                and item.get("project", {}).get("id") == project_id
            ):
                item_id = item.get("id")
                if isinstance(item_id, str):
                    return item_id

        next_cursor = next_page_cursor(
            connection, cursor, seen_cursors, "Project item"
        )
        if next_cursor is None:
            break
        cursor = next_cursor

    data = graphql(
        token,
        ADD_ITEM_MUTATION,
        {"projectId": project_id, "contentId": issue_id},
    )
    item = data.get("addProjectV2ItemById", {}).get("item", {})
    item_id = item.get("id") if isinstance(item, dict) else None
    if not isinstance(item_id, str):
        raise RuntimeError("GitHub did not return the added Project item ID")
    return item_id


def main() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    token = os.environ.get("PROJECT_TOKEN")
    owner = os.environ.get("PROJECT_OWNER", "TUSI-KHU")
    number_text = os.environ.get("PROJECT_NUMBER", "1")

    if not event_path:
        raise RuntimeError("GITHUB_EVENT_PATH is not set")
    if not token:
        raise RuntimeError(
            "PROJECT_TOKEN secret is not configured; it needs repo and project scopes"
        )

    event = json.loads(Path(event_path).read_text(encoding="utf-8"))
    issue = event.get("issue")
    if not isinstance(issue, dict):
        raise RuntimeError("GitHub event does not contain an Issue")
    issue_id = issue.get("node_id")
    body = issue.get("body") or ""
    if not isinstance(issue_id, str):
        raise RuntimeError("GitHub Issue does not contain a node_id")

    values = parse_issue_form(body)
    if not values:
        print("project sync: skipped (Issue was not created from the Task form)")
        return 0

    contract_path = Path(__file__).resolve().parents[1] / ".github/project-contract.json"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    project_id, field_nodes = load_project(token, owner, int(number_text))
    updates = build_field_updates(values, field_nodes, contract)
    item_id = find_or_add_item(token, issue_id, project_id)

    for field_id, option_id in updates:
        graphql(
            token,
            UPDATE_FIELD_MUTATION,
            {
                "projectId": project_id,
                "itemId": item_id,
                "fieldId": field_id,
                "optionId": option_id,
            },
        )

    print(f"project sync: updated {len(updates)} fields")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (FormValueError, RuntimeError, ValueError, OSError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)
