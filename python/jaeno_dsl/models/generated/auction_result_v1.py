# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/auction_result.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str | None = None
    currency: str | None = None
    winning_amount: float
    is_winner: bool
    order_id: str | None = Field(
        None,
        description="No test coverage confirming presence/absence rules. Dart defaults to '' if missing — kept optional here on that basis, not on a confirmed real payload.",
    )
    user_id: str | None = Field(
        None,
        description="Same caveat as order_id — code-derived, not confirmed against a real payload.",
    )


class AuctionResultV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["auction_result"]
    data: Data
