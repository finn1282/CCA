"""M1 — FFB ripeness classifier (EfficientNet-B0 transfer learning) → ONNX for the SawitSense API.

Data (D16): D1 Kamal et al. (2024), Indonesia, CC BY 4.0 → train/val/test.
            D2 Rosbi (2024), Malaysia, CC BY 4.0 → cross-country test (+ optional head fine-tune).
Classes (harmonised, PLAN M1): unripe · underripe · ripe · overripe  (D2 Empty/Damaged excluded).

Two stages, same script on a laptop CPU or a Kaggle GPU:
  1. Frozen backbone: extract pooled features (with flip/crop augmentation), train a linear head.
  2. Optional fine-tune of the last blocks (--finetune-epochs N; use on GPU).
Outputs (to --out, default 03_software/models/):
  m1_ripeness.onnx   — inputs "input" [N,3,224,224]; outputs "logits", "features" [N,1280,7,7]
  m1_ripeness.json   — classes, preprocessing, classifier weights (for CAM), metrics
  m1_metrics.json    — full metrics incl. confusion matrices
Examples:
  python train_m1.py --d1 ../../data/raw/d1 --d2 ../../data/raw/d2                     # CPU, stage 1 only
  python train_m1.py --d1 /kaggle/input/... --d2 /kaggle/input/... --device cuda --finetune-epochs 8 --out /kaggle/working
"""
from __future__ import annotations

import argparse
import json
import random
import re
import time
from collections import Counter
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from PIL import Image, ImageOps
from torch.utils.data import DataLoader, Dataset
from torchvision import models, transforms

CLASSES = ["unripe", "underripe", "ripe", "overripe"]
MEAN, STD = [0.485, 0.456, 0.406], [0.229, 0.224, 0.225]
IMG_EXT = {".jpg", ".jpeg", ".png", ".bmp"}
VERSION = "m1-effb0-0.1"


def map_class(path: Path) -> str | None:
    """Map a folder name from D1/D2/D3 to a harmonised class (order matters)."""
    s = "/".join(p.lower() for p in path.parts[-3:-1])
    if re.search(r"damaged|empty", s):
        return None
    if re.search(r"overripe|over[-_ ]ripe|decay", s):
        return "overripe"
    if re.search(r"partial|underripe|under[-_ ]ripe|mengkal", s):
        return "underripe"
    if re.search(r"immature|unripe|mentah", s):
        return "unripe"
    if re.search(r"ripe|masak|mature", s):
        return "ripe"
    return None


def split_of(path: Path) -> str | None:
    s = "/".join(p.lower() for p in path.parts)
    for name, keys in (("test", ("test",)), ("val", ("val", "valid")), ("train", ("train",))):
        if any(re.search(rf"(^|/|_|-){k}", s) for k in keys):
            return name
    return None


def scan(root: Path) -> list[tuple[Path, int, str | None]]:
    items = []
    for p in sorted(root.rglob("*")):
        if p.suffix.lower() in IMG_EXT and not p.name.startswith("."):
            c = map_class(p)
            if c:
                items.append((p, CLASSES.index(c), split_of(p.relative_to(root))))
    return items


def stratified(items, seed=42, val=0.15, test=0.15):
    rng = random.Random(seed)
    by = {}
    for it in items:
        by.setdefault(it[1], []).append(it)
    out = {"train": [], "val": [], "test": []}
    for lst in by.values():
        rng.shuffle(lst)
        n = len(lst); nt, nv = int(n * test), int(n * val)
        out["test"] += lst[:nt]; out["val"] += lst[nt:nt + nv]; out["train"] += lst[nt + nv:]
    return out


class ImgDS(Dataset):
    def __init__(self, items, tf, cache: Path | None = None):
        self.items, self.tf, self.cache = items, tf, cache

    def __len__(self):
        return len(self.items)

    def _open(self, p: Path) -> Image.Image:
        # Cache a 288-px copy: D2 originals are up to 5 MB, decoding them every epoch is slow on CPU.
        if self.cache:
            cp = self.cache / (str(abs(hash(str(p)))) + ".jpg")
            if cp.exists():
                return Image.open(cp).convert("RGB")
        img = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
        img.thumbnail((288 * 4, 288 * 4))
        w, h = img.size; s = 288 / min(w, h)
        img = img.resize((max(1, round(w * s)), max(1, round(h * s))), Image.BILINEAR)
        if self.cache:
            img.save(cp, quality=92)
        return img

    def __getitem__(self, i):
        p, y, _ = self.items[i]
        return self.tf(self._open(p)), y


def tfs(train: bool):
    if train:
        return transforms.Compose([transforms.RandomResizedCrop(224, scale=(0.6, 1.0)), transforms.RandomHorizontalFlip(),
                                   transforms.ColorJitter(0.15, 0.15, 0.1, 0.02), transforms.ToTensor(), transforms.Normalize(MEAN, STD)])
    return transforms.Compose([transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(), transforms.Normalize(MEAN, STD)])


@torch.no_grad()
def extract(backbone, items, tf, device, bs, workers, cache, passes=1):
    feats, ys = [], []
    for _ in range(passes):
        dl = DataLoader(ImgDS(items, tf, cache), batch_size=bs, num_workers=workers)
        for x, y in dl:
            f = backbone.avgpool(backbone.features(x.to(device))).flatten(1)
            feats.append(f.cpu()); ys.append(y)
    return torch.cat(feats), torch.cat(ys)


def train_head(head, X, y, Xv, yv, epochs=300, lr=1e-3, wd=1e-4, class_weight=None):
    opt = torch.optim.AdamW(head.parameters(), lr=lr, weight_decay=wd)
    lossf = nn.CrossEntropyLoss(weight=class_weight)
    best, best_state = -1, None
    for ep in range(epochs):
        head.train()
        perm = torch.randperm(len(X))
        for i in range(0, len(X), 256):
            idx = perm[i:i + 256]
            opt.zero_grad(); lossf(head(X[idx]), y[idx]).backward(); opt.step()
        if ep % 10 == 9 or ep == epochs - 1:
            head.eval()
            with torch.no_grad():
                acc = (head(Xv).argmax(1) == yv).float().mean().item()
            if acc > best:
                best, best_state = acc, {k: v.clone() for k, v in head.state_dict().items()}
    head.load_state_dict(best_state)
    return best


def metrics(y_true, y_pred, labels=range(len(CLASSES))):
    y_true, y_pred = np.asarray(y_true), np.asarray(y_pred)
    cm = np.zeros((len(CLASSES), len(CLASSES)), int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    present = [c for c in labels if cm[c].sum() > 0]
    f1s, per = [], {}
    for c in present:
        tp = cm[c, c]; fp = cm[:, c].sum() - tp; fn = cm[c].sum() - tp
        prec = tp / (tp + fp) if tp + fp else 0.0; rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        f1s.append(f1); per[CLASSES[c]] = {"precision": round(prec, 3), "recall": round(rec, 3), "f1": round(f1, 3), "n": int(cm[c].sum())}
    return {"n": int(len(y_true)), "accuracy": round(float((y_true == y_pred).mean()), 4),
            "macro_f1_present_classes": round(float(np.mean(f1s)), 4),
            "within_one_class_accuracy": round(float((np.abs(y_true - y_pred) <= 1).mean()), 4),
            "per_class": per, "confusion_matrix": {"labels": CLASSES, "rows_true_cols_pred": cm.tolist()}}


class Exportable(nn.Module):
    def __init__(self, net):
        super().__init__(); self.net = net

    def forward(self, x):
        f = self.net.features(x)
        return self.net.classifier(self.net.avgpool(f).flatten(1)), f


def predict(net, items, device, bs, workers, cache):
    net.eval(); preds = []
    with torch.no_grad():
        for x, _ in DataLoader(ImgDS(items, tfs(False), cache), batch_size=bs, num_workers=workers):
            preds.append(net(x.to(device)).argmax(1).cpu())
    return torch.cat(preds).numpy() if preds else np.array([], int)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d1", type=Path, help="extracted D1 root (omit = PROVISIONAL model trained on D2 train only)")
    ap.add_argument("--d2", type=Path, help="D2 root (FFBtest/ FFBtrain/)")
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parents[2] / "models")
    ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--aug-passes", type=int, default=2, help="augmented feature passes for the head (stage 1)")
    ap.add_argument("--finetune-epochs", type=int, default=0)
    ap.add_argument("--max-per-class", type=int, default=0, help="cap training images per class (quick runs)")
    ap.add_argument("--seed", type=int, default=42)
    a = ap.parse_args()
    torch.manual_seed(a.seed); random.seed(a.seed); np.random.seed(a.seed)
    a.out.mkdir(parents=True, exist_ok=True)
    cache = a.out / "_imgcache"; cache.mkdir(exist_ok=True)
    t0 = time.time()

    d2 = scan(a.d2) if a.d2 and a.d2.exists() else []
    d2_test = [it for it in d2 if it[2] == "test"]
    d2_train = [it for it in d2 if it[2] == "train"]
    print("D2:", dict(Counter(CLASSES[i[1]] for i in d2)), "test", len(d2_test), "train", len(d2_train), flush=True)
    provisional = False
    d1 = scan(a.d1) if a.d1 else []
    if not d1:
        if not (d2_train and d2_test):
            raise SystemExit("No D1 images and no D2 train/test split found")
        # PROVISIONAL: D1 unavailable on this machine -> train on Malaysian D2 train, test on D2 test.
        provisional = True
        tr = stratified(d2_train, a.seed, val=0.15, test=0.0)
        sp = {"train": tr["train"], "val": tr["val"], "test": d2_test}
        split_src = "PROVISIONAL: D2 train (85/15 train/val) -> D2 test; D1 not used"
        d2, d2_test, d2_train = [], [], []
    elif all(s for _, _, s in d1):
        sp = {k: [it for it in d1 if it[2] == k] for k in ("train", "val", "test")}
        split_src = "dataset-provided split"
    else:
        sp = stratified(d1, a.seed); split_src = "stratified 70/15/15 (seed 42)"
    if not provisional and not sp["val"]:
        tr = stratified(sp["train"], a.seed, val=0.15, test=0.0); sp["train"], sp["val"] = tr["train"], tr["val"]
    if a.max_per_class:
        cnt, keep = Counter(), []
        for it in sp["train"]:
            if cnt[it[1]] < a.max_per_class:
                keep.append(it); cnt[it[1]] += 1
        sp["train"] = keep
    print({k: dict(Counter(CLASSES[i[1]] for i in v)) for k, v in sp.items()}, split_src, flush=True)

    net = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1).to(a.device).eval()
    head = nn.Linear(1280, len(CLASSES))

    # Stage 1 — frozen features + linear head
    Xtr, ytr = extract(net, sp["train"], tfs(True), a.device, a.bs, a.workers, cache, passes=a.aug_passes)
    Xtr_c, ytr_c = extract(net, sp["train"], tfs(False), a.device, a.bs, a.workers, cache)
    Xtr, ytr = torch.cat([Xtr, Xtr_c]), torch.cat([ytr, ytr_c])
    Xv, yv = extract(net, sp["val"], tfs(False), a.device, a.bs, a.workers, cache)
    counts = torch.bincount(ytr, minlength=len(CLASSES)).float()
    cw = (counts.sum() / (len(CLASSES) * counts.clamp(min=1)))
    val_acc = train_head(head, Xtr, ytr, Xv, yv, class_weight=cw)
    print(f"stage1 val acc {val_acc:.4f}  ({time.time() - t0:.0f}s)", flush=True)
    net.classifier[1] = head.to(a.device)

    # Stage 2 — optional fine-tune (GPU recommended)
    if a.finetune_epochs:
        for p in net.features[:-3].parameters():
            p.requires_grad = False
        opt = torch.optim.AdamW([p for p in net.parameters() if p.requires_grad], lr=3e-4, weight_decay=1e-4)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, a.finetune_epochs)
        lossf = nn.CrossEntropyLoss(weight=cw.to(a.device), label_smoothing=0.05)
        dl = DataLoader(ImgDS(sp["train"], tfs(True), cache), batch_size=a.bs, shuffle=True, num_workers=a.workers)
        best, best_state = val_acc, {k: v.clone() for k, v in net.state_dict().items()}
        for ep in range(a.finetune_epochs):
            net.train()
            for x, y in dl:
                opt.zero_grad(); lossf(net(x.to(a.device)), y.to(a.device)).backward(); opt.step()
            sched.step()
            acc = float((predict(net, sp["val"], a.device, a.bs, a.workers, cache) == np.array([i[1] for i in sp["val"]])).mean())
            print(f"finetune ep{ep + 1} val acc {acc:.4f}", flush=True)
            if acc > best:
                best, best_state = acc, {k: v.clone() for k, v in net.state_dict().items()}
        net.load_state_dict(best_state); val_acc = best
    net.eval()

    version = VERSION + ("-provisional" if provisional else "")
    res = {"model_version": version, "provisional": provisional, "split": split_src, "val_accuracy": round(val_acc, 4),
           ("d2_malaysia_test" if provisional else "d1_test"): metrics([i[1] for i in sp["test"]], predict(net, sp["test"], a.device, a.bs, a.workers, cache))}
    if d2:
        res["d2_malaysia_all_zero_shot"] = metrics([i[1] for i in d2], predict(net, d2, a.device, a.bs, a.workers, cache))
    if d2_test:
        res["d2_malaysia_test_zero_shot"] = metrics([i[1] for i in d2_test], predict(net, d2_test, a.device, a.bs, a.workers, cache))
    if d2_train and d2_test:
        # Variant: adapt only the head with Malaysian train images (keeps the D1 backbone), test on D2 test.
        Xd, yd = extract(net, d2_train, tfs(True), a.device, a.bs, a.workers, cache, passes=a.aug_passes)
        head2 = nn.Linear(1280, len(CLASSES)); head2.load_state_dict(net.classifier[1].state_dict())
        Xmix = torch.cat([Xtr, Xd, Xd]); ymix = torch.cat([ytr, yd, yd])   # D2 up-weighted ×2
        train_head(head2.cpu(), Xmix, ymix, Xv.cpu(), yv, epochs=150)
        Xt2, yt2 = extract(net, d2_test, tfs(False), a.device, a.bs, a.workers, cache)
        res["d2_malaysia_test_after_head_finetune"] = metrics(yt2.numpy(), head2(Xt2).argmax(1).numpy())
    res["train_seconds"] = round(time.time() - t0)
    res["device"] = a.device
    res["finetune_epochs"] = a.finetune_epochs
    res["train_counts"] = dict(Counter(CLASSES[i[1]] for i in sp["train"]))

    # Export ONNX (logits + features for CAM)
    net_cpu = Exportable(net.cpu()).eval()
    onnx_path = a.out / "m1_ripeness.onnx"
    torch.onnx.export(net_cpu, torch.randn(1, 3, 224, 224), str(onnx_path), input_names=["input"],
                      output_names=["logits", "features"], dynamic_axes={"input": {0: "n"}, "logits": {0: "n"}, "features": {0: "n"}},
                      opset_version=17, dynamo=False)
    fc = net.classifier[1]
    meta = {"model_version": version, "provisional": provisional, "classes": CLASSES, "input_size": 224, "resize": 256, "mean": MEAN, "std": STD,
            "fc_weight": fc.weight.detach().cpu().numpy().round(6).tolist(), "fc_bias": fc.bias.detach().cpu().numpy().round(6).tolist(),
            "architecture": "EfficientNet-B0 (ImageNet) transfer learning", "explainability": "CAM from final linear layer (= Grad-CAM for GAP-linear head)",
            "data": ("PROVISIONAL: train/test D2 Rosbi 2024 Malaysia (CC BY 4.0); no underripe class in D2" if provisional
                     else "Train D1 Kamal et al. 2024 (CC BY 4.0); test D2 Rosbi 2024 Malaysia (CC BY 4.0)"),
            "metrics_summary": {k: v["accuracy"] for k, v in res.items() if isinstance(v, dict) and "accuracy" in v}}
    (a.out / "m1_ripeness.json").write_text(json.dumps(meta))
    (a.out / "m1_metrics.json").write_text(json.dumps(res, indent=2))
    print(json.dumps(meta["metrics_summary"], indent=2), f"\nsaved {onnx_path} ({onnx_path.stat().st_size / 1e6:.1f} MB)")

    # Sanity check: ONNX matches PyTorch
    import onnxruntime as ort
    x = torch.randn(2, 3, 224, 224)
    lo, fo = ort.InferenceSession(str(onnx_path)).run(None, {"input": x.numpy()})
    lt, ft = net_cpu(x)
    print("onnx max |diff| logits", float(np.abs(lo - lt.detach().numpy()).max()))


if __name__ == "__main__":
    main()
