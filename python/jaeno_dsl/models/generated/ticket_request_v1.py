# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/ticket_request.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, conint


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    event_id: str = Field(
        ...,
        description="Echoed back from the event_detail card. The agent's own identifier, opaque to Jaeno.",
    )
    event_title: str = Field(
        ...,
        description="Carried along so the rendered card stands alone — the agent keeps no record of the card it sent.",
    )
    tier_name: str
    price: str = Field(
        ...,
        description="The tier's price as the agent formatted it, echoed back unchanged. Per ticket, not a computed total — Jaeno does no arithmetic on money.",
    )
    quantity: conint(ge=1)


class TicketRequestV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["ticket_request"]
    data: Data = Field(
        ...,
        description="Client → agent: the tier and quantity a customer picked from an event_detail card, and nothing more. It reserves nothing. Whether the request is accepted, held, repriced or rejected is entirely the agent's call against its own capacity — Jaeno relays the choice and stops there. The client's sold-out and quantity limits are cosmetic, taken from the numbers the agent itself sent, so the agent must re-validate every request.",
    )
