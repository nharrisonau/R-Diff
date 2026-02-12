#!/usr/bin/env bash
set -euo pipefail

# Wrapper kept for compatibility with the Dockerfile and existing workflows.
# The new collector writes only to outputs/v2/{normal,stripped}.

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

BASE_DIR="${BASE_DIR:-$REPO_ROOT}"
OUT_BASE="${OUT_BASE:-$BASE_DIR/outputs}"

STRIP_TOOL="${STRIP_TOOL:-strip}"
STRIP_FLAGS="${STRIP_FLAGS:---strip-unneeded}"

read -r -a STRIP_FLAG_ARR <<< "${STRIP_FLAGS}"
STRIP_ARGS=()
for f in "${STRIP_FLAG_ARR[@]}"; do
  # Pass as --opt=value so argparse accepts values that start with '-'.
  STRIP_ARGS+=(--strip-flag="$f")
done

python3 "${REPO_ROOT}/targets/malicious/scripts/collect_outputs_v2.py" \
  --repo-root "${BASE_DIR}" \
  --out-base "${OUT_BASE}" \
  --strip-tool "${STRIP_TOOL}" \
  "${STRIP_ARGS[@]}"
