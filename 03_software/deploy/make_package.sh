#!/usr/bin/env bash
# Build deploy/sawitsense.zip for Azure App Service (Linux, Python). Run from 03_software/:
#   bash deploy/make_package.sh
# Contains runtime code, dashboard and the M1 model files (models/m1_ripeness.onnx + .json, ~16 MB),
# so the model is NOT on the critical path via Blob/SAS (S-18). No tests, data or secrets.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf deploy/build deploy/sawitsense.zip
mkdir -p deploy/build
cp -r src/app src/static deploy/build/
rm -rf deploy/build/app/__pycache__ deploy/build/static/heatmaps/* 2>/dev/null || true
grep -vE '^(pytest|httpx)' src/requirements.txt > deploy/build/requirements.txt
if [ -f models/m1_ripeness.onnx ] && [ -f models/m1_ripeness.json ]; then
  mkdir -p deploy/build/models && cp models/m1_ripeness.onnx models/m1_ripeness.json deploy/build/models/
else
  echo "WARNING: models/m1_ripeness.onnx/.json missing — ripeness endpoint will return 503 (train first)"
fi
(cd deploy/build && python3 -c "import shutil; shutil.make_archive('../sawitsense', 'zip', '.')")
echo "built deploy/sawitsense.zip ($(du -h deploy/sawitsense.zip | cut -f1))"
