"""jaeno-dsl — agent-side constructor for ``ai.jaeno.dsl`` Matrix event content.

Generated from the same ``schemas/*.json`` the Dart app and web widget use, so
the bot can't drift from the client's DSL contract.

    from jaeno_dsl import build_dsl_event_content
    content = build_dsl_event_content("banner", 1, {"title": "Closed", "message": "Back at 9am"})
    await client.room_send(room_id, "m.room.message", content)

or the per-card form:

    from jaeno_dsl.cards import banner_v1
    content = banner_v1(title="Closed", message="Back at 9am")

SPIKE STATE (JNO-347): envelope builder, fallback bodies, error taxonomy and
the calculator formula check are in. Still open: CI drift-check wiring,
packaging/distribution (JNO-348), and the schemas/ location (JNO-345).
"""

from .cards import CARD_CONSTRUCTORS
from .envelope import (
    DSL_EVENT_KEY,
    build_dsl_envelope,
    build_dsl_event_content,
    validate_before_send,
)
from .errors import DSLError, DSLInvalidPayloadError, DSLMalformedEnvelopeError, DSLUnknownTypeError
from .fallback import fallback_body
from .validate import is_valid_generated_dsl

__all__ = [
    "CARD_CONSTRUCTORS",
    "DSL_EVENT_KEY",
    "DSLError",
    "DSLInvalidPayloadError",
    "DSLMalformedEnvelopeError",
    "DSLUnknownTypeError",
    "build_dsl_envelope",
    "build_dsl_event_content",
    "fallback_body",
    "is_valid_generated_dsl",
    "validate_before_send",
]
