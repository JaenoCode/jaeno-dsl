# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/fulfillment_method.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    order_id: str
    title: str | None = None
    message: str | None = None


class FulfillmentMethodV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["fulfillment_method"]
    data: Data
