"""Pre-send validation taxonomy — the three failure modes and the happy path."""

from __future__ import annotations

import pytest

from jaeno_dsl import (
    DSLInvalidPayloadError,
    DSLMalformedEnvelopeError,
    DSLUnknownTypeError,
    build_dsl_event_content,
    validate_before_send,
)

VALID_BANNER = {"title": "Closed", "message": "Back at 9am"}


def test_happy_path() -> None:
    content = build_dsl_event_content("banner", 1, VALID_BANNER)
    assert content["ai.jaeno.dsl"] == {"v": 1, "type": "banner", "data": VALID_BANNER}
    assert content["body"] == "Closed — Back at 9am"


@pytest.mark.parametrize(
    ("dsl_type", "version", "data"),
    [
        ("", 1, VALID_BANNER),
        ("banner", "1", VALID_BANNER),
        ("banner", True, VALID_BANNER),
        ("banner", 1, ["not", "a", "mapping"]),
    ],
)
def test_malformed_envelope(dsl_type: object, version: object, data: object) -> None:
    with pytest.raises(DSLMalformedEnvelopeError):
        validate_before_send(dsl_type, version, data)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("dsl_type", "version"),
    [("banner", 2), ("no_such_card", 1), ("menu", 9)],
)
def test_unknown_type_or_version(dsl_type: str, version: int) -> None:
    with pytest.raises(DSLUnknownTypeError):
        validate_before_send(dsl_type, version, {"whatever": True})


@pytest.mark.parametrize(
    "data",
    [
        {"title": "x"},  # missing required 'message'
        {"title": 1, "message": "y"},  # wrong type
    ],
)
def test_invalid_payload(data: dict[str, object]) -> None:
    with pytest.raises(DSLInvalidPayloadError):
        build_dsl_event_content("banner", 1, data)


def test_data_extra_key_allowed() -> None:
    # data.additionalProperties is true by design across all schemas.
    content = build_dsl_event_content("banner", 1, {**VALID_BANNER, "agent_only_field": 42})
    assert content["ai.jaeno.dsl"]["data"]["agent_only_field"] == 42


def test_errors_raise_before_returning_anything() -> None:
    # nothing is "half-built" — the exception is the only output on failure
    with pytest.raises(DSLInvalidPayloadError) as exc:
        build_dsl_event_content("payment", 1, {"order_id": "o1"})  # missing 'amount'
    assert "amount" in str(exc.value)
