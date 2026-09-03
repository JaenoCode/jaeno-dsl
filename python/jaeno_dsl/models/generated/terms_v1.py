# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/terms.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    terms_id: str = Field(
        ..., description="Stable id for the agreement, echoed back in terms_response."
    )
    version: str = Field(
        ...,
        description="Agent-owned version label for this text, echoed back in terms_response. A string, not a date — the agent decides the scheme.",
    )
    title: str
    body: str = Field(
        ...,
        description="Full agreement text, markdown. The client currently renders it as plain text (see terms_handler.dart).",
    )
    signing_level: Literal["tap", "typed", "drawn"] = Field(
        ...,
        description="What the agent asks for. What the device actually delivered comes back as terms_response.method, which may be a lower rung after fallback (drawn -> typed -> tap).",
    )
    allow_decline: bool | None = Field(
        None,
        description="Defaults to true client-side — shows a Decline button that sends agreed: false.",
    )


class TermsV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["terms"]
    data: Data
