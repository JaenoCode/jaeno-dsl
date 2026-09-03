# DSL Schemas (Step 1.2)

JSON Schema (2020-12) for every `(type, version)` pair inventoried in
`examples/INVENTORY.md`. One file per pair, `<type>.v<version>.json`,
matching the example file of the same name in `examples/`.

## Conventions

- Each schema validates the **full envelope** — `{v, type, data}` — not
  just `data`. `v` and `type` are `const`, so the wrong schema can never
  accidentally validate the wrong payload.
- `data.additionalProperties` is `true` everywhere, deliberately. Only 3 of
  22 types (`auction`, `banner`, `reminder`) are backed by a real test
  fixture — the other 19 are reconstructed from `msg.get<T>(...)` call
  sites, which prove a field is *read* if present but say nothing about
  whether the agent might also send other fields today that the client
  just ignores. A closed (`additionalProperties: false`) schema on
  code-derived types would fail CI the moment the agent sends one more
  field than this repo happens to read — a false alarm, not a real schema
  violation. Revisit per-type once the agent side confirms its exhaustive
  field list.
- `required` lists only fields with real evidence of always being present
  (either a test fixture without a fallback, or a Dart field with no `??`
  default). Everything else is left optional even where a single example
  payload happens to include it — see `examples/INVENTORY.md` for which
  fields are confirmed-optional vs. assumed.
- Never edit a schema for a version already in use — add a new
  `.v<n+1>.json` file instead, matching the "never modify an existing
  version" rule in `DSL.md`.
- **Every bare numeric `const` must carry an explicit `"type": "integer"`
  (or `"number"`) alongside it.** Proven necessary in Step 1.3: quicktype's
  schema-to-Dart codegen infers `double` for a JSON number with no `type`,
  even when the value is a whole number like `"const": 1`. That silently
  produced `double v` in the generated `Banner` model, disagreeing with
  `DSLMessage.version`, which is `int` and is what the registry keys
  lookups on (`dsl_registry.dart`). All 22 `v` fields were patched to
  `{"type": "integer", "const": N}` for this reason — if you add a new
  schema by hand, don't drop this.

## Step 1.3 proof (quicktype, `banner.v1`)

Ran `quicktype --src schemas/banner.v1.json --src-lang schema --lang dart
--top-level Banner` to generate a Dart model, then parsed
`examples/banner.v1.json` through `Banner.fromJson` and re-encoded it —
values matched and the round-trip was structurally identical to the
original. `dart analyze` on the generated file was clean. This confirms
the schema → quicktype → Dart path works end to end, gated on the fix
above. Proof script and generated model are throwaway (scratch dir, not
committed) — Step 1.4 is what makes this repeatable for real.

## Known gaps to close before trusting this as CI-enforced

1. `menu_item.v1` / `menu_category.v1` — no confirmed real payload exists
   anywhere; schemas are a best guess from the handler code only.
2. `order_history.v1` `orders[].items` — intentionally typed as
   `oneOf [array<string>, string]` because the client code itself treats
   it as polymorphic. Not a schema weakness; a real inconsistency in what
   gets sent, called out for the agent team.
3. 19 of 22 examples are code-derived, not pulled from captured agent
   output. Swap in real payloads as they become available and re-run
   validation — that's what caught the `order_confirmation.items[].price`
   type mismatch (string vs. number) during this pass.

## Step 1.4 (`scripts/generate_dsl_models.sh`)

One script, loops `schemas/*.json`, runs quicktype per file, writes into
`lib/dsl/models/generated/`. Naming: `<type>.v<version>.json` →
`<type>.v<version>.dart`, top-level class `PascalCase(type)V<version>`
(e.g. `bid_confirmation.v1.json` → `BidConfirmationV1`).

**Why the script also renames nested classes/enums/vars, not just the
top-level type:** every schema shares the `{v, type, data}` envelope, so
quicktype independently emits `class Data`, `enum Type`, `final
typeValues`, `class EnumValues<T>` in **every one of the 22 files** —
verified by generating `menu.v1` / `order_history.v1` / `poll_results.v1`
side by side and diffing. Schemas that reuse a property name (`items`,
etc.) also collide on nested class names like `Item`. Left alone, this
compiles fine per-file but breaks the instant two generated files are
imported unprefixed into the same dispatcher — which Step 1.6 will need to
do for all 22. The script post-processes each file with a scoped rename
(`Data` → `BidConfirmationV1Data`, `typeValues` →
`bidConfirmationV1TypeValues`, etc.) so the whole directory can be
imported flat. Proved by generating all 22, then compiling a throwaway
file that imports all 22 unprefixed (`dart run` succeeded, 0 collisions).

`lib/dsl/models/generated/**` is excluded from `analyzer`/`dart_code_linter`
in `analysis_options.yaml` — generated code shouldn't carry the same style
bar as hand-written code (and gets thrown away on every regen). This only
suppresses lint output, not compilation: a genuinely broken generated file
still fails `flutter test` / `flutter build` / `dart analyze` run without
the exclude, same as any other Dart file.

**Generated output is committed, not gitignored** — Step 1.7's CI check is
a diff against what's committed, so there must be something to diff
against.

Rerun after any schema change:

```bash
./scripts/generate_dsl_models.sh
```

The script also emits `lib/dsl/models/generated/dsl_generated_validators.dart`
— a `(type, version) -> bool Function(Map)` table built from the same loop,
so adding a new schema automatically wires up its validation with no manual
edits anywhere. See Step 1.6 below.

## Step 1.6 (edge validation, `dsl_event_extension.dart`)

`EventDSLRuntime.buildDSLWidget()` / `.renderDSL()` now check a resolved
handler's raw envelope against `isValidGeneratedDSL()` before calling
`handler.render(...)`. Enforced for all 22 types from the start (not staged
by confidence level) — the tradeoff being that any of the 19 code-derived
schemas (see `examples/INVENTORY.md`) that turn out to be wrong about a
real field will show the fallback card for content that used to render,
until that schema is corrected against real agent output. Chosen
deliberately over a quieter log-only rollout so schema gaps surface
immediately instead of silently.

Tests: `test/dsl/edge_validation_test.dart` — known-good payload dispatches
normally; a wrong field type or a missing required field on a *known*
(type, version) now falls back instead of the pre-Step-1.6 behavior of
silently rendering with a blanked-out field; an unrecognized (type,
version) falls back (pre-existing registry behavior, still covered); a
structurally invalid envelope (`dsl` getter returns null) never reaches a
widget at all, confirmed to return `null` rather than throw.

## Validating

```bash
./scripts/validate_dsl_schemas.sh
```

Uses `ajv-cli` (pinned version, via `npx`) against the `--spec=draft2020`
profile, matching every schema's `$schema`. Also fails if `schemas/` and
`examples/` ever go out of 1:1 sync (a schema with no example, or vice
versa). This superseded an ad-hoc `python3` + `jsonschema` snippet used
while writing Step 1.2 — that one silently ignored the `"format"` keyword,
which is how `auction.v1.json`'s `ends_at` originally shipped with
`"format": "date-time"` unnoticed; ajv's stricter default caught it (see
Step 1.7).

## Step 1.7 (CI, `.github/workflows/integrate.yaml`)

Two steps added to the `code_tests` job, right after `flutter pub get` (so
`dart format` is available when `generate_dsl_models.sh` runs — running it
earlier, before Flutter's set up, would format-drift the output from what's
committed):

1. `./scripts/validate_dsl_schemas.sh` — every example must validate.
2. `./scripts/generate_dsl_models.sh` then `git diff --exit-code
   lib/dsl/models/generated/` — if regenerating produces anything different
   from what's committed, fail loudly with a specific "stale generated
   models" message rather than a bare diff dump.

Both `quicktype` and `ajv-cli` are pinned to exact versions in the scripts
(`quicktype@24.0.2`, `ajv-cli@5.0.0`) — unpinned, a tool update could change
codegen output or validation behavior on its own, and CI's failure message
would be misleading (blaming "stale models" for what's actually a tooling
version change). Bump deliberately when there's a reason to.

**Found while wiring this up:** `ajv-cli`'s default strict mode rejects
unrecognized `"format"` values instead of silently ignoring them like the
`python3`/`jsonschema` check used earlier in this doc did. That surfaced
`auction.v1.json`'s `"format": "date-time"` on `ends_at` as a hard failure.
Fixed by dropping the annotation rather than pulling in `ajv-formats`:
Dart's actual parsing (`DateTime.tryParse`, lenient) never matched strict
RFC 3339 anyway, and the annotation had a second, worse effect —
quicktype was using it to generate `DateTime? endsAt` with **strict**
`DateTime.parse()` in the generated model, which meant Step 1.6's edge
validation would reject a payload for a malformed-but-non-catastrophic
`ends_at` string that the real handler (`auction_handler.dart`, using
`tryParse`) would have tolerated fine. Regenerated after the fix; `ends_at`
is now `String?`, matching the handler's actual leniency.

Verified the wholee loop locally before trusting it: staged the current
tree as a stand-in for "committed," edited a schema field without
regenerating, ran the exact CI steps — confirmed step 2 fails with the
stale-models message and shows the real diff; then regenerated and
confirmed it passes clean. Reverted the simulated edit afterward.
