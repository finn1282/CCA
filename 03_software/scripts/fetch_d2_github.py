"""Download D2 (Rosbi 2024, CC BY 4.0) images for the 3 classes we use, from the GitHub mirror.
Usage: python scripts/fetch_d2_github.py data/raw/d2 [FFBtest FFBtrain]
Skips files already present. Damaged/Empty are excluded (no D1 equivalent, PLAN M1)."""
import json, sys, urllib.parse, urllib.request
from pathlib import Path
REPO = "MunirahRosbi/Outdoor-Tenera-Oil-Palm-Fruit-Image"
out = Path(sys.argv[1]); splits = sys.argv[2:] or ["FFBtest", "FFBtrain"]
tree = json.load(urllib.request.urlopen(f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1"))["tree"]
for x in tree:
    p = x["path"]
    if x["type"] != "blob" or p.split("/")[0] not in splits or any(k in p for k in ("Damaged", "Empty")):
        continue
    dst = out / p
    if dst.exists() and dst.stat().st_size == x["size"]:
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://raw.githubusercontent.com/{REPO}/main/" + urllib.parse.quote(p)
    with urllib.request.urlopen(url, timeout=120) as r:
        dst.write_bytes(r.read())
    print("ok", p, flush=True)
