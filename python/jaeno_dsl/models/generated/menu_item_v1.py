# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/menu_item.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    price: str | None = None
    image: str | None = None
    description: str | None = None


class MenuItemV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["menu_item"]
    data: Data = Field(
        ...,
        description="JNO-111 'highlighted single item' card. No observed call site anywhere in this repo as of this schema's writing — every field below is code-derived from MenuItemDSLHandler, not confirmed against a real agent payload. Confirm this type is actually emitted before trusting this schema in CI.",
    )
