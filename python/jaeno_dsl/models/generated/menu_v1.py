# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/menu.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str
    price: str = Field(
        ...,
        description="String, not a number — parsed with int.tryParse at render time (menu_handler.dart:484). Do not change to a numeric type without a v2 migration.",
    )
    image: str | None = None
    description: str | None = None


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str | None = None
    banner: str | None = None
    items: list[Item]


class MenuV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["menu"]
    data: Data
