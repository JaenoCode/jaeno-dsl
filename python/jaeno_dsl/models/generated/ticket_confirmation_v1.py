# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/ticket_confirmation.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, conint


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    event_id: str = Field(..., description="The agent's own identifier, opaque to Jaeno.")
    event_title: str
    reference: str = Field(
        ...,
        description="The booking reference the agent issued, rendered verbatim and given the most visual weight on the card. Jaeno neither generates nor checks it.",
    )
    tier_name: str | None = None
    quantity: conint(ge=1) | None = Field(
        None, description="Defaults to 1 client-side if missing or not an int."
    )
    starts_at: str | None = Field(
        None,
        description="ISO-8601. Same rendering as the event cards: d/m/yyyy · HH:mm, unparseable values shown verbatim.",
    )
    ends_at: str | None = Field(
        None, description="ISO-8601. When on the same day as starts_at, only its time is shown."
    )
    location_type: Literal["in_person", "online"] | None = None
    location: str | None = Field(None, description="Venue, for location_type in_person.")
    online_url: str | None = Field(
        None,
        description="Join link, for location_type online. Rendered as text, not a tappable link.",
    )


class TicketConfirmationV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["ticket_confirmation"]
    data: Data = Field(
        ...,
        description="Agent → client: the customer's proof of reservation. Jaeno has no role in deciding when a confirmation is issued or what counts as a valid reference code — this is purely a render target for whatever the agent secured. Sending one does not make a reservation real; the agent's own backend is the record.",
    )
