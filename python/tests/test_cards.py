"""Every generated card constructor produces a client-valid envelope.

Acceptance criterion for JNO-347: constructing any current (type, version)
yields an envelope that passes the generated validator and carries a
non-empty body.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from jaeno_dsl import DSL_EVENT_KEY, is_valid_generated_dsl
from jaeno_dsl.cards import CARD_CONSTRUCTORS

REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
EXAMPLES = sorted((REPO_ROOT / "examples").glob("*.json"))


@pytest.mark.parametrize("example", EXAMPLES, ids=lambda p: p.stem)
def test_constructor_builds_valid_event(example: pathlib.Path) -> None:
    payload = json.loads(example.read_text())
    dsl_type, version, data = payload["type"], payload["v"], payload["data"]

    ctor = CARD_CONSTRUCTORS[(dsl_type, version)]
    content = ctor(data)

    assert content["msgtype"] == "m.text"
    assert content["body"].strip(), "body must be non-empty"

    envelope = content[DSL_EVENT_KEY]
    assert envelope == {"v": version, "type": dsl_type, "data": data}
    assert is_valid_generated_dsl(dsl_type, version, envelope) is True


def test_every_registered_pair_has_a_constructor() -> None:
    from jaeno_dsl.models.generated.registry import DSL_MODELS

    registered = {(t, v) for t, versions in DSL_MODELS.items() for v in versions}
    assert set(CARD_CONSTRUCTORS) == registered


def test_kwargs_and_mapping_forms_agree() -> None:
    from jaeno_dsl.cards import banner_v1

    a = banner_v1({"title": "x", "message": "y"})
    b = banner_v1(title="x", message="y")
    assert a == b


def test_explicit_body_overrides_fallback() -> None:
    from jaeno_dsl.cards import banner_v1

    content = banner_v1(title="x", message="y", body="custom")
    assert content["body"] == "custom"
