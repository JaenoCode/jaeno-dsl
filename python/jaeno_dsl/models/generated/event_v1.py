# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/event.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Event(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    id: str = Field(
        ...,
        description="The agent's own identifier, echoed back on ticket_request. Opaque to Jaeno.",
    )
    title: str
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


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str
    events: list[Event] = Field(
        ...,
        description="Rows are display-only in v1. Picking a tier and quantity is ticket_request (JNO-335); until that ships a row has nothing to tap.",
    )


class EventV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["event"]
    data: Data = Field(
        ...,
        description="A list of events to browse. Every field is owned and populated by the business's own agent — Jaeno keeps no event table and no availability state, and renders exactly what arrives.",
    )
