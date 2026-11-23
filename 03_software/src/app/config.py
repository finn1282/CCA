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
MODEL_PATH = Path(os.getenv("SAWIT_MODEL", SW_DIR / "models" / "m1_ripeness.onnx"))
MODEL_META_PATH = MODEL_PATH.with_suffix(".json")

# Device credentials: "soilnode-01:key1,cam-01:key2". Default keys are for the local demo only.
_DEFAULT_KEYS = "soilnode-01:demo-soil-key,cam-01:demo-cam-key,sim-01:demo-sim-key"
DEVICE_KEYS: dict[str, str] = dict(
    pair.split(":", 1) for pair in os.getenv("SAWIT_DEVICE_KEYS", _DEFAULT_KEYS).split(",") if ":" in pair
)
REQUIRE_DEVICE_KEY = os.getenv("SAWIT_REQUIRE_DEVICE_KEY", "1") == "1"
# Optional token for dashboard write actions (calibration, commands, reviews). Empty = open (local demo).
ADMIN_TOKEN = os.getenv("SAWIT_ADMIN_TOKEN", "")
# Where this server runs; shown on the dashboard ("cloud" on Azure, "local" on the laptop).
DEPLOYMENT_MODE = os.getenv("SAWIT_MODE", "local")

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

# Harvest round interval (days) used in harvest advice. ASSUMPTION pending research R1(e).
HARVEST_ROUND_DAYS = int(os.getenv("SAWIT_HARVEST_ROUND_DAYS", "10"))


def ensure_dirs() -> None:
    for d in (RUNTIME_DIR, HEATMAP_DIR, IMAGE_DIR):
        d.mkdir(parents=True, exist_ok=True)
