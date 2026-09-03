# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/auction.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    auction_id: str
    title: str | None = None
    image: str | None = None
    currency: str | None = None
    starting_price: float
    min_bid: float | None = Field(
        None,
        description="Confirmed optional via test/dsl/auction_handler_test.dart — a live auction without a stated min_bid falls back to starting_price on the client.",
    )
    ends_at: str | None = Field(
        None,
        description='ISO 8601, parsed with DateTime.tryParse (lenient, not strict RFC3339 — deliberately not asserting "format": "date-time" here since neither validator in this pipeline enforces it and Dart\'s own parsing is looser anyway). Confirmed optional via test — omitting it renders without a countdown, does not fail.',
    )


class AuctionV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["auction"]
    data: Data
