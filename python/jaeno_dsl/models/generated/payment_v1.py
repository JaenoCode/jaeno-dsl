# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/payment.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    amount: int
    currency: str | None = None
    order_id: str
    customer_name: str | None = None
    user_id: str | None = None
    business_name: str | None = None
    created_at: str | None = None


class PaymentV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["payment"]
    data: Data
