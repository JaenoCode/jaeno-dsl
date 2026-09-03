"""Edge validation against the schema-generated models.

The peer of ``isValidGeneratedDSL`` in the Dart app
(``packages/widget_library/lib/models/generated/dsl_generated_validators.dart``):
given the full ``{v, type, data}`` envelope straight off (or on its way to) a
Matrix event, return whether it parses cleanly through the generated model for
that ``(type, version)``.

Returns ``True`` — not ``False`` — when no generated model exists for the pair
at all: an unmodeled type/version is "nothing to check against", not "known
invalid", matching the Dart contract exactly.
"""

from __future__ import annotations

from typing import Any

from pydantic import ValidationError

from .models.generated.registry import DSL_MODELS


def is_valid_generated_dsl(dsl_type: str, version: int, envelope: dict[str, Any]) -> bool:
    by_version = DSL_MODELS.get(dsl_type)
    if by_version is None:
        return True
    model = by_version.get(version)
    if model is None:
        return True
    try:
        model.model_validate(envelope)
    except ValidationError:
        return False
    return True
