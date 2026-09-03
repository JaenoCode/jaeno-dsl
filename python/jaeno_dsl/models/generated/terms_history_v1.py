# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/terms_history.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Agreement(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    terms_id: str | None = None
    title: str | None = None
    version: str | None = Field(
        None,
        description="The version of the terms that was actually presented — JNO-98's point is that each record names its own text.",
    )
    method: Literal["tap", "typed", "drawn"] | None = Field(
        None,
        description="As delivered by the device, echoed from terms_response.method — not the signing_level the agent asked for.",
    )
    signed_at: str | None = None
    body: str | None = Field(
        None,
        description="The agreement text as it read at this version, markdown. Optional: without it the row shows only the metadata, with it the row opens the full document the customer signed (JNO-97's 'view a copy'). Send the stored copy, never today's constant.",
    )
    agreed: bool | None = Field(
        None,
        description="Defaults to true client-side. Present so a history that includes declines renders them as declines rather than as agreements.",
    )


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    agreements: list[Agreement] = Field(
        ...,
        description="Agent-supplied, newest first. The agent owns the stored contracts (JNO-97) — the client only renders what it is handed.",
    )


class TermsHistoryV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["terms_history"]
    data: Data
