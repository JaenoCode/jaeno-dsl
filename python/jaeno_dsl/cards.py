# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/*.json (all)
# Regenerate with: ./python/scripts/generate_models.sh
#
"""One constructor per DSL (type, version). Each validates and returns a
Matrix event content dict — see jaeno_dsl.envelope.build_dsl_event_content.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any

from .envelope import build_dsl_event_content


def address_request_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("address_request", 1, data, body=body, **fields)


def address_response_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("address_response", 1, data, body=body, **fields)


def appointment_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("appointment", 1, data, body=body, **fields)


def auction_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("auction", 1, data, body=body, **fields)


def auction_result_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("auction_result", 1, data, body=body, **fields)


def banner_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("banner", 1, data, body=body, **fields)


def bid_confirmation_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("bid_confirmation", 1, data, body=body, **fields)


def calculator_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("calculator", 1, data, body=body, **fields)


def calculator_result_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("calculator_result", 1, data, body=body, **fields)


def car_request_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("car_request", 1, data, body=body, **fields)


def car_response_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("car_response", 1, data, body=body, **fields)


def countdown_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("countdown", 1, data, body=body, **fields)


def event_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("event", 1, data, body=body, **fields)


def event_detail_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("event_detail", 1, data, body=body, **fields)


def faq_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("faq", 1, data, body=body, **fields)


def fulfillment_method_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("fulfillment_method", 1, data, body=body, **fields)


def fulfillment_selection_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("fulfillment_selection", 1, data, body=body, **fields)


def menu_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("menu", 1, data, body=body, **fields)


def menu_v2(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("menu", 2, data, body=body, **fields)


def menu_category_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("menu_category", 1, data, body=body, **fields)


def menu_item_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("menu_item", 1, data, body=body, **fields)


def name_request_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("name_request", 1, data, body=body, **fields)


def name_response_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("name_response", 1, data, body=body, **fields)


def order_confirmation_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("order_confirmation", 1, data, body=body, **fields)


def order_confirmation_v2(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("order_confirmation", 2, data, body=body, **fields)


def order_confirmation_v3(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("order_confirmation", 3, data, body=body, **fields)


def order_history_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("order_history", 1, data, body=body, **fields)


def order_status_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("order_status", 1, data, body=body, **fields)


def order_summary_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("order_summary", 1, data, body=body, **fields)


def payment_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("payment", 1, data, body=body, **fields)


def payment_confirmation_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("payment_confirmation", 1, data, body=body, **fields)


def poll_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("poll", 1, data, body=body, **fields)


def poll_history_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("poll_history", 1, data, body=body, **fields)


def poll_results_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("poll_results", 1, data, body=body, **fields)


def reminder_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("reminder", 1, data, body=body, **fields)


def review_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("review", 1, data, body=body, **fields)


def terms_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("terms", 1, data, body=body, **fields)


def terms_history_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("terms_history", 1, data, body=body, **fields)


def terms_response_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("terms_response", 1, data, body=body, **fields)


def ticket_confirmation_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("ticket_confirmation", 1, data, body=body, **fields)


def ticket_request_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("ticket_request", 1, data, body=body, **fields)


def tip_declined_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("tip_declined", 1, data, body=body, **fields)


def tip_request_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("tip_request", 1, data, body=body, **fields)


def tip_selected_v1(
    data: Mapping[str, Any] | None = None,
    /,
    *,
    body: str | None = None,
    **fields: Any,
) -> dict[str, Any]:
    return build_dsl_event_content("tip_selected", 1, data, body=body, **fields)


CARD_CONSTRUCTORS: dict[tuple[str, int], Callable[..., dict[str, Any]]] = {
    ("address_request", 1): address_request_v1,
    ("address_response", 1): address_response_v1,
    ("appointment", 1): appointment_v1,
    ("auction", 1): auction_v1,
    ("auction_result", 1): auction_result_v1,
    ("banner", 1): banner_v1,
    ("bid_confirmation", 1): bid_confirmation_v1,
    ("calculator", 1): calculator_v1,
    ("calculator_result", 1): calculator_result_v1,
    ("car_request", 1): car_request_v1,
    ("car_response", 1): car_response_v1,
    ("countdown", 1): countdown_v1,
    ("event", 1): event_v1,
    ("event_detail", 1): event_detail_v1,
    ("faq", 1): faq_v1,
    ("fulfillment_method", 1): fulfillment_method_v1,
    ("fulfillment_selection", 1): fulfillment_selection_v1,
    ("menu", 1): menu_v1,
    ("menu", 2): menu_v2,
    ("menu_category", 1): menu_category_v1,
    ("menu_item", 1): menu_item_v1,
    ("name_request", 1): name_request_v1,
    ("name_response", 1): name_response_v1,
    ("order_confirmation", 1): order_confirmation_v1,
    ("order_confirmation", 2): order_confirmation_v2,
    ("order_confirmation", 3): order_confirmation_v3,
    ("order_history", 1): order_history_v1,
    ("order_status", 1): order_status_v1,
    ("order_summary", 1): order_summary_v1,
    ("payment", 1): payment_v1,
    ("payment_confirmation", 1): payment_confirmation_v1,
    ("poll", 1): poll_v1,
    ("poll_history", 1): poll_history_v1,
    ("poll_results", 1): poll_results_v1,
    ("reminder", 1): reminder_v1,
    ("review", 1): review_v1,
    ("terms", 1): terms_v1,
    ("terms_history", 1): terms_history_v1,
    ("terms_response", 1): terms_response_v1,
    ("ticket_confirmation", 1): ticket_confirmation_v1,
    ("ticket_request", 1): ticket_request_v1,
    ("tip_declined", 1): tip_declined_v1,
    ("tip_request", 1): tip_request_v1,
    ("tip_selected", 1): tip_selected_v1,
}
