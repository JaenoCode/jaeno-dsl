# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/order_history.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Order(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    status: str | None = None
    items: list[str] | str | None = Field(
        None,
        description="Genuinely polymorphic on the wire today — order_history_dsl_handler.dart:166-192 explicitly normalizes 'real List, clean comma string, and stringified Python list'. Schema allows the two intentional shapes (array or plain string); the stringified-Python-list case is a parsing workaround for a malformed string, not a shape to encode as valid. Flag to the agent side rather than treat as permanent.",
    )
    total_amount: float | None = None
    created_at: str | None = None


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    orders: list[Order]


class OrderHistoryV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["order_history"]
    data: Data
