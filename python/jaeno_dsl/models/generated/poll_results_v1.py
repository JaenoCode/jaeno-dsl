# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/poll_results.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Result(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    option: str | None = None
    percent: float | None = None


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    question: str
    poll_type: (
        Literal["single_choice", "multi_select", "yes_no", "rating", "open_text", "ranking"] | None
    ) = None
    menu_item: str | None = None
    average_x10: int | None = Field(
        None,
        description="Fixed-point: real average = average_x10 / 10.0. Only meaningful for poll_type = rating.",
    )
    total_votes: int | None = None
    results: list[Result] | None = None


class PollResultsV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["poll_results"]
    data: Data
