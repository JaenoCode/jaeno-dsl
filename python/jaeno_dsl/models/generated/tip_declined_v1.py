# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/tip_declined.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    recipient_name: str | None = None


class TipDeclinedV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["tip_declined"]
    data: Data
