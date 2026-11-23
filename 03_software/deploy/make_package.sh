#!/usr/bin/env bash
# Build deploy/sawitsense.zip for Azure App Service (Linux, Python). Run from 03_software/:
#   bash deploy/make_package.sh
# Contains only runtime code + dashboard (no tests, data, models or secrets). The model is fetched
# from Blob at first use via SAWIT_MODEL_URL / SAWIT_MODEL_META_URL (see DEPLOY_AZURE.md).
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf deploy/build deploy/sawitsense.zip
mkdir -p deploy/build
cp -r src/app src/static deploy/build/
rm -rf deploy/build/app/__pycache__ deploy/build/static/heatmaps/* 2>/dev/null || true
grep -vE '^(pytest|httpx)' src/requirements.txt > deploy/build/requirements.txt
cat > deploy/build/startup.sh <<'SH'
#!/bin/sh
# App Service startup: ONE worker (SQLite + in-process lock), persistent data under /home/data.
mkdir -p /home/data
exec python -m uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}" --workers 1 --proxy-headers
SH
chmod +x deploy/build/startup.sh
(cd deploy/build && python3 -c "import shutil; shutil.make_archive('../sawitsense', 'zip', '.')")
echo "built deploy/sawitsense.zip ($(du -h deploy/sawitsense.zip | cut -f1))"
