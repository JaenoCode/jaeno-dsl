"""Calculator formula grammar + field rules, ported from calculator_handler.dart."""

from __future__ import annotations

import pytest

from jaeno_dsl import DSLInvalidPayloadError, build_dsl_event_content
from jaeno_dsl.calculator import FormulaError, parse_calculator_formula

KEYS = {"guests", "hours", "tier"}


@pytest.mark.parametrize(
    "formula",
    [
        "guests * tier + hours * 2000",
        "(guests + 1) * tier",
        "-guests + +hours",
        "guests / hours",
        "3.5 * guests",
    ],
)
def test_valid_formulas(formula: str) -> None:
    parse_calculator_formula(formula, KEYS)


@pytest.mark.parametrize(
    "formula",
    [
        "guests ** 2",  # exponent
        "guests ^ 2",
        "guests % 2",
        "max(guests, 1)",  # call
        "guests.count",  # attribute
        "guests[0]",  # index
        "guests > 1",  # comparison
        "unknown_field * 2",  # undeclared identifier
        "guests +",  # dangling operator
        "(guests + 1",  # unbalanced
        "guests 1",  # trailing token
        "'string'",
        "guests, hours",
    ],
)
def test_rejected_formulas(formula: str) -> None:
    with pytest.raises(FormulaError):
        parse_calculator_formula(formula, KEYS)


def _calc(**overrides: object) -> dict[str, object]:
    data: dict[str, object] = {
        "title": "Estimate",
        "fields": [
            {"key": "guests", "label": "Guests", "type": "number"},
            {
                "key": "tier",
                "label": "Tier",
                "type": "choice",
                "options": [{"label": "Std", "value": 1}, {"label": "Premium", "value": 2}],
            },
        ],
        "formula": "guests * tier",
        "result_label": "Total",
    }
    data.update(overrides)
    return data


def test_valid_calculator_builds() -> None:
    content = build_dsl_event_content("calculator", 1, _calc())
    assert content["ai.jaeno.dsl"]["type"] == "calculator"


def test_ninth_field_rejected() -> None:
    fields = [{"key": f"f{i}", "label": f"F{i}", "type": "number"} for i in range(9)]
    with pytest.raises(DSLInvalidPayloadError):
        build_dsl_event_content("calculator", 1, _calc(fields=fields, formula="f0"))


def test_choice_without_options_rejected() -> None:
    with pytest.raises(DSLInvalidPayloadError):
        build_dsl_event_content(
            "calculator",
            1,
            _calc(fields=[{"key": "t", "label": "T", "type": "choice"}], formula="t"),
        )


def test_unparseable_formula_rejected() -> None:
    with pytest.raises(DSLInvalidPayloadError):
        build_dsl_event_content("calculator", 1, _calc(formula="guests ** 2"))


def test_duplicate_field_key_rejected() -> None:
    with pytest.raises(DSLInvalidPayloadError):
        build_dsl_event_content(
            "calculator",
            1,
            _calc(
                fields=[
                    {"key": "g", "label": "A", "type": "number"},
                    {"key": "g", "label": "B", "type": "number"},
                ],
                formula="g",
            ),
        )
