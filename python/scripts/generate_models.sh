#!/usr/bin/env bash
#
# Regenerates Pydantic v2 models for every DSL (type, version) pair from
# schemas/ in this repo. The peer of the Dart generator in JaenoCode/jaeno
# (Dart) and JNO-338 (TypeScript) — same source of truth, same "commit the
# output, CI diffs against it" contract.
#
# datamodel-code-generator + black + isort are pinned to exact versions, for
# the same reason quicktype is pinned on the Dart side: an unpinned tool can
# change codegen or formatting output on its own, and CI's "stale generated
# models" failure would then be about tooling drift, not a schema change.
# Bump deliberately, regenerate, commit as its own change.
#
# Usage: ./python/scripts/generate_models.sh
#

set -euo pipefail

DCG_VERSION="0.76.1"
BLACK_VERSION="24.10.0"
ISORT_VERSION="5.13.2"

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"  # jaeno-dsl repo root
SCHEMAS_DIR="$ROOT_DIR/schemas"
OUT_DIR="$ROOT_DIR/python/jaeno_dsl/models/generated"

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"

to_pascal_case() {
  echo "$1" | sed -E 's/(^|_)([a-z0-9])/\U\2/g'
}

registry_entries=()

for schema_file in "$SCHEMAS_DIR"/*.json; do
  base="$(basename "$schema_file" .json)"   # banner.v1
  version_part="${base##*.v}"               # 1
  type_part="${base%.v*}"                   # banner
  class_name="$(to_pascal_case "$type_part")V${version_part}"  # BannerV1
  module_name="$(echo "$base" | tr '.' '_')"                   # banner_v1
  out_file="$OUT_DIR/${module_name}.py"

  echo "schemas/${base}.json -> python/jaeno_dsl/models/generated/${module_name}.py (${class_name})"

  uvx --from "datamodel-code-generator==${DCG_VERSION}" datamodel-codegen \
    --input "$schema_file" \
    --input-file-type jsonschema \
    --output-model-type pydantic_v2.BaseModel \
    --target-python-version 3.12 \
    --use-standard-collections \
    --use-union-operator \
    --class-name "$class_name" \
    --enum-field-as-literal all \
    --collapse-root-models \
    --disable-timestamp \
    --custom-file-header "# GENERATED CODE - DO NOT EDIT BY HAND.
# Source: schemas/${base}.json
# Regenerate with: ./python/scripts/generate_models.sh" \
    --output "$out_file"

  registry_entries+=("${type_part}|${version_part}|${class_name}|${module_name}")
done

# Sort by type then numeric version so regenerating twice is byte-identical
# (CI diffs this against what's committed).
mapfile -t sorted_entries < <(printf '%s\n' "${registry_entries[@]}" | sort -t'|' -k1,1 -k2,2n)

registry_file="$OUT_DIR/registry.py"
{
  echo "# GENERATED CODE - DO NOT EDIT BY HAND."
  echo "# Source: schemas/*.json (all)"
  echo "# Regenerate with: ./python/scripts/generate_models.sh"
  echo "#"
  echo "# Maps every (type, version) to its generated Pydantic model, so DSL"
  echo "# edge validation can check a raw envelope against the schema-derived"
  echo "# model before send — the peer of dsl_generated_validators.dart."
  echo "from __future__ import annotations"
  echo
  echo "from pydantic import BaseModel"
  echo
  for e in "${sorted_entries[@]}"; do
    IFS='|' read -r _ _ cn mn <<<"$e"
    echo "from .${mn} import ${cn}"
  done
  echo
  echo "DSL_MODELS: dict[str, dict[int, type[BaseModel]]] = {"
  current_type=""
  for e in "${sorted_entries[@]}"; do
    IFS='|' read -r tp vp cn _ <<<"$e"
    if [ "$tp" != "$current_type" ]; then
      [ -n "$current_type" ] && echo "    },"
      echo "    \"${tp}\": {"
      current_type="$tp"
    fi
    echo "        ${vp}: ${cn},"
  done
  echo "    },"
  echo "}"
} >"$registry_file"

touch "$OUT_DIR/__init__.py"

# ── generated card constructors ─────────────────────────────────────────────
# One thin forwarder per (type, version). The ergonomic hand-written layer
# (envelope builder, fallback bodies, error taxonomy, calculator grammar)
# lives in jaeno_dsl/*.py; these are just the schema-driven entry points, so
# there's no hardcoded type list to drift.
cards_file="$ROOT_DIR/python/jaeno_dsl/cards.py"
{
  echo "# GENERATED CODE - DO NOT EDIT BY HAND."
  echo "# Source: schemas/*.json (all)"
  echo "# Regenerate with: ./python/scripts/generate_models.sh"
  echo "#"
  echo '"""One constructor per DSL (type, version). Each validates and returns a'
  echo 'Matrix event content dict — see jaeno_dsl.envelope.build_dsl_event_content.'
  echo '"""'
  echo "from __future__ import annotations"
  echo
  echo "from collections.abc import Callable, Mapping"
  echo "from typing import Any"
  echo
  echo "from .envelope import build_dsl_event_content"
  echo
  for e in "${sorted_entries[@]}"; do
    IFS='|' read -r tp vp _ mn <<<"$e"
    echo
    echo "def ${mn}("
    echo "    data: Mapping[str, Any] | None = None,"
    echo "    /,"
    echo "    *,"
    echo "    body: str | None = None,"
    echo "    **fields: Any,"
    echo ") -> dict[str, Any]:"
    echo "    return build_dsl_event_content(\"${tp}\", ${vp}, data, body=body, **fields)"
  done
  echo
  echo "CARD_CONSTRUCTORS: dict[tuple[str, int], Callable[..., dict[str, Any]]] = {"
  for e in "${sorted_entries[@]}"; do
    IFS='|' read -r tp vp _ mn <<<"$e"
    echo "    (\"${tp}\", ${vp}): ${mn},"
  done
  echo "}"
} >"$cards_file"

# One formatter of record for the whole generated tree: datamodel-codegen's
# bundled black is a different version and normalizes quotes differently, so
# the pinned black+isort here — reading packages/dsl_py/pyproject.toml — is
# what CI's `black --check` is diffed against. Covers models/, registry.py and
# the hand-templated cards.py.
GEN_DIR="$ROOT_DIR/python/jaeno_dsl/models/generated"
uvx --from "isort==${ISORT_VERSION}" isort -q --settings-path "$ROOT_DIR/python" "$GEN_DIR" "$cards_file"
uvx --from "black==${BLACK_VERSION}" black -q --config "$ROOT_DIR/python/pyproject.toml" "$GEN_DIR" "$cards_file"

# Round-trip fixtures for the Dart side (JNO-348) — built through the freshly
# regenerated package so they can't lag the models.
uv run --no-project --with "pydantic>=2" python3 \
  "$ROOT_DIR/python/scripts/emit_roundtrip.py"

echo
echo "Generated ${#sorted_entries[@]} model(s) + registry.py + cards.py + roundtrip/"
