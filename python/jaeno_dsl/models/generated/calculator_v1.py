# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/calculator.v1.json
# Regenerate with: ./python/scripts/generate_models.sh

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Option(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    label: str
    value: float


class FieldModel(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    key: str = Field(..., description="Identifier the formula references.")
    label: str
    type: Literal["number", "choice"]
    min: float | None = None
    max: float | None = None
    required: bool | None = None
    options: list[Option] | None = Field(
        None,
        description="Required in practice when type is choice; a choice field with no options throws in render(). Not expressible here without an if/then the codegen would ignore anyway.",
    )


class Data(BaseModel):
    model_config = ConfigDict(
        extra="allow",
    )
    title: str
    subtitle: str | None = None
    fields: list[FieldModel] = Field(
        ...,
        description="Capped at 8. NOT enforced by the generated model — quicktype drops maxItems — so calculator_handler.dart re-checks the cap in render() and throws, which routes to the same failed fallback card. This keyword is the contract for the bot side.",
        max_length=8,
    )
    formula: str = Field(
        ...,
        description="Restricted arithmetic only: numeric literals, declared field keys, + - * /, unary sign, parentheses. Grammar is enforced by the hand-rolled parser in calculator_handler.dart, not here — an unparseable formula is still a well-formed JSON string.",
    )
    result_label: str
    result_unit: str | None = None


class CalculatorV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["calculator"]
    data: Data
