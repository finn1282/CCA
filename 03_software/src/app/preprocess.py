"""Shared M1 image preprocessing — the SAME code runs in training/evaluation (train_m1.py) and in the
API (inference.py), so reported metrics are the serving-path metrics (S-16).
Pure PIL + numpy, no relative imports (train_m1.py imports it as a plain module)."""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageOps

MEAN = (0.485, 0.456, 0.406)
STD = (0.229, 0.224, 0.225)
BASE_SHORT = 288   # stage 1: normalise any upload (phone/drone, up to 5 MB) to a 288-px short side
RESIZE = 256       # stage 2: short side 256 …
SIZE = 224         # … centre crop 224


def base_image(img: Image.Image) -> Image.Image:
    """EXIF-orient, RGB, downscale so the short side is BASE_SHORT (bilinear)."""
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:  # noqa: BLE001 — some phone JPEGs carry malformed EXIF
        pass
    img = img.convert("RGB")
    img.thumbnail((BASE_SHORT * 4, BASE_SHORT * 4))
    w, h = img.size
    s = BASE_SHORT / min(w, h)
    return img.resize((max(1, round(w * s)), max(1, round(h * s))), Image.BILINEAR)


def eval_crop(img288: Image.Image, resize: int = RESIZE, size: int = SIZE) -> Image.Image:
    w, h = img288.size
    s = resize / min(w, h)
    img = img288.resize((max(size, round(w * s)), max(size, round(h * s))), Image.BILINEAR)
    w, h = img.size
    left, top = (w - size) // 2, (h - size) // 2
    return img.crop((left, top, left + size, top + size))


def to_array(crop: Image.Image, mean=MEAN, std=STD) -> np.ndarray:
    a = (np.asarray(crop, dtype=np.float32) / 255.0 - np.array(mean, np.float32)) / np.array(std, np.float32)
    return a.transpose(2, 0, 1).astype(np.float32)        # CHW


def eval_array(img: Image.Image) -> tuple[np.ndarray, Image.Image]:
    """Full serving path for an opened image: returns (CHW float32, 224-px RGB crop)."""
    crop = eval_crop(base_image(img))
    return to_array(crop), crop
