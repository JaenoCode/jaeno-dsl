# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/order_confirmation.v2.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    qty: float | None = None
    price: float | None = Field(
        None,
        description="Nullable — OrderItem.price stays null if the field isn't a num (order_confirmation_dsl_handler.dart:33-38), no default applied.",
    )
    image: str | None = None


class Fulfillment(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    method: str | None = Field(None, description="dine_in / pickup / car / delivery")
    summary: str | None = Field(
        None, description="e.g. the customer name, or the car/address one-line summary"
    )


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    order_id: str
    user_id: str | None = None
    customer_name: str | None = None
    currency: str | None = None
    total_amount: float | None = Field(
        None,
        description="No client-side fallback (msg.get<num>, no '??') — genuinely optional/nullable on the wire, unlike most other numeric fields in this inventory which default to 0.",
    )
    location: str | None = None
    created_at: str | None = None
    raw_order_text: str | None = None
    items: list[Item]
    fulfillment: Fulfillment | None = Field(
        None,
        description="New in v2 (JNO-184/185). A flat, display-ready summary of the chosen fulfillment method — the agent has already received the structured fulfillment_selection/name_response/car_response/address_response events and composes this itself.",
    )


class OrderConfirmationV2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[2]
    type: Literal["order_confirmation"]
    data: Data
