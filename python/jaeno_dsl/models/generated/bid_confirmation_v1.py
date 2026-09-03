# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/bid_confirmation.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    auction_id: str
    title: str | None = None
    currency: str | None = None
    amount: float


class BidConfirmationV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["bid_confirmation"]
    data: Data
