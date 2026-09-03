# jaeno-dsl

The source-of-truth JSON Schemas for Jaeno's `ai.jaeno.dsl` messaging system —
the structured widget cards (menu, payment, appointment, banner, calculator,
…) that a Jaeno agent sends into a Matrix room and the client renders — plus
the reference **Python sender package** under `python/`.

```
schemas/     JSON Schema per (type, version) — the contract
examples/    a valid example payload per pair, 1:1 with schemas/
roundtrip/   the full Matrix event content the Python sender emits per pair
             (the conformance set the Flutter client's round-trip test checks)
python/      the reference sender: `pip install`-able, generated from schemas/
scripts/     validate_dsl_schemas.sh — pinned ajv-cli, runs in CI
```

One file per `(type, version)` pair:

- `schemas/<type>.v<version>.json` — JSON Schema (2020-12) for the **full
  envelope** (`{v, type, data}`), not just `data`.
- `examples/<type>.v<version>.json` — a valid example payload, 1:1 with the
  schemas. Also the fixture set the generators and round-trip tests use.
- `scripts/validate_dsl_schemas.sh` — validates every example against its
  schema with a pinned `ajv-cli`, and fails if `schemas/` and `examples/`
  ever go out of 1:1 sync. Run in CI on every push.

See `schemas/README.md` for the schema conventions (why `data` is open, how
`required` is decided, the `{"type":"integer"}` rule on `const` numbers) and
`examples/INVENTORY.md` for which fields are confirmed vs. code-derived.

## Consumers

Each consumer generates typed models + a validator from these schemas — never
hand-writes them — so no implementation can drift from the contract:

| Consumer | What it generates |
|---|---|
| `JaenoCode/jaeno` (Flutter client) | Dart models + `dsl_generated_validators.dart`; embeds this repo as a git submodule at `dsl/` |
| `python/` (this repo) | Pydantic v2 models + the reference DSL sender package — `uv add "jaeno-dsl @ git+https://github.com/JaenoCode/jaeno-dsl@<tag>#subdirectory=python"` |
| Web widget (JNO-338) | TypeScript interfaces + validator (planned) |

See `python/README.md` for the sender API.

## Versioning

Schemas are **strictly versioned**. Never edit a schema for a version already
in use — add a new `<type>.v<n+1>.json` instead. Consumers key their handler
lookup on `(type, version)`, so an in-place change silently breaks older
clients.

## Changing a schema

1. Edit or add `schemas/<type>.v<version>.json` and its `examples/` twin.
2. `./scripts/validate_dsl_schemas.sh` (needs `npx`).
3. `./python/scripts/generate_models.sh` and commit the regenerated `python/`
   + `roundtrip/`.
4. Open a PR here. On merge, tag a release.
5. In `JaenoCode/jaeno`: bump the `dsl/` submodule, rerun
   `./scripts/generate_dsl_models.sh`, commit.
