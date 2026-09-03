# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/terms_response.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    terms_id: str
    version: str = Field(
        ...,
        description="Echoed from the terms card, so the record names the exact text that was agreed to.",
    )
    agreed: bool = Field(..., description="false when the customer declined.")
    method: Literal["tap", "typed", "drawn"] = Field(
        ...,
        description="What the device actually delivered, NOT what terms.signing_level asked for. This is the field the signed record has to store.",
    )
    signature: str | None = Field(
        None,
        description="Absent for method 'tap' and for declines. The typed name for 'typed'; a base64 PNG (no data: prefix, capped well under the ~64KB Matrix event limit) for 'drawn'.",
    )
    signed_at: str = Field(
        ...,
        description="ISO 8601 UTC, e.g. 2026-08-05T14:22:10Z. No 'format' annotation on purpose — see schemas/README.md on ajv strict mode and quicktype's strict DateTime.parse.",
    )


class TermsResponseV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["terms_response"]
    data: Data
