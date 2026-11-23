"""Hybrid recommender: rule engine (authoritative) + M6 tree (confidence and attributions).

The M6 tree is trained on SIMULATED data (training/fertiliser/train_m6.py) and stored as JSON, so
inference needs no ML library. Attributions use the Saabas path method: the change in the predicted
class probability contributed by each split on the decision path (a fast tree approximation of SHAP).
"""
from __future__ import annotations

import json
from functools import lru_cache

from . import config as C
from . import rules

LABELS = {"soil_moisture_pct": "moisture", "soil_ph": "pH", "tds_ratio": "TDS vs baseline", "soil_temp_c": "soil temp"}


@lru_cache(maxsize=1)
def _tree() -> dict | None:
    p = C.ASSETS_DIR / "m6_tree.json"
    return json.loads(p.read_text()) if p.exists() else None


def tree_predict(x: dict) -> tuple[dict, dict] | None:
    t = _tree()
    if t is None:
        return None
    vals = [x.get(f) for f in t["features"]]
    node, contrib = 0, {f: [0.0] * len(t["classes"]) for f in t["features"]}
    while t["children_left"][node] != -1:
        fi = t["feature"][node]
        v = vals[fi]
        nxt = t["children_left"][node] if v <= t["threshold"][node] else t["children_right"][node]
        f = t["features"][fi]
        contrib[f] = [c + (b - a) for c, a, b in zip(contrib[f], t["probs"][node], t["probs"][nxt])]
        node = nxt
    probs = dict(zip(t["classes"], t["probs"][node]))
    return probs, {f: dict(zip(t["classes"], v)) for f, v in contrib.items()}


def recommend(reading: dict, baseline: float | None, margin: float | None) -> dict:
    rec = rules.recommend(reading, baseline, margin)
    t = _tree()
    feats = {
        "soil_moisture_pct": reading.get("soil_moisture_pct"),
        "soil_ph": reading.get("soil_ph"),
        "tds_ratio": (reading["tds_ppm"] / baseline) if (reading.get("tds_ppm") is not None and baseline) else 1.0,
        "soil_temp_c": reading.get("soil_temp_c") if reading.get("soil_temp_c") is not None else 28.0,
    }
    if t is None or feats["soil_moisture_pct"] is None or feats["soil_ph"] is None:
        rec["ml"] = None
        return rec
    probs, contrib = tree_predict(feats)
    act = rec["action"]
    p_act = probs.get(act, 0.0)
    top = sorted(((f, contrib[f].get(act, 0.0)) for f in contrib), key=lambda kv: abs(kv[1]), reverse=True)
    ml_choice = max(probs, key=probs.get)
    rec["ml"] = {
        "model_version": t["meta"]["model_version"],
        "simulated_training_data": True,
        "probs": {k: round(v, 3) for k, v in probs.items()},
        "agrees_with_rules": ml_choice == act,
        "attributions": [{"feature": LABELS[f], "contribution": round(c, 3)} for f, c in top if abs(c) > 0.005][:3],
    }
    # Blend: rules give the action; the model's probability for that action tempers confidence.
    rec["confidence"] = round(0.5 * rec["confidence"] + 0.5 * p_act, 2)
    rec["needs_review"] = (ml_choice != act) or rec["confidence"] < 0.6
    rec["method"] = "rules+ml"
    return rec
