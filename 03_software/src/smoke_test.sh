#!/usr/bin/env bash
# End-to-end smoke test: simulator -> API -> dashboard feeds. Run from 03_software/src.
set -euo pipefail
PY=${PY:-python}
PORT=${PORT:-8791}
BASE=http://127.0.0.1:$PORT
export SAWIT_RUNTIME_DIR=$(mktemp -d)
$PY -m uvicorn app.main:app --port $PORT --log-level warning & SRV=$!
trap 'kill $SRV' EXIT
for i in $(seq 30); do curl -sf $BASE/api/v1/health >/dev/null && break; sleep 0.3; done
echo "== health";       curl -s $BASE/api/v1/health; echo
echo "== simulator (warm-up, normal)"
$PY simulator.py --base $BASE --scenario normal --count 3 --interval 0.1
echo "== calibrate TDS baseline from current reading"
curl -s -X POST $BASE/api/v1/devices/sim-01/calibration -H 'Content-Type: application/json' -d '{"use_latest":true,"tds_margin":0.3}'; echo
echo "== simulator (cycle through all scenarios)"
$PY simulator.py --base $BASE --scenario cycle --count 40 --per-scenario 5 --interval 0.05
if [ -n "${IMAGE:-}" ]; then echo "== camera"; $PY simulator.py --base $BASE --count 0 --image "$IMAGE" --scenario normal --interval 0 --count 1; fi
echo "== calibration GET (as device)"
curl -s $BASE/api/v1/devices/sim-01/calibration -H 'X-Device-Id: sim-01' -H 'X-Device-Key: demo-sim-key'; echo
echo "== latest";       curl -s $BASE/api/v1/latest | $PY -c "import json,sys;d=json.load(sys.stdin);s=d['soil'][0];print(s['device_id'],s['reading']['soil_moisture_pct'],s['recommendation']['action'],'evidence:',d['evidence_count'])"
echo "== verify chain"; curl -s $BASE/api/v1/evidence/verify; echo
echo "== audit pack (head)"; curl -s $BASE/api/v1/evidence/export | head -16
echo "== harvest plan"; curl -s "$BASE/api/v1/harvest/plan?crew=12" | $PY -c "import json,sys;d=json.load(sys.stdin);print('at risk',d['bunches_at_risk_total'],[ (b['block_id'],b['assigned_harvesters'],b['status']) for b in d['blocks']])"
echo "== screening";    curl -s $BASE/api/v1/screening | $PY -c "import json,sys;d=json.load(sys.stdin);print([b['block_id'] for b in d['stage1_satellite']['flagged']], d['stage1_satellite']['source'])"
echo "== dashboard";    for p in / /harvester /static/app.js /static/vendor/chart.umd.min.js; do printf "%s %s\n" "$(curl -s -o /dev/null -w '%{http_code}' $BASE$p)" "$p"; done
echo "SMOKE TEST PASSED"
