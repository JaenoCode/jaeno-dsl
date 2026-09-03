# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/faq.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    question: str
    answer: str = Field(
        ...,
        description="Plain text. Markdown is not rendered — widget_library has no markdown renderer (same as terms.body).",
    )


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str | None = Field(None, description="Card headline. Defaults client-side to 'FAQ'.")
    items: list[Item] = Field(
        ...,
        description="One entry renders expanded — the direct answer to one question (JNO-55). Several render as a collapsed accordion to browse (JNO-56). One type either way: the agent sends what it has and the card decides how to show it.",
    )


class FaqV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["faq"]
    data: Data
