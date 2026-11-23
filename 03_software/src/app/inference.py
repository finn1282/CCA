"""M1 ripeness inference (ONNX Runtime, CPU) with a class-activation heatmap + M2 harvest advice.

The ONNX graph (training/ripeness/train_m1.py) outputs `logits` and the last convolutional
`features` map. EfficientNet-B0's head is global-average-pool → linear, so the class activation
map  CAM_c = Σ_k w_ck · F_k  equals Grad-CAM for that head without needing gradients at inference.
"""
from __future__ import annotations

import io
import json
from functools import lru_cache

import numpy as np
from PIL import Image

from . import config as C
from .preprocess import base_image, eval_crop, to_array


class ModelUnavailable(RuntimeError):
    pass


def _fetch_from_blob() -> None:
    """Cloud build: if the model is not on disk, download it from Azure Blob Storage using SAS URLs given
    in env vars SAWIT_MODEL_URL / SAWIT_MODEL_META_URL (credentials never live in the repo)."""
    import os
    import urllib.request
    for url_var, dst in (("SAWIT_MODEL_URL", C.MODEL_PATH), ("SAWIT_MODEL_META_URL", C.MODEL_META_PATH)):
        url = os.getenv(url_var)
        if url and not dst.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            tmp = dst.with_suffix(dst.suffix + ".part")
            urllib.request.urlretrieve(url, tmp)
            tmp.replace(dst)


@lru_cache(maxsize=1)
def _load():
    if not C.MODEL_PATH.exists() or not C.MODEL_META_PATH.exists():
        try:
            _fetch_from_blob()
        except Exception as e:  # noqa: BLE001
            raise ModelUnavailable(f"Model download from Blob failed: {e}") from e
    if not C.MODEL_PATH.exists() or not C.MODEL_META_PATH.exists():
        raise ModelUnavailable(f"Ripeness model not found at {C.MODEL_PATH} — train it with training/ripeness/train_m1.py")
    import onnxruntime as ort
    sess = ort.InferenceSession(str(C.MODEL_PATH), providers=["CPUExecutionProvider"])
    meta = json.loads(C.MODEL_META_PATH.read_text())
    meta["_W"] = np.asarray(meta.pop("fc_weight"), dtype=np.float32)
    return sess, meta


def model_info() -> dict:
    try:
        _, meta = _load()
        return {k: v for k, v in meta.items() if not k.startswith("_")}
    except ModelUnavailable as e:
        return {"available": False, "error": str(e)}


def _preprocess(img: Image.Image, meta: dict) -> tuple[np.ndarray, Image.Image]:
    """Identical to training/evaluation preprocessing (shared module, S-16)."""
    crop = eval_crop(base_image(img), meta.get("resize", 256), meta["input_size"])
    return to_array(crop, meta["mean"], meta["std"])[None], crop


def _colormap(x: np.ndarray) -> np.ndarray:
    """Jet-like colormap for x in [0,1] → uint8 RGB."""
    r = np.clip(1.5 - np.abs(4 * x - 3), 0, 1)
    g = np.clip(1.5 - np.abs(4 * x - 2), 0, 1)
    b = np.clip(1.5 - np.abs(4 * x - 1), 0, 1)
    return (np.stack([r, g, b], -1) * 255).astype(np.uint8)


def _hue_name(rgb: np.ndarray) -> str:
    r, g, b = rgb
    if max(r, g, b) < 60:
        return "dark/black"
    if r > 1.3 * g and r > 1.3 * b:
        return "red/orange" if g > 0.45 * r else "deep red"
    if r > b and g > b and abs(r - g) < 0.25 * max(r, g):
        return "yellow/brown"
    if g >= r and g >= b:
        return "green"
    return "purple/dark"


def _region_name(cy: float, cx: float) -> str:
    v = "upper" if cy < 0.4 else "lower" if cy > 0.6 else "central"
    h = "left" if cx < 0.4 else "right" if cx > 0.6 else ""
    return (v + ("-" + h if h else "")) if not (v == "central" and not h) else "centre"


HARVEST = {
    "unripe": "Not ready — re-check in about two harvest rounds (~{d2} days)",
    "underripe": "Nearly ready — re-check next round (~{d1} days)",
    "ripe": "Harvest this round",
    "overripe": "Harvest immediately — loose-fruit and FFA risk; flag block for a shorter round",
}


def harvest_advice(label: str) -> str:
    """M2 — rule-based harvest window from ripeness class (19–24 weeks after anthesis [RAMLI2026]).
    Round interval is a configurable assumption (SIMULATED schedule) pending research R1(e)."""
    return HARVEST.get(label, "Grade manually").format(d1=C.HARVEST_ROUND_DAYS, d2=2 * C.HARVEST_ROUND_DAYS)


def predict(jpeg: bytes, heatmap_name: str | None = None) -> dict:
    sess, meta = _load()
    try:
        img = Image.open(io.BytesIO(jpeg)).convert("RGB")
    except Exception as e:  # noqa: BLE001
        raise ValueError(f"Not a decodable image: {e}") from e
    x, crop = _preprocess(img, meta)
    logits, feats = sess.run(["logits", "features"], {"input": x})
    z = logits[0] - logits[0].max()
    p = np.exp(z) / np.exp(z).sum()
    classes = meta["classes"]
    k = int(p.argmax())
    label = classes[k]

    # CAM for the predicted class
    cam = np.tensordot(meta["_W"][k], feats[0], axes=(0, 0))
    cam = np.maximum(cam, 0)
    cam = cam / cam.max() if cam.max() > 0 else cam
    s = meta["input_size"]
    cam_img = np.asarray(Image.fromarray((cam * 255).astype(np.uint8)).resize((s, s), Image.BILINEAR), np.float32) / 255
    hot = cam_img >= np.quantile(cam_img, 0.8)
    ys, xs = np.nonzero(hot)
    region = _region_name(ys.mean() / s, xs.mean() / s) if len(ys) else "whole image"
    crop_a = np.asarray(crop, dtype=np.float32)
    colour = _hue_name(crop_a[hot].mean(0)) if hot.any() else "n/a"
    coverage = float(hot.mean())

    heatmap_url = None
    if heatmap_name:
        overlay = (0.55 * crop_a + 0.45 * _colormap(cam_img)).astype(np.uint8)
        side = np.concatenate([crop_a.astype(np.uint8), overlay], axis=1)
        Image.fromarray(side).save(C.HEATMAP_DIR / f"{heatmap_name}.png")
        heatmap_url = f"/static/heatmaps/{heatmap_name}.png"

    second = classes[int(np.argsort(p)[-2])]
    explanation = (f"Model attends to the {region} of the image (top-20% heat), where the dominant colour is {colour}; "
                   f"{p[k]:.0%} {label} vs {p[classes.index(second)]:.0%} {second}.")
    if p[k] < 0.6:
        explanation += " Low confidence — send to grader for review."
    return {
        "label": label,
        "confidence": round(float(p[k]), 3),
        "probs": {c: round(float(v), 3) for c, v in zip(classes, p)},
        "harvest_advice": harvest_advice(label),
        "explanation": explanation,
        "heatmap_url": heatmap_url,
        "model_version": meta["model_version"],
        "needs_review": bool(p[k] < 0.6),
        "attention": {"region": region, "colour": colour, "hot_fraction": round(coverage, 2)},
    }
