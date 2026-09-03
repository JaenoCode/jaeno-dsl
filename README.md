# jaeno-dsl

The source-of-truth JSON Schemas for Jaeno's `ai.jaeno.dsl` messaging system —
the structured widget cards (menu, payment, appointment, banner, calculator,
…) that a Jaeno agent sends into a Matrix room and the client renders.

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
| `JaenoCode/jaeno` (Flutter client) | Dart models + `dsl_generated_validators.dart`, via a git submodule at `dsl/` |
| `JaenoCode/jaeno` `packages/dsl_py` | Pydantic v2 models + the Python DSL sender package |
| Web widget (JNO-338) | TypeScript interfaces + validator |

## Versioning

Schemas are **strictly versioned**. Never edit a schema for a version already
in use — add a new `<type>.v<n+1>.json` instead. Consumers key their handler
lookup on `(type, version)`, so an in-place change silently breaks older
clients.

## Changing a schema

1. Edit or add `schemas/<type>.v<version>.json` and its `examples/` twin.
2. `./scripts/validate_dsl_schemas.sh` (needs `npx`).
3. Open a PR here. On merge, tag a release.
4. In each consumer, bump the submodule / dependency and regenerate.
