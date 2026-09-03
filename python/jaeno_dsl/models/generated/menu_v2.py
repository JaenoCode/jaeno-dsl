# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/menu.v2.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Item(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str
    price: str = Field(..., description="String, matches menu.v1 item price convention.")
    image: str | None = None
    orderable: bool | None = Field(
        None,
        description="Per-item override of the menu-wide 'orderable' flag. Defaults to true if absent.",
    )


class Category(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str
    banner: str | None = None
    items: list[Item]


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str | None = None
    banner: str | None = None
    orderable: bool | None = Field(
        None, description="Menu-wide default, defaults to true if absent."
    )
    categories: list[Category]


class MenuV2(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[2]
    type: Literal["menu"]
    data: Data
