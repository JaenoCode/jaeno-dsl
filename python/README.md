# jaeno-dsl (Python)

Agent-side constructor for `ai.jaeno.dsl` Matrix event content. The models are
generated from `../schemas`, the same set the Flutter client and web widget
generate from, so a bot can't drift from the client's DSL contract.

## Install

```
uv add "jaeno-dsl @ git+https://github.com/JaenoCode/jaeno-dsl@v0.2.0#subdirectory=python"
```

or in `pyproject.toml`:

```toml
[project]
dependencies = [
  "jaeno-dsl @ git+https://github.com/JaenoCode/jaeno-dsl@v0.2.0#subdirectory=python",
]
```

Only runtime dependency is `pydantic>=2`.

## Use

```python
from jaeno_dsl import build_dsl_event_content

content = build_dsl_event_content("banner", 1, {"title": "Closed", "message": "Back at 9am"})
await client.room_send(room_id, "m.room.message", content)
```

Per-card form, kwargs or mapping:

```python
from jaeno_dsl.cards import banner_v1, payment_v1

banner_v1(variant="warning", title="Kitchen closed", message="Back at 5pm")
payment_v1(order_id="ord_9021", amount=1450, currency="PKR")
```

Every constructor **validates before returning**. On a bad payload it raises —
never a half-built dict:

| exception | Dart `DSLResolution` peer | when |
|---|---|---|
| `DSLMalformedEnvelopeError` | `DSLMalformedEnvelope` | non-int `v`, empty `type`, non-mapping `data` |
| `DSLUnknownTypeError` | `DSLUnknownHandler` | `(type, version)` not in the registry |
| `DSLInvalidPayloadError` | `DSLInvalidPayload` | fails the generated model, or the `calculator` formula/field checks |

`DSLUntrustedSender` / `DSLBotSuspended` have no peer here — client-side render
gates, not a sender's job.

## Layout

```
python/
  jaeno_dsl/
    envelope.py            build_dsl_event_content, validate_before_send   (hand-written)
    errors.py              the exception taxonomy                          (hand-written)
    fallback.py            per-type fallback body text + generic default   (hand-written)
    calculator.py          formula grammar + field rules, ported from Dart (hand-written)
    cards.py               one constructor per (type, version)             (GENERATED)
    models/generated/      one Pydantic model per schema + registry.py     (GENERATED)
  scripts/generate_models.sh   regenerates generated/ + cards.py + ../roundtrip/
  scripts/emit_roundtrip.py    builds ../roundtrip/ from ../examples/ (called by the above)
  tests/
DESIGN.md                    the codegen-tool decision + design record
```

`../roundtrip/<type>.v<version>.json` is the full event content this package
emits for each pair — the conformance set the Flutter client's round-trip test
checks against (`packages/docs_app/test/python_roundtrip_test.dart` in
`JaenoCode/jaeno`).

## Regenerate

```bash
./python/scripts/generate_models.sh
```

Run after any schema change. Output is committed and byte-stable; the `python`
CI workflow regenerates and `git diff --exit-code`s it. `datamodel-code-generator`,
`black` and `isort` are pinned in the script.

## Test

```bash
uv run --no-project --with 'pydantic>=2' --with 'pytest>=8' python -m pytest python -q
```
