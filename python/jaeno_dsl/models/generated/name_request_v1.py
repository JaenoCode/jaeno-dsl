# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/name_request.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    order_id: str
    method: str = Field(..., description="dine_in or pickup — adapts the prompt copy client-side.")
    title: str | None = None


class NameRequestV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["name_request"]
    data: Data
