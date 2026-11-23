#!/usr/bin/env bash
# End-to-end smoke test: starts its own server (temp DB, port 8791), then runs asserted checks
# (tests/smoke_e2e.py). Exits non-zero on any failure. Run from 03_software/src.
#   PY=../.venv/bin/python ./smoke_test.sh [path/to/ffb.jpg]
set -euo pipefail
PY=${PY:-python}
PORT=${PORT:-8791}
BASE=http://127.0.0.1:$PORT
export SAWIT_RUNTIME_DIR=$(mktemp -d)
if curl -sf "$BASE/api/v1/health" >/dev/null 2>&1; then echo "Port $PORT already in use — set PORT=..."; exit 2; fi
$PY -m uvicorn app.main:app --port "$PORT" --log-level warning & SRV=$!
trap 'kill $SRV 2>/dev/null || true; rm -rf "$SAWIT_RUNTIME_DIR"' EXIT
for i in $(seq 40); do curl -sf "$BASE/api/v1/health" >/dev/null && break; sleep 0.25; done
$PY tests/smoke_e2e.py "$BASE" "${1:-}"
