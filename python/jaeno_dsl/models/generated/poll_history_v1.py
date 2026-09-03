# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/poll_history.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Answer(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    question: str | None = None
    answer: str | None = Field(
        None,
        description="Free text regardless of the originating poll_type — e.g. a rating comes through as the stringified number ('5').",
    )
    poll_type: (
        Literal["single_choice", "multi_select", "yes_no", "rating", "open_text", "ranking"] | None
    ) = None
    created_at: str | None = None


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    answers: list[Answer]


class PollHistoryV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["poll_history"]
    data: Data
