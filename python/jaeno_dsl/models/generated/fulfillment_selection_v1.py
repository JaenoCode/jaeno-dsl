# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/fulfillment_selection.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    order_id: str
    method: str = Field(
        ...,
        description="One of dine_in, pickup, car, delivery today; left as a free string rather than an enum since the agent is the source of truth for valid methods.",
    )


class FulfillmentSelectionV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["fulfillment_selection"]
    data: Data
