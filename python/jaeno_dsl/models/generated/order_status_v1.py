# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/order_status.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    order_id: str
    status: str = Field(
        ...,
        description="Free-text, not enum-restricted — preparing/ready/on_the_way/delivered are recognized client-side with a graceful fallback for anything else, matching order_history.v1's status field.",
    )
    message: str | None = None


class OrderStatusV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["order_status"]
    data: Data
