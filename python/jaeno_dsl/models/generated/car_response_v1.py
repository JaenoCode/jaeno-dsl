# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/car_response.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    order_id: str
    label: str | None = None
    make: str
    model: str
    color: str
    plate_number: str


class CarResponseV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["car_response"]
    data: Data
