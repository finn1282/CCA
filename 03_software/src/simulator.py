"""SawitSense soil-node simulator — lets the demo run without hardware.

Emits INTERFACES v0.2.1 payloads with realistic drift and noise. Scenarios:
  normal | dry | wet | acidic | low_nutrient | over_fertilised | sensor_fault | cycle (walks through all)
Examples (from 03_software/src):
  python simulator.py --scenario cycle --interval 2
  python simulator.py --scenario dry --count 5 --base https://<app>.azurewebsites.net
  python simulator.py --image ../data/demo/ripe.jpg      # also post one camera image
Stdlib only (no extra install). SIMULATED data — label it as such when shown.
"""
from __future__ import annotations

import argparse
import json
import random
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

TARGETS = {  # (moisture %, pH, TDS ppm) the state drifts toward
    "normal": (55, 5.0, 600),
    "dry": (22, 5.0, 600),
    "wet": (88, 5.1, 560),
    "acidic": (50, 3.7, 620),
    "low_nutrient": (52, 5.0, 330),
    "over_fertilised": (50, 4.9, 950),
    "sensor_fault": (50, 5.0, 600),
}
CYCLE = ["normal", "dry", "normal", "acidic", "low_nutrient", "over_fertilised", "wet", "sensor_fault"]


class Node:
    def __init__(self, device_id: str, block: str):
        self.device_id, self.block, self.seq = device_id, block, 0
        self.m, self.ph, self.tds, self.t = 55.0, 5.0, 600.0, 27.5

    def step(self, scenario: str) -> dict:
        tm, tph, ttds = TARGETS[scenario]
        a = 0.35  # drift rate toward the scenario target
        self.m += a * (tm - self.m) + random.gauss(0, 0.8)
        self.ph += a * (tph - self.ph) + random.gauss(0, 0.03)
        self.tds += a * (ttds - self.tds) + random.gauss(0, 10)
        self.t += 0.1 * (27.5 - self.t) + random.gauss(0, 0.1)
        self.seq += 1
        fault = scenario == "sensor_fault"
        return {
            "device_id": self.device_id, "seq": self.seq,
            "ts": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "buffered": False, "block_id": self.block,
            "soil_moisture_pct": round(min(100, max(0, self.m)), 1),
            "soil_ph": None if fault else round(self.ph, 2),       # failed sensor → null (INTERFACES §2)
            "tds_ppm": round(max(0, self.tds)), "ec_us_cm": None,
            "soil_temp_c": round(self.t, 1), "air_temp_c": round(self.t + 2.5 + random.gauss(0, 0.3), 1),
            "air_rh_pct": round(78 + random.gauss(0, 2), 1), "rssi_dbm": random.randint(-72, -55),
            "cal_id": datetime.now().strftime("%Y-%m-%d"), "fw_version": "sim-0.2.1",
        }


def post(url: str, body: bytes, headers: dict) -> dict:
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="http://localhost:8000")
    ap.add_argument("--device", default="sim-01")
    ap.add_argument("--key", default="demo-sim-key")
    ap.add_argument("--block", default="DEMO-A1")
    ap.add_argument("--scenario", default="cycle", choices=[*TARGETS, "cycle"])
    ap.add_argument("--interval", type=float, default=10.0)
    ap.add_argument("--count", type=int, default=0, help="0 = run forever")
    ap.add_argument("--per-scenario", type=int, default=6, help="readings per scenario in cycle mode")
    ap.add_argument("--image", help="post this JPEG to the ripeness endpoint once (as cam-01)")
    ap.add_argument("--cam-key", default="demo-cam-key")
    a = ap.parse_args()

    if a.image:
        with open(a.image, "rb") as f:
            res = post(f"{a.base}/api/v1/infer/ripeness", f.read(),
                       {"Content-Type": "image/jpeg", "X-Device-Id": "cam-01", "X-Device-Key": a.cam_key})
        print("camera:", res["label"], res["confidence"], "|", res["harvest_advice"], "|", res["evidence_id"])

    node, n = Node(a.device, a.block), 0
    hdr = {"Content-Type": "application/json", "X-Device-Id": a.device, "X-Device-Key": a.key}
    while a.count == 0 or n < a.count:
        sc = CYCLE[(n // a.per_scenario) % len(CYCLE)] if a.scenario == "cycle" else a.scenario
        p = node.step(sc)
        try:
            r = post(f"{a.base}/api/v1/readings", json.dumps(p).encode(), hdr)
            print(f"[{sc:15s}] seq={p['seq']:4d} m={p['soil_moisture_pct']:5.1f} pH={p['soil_ph']} tds={p['tds_ppm']:4d}"
                  f" -> {r['action']:15s} {r['led']:5s} conf={r['confidence']:.2f} {r['evidence_id']} | {' / '.join(r['oled'])}")
        except urllib.error.HTTPError as e:
            print("HTTP", e.code, e.read().decode()[:200])
        except urllib.error.URLError as e:
            print("connection failed:", e.reason)
        n += 1
        if a.count == 0 or n < a.count:
            time.sleep(a.interval)


if __name__ == "__main__":
    main()
