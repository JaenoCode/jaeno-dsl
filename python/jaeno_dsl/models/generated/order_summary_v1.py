# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/order_summary.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    qty: int | None = Field(None, description="Defaults to 1 client-side if missing or not an int.")


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    items: list[Item]
    total: int


class OrderSummaryV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["order_summary"]
    data: Data
