"""Independent re-evaluation of the exported M1 ripeness model on local D2 files (no downloads, D43).

Written by SW Verification. Uses only onnxruntime + numpy + Pillow (03_software/.venv), not the training code:
  * own folder->class mapping for D2 (TestUnripe/TestRipe/TestOverripe), cross-checked with train_m1.map_class/split_of
  * two preprocessing paths on the D2 test originals:
      A "serving"  = exactly what src/app/inference.py does with uploaded bytes (no EXIF transpose)
      B "training" = EXIF transpose first (as train_m1.ImgDS._open), then the same resize/crop/normalise
  * confusion matrix / accuracy / macro-F1, compared with training/ripeness/m1_metrics_provisional.json
  * leakage: exact (MD5) and near-duplicate (64-bit dHash, Hamming <= 6) pairs across FFBtrain x FFBtest
Run:  03_software/.venv/bin/python 07_verification/software/tests/eval_m1.py [--out results.md]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

REPO = Path(__file__).resolve().parents[3]
SW = REPO / "03_software"
D2 = SW / "data" / "raw" / "d2"
MODEL = SW / "models" / "m1_ripeness.onnx"
META = SW / "models" / "m1_ripeness.json"
METRICS = SW / "training" / "ripeness" / "m1_metrics_provisional.json"
FOLDER_CLASS = {"unripe": "unripe", "ripe": "ripe", "overripe": "overripe"}   # D2 Test<X>/Train<X> -> class


def own_class(folder: str) -> str | None:
    x = folder.lower().removeprefix("test").removeprefix("train")
    return FOLDER_CLASS.get(x)


def files(split: str):
    out = []
    for d in sorted((D2 / split).iterdir()):
        c = own_class(d.name)
        for f in sorted(d.iterdir()):
            if f.suffix.lower() in (".jpg", ".jpeg", ".png") and c:
                out.append((f, c))
    return out


def preprocess(img: Image.Image, meta: dict) -> np.ndarray:
    """Mirror of inference._preprocess (resize short side to meta.resize, centre crop, normalise)."""
    s = meta["input_size"]
    w, h = img.size
    scale = meta.get("resize", 256) / min(w, h)
    img = img.resize((max(s, round(w * scale)), max(s, round(h * scale))), Image.BILINEAR)
    w, h = img.size
    l, t = (w - s) // 2, (h - s) // 2
    img = img.crop((l, t, l + s, t + s))
    a = (np.asarray(img, np.float32) / 255.0 - np.array(meta["mean"], np.float32)) / np.array(meta["std"], np.float32)
    return a.transpose(2, 0, 1)[None].astype(np.float32)


def metrics(y, p, classes):
    k = len(classes)
    cm = np.zeros((k, k), int)
    for a, b in zip(y, p):
        cm[a, b] += 1
    per, f1s = {}, []
    for c in range(k):
        tp, n_true, n_pred = cm[c, c], cm[c].sum(), cm[:, c].sum()
        if n_true == 0:
            continue
        prec = tp / n_pred if n_pred else 0.0
        rec = tp / n_true
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        per[classes[c]] = {"precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3), "n": int(n_true)}
        f1s.append(f1)
    return {"n": int(cm.sum()), "accuracy": round(float(np.trace(cm) / cm.sum()), 4),
            "macro_f1_present_classes": round(float(np.mean(f1s)), 4), "per_class": per, "cm": cm.tolist()}


def exif_t(im: Image.Image) -> Image.Image:
    """As train_m1: some phone JPEGs carry malformed EXIF -> keep the original orientation."""
    try:
        return ImageOps.exif_transpose(im)
    except Exception:  # noqa: BLE001
        return im


def dhash(path: Path) -> int:
    im = exif_t(Image.open(path)).convert("L")
    im.draft("L", (64, 64))
    a = np.asarray(im.resize((9, 8), Image.BILINEAR), np.int16)
    bits = (a[:, 1:] > a[:, :-1]).flatten()
    return int("".join("1" if b else "0" for b in bits), 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    a = ap.parse_args()
    import onnxruntime as ort
    meta = json.loads(META.read_text())
    classes = meta["classes"]
    W = np.asarray(meta["fc_weight"], np.float32)
    sess = ort.InferenceSession(str(MODEL), providers=["CPUExecutionProvider"])
    rep = {"model_version": meta["model_version"], "classes": classes}

    test, train = files("FFBtest"), files("FFBtrain")
    rep["counts"] = {"test": {c: sum(1 for _, k in test if k == c) for c in classes},
                     "train": {c: sum(1 for _, k in train if k == c) for c in classes}}

    # class mapping / split cross-check with the training code (optional: needs torch importable)
    try:
        sys.path.insert(0, str(SW / "training" / "ripeness"))
        import train_m1  # noqa: E402
        mism = [(str(f.relative_to(D2)), c, train_m1.map_class(f)) for f, c in test + train if train_m1.map_class(f) != c]
        spl = [str(f.relative_to(D2)) for f, _ in test if train_m1.split_of(f.relative_to(D2)) != "test"] + \
              [str(f.relative_to(D2)) for f, _ in train if train_m1.split_of(f.relative_to(D2)) != "train"]
        rep["mapping_check"] = {"class_mismatches": mism[:10], "n_class_mismatches": len(mism),
                                "split_mismatches": spl[:10], "n_split_mismatches": len(spl),
                                "D1_names": {n: train_m1.map_class(Path(f"D1/{n}/x.jpg")) for n in
                                             ("Immature", "Partially Ripe", "Fully Ripe", "Overripe", "Decayed",
                                              "Unripe", "Mature", "Underripe")}}
    except Exception as e:  # noqa: BLE001
        rep["mapping_check"] = {"error": repr(e)}

    # evaluation, two preprocessing paths
    exif_rot = 0
    sys.path.insert(0, str(SW / "src" / "app"))
    try:
        import preprocess as PP  # the API's shared preprocessing (S-16 fix, Pass 3)
    except ImportError:
        PP = None
    paths = [("A_legacy_serving_no_exif", "legacy", False), ("B_legacy_exif", "legacy", True)]
    if PP:
        paths.append(("C_shared_serving_path", "shared", False))
    for name, mode, use_exif in paths:
        y, p, lat, cam_centre, names = [], [], [], [], []
        for f, c in test:
            im = Image.open(f)
            if use_exif:
                o = im.getexif().get(0x0112, 1)
                exif_rot += int(o not in (1, None))
                im = exif_t(im)
            if mode == "shared":
                x = PP.eval_array(im)[0][None]
            else:
                x = preprocess(im.convert("RGB"), meta)
            t0 = time.perf_counter()
            logits, feats = sess.run(["logits", "features"], {"input": x})
            lat.append(time.perf_counter() - t0)
            k = int(logits[0].argmax())
            y.append(classes.index(c)); p.append(k); names.append(str(f.relative_to(D2)))
            cam = np.maximum(np.tensordot(W[k], feats[0], axes=(0, 0)), 0)
            if cam.max() > 0:
                cam = cam / cam.sum()
                cam_centre.append(float(cam[1:6, 1:6].sum()))   # mass in the central 5x5 of 7x7
        m = metrics(y, p, classes)
        m["onnx_latency_ms_p50"] = round(1000 * float(np.median(lat)), 1)
        m["cam_mass_in_centre_mean"] = round(float(np.mean(cam_centre)), 3)
        m["_pred"] = list(zip(names, y, p))
        rep[name] = m
    rep["exif_rotated_test_images"] = exif_rot

    mj = json.loads(METRICS.read_text()) if METRICS.exists() else {}
    rep["reported"] = mj.get("d2_malaysia_test")
    rep["reported_serving_path"] = (mj.get("serving_path") or {}).get("d2_malaysia_test")
    if rep["reported"] is not None:
        rep["reported"]["_dropped"] = mj.get("d2_test_duplicates_removed", [])

    # leakage across the provided split
    md5 = lambda f: hashlib.md5(f.read_bytes()).hexdigest()  # noqa: E731
    tr_md5 = {md5(f): f for f, _ in train}
    exact = [(str(f.relative_to(D2)), str(tr_md5[h].relative_to(D2))) for f, _ in test if (h := md5(f)) in tr_md5]
    tr_h = [(dhash(f), f) for f, _ in train]
    near = []
    for f, _ in test:
        h = dhash(f)
        best = min(((bin(h ^ g).count("1"), t) for g, t in tr_h), key=lambda z: z[0])
        if best[0] <= 6:
            near.append((str(f.relative_to(D2)), str(best[1].relative_to(D2)), best[0]))
    od = {"FFBtest/" + d["test"] for d in (rep["reported"] or {}).get("_dropped", [])}
    mine = {a for a, *_ in near} | {a for a, _ in exact}
    rep["owner_dedupe_covers_mine"] = {"covered": sorted(mine & od), "missing": sorted(mine - od), "owner_extra": sorted(od - mine)}
    rep["leakage"] = {"exact_md5_pairs": exact, "near_dup_pairs_hamming_le6": near,
                      "n_exact": len(exact), "n_near": len(near)}

    leaked = {a for a, *_ in near} | {a for a, _ in exact}
    owner = {"FFBtest/" + d["test"] for d in (rep["reported"] or {}).get("_dropped", [])}
    for name, *_ in paths:
        pr = rep[name]["_pred"]
        if owner:
            keep = [(y, p) for n, y, p in pr if n not in owner]
            rep[name]["owner_dedup_test"] = {k: v for k, v in metrics([y for y, _ in keep], [p for _, p in keep], classes).items()
                                             if k != "per_class"}
        pr = rep[name].pop("_pred")
        keep = [(y, p) for n, y, p in pr if n not in leaked]
        rep[name]["dedup_test"] = {k: v for k, v in metrics([y for y, _ in keep], [p for _, p in keep], classes).items() if k != "per_class"}
        rep[name]["errors"] = [(n, classes[y], classes[p]) for n, y, p in pr if y != p]
    txt = json.dumps(rep, indent=1)
    print(txt)
    if a.out:
        Path(a.out).write_text("# eval_m1.py output\n\n```json\n" + txt + "\n```\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
