# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/address_response.v1.json
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
    line1: str
    line2: str | None = None
    city: str
    notes: str | None = None


class AddressResponseV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["address_response"]
    data: Data
