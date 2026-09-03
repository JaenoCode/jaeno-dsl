# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/banner.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    variant: str | None = Field(
        None,
        description="Confirmed optional via test/dsl/banner_handler_test.dart (defaults to 'info'). Observed values so far: outage, success — not a closed enum, banner is meant to render arbitrary agent content per the same test file.",
    )
    title: str
    message: str
    meta: str | None = Field(None, description="Confirmed optional via test.")


class BannerV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["banner"]
    data: Data
