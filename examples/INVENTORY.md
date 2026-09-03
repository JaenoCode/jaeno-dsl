# DSL Type Inventory (Step 1.1)

Ground truth as of the current `setupDSL()` registration in `lib/main.dart`.
22 `(type, version)` pairs across 14 handler files, 21 registered handler
classes (`menu` has two versions from two classes).

| type | v | handler class | file | example | source |
|---|---|---|---|---|---|
| appointment | 1 | `AppointmentDSLHandler` | appointment_handler.dart | appointment.v1.json | code-derived |
| auction | 1 | `AuctionDSLHandler` | auction_handler.dart | auction.v1.json | test-verified (`test/dsl/auction_handler_test.dart`) |
| bid_confirmation | 1 | `BidConfirmationDSLHandler` | auction_handler.dart | bid_confirmation.v1.json | code-derived |
| auction_result | 1 | `AuctionResultDSLHandler` | auction_handler.dart | auction_result.v1.json | code-derived |
| banner | 1 | `BannerDSLHandler` | banner_handler.dart | banner.v1.json | test-verified (`test/dsl/banner_handler_test.dart`) |
| menu | 1 | `MenuDSLHandler` | menu_handler.dart | menu.v1.json | code-derived |
| menu | 2 | `MenuWithCategoriesDSLHandler` | menu_handler.dart | menu.v2.json | code-derived |
| menu_item | 1 | `MenuItemDSLHandler` | menu_handler.dart | menu_item.v1.json | code-derived, **no observed call site** |
| menu_category | 1 | `MenuCategoryDSLHandler` | menu_handler.dart | menu_category.v1.json | code-derived, **no observed call site** |
| order_summary | 1 | `OrderSummaryDSLHandler` | menu_handler.dart | order_summary.v1.json | code-derived |
| order_confirmation | 1 | `OrderConfirmationDSLHandler` | order_confirmation_dsl_handler.dart | order_confirmation.v1.json | code-derived |
| order_history | 1 | `OrderHistoryDSLHandler` | order_history_dsl_handler.dart | order_history.v1.json | code-derived, **polymorphic field**, see below |
| payment_confirmation | 1 | `PaymentConfirmationDSLHandler` | payment_confirmation_dsl_handler.dart | payment_confirmation.v1.json | code-derived |
| payment | 1 | `PaymentDSLHandler` | payment_dsl_handler.dart | payment.v1.json | code-derived |
| poll | 1 | `PollDSLHandler` | poll_dsl_handler.dart | poll.v1.json | code-derived |
| poll_history | 1 | `PollHistoryDSLHandler` | poll_history_dsl_handler.dart | poll_history.v1.json | code-derived |
| poll_results | 1 | `PollResultsDSLHandler` | poll_results_dsl_handler.dart | poll_results.v1.json | code-derived |
| review | 1 | `ReviewDSLHandler` | rating_handler.dart | review.v1.json | code-derived |
| reminder | 1 | `ReminderDSLHandler` | reminder_handler.dart | reminder.v1.json | test-verified (`test/dsl/reminder_handler_test.dart`) |
| tip_request | 1 | `TipRequestDSLHandler` | tip_handler.dart | tip_request.v1.json | code-derived |
| tip_selected | 1 | `TipSelectedDSLHandler` | tip_handler.dart | tip_selected.v1.json | code-derived |
| tip_declined | 1 | `TipDeclinedDSLHandler` | tip_handler.dart | tip_declined.v1.json | code-derived |

"code-derived" = reconstructed by reading each handler's `msg.get<T>(...)` /
`msg.data[...]` extraction, not pulled from a captured real agent payload.
These need a pass against actual bot output before Step 1.2 schemas are
treated as authoritative — flagged explicitly per [[dsl_agent_owns_data]]:
the agent backend, not this repo, is the real source of these shapes today.

## Decisions made, and why

1. **`menu_item` / `menu_category` are real, kept in.** No call site sends
   these types today (grepped the whole `lib/` tree), but both are dated,
   ticketed additions (`JNO-111`, `JNO-112`, comments in
   `menu_handler.dart:80,104`) for "highlighted single item/category" cards.
   Treat as live types the agent may emit, not dead code — worth a direct
   confirmation from whoever owns the agent side before Step 1.2, since an
   unused type sitting in the schema set is harmless but a *wrong* schema
   for a type nobody's exercised is a silent landmine.

2. **`order_history.orders[].items` is polymorphic — flagged, not resolved.**
   `order_history_dsl_handler.dart:168-192` has a comment: "Normalizes
   whatever the DB returned into ... Handles: real List, clean comma string,
   and stringified Python list." The model is `Object? items` — no shape at
   all. The example file shows both a plain string and a `List<String>`
   for this reason. **Decision: do not paper over this in the schema as a
   single type.** Step 1.2 should write `items` as `oneOf: [string, array
   of string]` and treat the stringified-Python-list case as a known wart
   to normalize server-side, not something the Dart model should special-case
   forever. Bring this to whoever owns the agent/bot output — it's the
   clearest sign in the whole inventory of the schema drifting from the
   sender's actual behavior over time.

3. **`appointment.v1` is a near-empty payload (`{title}` only) — correct
   as inventoried, not a mistake.** The other ~800 lines of
   `appointment_handler.dart` are self-contained client-side booking-form
   UI (calendar, time slots, service picker) with no DSL data backing it.
   The DSL card is just a trigger. Confirmed by grep: exactly one `msg.`
   reference in the whole file.

4. **`menu` v1 vs v2 are genuinely different shapes** (flat `items[]` vs
   nested `categories[].items[]`), not a versioning mistake — both handlers
   are still registered and presumably both still in active use. Keep as
   two separate schema files, `menu.v1.json` / `menu.v2.json`, per the
   "never modify an existing version" rule in `DSL.md`.

5. **Numeric fields are inconsistently typed across the inventory** and this
   is preserved as-is rather than "fixed" in the examples:
   - `menu.items[].price` is a **string** (`"1200"`), parsed via
     `int.tryParse` at render time.
   - `payment.amount`, `payment_confirmation.amount`, `order_summary.total`
     are **int**.
   - `order_confirmation.total_amount`, `auction.starting_price`/`min_bid`,
     `bid_confirmation.amount`, `auction_result.winning_amount` are **num**
     (accept int or double, via a local `_asNum` helper).
   Step 1.2 needs to encode these exactly as they are per-type, not
   normalize them to one convention — that's a v2 migration if it's wanted,
   not a schema-writing decision.

6. **`poll.poll_type` enum has 6 values, all handled.**
   `single_choice | multi_select | yes_no | rating | open_text | ranking`
   (documented at `poll_dsl_handler.dart:37`, and every value has a
   dedicated case in the `_PollBody` switch at line ~352 — `yes_no` shares
   `single_choice`'s widget, everything else gets its own; an unrecognized
   value falls soft to `SizedBox.shrink()`). Schema should enum all 6, not
   just the 3 exercised by the example payloads above — `example.v1.json`
   only shows `rating`, so this is a case where the schema is written from
   the code/comment, not the single example on file. Worth grabbing one
   real example per `poll_type` variant if you want fuller example coverage
   later, but it's not blocking Step 1.2.

7. **`menu.items[].price` (string) and `order_confirmation.items[].price`
   (number) are not the same convention, despite both being "an item's
   price" in adjacent DSL types.** Caught during Step 1.2 validation: the
   first draft of `examples/order_confirmation.v1.json` copied menu's
   string-price convention and `ajv`/`jsonschema` correctly rejected it
   against `OrderItem.price`'s `price is num ? price : null` check in
   `order_confirmation_dsl_handler.dart:33-38`. Fixed the example, not the
   schema — this is exactly the class of bug Step 1.2's validation pass is
   supposed to catch. If the agent side ever sends a string price for
   `order_confirmation`, it silently nulls out today instead of erroring;
   worth a defensive look independent of this schema work.

## Not included

`loyalty` and `subscriptions` (named in the original rough plan) are not
DSL types — they're plain Supabase-backed features (`LoyaltyService` etc.)
with no `ai.jaeno.dsl` payload, so they're out of scope for this pipeline
entirely.
