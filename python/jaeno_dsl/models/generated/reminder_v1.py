# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/reminder.v1.json
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
        description="Confirmed optional via test/dsl/reminder_handler_test.dart (defaults to 'default'). Observed values: default, urgent — not a closed enum.",
    )
    title: str | None = Field(
        None, description="Confirmed optional via test (defaults to 'Reminder')."
    )
    message: str
    time: str | None = Field(
        None,
        description="Confirmed optional via test. Free-text, not ISO 8601 in the observed examples ('Tomorrow at 3:00 PM').",
    )


class ReminderV1(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    v: Literal[1]
    type: Literal["reminder"]
    data: Data
