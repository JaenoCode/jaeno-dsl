"""Pre-send validation errors.

Conceptual peers of the sealed ``DSLResolution`` outcomes in the Dart app
(``packages/widget_library/lib/models/dsl_resolution.dart``). The bot must
never emit an envelope the client will fall back on, so every one of these is
raised *before* the event is built, not after.

| this module                 | Dart `DSLResolution`      |
|-----------------------------|--------------------------|
| `DSLMalformedEnvelopeError` | `DSLMalformedEnvelope`   |
| `DSLUnknownTypeError`       | `DSLUnknownHandler`      |
| `DSLInvalidPayloadError`    | `DSLInvalidPayload`      |

`DSLUntrustedSender` / `DSLBotSuspended` have no peer here — they are
client-side render-time gates, out of scope for a sender (see JNO-347).
"""

from __future__ import annotations


class DSLError(Exception):
    """Base for every pre-send DSL failure."""


class DSLMalformedEnvelopeError(DSLError):
    """The ``{v, type, data}`` envelope is structurally wrong — non-int ``v``,
    empty/non-str ``type``, or ``data`` that isn't a mapping."""


class DSLUnknownTypeError(DSLError):
    """No generated model is registered for this ``(type, version)``.

    Unlike :func:`jaeno_dsl.validate.is_valid_generated_dsl` (which returns
    ``True`` for an unmodeled pair, matching the client's "nothing to check
    against" contract), the *sender* treats an unknown pair as a hard error:
    the bot has no business emitting a type the registry doesn't know.
    """

    def __init__(self, dsl_type: str, version: int) -> None:
        self.dsl_type = dsl_type
        self.version = version
        super().__init__(
            f"no DSL model registered for ({dsl_type!r}, v{version}) — "
            "not a known card type/version"
        )


class DSLInvalidPayloadError(DSLError):
    """The payload fails validation against the schema-generated model (or a
    hand-written check layered on top, e.g. the calculator formula grammar)."""

    def __init__(self, dsl_type: str, version: int, detail: object) -> None:
        self.dsl_type = dsl_type
        self.version = version
        self.detail = detail
        super().__init__(f"invalid {dsl_type} v{version} payload: {detail}")
