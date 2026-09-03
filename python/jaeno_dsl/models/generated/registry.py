# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/*.json (all)
# Regenerate with: ./python/scripts/generate_models.sh
#
# Maps every (type, version) to its generated Pydantic model, so DSL
# edge validation can check a raw envelope against the schema-derived
# model before send — the peer of dsl_generated_validators.dart.
from __future__ import annotations

from pydantic import BaseModel

from .address_request_v1 import AddressRequestV1
from .address_response_v1 import AddressResponseV1
from .appointment_v1 import AppointmentV1
from .auction_result_v1 import AuctionResultV1
from .auction_v1 import AuctionV1
from .banner_v1 import BannerV1
from .bid_confirmation_v1 import BidConfirmationV1
from .calculator_result_v1 import CalculatorResultV1
from .calculator_v1 import CalculatorV1
from .car_request_v1 import CarRequestV1
from .car_response_v1 import CarResponseV1
from .countdown_v1 import CountdownV1
from .faq_v1 import FaqV1
from .fulfillment_method_v1 import FulfillmentMethodV1
from .fulfillment_selection_v1 import FulfillmentSelectionV1
from .menu_category_v1 import MenuCategoryV1
from .menu_item_v1 import MenuItemV1
from .menu_v1 import MenuV1
from .menu_v2 import MenuV2
from .name_request_v1 import NameRequestV1
from .name_response_v1 import NameResponseV1
from .order_confirmation_v1 import OrderConfirmationV1
from .order_confirmation_v2 import OrderConfirmationV2
from .order_confirmation_v3 import OrderConfirmationV3
from .order_history_v1 import OrderHistoryV1
from .order_status_v1 import OrderStatusV1
from .order_summary_v1 import OrderSummaryV1
from .payment_confirmation_v1 import PaymentConfirmationV1
from .payment_v1 import PaymentV1
from .poll_history_v1 import PollHistoryV1
from .poll_results_v1 import PollResultsV1
from .poll_v1 import PollV1
from .reminder_v1 import ReminderV1
from .review_v1 import ReviewV1
from .terms_history_v1 import TermsHistoryV1
from .terms_response_v1 import TermsResponseV1
from .terms_v1 import TermsV1
from .tip_declined_v1 import TipDeclinedV1
from .tip_request_v1 import TipRequestV1
from .tip_selected_v1 import TipSelectedV1

DSL_MODELS: dict[str, dict[int, type[BaseModel]]] = {
    "address_request": {
        1: AddressRequestV1,
    },
    "address_response": {
        1: AddressResponseV1,
    },
    "appointment": {
        1: AppointmentV1,
    },
    "auction": {
        1: AuctionV1,
    },
    "auction_result": {
        1: AuctionResultV1,
    },
    "banner": {
        1: BannerV1,
    },
    "bid_confirmation": {
        1: BidConfirmationV1,
    },
    "calculator": {
        1: CalculatorV1,
    },
    "calculator_result": {
        1: CalculatorResultV1,
    },
    "car_request": {
        1: CarRequestV1,
    },
    "car_response": {
        1: CarResponseV1,
    },
    "countdown": {
        1: CountdownV1,
    },
    "faq": {
        1: FaqV1,
    },
    "fulfillment_method": {
        1: FulfillmentMethodV1,
    },
    "fulfillment_selection": {
        1: FulfillmentSelectionV1,
    },
    "menu": {
        1: MenuV1,
        2: MenuV2,
    },
    "menu_category": {
        1: MenuCategoryV1,
    },
    "menu_item": {
        1: MenuItemV1,
    },
    "name_request": {
        1: NameRequestV1,
    },
    "name_response": {
        1: NameResponseV1,
    },
    "order_confirmation": {
        1: OrderConfirmationV1,
        2: OrderConfirmationV2,
        3: OrderConfirmationV3,
    },
    "order_history": {
        1: OrderHistoryV1,
    },
    "order_status": {
        1: OrderStatusV1,
    },
    "order_summary": {
        1: OrderSummaryV1,
    },
    "payment": {
        1: PaymentV1,
    },
    "payment_confirmation": {
        1: PaymentConfirmationV1,
    },
    "poll": {
        1: PollV1,
    },
    "poll_history": {
        1: PollHistoryV1,
    },
    "poll_results": {
        1: PollResultsV1,
    },
    "reminder": {
        1: ReminderV1,
    },
    "review": {
        1: ReviewV1,
    },
    "terms": {
        1: TermsV1,
    },
    "terms_history": {
        1: TermsHistoryV1,
    },
    "terms_response": {
        1: TermsResponseV1,
    },
    "tip_declined": {
        1: TipDeclinedV1,
    },
    "tip_request": {
        1: TipRequestV1,
    },
    "tip_selected": {
        1: TipSelectedV1,
    },
}
