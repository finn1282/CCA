"""M6 fertiliser/irrigation model trained on a SIMULATED dataset (D12 in 01_research/03_datasets.md).

Why simulated: no public oil-palm soil-sensor dataset exists (SPEC §8). We sample "true" soil
states, label each with the agronomic rules (INTERFACES v0.2 §4), then add realistic sensor noise
to the features. The tree therefore learns how *measurement uncertainty* blurs each threshold,
which gives the live system a calibrated confidence and feature attributions on top of the rules.
The rules stay authoritative for the action; the model never overrides them.

Output: src/app/assets/m6_tree.json (pure JSON, inference needs no scikit-learn) + metrics JSON.
Run:  python training/fertiliser/train_m6.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

SW = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SW / "src"))
from app import rules  # noqa: E402

FEATURES = ["soil_moisture_pct", "soil_ph", "tds_ratio", "soil_temp_c"]
NOISE = {"soil_moisture_pct": 3.0, "soil_ph": 0.1, "tds_ratio": 0.05, "soil_temp_c": 0.5}
BASELINE = 600.0  # arbitrary; features use the ratio to the device baseline
SEED = 42


def simulate(n: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    moist = rng.uniform(10, 95, n)
    ph = np.clip(rng.normal(4.9, 0.8, n), 3.3, 7.5)
    ratio = np.clip(rng.lognormal(0.0, 0.35, n), 0.3, 2.2)
    temp = rng.uniform(24, 33, n)
    labels = []
    for m, p, r in zip(moist, ph, ratio):
        rec = rules.recommend({"soil_moisture_pct": m, "soil_ph": p, "tds_ppm": r * BASELINE}, BASELINE, 0.30)
        labels.append(rec["action"])
    X_true = np.column_stack([moist, ph, ratio, temp])
    X_obs = X_true + rng.normal(0, [NOISE[f] for f in FEATURES], X_true.shape)
    return X_obs, np.array(labels)


def export_tree(clf: DecisionTreeClassifier) -> dict:
    t = clf.tree_
    values = t.value[:, 0, :]
    probs = values / values.sum(axis=1, keepdims=True)
    return {
        "features": FEATURES,
        "classes": [str(c) for c in clf.classes_],
        "children_left": t.children_left.tolist(),
        "children_right": t.children_right.tolist(),
        "feature": t.feature.tolist(),
        "threshold": [round(float(x), 5) for x in t.threshold],
        "probs": [[round(float(p), 5) for p in row] for row in probs],
    }


def main() -> None:
    rng = np.random.default_rng(SEED)
    X, y = simulate(20000, rng)
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
    clf = DecisionTreeClassifier(max_depth=7, min_samples_leaf=40, random_state=SEED).fit(Xtr, ytr)
    pred = clf.predict(Xte)
    acc = accuracy_score(yte, pred)
    report = classification_report(yte, pred, output_dict=True, zero_division=0)
    print(classification_report(yte, pred, zero_division=0))
    out = export_tree(clf)
    out["meta"] = {
        "model_version": "m6-tree-0.1",
        "data": "SIMULATED (rules on true state + sensor noise), n=20000, seed=42",
        "test_accuracy": round(acc, 4),
        "depth": int(clf.get_depth()), "leaves": int(clf.get_n_leaves()),
        "label_distribution": {k: int(v) for k, v in zip(*np.unique(y, return_counts=True))},
    }
    dst = SW / "src" / "app" / "assets" / "m6_tree.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out))
    (Path(__file__).parent / "metrics_m6.json").write_text(json.dumps(
        {"accuracy": acc, "per_class": {k: v for k, v in report.items() if k in out["classes"]}, **out["meta"]}, indent=2))
    print(f"accuracy={acc:.4f} -> {dst}")


if __name__ == "__main__":
    main()
