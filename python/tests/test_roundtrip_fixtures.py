"""The committed roundtrip/ fixtures must match a fresh build.

The Dart side (packages/docs_app/test/python_roundtrip_test.dart) trusts these
files as "what the Python package emits". This guards them the same way the
generated models are guarded — regenerate, compare — so a stale fixture fails
here in addition to the CI ``git diff`` check.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from jaeno_dsl.envelope import build_dsl_event_content
from jaeno_dsl.models.generated.registry import DSL_MODELS

_PKG = pathlib.Path(__file__).resolve().parents[1]  # python/
_ROOT = _PKG.parents[0]  # jaeno-dsl repo root
_FIXTURES = sorted((_ROOT / "roundtrip").glob("*.json"))

_REGISTERED = {f"{t}.v{v}" for t, versions in DSL_MODELS.items() for v in versions}


def test_one_fixture_per_registered_pair() -> None:
    on_disk = {f.stem for f in _FIXTURES}
    assert on_disk == _REGISTERED


@pytest.mark.parametrize("fixture", _FIXTURES, ids=lambda p: p.stem)
def test_fixture_is_current(fixture: pathlib.Path) -> None:
    dsl_type, version = fixture.stem.rsplit(".v", 1)
    example = json.loads((_ROOT / "examples" / fixture.name).read_text())
    fresh = build_dsl_event_content(dsl_type, int(version), example["data"])
    committed = json.loads(fixture.read_text())
    assert committed == fresh, f"{fixture.name} is stale — run ./python/scripts/generate_models.sh"
