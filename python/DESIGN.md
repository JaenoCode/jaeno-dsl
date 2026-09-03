# Design record — Python DSL sender

Why this package is built the way it is. Originated as the JNO-346 codegen
spike in `JaenoCode/jaeno`; moved here (JNO-345/348) once the schemas did.

## Verdict: `datamodel-code-generator` → Pydantic v2 confirmed

All 7 checks the plan asked for pass. It fixes the exact bugs the Dart side had
to work around, adds zero new runtime dependencies to `jaeno-agent-template`
(`pydantic>=2` is already there and in its import-graph allowlist), and the
Python module-per-schema layout sidesteps the nested-class-collision problem
that forced the Dart script's `sed` renaming pass.

### What was run

```
./python/scripts/generate_models.sh   # 40 models + registry.py
uv run --with pydantic --with pytest pytest -q     # 44 passed
```

- **40/40 schemas** generate with no errors.
- **40/40 `examples/*.json`** validate through their generated model.
- Negative cases behave correctly: missing required field → reject, wrong field
  type → reject, wrong version → reject, unknown envelope key → reject,
  **unknown `data` key → accept** (schemas set `data.additionalProperties: true`
  on purpose — the agent may send fields the client doesn't read yet).
- Regenerating twice is **byte-identical** (`git diff` clean) — the
  commit-and-diff CI check will work.

### The Dart gotchas, re-checked

| Dart problem (`schemas/README.md`) | Python result |
|---|---|
| quicktype infers `double v` from `{"type":"integer","const":1}`, disagreeing with `int` | `v: Literal[1]` — correct, exact |
| `type` const → hand-rolled enum + `values.map[...]!` | `type: Literal['banner']` — clean |
| every file emits `class Data` / `enum Type` → flat-import collisions, needs `sed` rename | one module per schema (`banner_v1.BannerV1`); collisions are a non-issue in Python |
| `"format": "date-time"` made quicktype emit strict `DateTime.parse()`, rejecting lenient strings the handler tolerates | schemas already dropped the annotation; `ends_at: str \| None` — matches handler leniency |
| `oneOf: [array<string>, string]` (`order_history`) | `items: list[str] \| str \| None` — exact |

## Divergences from the Dart model — for the JNO-346 / JNO-347 decisions

1. **`calculator` `maxItems: 8` is enforced** (`fields: list[...] = Field(max_length=8)`).
   Dart drops it; `calculator_handler.dart` re-checks in `render()`. The Python
   model is *stricter* here. Good for a pre-send check (bot told early), and our
   own builder won't send 9 fields, so round-trip is unaffected. The
   formula-grammar check still has to be hand-written in JNO-347 — it isn't
   schema-expressible either way.

2. **Envelope is `extra='forbid'`** (schema `additionalProperties: false`),
   while Dart's `DSLMessage.fromMap` just ignores unknown top-level keys.
   Only bites if the bot puts junk *beside* `v/type/data` — which it shouldn't.
   Open question for JNO-346: keep `forbid` (stricter, catches bot bugs) or
   relax the envelope to `ignore` for exact Dart parity.

3. **`number` → `float`.** JSON ints validate fine via Pydantic coercion
   (`starting_price: 100` → `100.0`). Matches Dart's `num`.

## Generator settings that matter (pin all of these)

- `datamodel-code-generator==0.76.1`, `black==24.10.0`, `isort==5.13.2`
  (via `uvx --from`). Unpinned = silent codegen/formatting drift, same reasoning
  as `quicktype@24.0.2` on the Dart side.
- `--formatters black --formatters isort` **must be explicit** — a FutureWarning
  says the built-in default is changing.
- `--enum-field-as-literal all` (no Enum classes), `--collapse-root-models`,
  `--use-standard-collections --use-union-operator` (3.12 syntax),
  `--disable-timestamp` (determinism), `--custom-file-header` for the
  DO-NOT-EDIT banner.
- **Do NOT pass `--allow-extra-fields`** — dmcg honors per-schema
  `additionalProperties` on its own (envelope forbid, `data` allow), which is
  exactly what we want.
- Per-file loop, not `--input schemas/` directory mode — directory mode trips
  on `schemas/README.md`, and per-file gives us the class/module naming that
  matches the Dart convention.

## Follow-on: JNO-347 (hand-written sender layer) — done on this branch

- `jaeno_dsl/envelope.py` — `build_dsl_event_content()` / `validate_before_send()`.
- `jaeno_dsl/errors.py` — `DSLMalformedEnvelopeError` / `DSLUnknownTypeError` /
  `DSLInvalidPayloadError`, mapped to the sealed `DSLResolution` outcomes.
- `jaeno_dsl/fallback.py` — per-type body text (17 types) + generic default.
- `jaeno_dsl/calculator.py` — formula grammar + field rules ported token-for-token
  from `calculator_handler.dart`.
- `jaeno_dsl/cards.py` — 40 generated constructors, `CARD_CONSTRUCTORS` map.
- 122 tests green (40 examples round-trip through their constructor, plus each
  error branch and the full calculator grammar).

Decisions taken here, revisit in JNO-346/347 review:
- Envelope kept `extra='forbid'` (stricter than Dart, catches bot bugs).
- `calculator` 8-field cap enforced by both the model *and* `calculator.py`.
- Constructors are generated, not hand-written — 40 forwarders add no value
  over a schema-driven loop, and this keeps the "no hardcoded type list" rule.

## CI drift-check (JNO-346) — wired

`.github/workflows/integrate.yaml` gets a `dsl_py` job (separate from
`code_tests` — pure Python/uv, no Flutter SDK):

1. run `generate_dsl_models.sh`, then `git diff --exit-code` on
   `models/generated/` + `cards.py` with a "stale — regenerate" message,
   mirroring the Dart `code_tests` step.
2. `black --check packages/dsl_py`
3. `pytest packages/dsl_py`

Verified locally: clean regen = no drift; a schema edit without regen is
caught; revert is clean.

## Round-trip test against Dart (JNO-348) — done

- `scripts/emit_roundtrip.py` (run by `generate_dsl_models.sh`) writes
  `python/roundtrip/<type>.v<version>.json` — the full Matrix event
  content the bot would send for each pair, built through the real
  `build_dsl_event_content()` from that pair's `examples/` payload. Committed,
  byte-stable, covered by the `dsl_py` CI drift diff and `test_roundtrip_fixtures.py`.
- `packages/docs_app/test/python_roundtrip_test.dart` reads them back: for all
  40, `resolveDSL()` returns `DSLResolved` and `handler.render()` produces a
  widget that pumps without throwing. Plus a coverage check (one fixture per
  registered pair) and the `m.text` / non-empty-body asserts.
- CI: `code_tests` now also runs `flutter analyze && flutter test` for
  `packages/docs_app` (it had no CI coverage before).
- Fixed a latent bug this surfaced: `faq_handler.dart`'s multi-item accordion
  put a `ListTile` (via `ExpansionTile`) under a plain `Container`, not a
  `Material` — asserts in a bare render context, only looked fine in-app
  because the message list sits on a Material. Wrapped in
  `Material(type: transparency)`; also un-reds `docs_app/test/all_types_test.dart`.

## Schema source of truth (JNO-345) — done

`schemas/` + `examples/` moved to the public `JaenoCode/jaeno-dsl` repo,
embedded here as a git submodule at `dsl/` pinned to a tag. Both generators
read `schemas/`; every `actions/checkout` in `integrate.yaml` now does
`submodules: recursive`, and CI runs the schema validation from
`dsl/scripts/validate_dsl_schemas.sh`. Fresh checkout needs
`git submodule update --init`.

## Still not done (later stories)

- Packaging / distribution / PyPI → JNO-348 (blocked on the distribution decision)
