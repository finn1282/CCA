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
# 3x3 grid IDs, identical to gee/ndvi_estate.py block_id() (S-24)
for i, name in enumerate(["DEMO-A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2", "C3"]):
    area = float(rng.uniform(25, 45))
    planted = rng.choice([2001, 2005, 2009, 2013, 2017])
    palms = int(area * 136)                      # ~136 palms/ha triangular planting (assumption)
    ripe = int(palms * rng.uniform(0.05, 0.16))  # ripe bunches available this round (SIMULATED)
    blocks.append({
        "block_id": name, "area_ha": round(area, 1), "palms": palms,
        "planted": int(planted),
        "ripe_bunches_est": ripe, "overripe_share": round(float(rng.uniform(0.02, 0.25)), 2),
        # Productivity falls with palm height [AHMAD2020]: 400–1,000 bunches/day per 2-person team on
        # palms <3 m, 50–90 on palms >12 m. Per harvester: young 250, mid-age 120 (interpolated), old 40.
        "bunches_per_harvester_day": 250 if (2026 - int(planted)) < 12 else (120 if (2026 - int(planted)) < 20 else 40),
        "ndvi_z": round(float(rng.normal(-0.2, 0.9)), 2) if name != "B2" else -2.1,
    })
out = {
    "simulated": True,
    "estate": "SawitSense demo estate (SIMULATED)",
    "crew_size": 30,
    "bunches_per_harvester_day": 120,
    "round_days": "10–15 (recommended 7–13 [AHMAD2020]; optimum 10–12, ≥12–15 to avoid over-ripening [MPOB-NEWS2020])",
    "assumptions": [
        "Block ripe-bunch estimates are SIMULATED (in production: aggregated M1 grades + M2 schedule).",
        "Harvester productivity by palm age from [AHMAD2020] (per-harvester values derived from 2-person team figures; mid-age interpolated).",
        "Crew of 30 per round is an assumption for the demo estate.",
        "~136 palms/ha planting density is an assumption.",
    ],
    "blocks": blocks,
}
dst = Path(__file__).resolve().parents[2] / "src" / "static" / "precomputed" / "estate_blocks.json"
dst.write_text(json.dumps(out, indent=1))
print("wrote", dst)
