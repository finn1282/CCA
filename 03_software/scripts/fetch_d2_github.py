"""Download D2 (Rosbi 2024, CC BY 4.0) images for the 3 classes we use, from the GitHub mirror.
Usage: python scripts/fetch_d2_github.py data/raw/d2 [FFBtest FFBtrain] [--max-per-class N]
Skips files already present. Damaged/Empty are excluded (no D1 equivalent, PLAN M1).
--max-per-class N keeps at most N files per class folder, smallest first (quick runs on slow links)."""
import json
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

REPO = "MunirahRosbi/Outdoor-Tenera-Oil-Palm-Fruit-Image"
args = sys.argv[1:]
cap = 0
if "--max-per-class" in args:
    i = args.index("--max-per-class")
    cap = int(args[i + 1])
    del args[i:i + 2]
out = Path(args[0])
splits = args[1:] or ["FFBtest", "FFBtrain"]
tree = json.load(urllib.request.urlopen(f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1"))["tree"]
taken = defaultdict(int)
for x in sorted(tree, key=lambda t: t.get("size") or 0):
    p = x["path"]
    if x["type"] != "blob" or p.split("/")[0] not in splits or any(k in p for k in ("Damaged", "Empty")):
        continue
    folder = p.rsplit("/", 1)[0]
    if cap and taken[folder] >= cap:
        continue
    taken[folder] += 1
    dst = out / p
    if dst.exists() and dst.stat().st_size == x["size"]:
        continue
    dst.parent.mkdir(parents=True, exist_ok=True)
    url = f"https://raw.githubusercontent.com/{REPO}/main/" + urllib.parse.quote(p)
    with urllib.request.urlopen(url, timeout=120) as r:
        dst.write_bytes(r.read())
    print("ok", p, flush=True)
