# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/menu_category.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    name: str | None = None
    banner: str | None = None
    items: list[dict[str, Any]] | None = Field(
        None,
        description="Passed straight through to the items sheet untyped in the handler (List, not parsed into a model here) — item shape assumed to match menu.v1 items.",
    )


class MenuCategoryV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["menu_category"]
    data: Data = Field(
        ...,
        description="JNO-112 'highlighted single category' card. No observed call site anywhere in this repo as of this schema's writing — code-derived from MenuCategoryDSLHandler only. Confirm this type is actually emitted before trusting this schema in CI.",
    )
