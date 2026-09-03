# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/review.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    menu_item: str | None = None
    order_id: str | None = None


class ReviewV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["review"]
    data: Data
