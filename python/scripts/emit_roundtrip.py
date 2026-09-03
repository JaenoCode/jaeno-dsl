"""Emit the round-trip fixtures the Dart side checks (JNO-348).

For every registered ``(type, version)``, build the full Matrix event content
from that pair's ``examples/*.json`` payload — through the real
``build_dsl_event_content`` — and write it to
``roundtrip/<type>.v<version>.json``.

`packages/docs_app/test/python_roundtrip_test.dart` reads these back and
asserts the Dart ``resolveDSL()`` + handler accept them. Committed and
byte-stable: the ``dsl_py`` CI job regenerates and diffs, so Python output
that stops matching what Dart accepts fails loudly on one side or the other.

Run via ``generate_dsl_models.sh`` (which regenerates the models first).
"""

from __future__ import annotations

import json
import pathlib
import sys

_PKG = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PKG))

from jaeno_dsl.envelope import build_dsl_event_content  # noqa: E402
from jaeno_dsl.models.generated.registry import DSL_MODELS  # noqa: E402

_ROOT = pathlib.Path(__file__).resolve().parents[2]  # jaeno-dsl repo root
_EXAMPLES = _ROOT / "examples"
_OUT = _ROOT / "roundtrip"


def main() -> int:
    _OUT.mkdir(exist_ok=True)
    for stale in _OUT.glob("*.json"):
        stale.unlink()

    count = 0
    for dsl_type in sorted(DSL_MODELS):
        for version in sorted(DSL_MODELS[dsl_type]):
            example = _EXAMPLES / f"{dsl_type}.v{version}.json"
            if not example.exists():
                print(f"no example for ({dsl_type}, v{version}) at {example}", file=sys.stderr)
                return 1
            data = json.loads(example.read_text())["data"]
            content = build_dsl_event_content(dsl_type, version, data)
            (_OUT / f"{dsl_type}.v{version}.json").write_text(
                json.dumps(content, indent=2, sort_keys=True) + "\n"
            )
            count += 1

    print(f"emitted {count} round-trip fixture(s) into roundtrip/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
