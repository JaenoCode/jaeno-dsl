"""Fallback ``body`` text for a DSL event.

Every ``ai.jaeno.dsl`` event is sent as ``m.text`` with a plain ``body``. The
Jaeno client renders the card and ignores the body; every *other* client, plus
push notifications and timeline previews, shows the body and nothing else. So
it has to say something useful on its own.

Per-type builders exist only where a one-liner is genuinely better than the
generic default (JNO-347 decision). Anything not listed falls through to
:data:`_GENERIC`. A builder that raises is ignored — the generic default is
always a safe answer.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

_GENERIC = "Open the Jaeno app to view this message."


def _join(*parts: object) -> str:
    return " — ".join(str(p) for p in parts if p not in (None, ""))


def _payment(d: dict[str, Any]) -> str:
    amount, currency = d.get("amount"), d.get("currency")
    if amount is None:
        return "Payment request"
    return _join("Payment request", f"{amount} {currency}".strip() if currency else str(amount))


_BUILDERS: dict[str, Callable[[dict[str, Any]], str]] = {
    "banner": lambda d: _join(d.get("title"), d.get("message")),
    "reminder": lambda d: _join(d.get("title") or "Reminder", d.get("message"), d.get("time")),
    "countdown": lambda d: _join(d.get("title"), d.get("subtitle")),
    "menu": lambda d: _join("Menu", d.get("title")),
    "menu_item": lambda d: _join(d.get("name"), d.get("price")),
    "menu_category": lambda d: _join("Menu", d.get("name")),
    "faq": lambda d: d.get("title") or "FAQ",
    "payment": _payment,
    "payment_confirmation": lambda d: "Payment confirmed",
    "order_confirmation": lambda d: "Order confirmed",
    "order_status": lambda d: _join("Order status", d.get("status")),
    "appointment": lambda d: _join("Appointment", d.get("title")),
    "poll": lambda d: d.get("question") or "Poll",
    "review": lambda d: d.get("question") or "Leave a review",
    "terms": lambda d: _join("Agreement", d.get("title")),
    "tip_request": lambda d: d.get("title") or "Add a tip?",
    "auction": lambda d: _join("Auction", d.get("title")),
}


def fallback_body(dsl_type: str, version: int, data: dict[str, Any]) -> str:
    builder = _BUILDERS.get(dsl_type)
    if builder is not None:
        try:
            text = builder(data)
        except Exception:  # noqa: BLE001 - a bad builder must never block a send
            text = ""
        if text and text.strip():
            return text.strip()
    return _GENERIC
