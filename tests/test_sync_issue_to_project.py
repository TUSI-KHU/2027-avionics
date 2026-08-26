from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from sync_issue_to_project import (  # noqa: E402
    FormValueError,
    build_field_updates,
    find_or_add_item,
    load_project,
    parse_issue_form,
)


CONTRACT = {
    "fields": {
        "Status": ["Backlog", "In Progress", "Review", "Done", "Canceled"],
        "Priority": ["P0", "P1", "P2"],
        "유형": ["Feature", "Change", "Defect", "Research", "Test", "Risk", "Anomaly"],
        "Subsystem": ["SYS", "HW", "FSW", "GNC", "RF", "GS", "TEST"],
        "Gate": ["G0", "G1", "G2", "G3", "Post-flight"],
    }
}

ISSUE_BODY = """### 무엇을 하려나요?

Project 입력을 자동화한다.

### 작업 종류

Change

### 담당 분야

SYS

### 중요도

P0

### 개발 단계

G0

### 언제 끝났다고 볼 수 있나요?

- [ ] Project field가 반영된다.
"""


class IssueProjectSyncTest(unittest.TestCase):
    def test_parse_issue_form_extracts_project_values(self) -> None:
        values = parse_issue_form(ISSUE_BODY)

        self.assertEqual(
            values,
            {
                "유형": "Change",
                "Subsystem": "SYS",
                "Priority": "P0",
                "Gate": "G0",
            },
        )

    def test_build_field_updates_resolves_live_option_ids(self) -> None:
        project_fields = [
            {
                "id": "priority-field",
                "name": "Priority",
                "options": [
                    {"id": "priority-p0", "name": "P0"},
                    {"id": "priority-p1", "name": "P1"},
                ],
            },
            {
                "id": "type-field",
                "name": "유형",
                "options": [{"id": "type-change", "name": "Change"}],
            },
        ]

        updates = build_field_updates(
            {"Priority": "P0", "유형": "Change"}, project_fields, CONTRACT
        )

        self.assertEqual(
            updates,
            [
                ("priority-field", "priority-p0"),
                ("type-field", "type-change"),
            ],
        )

    def test_unknown_form_value_is_rejected(self) -> None:
        with self.assertRaisesRegex(FormValueError, "Priority.*P9"):
            build_field_updates(
                {"Priority": "P9"},
                [
                    {
                        "id": "priority-field",
                        "name": "Priority",
                        "options": [{"id": "priority-p0", "name": "P0"}],
                    }
                ],
                CONTRACT,
            )

    def test_missing_project_option_is_rejected(self) -> None:
        with self.assertRaisesRegex(FormValueError, "Project.*Change"):
            build_field_updates(
                {"유형": "Change"},
                [{"id": "type-field", "name": "유형", "options": []}],
                CONTRACT,
            )

    def test_project_fields_are_loaded_from_every_page(self) -> None:
        pages = [
            {
                "organization": {
                    "projectV2": {
                        "id": "project-1",
                        "fields": {
                            "nodes": [{"id": "field-1", "name": "Priority"}],
                            "pageInfo": {
                                "hasNextPage": True,
                                "endCursor": "cursor-1",
                            },
                        },
                    }
                }
            },
            {
                "organization": {
                    "projectV2": {
                        "id": "project-1",
                        "fields": {
                            "nodes": [{"id": "field-2", "name": "Gate"}],
                            "pageInfo": {"hasNextPage": False, "endCursor": None},
                        },
                    }
                }
            },
        ]

        with patch("sync_issue_to_project.graphql", side_effect=pages) as request:
            project_id, fields = load_project("token", "TUSI-KHU", 1)

        self.assertEqual("project-1", project_id)
        self.assertEqual(["field-1", "field-2"], [field["id"] for field in fields])
        self.assertEqual("cursor-1", request.call_args_list[1].args[2]["after"])

    def test_existing_project_item_is_found_on_later_page(self) -> None:
        pages = [
            {
                "node": {
                    "projectItems": {
                        "nodes": [
                            {"id": "other-item", "project": {"id": "other-project"}}
                        ],
                        "pageInfo": {"hasNextPage": True, "endCursor": "cursor-1"},
                    }
                }
            },
            {
                "node": {
                    "projectItems": {
                        "nodes": [
                            {"id": "wanted-item", "project": {"id": "project-1"}}
                        ],
                        "pageInfo": {"hasNextPage": False, "endCursor": None},
                    }
                }
            },
        ]

        with patch("sync_issue_to_project.graphql", side_effect=pages) as request:
            item_id = find_or_add_item("token", "issue-1", "project-1")

        self.assertEqual("wanted-item", item_id)
        self.assertEqual(2, request.call_count)
        self.assertEqual("cursor-1", request.call_args_list[1].args[2]["after"])

    def test_incomplete_project_items_response_fails_before_add(self) -> None:
        responses = [
            {"node": {}},
            {"addProjectV2ItemById": {"item": {"id": "unexpected-item"}}},
        ]

        with patch("sync_issue_to_project.graphql", side_effect=responses) as request:
            with self.assertRaisesRegex(RuntimeError, "projectItems"):
                find_or_add_item("token", "issue-1", "project-1")

        self.assertEqual(1, request.call_count)

    def test_project_item_cursor_must_advance(self) -> None:
        repeated_page = {
            "node": {
                "projectItems": {
                    "nodes": [],
                    "pageInfo": {"hasNextPage": True, "endCursor": "same"},
                }
            }
        }

        with patch(
            "sync_issue_to_project.graphql",
            side_effect=[repeated_page, repeated_page],
        ) as request:
            with self.assertRaisesRegex(RuntimeError, "did not advance"):
                find_or_add_item("token", "issue-1", "project-1")

        self.assertEqual(2, request.call_count)

    def test_project_field_cursor_must_advance(self) -> None:
        repeated_page = {
            "organization": {
                "projectV2": {
                    "id": "project-1",
                    "fields": {
                        "nodes": [],
                        "pageInfo": {"hasNextPage": True, "endCursor": "same"},
                    },
                }
            }
        }

        with patch(
            "sync_issue_to_project.graphql",
            side_effect=[repeated_page, repeated_page],
        ) as request:
            with self.assertRaisesRegex(RuntimeError, "did not advance"):
                load_project("token", "TUSI-KHU", 1)

        self.assertEqual(2, request.call_count)


if __name__ == "__main__":
    unittest.main()
