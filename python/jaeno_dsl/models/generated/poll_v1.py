# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/poll.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    poll_id: str
    question: str
    poll_type: Literal[
        "single_choice", "multi_select", "yes_no", "rating", "open_text", "ranking"
    ] = Field(
        ...,
        description="All 6 values documented at poll_dsl_handler.dart:37 and have a dedicated render branch (_PollBody switch, ~line 352). Only 'rating' is covered by examples/poll.v1.json — the other 5 are enumerated from code/comment, not from a captured real payload.",
    )
    options: list[str] | None = Field(
        None,
        description="Required for single_choice/multi_select/ranking; meaningless for rating/open_text but the client tolerates an empty or absent array either way.",
    )
    allow_multiple: bool | None = None
    rating_style: str | None = Field(
        None, description="Only relevant when poll_type = rating. Default 'stars'."
    )
    rating_max: int | None = Field(
        None, description="Only relevant when poll_type = rating. Default 5."
    )
    chain_id: str | None = Field(
        None,
        description="Groups the questions of one flow into a single card: polls carrying the same chain_id share one card, which steps through them one question at a time, instead of arriving as separate tiles (packages/widget_library/lib/models/poll_chain.dart). The whole group may be sent at once — no need to wait for each answer. Send it on every question in the group, including the first. OMIT it for a question that should stand on its own — a confirmation, say — and never reuse a group's value for one, or that question lands inside the card the customer just finished. Any stable string works; the order id is the natural choice.",
    )


class PollV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["poll"]
    data: Data
