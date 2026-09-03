"""Build a Matrix event content dict for an ``ai.jaeno.dsl`` card, validated
before it leaves the process.

This is the whole point of the package: the agent hands over a ``(type,
version, data)`` triple, and gets back a dict ready for ``room_send`` that the
Jaeno client is guaranteed to accept — or a :class:`~jaeno_dsl.errors.DSLError`
explaining why it won't.

It does **not** send anything (no Matrix client here) and does not concern
itself with sender-trust or business-suspension — those are client-side
render gates (JNO-286), not sender responsibilities.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from pydantic import ValidationError

from .calculator import validate_calculator_data
from .errors import DSLInvalidPayloadError, DSLMalformedEnvelopeError, DSLUnknownTypeError
from .fallback import fallback_body
from .models.generated.registry import DSL_MODELS

#: The Matrix event content field every DSL card travels in.
DSL_EVENT_KEY = "ai.jaeno.dsl"

#: Hand-written checks layered on top of the generated model, keyed by
#: ``(type, version)``. Each raises ``ValueError`` on a bad payload.
_EXTRA_VALIDATORS: dict[tuple[str, int], Callable[[dict[str, Any]], None]] = {
    ("calculator", 1): validate_calculator_data,
}


def validate_before_send(dsl_type: str, version: int, data: Mapping[str, Any]) -> None:
    """Raise the matching :class:`~jaeno_dsl.errors.DSLError` if
    ``{v: version, type: dsl_type, data: data}`` is anything the Jaeno client
    would fall back on. Returns ``None`` when the payload is good to send.

    The three failure modes mirror ``resolveDSL()``'s parse / lookup /
    edge-validate stages (``packages/widget_library/lib/dsl_runtime.dart``).
    """
    # 1. malformed envelope — structural, before any schema is consulted
    if not isinstance(dsl_type, str) or not dsl_type:
        raise DSLMalformedEnvelopeError("type must be a non-empty string")
    if not isinstance(version, int) or isinstance(version, bool):
        raise DSLMalformedEnvelopeError("v must be an int")
    if not isinstance(data, Mapping):
        raise DSLMalformedEnvelopeError("data must be a mapping")

    # 2. unknown (type, version) — the sender treats this as an error, not
    #    "nothing to check against" (see DSLUnknownTypeError).
    by_version = DSL_MODELS.get(dsl_type)
    if by_version is None or version not in by_version:
        raise DSLUnknownTypeError(dsl_type, version)

    envelope = {"v": version, "type": dsl_type, "data": dict(data)}

    # 3. invalid payload — against the schema-generated model …
    model = by_version[version]
    try:
        model.model_validate(envelope)
    except ValidationError as exc:
        raise DSLInvalidPayloadError(dsl_type, version, _summarize(exc)) from exc

    # … and against any hand-written check layered on top.
    extra = _EXTRA_VALIDATORS.get((dsl_type, version))
    if extra is not None:
        try:
            extra(envelope["data"])
        except ValueError as exc:
            raise DSLInvalidPayloadError(dsl_type, version, str(exc)) from exc


def build_dsl_envelope(dsl_type: str, version: int, data: Mapping[str, Any]) -> dict[str, Any]:
    """The inner ``{v, type, data}`` object, validated. Rarely needed directly
    — :func:`build_dsl_event_content` wraps it in a Matrix event."""
    validate_before_send(dsl_type, version, data)
    return {"v": version, "type": dsl_type, "data": dict(data)}


def build_dsl_event_content(
    dsl_type: str,
    version: int,
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    """Full Matrix ``m.room.message`` content for a DSL card.

    ``data`` may be passed as a mapping, as keyword fields, or both (keywords
    win on a key clash). ``body`` overrides the auto-generated fallback text.

    Raises a :class:`~jaeno_dsl.errors.DSLError` before returning anything if
    the payload is invalid.
    """
    merged: dict[str, Any] = {**(dict(data) if data else {}), **fields}
    validate_before_send(dsl_type, version, merged)
    return {
        "msgtype": "m.text",
        "body": body if (body and body.strip()) else fallback_body(dsl_type, version, merged),
        DSL_EVENT_KEY: {"v": version, "type": dsl_type, "data": merged},
    }


def _summarize(exc: ValidationError) -> str:
    parts = []
    for err in exc.errors():
        loc = ".".join(str(p) for p in err["loc"])
        parts.append(f"{loc}: {err['msg']}" if loc else err["msg"])
    return "; ".join(parts)
