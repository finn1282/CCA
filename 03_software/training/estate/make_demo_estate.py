"""Generate the SIMULATED demo estate used by the harvester-allocation and cascade panels.

No public block-level ripeness or crew data exists (SPEC §8), so blocks are simulated. Every value
here is labelled SIMULATED in the API and dashboard. Productivity figures are assumptions pending
research request R1(e) and must be replaced with cited values in the report.
Run: python training/estate/make_demo_estate.py
"""
import json
from pathlib import Path

import numpy as np

rng = np.random.default_rng(7)
blocks = []
for i, name in enumerate(["DEMO-A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2"]):
    area = float(rng.uniform(25, 45))
    palms = int(area * 136)                      # ~136 palms/ha triangular planting (assumption)
    ripe = int(palms * rng.uniform(0.05, 0.16))  # ripe bunches available this round (SIMULATED)
    blocks.append({
        "block_id": name, "area_ha": round(area, 1), "palms": palms,
        "planted": int(rng.choice([2001, 2005, 2009, 2013, 2017])),
        "ripe_bunches_est": ripe, "overripe_share": round(float(rng.uniform(0.02, 0.25)), 2),
        "ndvi_z": round(float(rng.normal(-0.2, 0.9)), 2) if name != "B2" else -2.1,
    })
out = {
    "simulated": True,
    "estate": "SawitSense demo estate (SIMULATED)",
    "crew_size": 12,
    "bunches_per_harvester_day": 90,
    "assumptions": [
        "Block ripe-bunch estimates are SIMULATED (in production: aggregated M1 grades + M2 schedule).",
        "Harvester productivity 90 bunches/day and crew of 12 are placeholders pending research R1(e).",
        "~136 palms/ha planting density is an assumption.",
    ],
    "blocks": blocks,
}
dst = Path(__file__).resolve().parents[2] / "src" / "static" / "precomputed" / "estate_blocks.json"
dst.write_text(json.dumps(out, indent=1))
print("wrote", dst)
