"""Every examples/*.json must validate through its generated model.

Mirrors the Dart side's edge_validation_test.dart intent: the schema-derived
model is the gate, and the committed example payloads are the known-good set.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from jaeno_dsl.validate import is_valid_generated_dsl

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES = sorted((REPO_ROOT / "examples").glob("*.json"))


@pytest.mark.parametrize("example", EXAMPLES, ids=lambda p: p.stem)
def test_example_validates(example: pathlib.Path) -> None:
    payload = json.loads(example.read_text())
    assert is_valid_generated_dsl(payload["type"], payload["v"], payload) is True


def test_unmodeled_pair_passes() -> None:
    assert (
        is_valid_generated_dsl("no_such_type", 1, {"v": 1, "type": "no_such_type", "data": {}})
        is True
    )


def test_wrong_field_type_fails() -> None:
    assert (
        is_valid_generated_dsl(
            "banner", 1, {"v": 1, "type": "banner", "data": {"title": 1, "message": "y"}}
        )
        is False
    )


def test_missing_required_field_fails() -> None:
    assert (
        is_valid_generated_dsl("banner", 1, {"v": 1, "type": "banner", "data": {"title": "x"}})
        is False
    )


def test_data_extra_key_is_allowed() -> None:
    # data.additionalProperties is true everywhere by design — the agent may
    # send fields the client doesn't read yet.
    assert (
        is_valid_generated_dsl(
            "banner",
            1,
            {"v": 1, "type": "banner", "data": {"title": "x", "message": "y", "future_field": "z"}},
        )
        is True
    )
