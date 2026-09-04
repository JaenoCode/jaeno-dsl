# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/event_detail.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, conint


class Tier(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str
    price: str = Field(
        ...,
        description="Pre-formatted by the agent, same convention as menu item prices — Jaeno does no currency handling.",
    )
    remaining: conint(ge=0) | None = Field(
        None,
        description="Optional. 0 renders 'Sold out', a positive number renders 'N left', and omitting it renders neither. Stale the moment it is sent, so an agent that cannot keep it accurate should leave it out rather than send a number that will be wrong.",
    )


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    id: str = Field(
        ...,
        description="The agent's own identifier, echoed back on ticket_request. Opaque to Jaeno.",
    )
    title: str
    description: str | None = None
    starts_at: str = Field(
        ...,
        description="ISO-8601. Rendered as d/m/y plus HH:mm; an unparseable value renders as-is rather than being dropped.",
    )
    ends_at: str | None = Field(
        None,
        description="ISO-8601. When present and on the same day as starts_at, only its time is shown.",
    )
    location_type: Literal["in_person", "online"]
    location: str | None = Field(None, description="Venue, for location_type in_person.")
    online_url: str | None = Field(
        None,
        description="Join link, for location_type online. Rendered as text, not a tappable link — the agent sends it when it decides the customer should have it.",
    )
    tiers: list[Tier] | None = Field(
        None, description="Ticket tiers, in the order the agent wants them shown."
    )


class EventDetailV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["event_detail"]
    data: Data = Field(
        ...,
        description="One event in full. Capacity, holds and releases live entirely in the business's agent — 'remaining' below is a number the agent chose to show, not a figure Jaeno tracks or can keep current.",
    )
