#!/usr/bin/env bash
# Copy latest V2 min chat_request catalogs from a local Zeus checkout into this repo.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ZEUS_ROOT="${1:-${ZEUS_ROOT:-}}"
if [[ -z "${ZEUS_ROOT}" ]]; then
  echo "Usage: $0 /path/to/Zeus" >&2
  echo "   or: ZEUS_ROOT=/path/to/Zeus $0" >&2
  exit 2
fi
SRC="${ZEUS_ROOT}/ai/V2/variants/min"
if [[ ! -d "$SRC" ]]; then
  echo "missing $SRC — generate first: (cd Zeus && go run . ai-snapshot --mode=all --api-version=v2 --min)" >&2
  exit 1
fi
mkdir -p "$ROOT/v2/min"
cp -v "$SRC"/chat_request_*_v2_min.json "$ROOT/v2/min/"
echo "Copied. Refresh manifest: python3 scripts/refresh_manifest.py (or re-run package init)."
