#!/usr/bin/env bash
#
# Validates every examples/*.json payload against its matching schemas/*.json
# (Step 1.2's test, formalized so CI — and anyone locally — can run it).
# A missing schema for an example, or vice versa, is also a failure: the two
# directories are meant to be exactly 1:1.
#
# ajv-cli is pinned to an exact version for the same reason quicktype is
# pinned in generate_dsl_models.sh: an unpinned tool can start failing (or
# passing) payloads it used to disagree with, for reasons that have nothing
# to do with an actual schema change.
#
# Usage: ./scripts/validate_dsl_schemas.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMAS_DIR="$ROOT_DIR/schemas"
EXAMPLES_DIR="$ROOT_DIR/examples"

failures=0
checked=0

for example_file in "$EXAMPLES_DIR"/*.json; do
  base="$(basename "$example_file")"
  schema_file="$SCHEMAS_DIR/$base"

  if [ ! -f "$schema_file" ]; then
    echo "FAIL  $base: no matching schema at schemas/$base"
    failures=$((failures + 1))
    continue
  fi

  checked=$((checked + 1))
  if npx --yes ajv-cli@5.0.0 validate -s "$schema_file" -d "$example_file" --spec=draft2020 >/tmp/ajv_out.$$ 2>&1; then
    echo "PASS  $base"
  else
    echo "FAIL  $base"
    sed 's/^/      /' /tmp/ajv_out.$$
    failures=$((failures + 1))
  fi
  rm -f /tmp/ajv_out.$$
done

# Catch schemas with no matching example too — same 1:1 invariant.
for schema_file in "$SCHEMAS_DIR"/*.json; do
  base="$(basename "$schema_file")"
  if [ ! -f "$EXAMPLES_DIR/$base" ]; then
    echo "FAIL  $base: no matching example at examples/$base"
    failures=$((failures + 1))
  fi
done

echo ""
echo "${checked} example(s) checked, ${failures} failure(s)"

if [ "$failures" -gt 0 ]; then
  exit 1
fi
