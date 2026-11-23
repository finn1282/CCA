"""Runtime configuration (environment variables, safe defaults for the local demo)."""
from __future__ import annotations

import os
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent          # 03_software/src
SW_DIR = SRC_DIR.parent                                    # 03_software
RUNTIME_DIR = Path(os.getenv("SAWIT_RUNTIME_DIR", SRC_DIR / "runtime"))
DB_PATH = Path(os.getenv("SAWIT_DB", RUNTIME_DIR / "sawitsense.db"))
HEATMAP_DIR = RUNTIME_DIR / "heatmaps"
IMAGE_DIR = RUNTIME_DIR / "images"
STATIC_DIR = SRC_DIR / "static"
ASSETS_DIR = Path(__file__).resolve().parent / "assets"
# Model: env var, else models/ next to app/ (deploy zip), else 03_software/models (repo checkout)
_pkg_model = SRC_DIR / "models" / "m1_ripeness.onnx"
MODEL_PATH = Path(os.getenv("SAWIT_MODEL", _pkg_model if _pkg_model.exists() else SW_DIR / "models" / "m1_ripeness.onnx"))
MODEL_META_PATH = MODEL_PATH.with_suffix(".json")

# Device credentials: "soilnode-01:key1,cam-01:key2". Default keys are for the local demo only.
# Where this server runs; shown on the dashboard ("cloud" on Azure, "local" on the laptop).
DEPLOYMENT_MODE = os.getenv("SAWIT_MODE", "local")
CLOUD = DEPLOYMENT_MODE == "cloud"
# Demo keys are active ONLY in local mode (D-12). In cloud mode keys must come from SAWIT_DEVICE_KEYS;
# if it is unset, every device request is rejected (fail closed).
_DEFAULT_KEYS = "" if CLOUD else "soilnode-01:demo-soil-key,cam-01:demo-cam-key,sim-01:demo-sim-key"
DEVICE_KEYS: dict[str, str] = dict(
    pair.split(":", 1) for pair in os.getenv("SAWIT_DEVICE_KEYS", _DEFAULT_KEYS).split(",") if ":" in pair
)
REQUIRE_DEVICE_KEY = CLOUD or os.getenv("SAWIT_REQUIRE_DEVICE_KEY", "1") == "1"
# Token for dashboard write actions (calibration, commands, reviews). Local: empty = open.
# Cloud: required — if unset, write actions are refused (fail closed).
ADMIN_TOKEN = os.getenv("SAWIT_ADMIN_TOKEN", "")

# Device → estate block mapping for devices that do not send block_id (camera).
DEVICE_BLOCKS = {"cam-01": "DEMO-A1"}

# INTERFACES v0.2 §4 — shared thresholds (D17 corrected, D25)
MOISTURE_LOW = 30.0
MOISTURE_HIGH = 80.0
PH_LIME = 4.0
PH_WATCH_TOP = 4.2
PH_TYPICAL_TOP = 5.5
PH_HIGH = 6.5
TDS_DEFAULT_MARGIN = 0.30

# Harvest round interval (days): recommended 7–13 [AHMAD2020], optimum 10–12 [MPOB-NEWS2020].
HARVEST_ROUND_DAYS = int(os.getenv("SAWIT_HARVEST_ROUND_DAYS", "10"))


def ensure_dirs() -> None:
    for d in (RUNTIME_DIR, HEATMAP_DIR, IMAGE_DIR):
        d.mkdir(parents=True, exist_ok=True)
