# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/countdown.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str = Field(
        ...,
        description="The label above the timer. Required: a countdown with no label is a number with no meaning.",
    )
    ends_at: str = Field(
        ...,
        description="ISO 8601 with offset, as produced by Python's datetime.now(timezone.utc).isoformat() — microseconds and a '+00:00' offset rather than 'Z'. Same shape the auction card already receives, parsed the same way (DateTime.tryParse, lenient; no 'format' annotation on purpose, see schemas/README.md).",
    )
    subtitle: str | None = Field(None, description="One line of context under the timer.")
    expired_text: str | None = Field(
        None, description="Shown once the deadline passes. Defaults client-side to 'Ended'."
    )


class CountdownV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["countdown"]
    data: Data
