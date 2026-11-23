"""End-to-end smoke checks against a RUNNING server (called by smoke_test.sh). Exits 1 on any failure.
Usage: python tests/smoke_e2e.py http://127.0.0.1:8791 [image.jpg]"""
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from simulator import Node  # noqa: E402

BASE = sys.argv[1]
IMAGE = sys.argv[2] if len(sys.argv) > 2 else None
SIM = {"X-Device-Id": "sim-01", "X-Device-Key": "demo-sim-key"}
fails = []


def req(method, path, body=None, headers=None, raw=False):
    data = body if raw else (json.dumps(body).encode() if body is not None else None)
    h = {"Content-Type": "image/jpeg" if raw else "application/json", **(headers or {})}
    r = urllib.request.Request(BASE + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            txt = resp.read().decode()
            return resp.status, (json.loads(txt) if txt[:1] in "{[" else txt)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        fails.append(name)


st, h = req("GET", "/api/v1/health")
check("health 200 + ok", st == 200 and h["status"] == "ok", h)

node = Node("sim-01", "DEMO-A1")
for _ in range(3):
    st, r = req("POST", "/api/v1/readings", node.step("normal"), SIM)
check("normal readings → ok/green", st == 200 and r["action"] == "ok" and r["led"] == "green", r)
st, c = req("POST", "/api/v1/devices/sim-01/calibration", {"use_latest": True, "tds_margin": 0.3})
check("calibrate from latest", st == 200 and c["tds_baseline_ppm"] and c["tds_margin"] == 0.3, c)

EXPECT = {"dry": ("irrigate", "MOIST_LOW", "red"), "wet": ("drain", "MOIST_HIGH", "amber"),
          "acidic": ("lime", "PH_LIME", "red"), "low_nutrient": ("fertilise", "TDS_LOW", "amber"),
          "over_fertilised": ("skip_fertiliser", "TDS_HIGH", "amber")}
for sc, (act, rule, led) in EXPECT.items():
    node = Node("sim-01", "DEMO-A1"); node.seq = 1000 * (list(EXPECT).index(sc) + 1)
    seen = None
    for _ in range(12):   # drift toward the scenario target
        st, r = req("POST", "/api/v1/readings", node.step(sc), SIM)
        if r.get("action") == act:
            seen = r
            break
    ok = bool(seen) and seen["actions"][0]["rule_id"] == rule and seen["led"] == led \
        and all(len(x) <= 16 for x in seen["oled"]) and len(seen["oled"]) == 2
    check(f"{sc} → {act}/{rule}/{led}", ok, seen or r)
    if ok and act in ("fertilise", "skip_fertiliser"):
        check(f"{sc} flagged simulated", seen["simulated"] is True)

node.seq = 9000
st, r = req("POST", "/api/v1/readings", node.step("sensor_fault"), SIM)
check("null pH → OK (partial), no fabricated value", r["oled"] == ["OK (partial)", "no pH reading"], r)

# idempotent repeat
p = node.step("normal")
_, a = req("POST", "/api/v1/readings", p, SIM)
_, b = req("POST", "/api/v1/readings", p, SIM)
check("repeat (device_id, seq) idempotent", a["evidence_id"] == b["evidence_id"] and b.get("duplicate"), b)

st, g = req("GET", "/api/v1/devices/sim-01/calibration", headers=SIM)
check("calibration GET as device", st == 200 and set(g) >= {"tds_baseline_ppm", "tds_margin", "updated_at"}, g)

# camera command queue
req("POST", "/api/v1/devices/cam-01/commands", {"cmd": "capture"})
CAM = {"X-Device-Id": "cam-01", "X-Device-Key": "demo-cam-key"}
_, c1 = req("GET", "/api/v1/devices/cam-01/commands", headers=CAM)
_, c2 = req("GET", "/api/v1/devices/cam-01/commands", headers=CAM)
check("command delivered once", c1.get("cmd") == "capture" and c2 == {"cmd": "none"}, (c1, c2))

st, m = req("GET", "/api/v1/meta")
model_ok = m["ripeness_model"].get("available", True) is not False
if IMAGE and model_ok:
    st, rp = req("POST", "/api/v1/infer/ripeness", Path(IMAGE).read_bytes(), CAM, raw=True)
    check("ripeness inference", st == 200 and rp["label"] in rp["probs"] and abs(sum(rp["probs"].values()) - 1) < 0.01, rp)
    if st == 200:
        print(f"     camera: {rp['label']} {rp['confidence']} | {rp['harvest_advice']} | {rp['evidence_id']}")
        hs, _ = req("GET", rp["heatmap_url"].replace("/static", "/static", 1))
        check("heat-map served", hs == 200)
else:
    st, rp = req("POST", "/api/v1/infer/ripeness", b"\xff\xd8\xff", CAM, raw=True)
    check("ripeness without model → 503 (or 400 bad image)", st in (503, 400) if not model_ok else st == 400, (st, rp))

st, l = req("GET", "/api/v1/latest")
check("latest shows sim-01", st == 200 and any(s["device_id"] == "sim-01" for s in l["soil"]), l if st != 200 else "")
st, v = req("GET", "/api/v1/evidence/verify")
check("evidence chain verified", st == 200 and v["ok"] is True, v)
print("     " + v.get("message", ""))
st, pack = req("GET", "/api/v1/evidence/export")
check("audit pack VERIFIED + head hash + clauses", st == 200 and "VERIFIED" in pack and v["head"] in pack and "4.5.4" in pack)
st, hp = req("GET", "/api/v1/harvest/plan?crew=30")
check("harvest plan", st == 200 and hp["available"] and sum(b["assigned_harvesters"] for b in hp["blocks"]) <= 30, hp)
print(f"     harvest: {hp['bunches_at_risk_total']} bunches at risk; " + ", ".join(f"{b['block_id']}:{b['assigned_harvesters']}" for b in hp["blocks"]))
st, sc = req("GET", "/api/v1/screening")
check("screening cascade", st == 200 and sc["available"], sc)
print("     satellite source:", sc["stage1_satellite"]["source"], "| flagged:", [b["block_id"] for b in sc["stage1_satellite"]["flagged"]])
for path in ("/", "/harvester", "/static/app.js", "/static/vendor/chart.umd.min.js"):
    st, _ = req("GET", path)
    check(f"GET {path} 200", st == 200)

print(f"\n{len(fails)} failure(s)" if fails else "\nSMOKE TEST PASSED (all assertions)")
sys.exit(1 if fails else 0)
