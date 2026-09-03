# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/appointment.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str | None = None


class AppointmentV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["appointment"]
    data: Data = Field(
        ...,
        description="Trigger-only card. Fields beyond 'title' are not read by AppointmentDSLHandler today — the booking form itself is entirely client-side state (date/time/service), not agent-supplied.",
    )
