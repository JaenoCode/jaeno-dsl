# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/calculator_result.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Input(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    label: str
    value: str = Field(
        ..., description="For a choice field this is the option's label, not its numeric value."
    )


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str
    inputs: list[Input] = Field(
        ...,
        description="Display labels and formatted values, never field keys or raw indices — the bot keeps no state about the card it sent, so this has to be self-contained.",
    )
    result_label: str
    result_value: str
    result_unit: str | None = None


class CalculatorResultV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["calculator_result"]
    data: Data
