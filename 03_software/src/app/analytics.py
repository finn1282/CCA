"""Estate analytics: harvester allocation (P1) and the satellite → drone → ground cascade (P2).

Inputs are pre-computed files in static/precomputed/:
- estate_blocks.json  — SIMULATED demo estate (block ripe-bunch estimates, crew size): no public data.
- satellite.json      — M5 Sentinel-2 NDVI anomaly per block (real data, training/satellite/).
- screening.json      — M3 drone palm scores (D4 model output or dataset annotations, see file's 'source').
"""
from __future__ import annotations

import json
import math
from functools import lru_cache

from . import config as C

PRE = C.STATIC_DIR / "precomputed"


@lru_cache(maxsize=8)
def _load(name: str) -> dict | None:
    p = PRE / name
    return json.loads(p.read_text()) if p.exists() else None


def harvest_plan(crew: int | None = None, live_ripeness: dict | None = None) -> dict:
    est = _load("estate_blocks.json")
    if not est:
        return {"available": False}
    crew = crew or est["crew_size"]
    cap = est["bunches_per_harvester_day"]
    blocks = []
    for b in est["blocks"]:
        ripe, over = b["ripe_bunches_est"], b["overripe_share"]
        if live_ripeness and b["block_id"] == live_ripeness.get("block_id"):
            # A live camera grade nudges the block's urgency (demo of data fusion).
            if live_ripeness["label"] in ("ripe", "overripe"):
                over = min(1.0, over + (0.1 if live_ripeness["label"] == "overripe" else 0.03))
        bcap = b.get("bunches_per_harvester_day", cap)   # tall old palms are slower to harvest [AHMAD2020]
        need = math.ceil(ripe / bcap) if ripe else 0
        # Priority = ripe bunches one harvester can save today, weighted up where fruit is close to
        # over-ripening (loose fruit, FFA). Tall ageing blocks score low → flags them for replanting (P2).
        blocks.append({**b, "_cap": bcap, "overripe_share": round(over, 2), "harvester_days_needed": need,
                       "urgency": round(bcap * (1 + 2 * over), 1)})
    blocks.sort(key=lambda b: b["urgency"], reverse=True)
    left = crew
    for b in blocks:
        give = min(left, b["harvester_days_needed"])
        b["assigned_harvesters"] = give
        b["status"] = "covered" if give >= b["harvester_days_needed"] else ("partial" if give else "deferred")
        b["bunches_at_risk"] = max(0, b["ripe_bunches_est"] - give * b.pop("_cap"))
        left -= give
    return {
        "available": True, "simulated": True, "crew": crew, "bunches_per_harvester_day": cap,
        "unassigned_harvesters": left, "blocks": blocks,
        "bunches_at_risk_total": sum(b["bunches_at_risk"] for b in blocks),
        "method": "Greedy allocation by bunches saved per harvester, weighted by over-ripening risk (SIMULATED estate data)",
        "assumptions": est.get("assumptions", []),
    }


def cascade(z_threshold: float = -1.5, p_threshold: float = 0.3) -> dict:
    sat = _load("satellite.json")
    scr = _load("screening.json")
    est = _load("estate_blocks.json")
    if sat:
        blocks = [{"block_id": b["block_id"], "ndvi_z": b["ndvi_z_latest"], "ndvi": b["ndvi_latest"]} for b in sat["blocks"]]
        sat_src = sat.get("source", "Sentinel-2")
    elif est:
        blocks = [{"block_id": b["block_id"], "ndvi_z": b.get("ndvi_z", 0), "ndvi": None} for b in est["blocks"]]
        sat_src = "SIMULATED (satellite pre-compute not yet available)"
    else:
        return {"available": False}
    flagged = sorted([b for b in blocks if b["ndvi_z"] is not None and b["ndvi_z"] <= z_threshold], key=lambda b: b["ndvi_z"])

    ground = []
    if scr:
        confirmed = [p for p in scr["palms"] if p.get("confirmed")]
        d0 = scr.get("spread_scale_m", 20.0)  # neighbour-spread distance scale — citation pending (R1d)
        for p in scr["palms"]:
            if p.get("confirmed") or p["p_ganoderma"] < p_threshold:
                continue
            d = min((math.dist((p["x_m"], p["y_m"]), (c["x_m"], c["y_m"])) for c in confirmed), default=None)
            boost = 0.5 * math.exp(-d / d0) if d is not None else 0.0
            ground.append({**p, "dist_to_confirmed_m": round(d, 1) if d is not None else None,
                           "priority": round(p["p_ganoderma"] * (1 + boost), 3)})
        ground.sort(key=lambda p: p["priority"], reverse=True)
    return {
        "available": True,
        "stage1_satellite": {"source": sat_src, "threshold_z": z_threshold, "blocks_total": len(blocks), "flagged": flagged},
        "stage2_drone": {"source": scr.get("source") if scr else None, "block": scr.get("block_id") if scr else None,
                         "palms_scored": len(scr["palms"]) if scr else 0, "image": scr.get("image") if scr else None,
                         "metrics": scr.get("metrics") if scr else None},
        "stage3_ground": {"threshold_p": p_threshold, "ranked": ground[:15],
                          "note": "Screening, not diagnosis: ranked palms go for ground/GSM confirmation (SPEC §8)."},
    }


def satellite() -> dict:
    return _load("satellite.json") or {"available": False}
