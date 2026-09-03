# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/tip_request.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    tip_id: str
    title: str | None = None
    message: str | None = None
    recipient_name: str
    currency: str | None = None
    presets: list[float] | None = Field(
        None, description="Non-positive values are filtered out client-side (tip_handler.dart:43)."
    )
    allow_custom: bool | None = None
    allow_decline: bool | None = None


class TipRequestV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["tip_request"]
    data: Data
