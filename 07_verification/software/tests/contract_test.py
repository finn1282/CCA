"""Independent black-box tests of the SawitSense backend against 00_lead/INTERFACES.md v0.2.6
(v0.2.2 age_s/captured_at; v0.2.3 ts validation, idempotent seq, NO DATA, 1-dp rounding; v0.2.4 seq-reuse rule;
v0.2.6 /latest = most recently captured non-buffered reading).

Written by SW Verification (07_verification/software). It does not import the app: it starts the real
server (uvicorn) on a private port with a throw-away runtime dir and talks HTTP only, then emulates the
firmware's ArduinoJson response parsing (02_hardware/firmware/*.ino) on the replies.

Run (from anywhere; PY = a python with 03_software/src/requirements.txt installed):
    $PY 07_verification/software/tests/contract_test.py [--port 8833] [--out results.txt]
Exit code 0 = no FAIL. Statuses: PASS, FAIL, OBS (contract met but noted), BLOCKED.
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SRC = REPO / "03_software" / "src"
SOIL = {"X-Device-Id": "soilnode-01", "X-Device-Key": "demo-soil-key"}
CAM = {"X-Device-Id": "cam-01", "X-Device-Key": "demo-cam-key"}
SIM = {"X-Device-Id": "sim-01", "X-Device-Key": "demo-sim-key"}
ACTIONS = ["ok", "irrigate", "drain", "lime", "fertilise", "skip_fertiliser", "watch"]
LED_OF = {"irrigate": "red", "lime": "red", "drain": "amber", "fertilise": "amber",
          "skip_fertiliser": "amber", "watch": "amber", "ok": "green"}

RESULTS: list[tuple[str, str, str, str]] = []
RESPONSES: list[dict] = []          # every /readings 200 body, for the global OLED/LED checks


def record(tid: str, status: str, desc: str, ev: str = "") -> None:
    RESULTS.append((tid, status, desc, ev))
    print(f"{status:7} {tid:7} {desc}  [{ev}]" if ev else f"{status:7} {tid:7} {desc}", flush=True)


def check(tid: str, desc: str, ok: bool, ev: str = "") -> bool:
    record(tid, "PASS" if ok else "FAIL", desc, ev)
    return ok


# ------------------------------------------------------------------ server + http
class Server:
    def __init__(self, py: str, port: int, env: dict):
        self.port, self.base = port, f"http://127.0.0.1:{port}"
        self.rt = tempfile.mkdtemp(prefix="sawit_ver_", dir=os.environ.get("TMPDIR"))
        e = {**os.environ, "SAWIT_RUNTIME_DIR": self.rt, "PYTHONDONTWRITEBYTECODE": "1", **env}
        self.p = subprocess.Popen([py, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", str(port),
                                   "--log-level", "warning"], cwd=SRC, env=e)
        for _ in range(100):
            try:
                if self.req("GET", "/api/v1/health")[0] == 200:
                    return
            except Exception:  # noqa: BLE001
                pass
            time.sleep(0.15)
        self.stop()
        raise RuntimeError("server did not start")

    @property
    def db(self) -> Path:
        return Path(self.rt) / "sawitsense.db"

    def req(self, method: str, path: str, body=None, headers=None, raw: bytes | None = None, ctype=None):
        h = dict(headers or {})
        data = None
        if raw is not None:
            data = raw
            h.setdefault("Content-Type", ctype or "image/jpeg")
        elif body is not None:
            data = body.encode() if isinstance(body, str) else json.dumps(body).encode()
            h.setdefault("Content-Type", "application/json")
        r = urllib.request.Request(self.base + path, data=data, method=method, headers=h)
        try:
            with urllib.request.urlopen(r, timeout=15) as resp:
                code, txt = resp.status, resp.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            code, txt = e.code, e.read().decode("utf-8", "replace")
        try:
            return code, json.loads(txt), txt
        except ValueError:
            return code, None, txt

    def stop(self) -> None:
        self.p.terminate()
        try:
            self.p.wait(5)
        except subprocess.TimeoutExpired:
            self.p.kill()


def reading(**kw) -> dict:
    base = {"device_id": "soilnode-01", "seq": 1, "ts": None, "buffered": False, "block_id": "DEMO-A1",
            "soil_moisture_pct": 50.0, "soil_ph": 5.0, "tds_ppm": 600, "ec_us_cm": None, "soil_temp_c": 27.8,
            "air_temp_c": 30.1, "air_rh_pct": 78.5, "rssi_dbm": -61, "cal_id": "2026-12-09", "fw_version": "0.2.0"}
    base.update(kw)
    return base


SEQ = [1000]


def post(s: Server, hdr=SOIL, **kw):
    SEQ[0] += 1
    kw.setdefault("seq", SEQ[0])
    kw.setdefault("device_id", hdr["X-Device-Id"])
    code, j, txt = s.req("POST", "/api/v1/readings", reading(**kw), hdr)
    if code == 200:
        RESPONSES.append(j)
    return code, j, txt


# ------------------------------------------------------------------ firmware emulation
def fw_soil_parse(txt: str) -> dict | None:
    """Python port of soil_node.ino applyCloudResponse() (ArduinoJson `|` defaults)."""
    try:
        d = json.loads(txt)
    except ValueError:
        return None
    s = lambda v, dflt: v if isinstance(v, str) else dflt  # noqa: E731
    a = s(d.get("action"), "")
    if not a:
        return None
    o = d.get("oled") if isinstance(d.get("oled"), list) else []
    l1 = s(o[0] if len(o) > 0 else None, "")
    l2 = s(o[1] if len(o) > 1 else None, "")
    if not l1:
        l1 = a.upper()
    if not l2:
        l2 = s(d.get("reason"), "")
    return {"source": "CLOUD", "line1": l1[:16], "line2": l2[:16], "led": s(d.get("led"), "amber"),
            "evidence": s(d.get("evidence_id"), ""), "raw_l1": l1, "raw_l2": l2}


def fw_cal_parse(txt: str, prev_b=float("nan"), prev_m=0.30):
    """Port of soil_node.ino fetchCalibration(): NAN default, keep previous unless valid."""
    d = json.loads(txt)
    num = lambda v: float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else float("nan")  # noqa: E731
    b, m = num(d.get("tds_baseline_ppm")), num(d.get("tds_margin"))
    if b == b and b > 0:
        prev_b = b
    if m == m and 0 < m < 1:
        prev_m = m
    return prev_b, prev_m


def r1(v):
    """soil_node.ino r1(): roundf(v*10)/10 (half away from zero), applied at capture (v0.2.3)."""
    import math
    return None if v is None else math.copysign(math.floor(abs(v) * 10 + 0.5), v) / 10


def fw_local(moist, ph, tds, base=float("nan"), margin=0.30):
    """Port of soil_node.ino localDecision() v0.2.3: rules on 1-dp rounded values; all-null -> NO DATA amber."""
    moist, ph, tds = r1(moist), r1(ph), r1(tds)
    if moist is None and ph is None and tds is None:
        return "ok", "amber", "NO DATA", "check sensors"
    best, act, led, l2 = 0, "ok", "green", "all in range"
    cand = []
    if moist is not None:
        if moist < 30: cand.append((4, "irrigate", "red", f"moist {moist:.0f}%<30%"))
        if moist > 80: cand.append((4, "drain", "amber", f"moist {moist:.0f}%>80%"))
    if ph is not None:
        if ph < 4.0: cand.append((3, "lime", "red", f"pH {ph:.1f}<4.0"))
        elif ph < 4.2: cand.append((1, "watch", "amber", f"pH {ph:.1f} 4.0-4.2"))
        elif ph > 6.5: cand.append((1, "watch", "amber", f"pH {ph:.1f}>6.5"))
    if tds is not None and base == base and base > 0:
        if tds < base * (1 - margin): cand.append((2, "fertilise", "amber", "TDS low (sim)"))
        if tds > base * (1 + margin): cand.append((2, "skip_fertiliser", "amber", "TDS high (sim)"))
    for p, a, c, w in cand:
        if p > best:
            best, act, led, l2 = p, a, c, w
    l1 = act.upper().replace("SKIP_FERTILISER", "SKIP FERTILISER")
    return act, led, l1[:16], l2[:16]


def fw_soil_json(seq, ts=None, moist=41.2, ph=5.4, tds=620, soil_t=27.8, air_t=30.1, rh=78.5, rssi=-61,
                 cal_id="uncalibrated", buffered=False, age_s=0) -> str:
    """Shape of soil_node.ino v0.2.3 toJson(): ArduinoJson key order; every value r1()-rounded at capture (1 dp)."""
    d = {"device_id": "soilnode-01", "seq": seq, "ts": ts, "buffered": buffered, "age_s": age_s,
         "block_id": "DEMO-A1", "soil_moisture_pct": r1(moist), "soil_ph": r1(ph), "tds_ppm": r1(tds), "ec_us_cm": None,
         "soil_temp_c": r1(soil_t), "air_temp_c": r1(air_t), "air_rh_pct": r1(rh),
         "rssi_dbm": rssi if rssi else None, "cal_id": cal_id, "fw_version": "0.2.3"}
    return json.dumps(d, separators=(",", ":"))


D2 = REPO / "03_software" / "data" / "raw" / "d2"


def cam_jpeg(src: Path | None = None, size=(800, 600), q=85) -> bytes:
    """An ESP32-CAM-like frame (SVGA JPEG) made from a local D2 test image (no download, D43)."""
    from PIL import Image
    src = src or next(iter(sorted((D2 / "FFBtest" / "TestRipe").glob("*"))), None)
    if src is None:
        return jpeg_bytes()
    im = Image.open(src).convert("RGB")
    im.thumbnail((size[0] * 2, size[1] * 2))
    w, h = im.size
    t = size[0] / size[1]
    cw, ch = (int(h * t), h) if w / h > t else (w, int(w / t))
    im = im.crop(((w - cw) // 2, (h - ch) // 2, (w - cw) // 2 + cw, (h - ch) // 2 + ch)).resize(size)
    b = io.BytesIO(); im.save(b, "JPEG", quality=q)
    return b.getvalue()


def jpeg_bytes() -> bytes:
    try:
        from PIL import Image
        b = io.BytesIO()
        Image.new("RGB", (64, 48), (200, 80, 30)).save(b, "JPEG")
        return b.getvalue()
    except ImportError:  # minimal fallback: JPEG SOI/EOI markers only
        return b"\xff\xd8\xff\xe0" + b"\x00" * 64 + b"\xff\xd9"


# ------------------------------------------------------------------ test groups
def t_health_meta(s):
    c, j, _ = s.req("GET", "/api/v1/health")
    check("BE-01", "GET /health 200 status ok", c == 200 and j.get("status") == "ok", f"{c} {j}")
    c, j, _ = s.req("GET", "/api/v1/meta")
    t = j["thresholds"]
    check("BE-02", "meta thresholds equal §4 (30/80, 4.0/4.2/6.5, margin 0.30)",
          (t["moisture_low"], t["moisture_high"], t["ph_lime"], t["ph_watch_top"], t["ph_high"], t["tds_default_margin"])
          == (30.0, 80.0, 4.0, 4.2, 6.5, 0.30), json.dumps(t))
    check("BE-03", "meta action vocabulary == §4 set", sorted(j["actions"]) == sorted(ACTIONS), str(j["actions"]))


def t_auth(s):
    r = reading()
    c, *_ = s.req("POST", "/api/v1/readings", r, {})
    check("AU-01", "POST /readings without headers -> 401", c == 401, str(c))
    c, *_ = s.req("POST", "/api/v1/readings", r, {"X-Device-Id": "soilnode-01"})
    check("AU-02", "X-Device-Id without X-Device-Key -> 401", c == 401, str(c))
    c, *_ = s.req("POST", "/api/v1/readings", r, {"X-Device-Id": "soilnode-01", "X-Device-Key": "wrong"})
    check("AU-03", "wrong X-Device-Key -> 401", c == 401, str(c))
    c, *_ = s.req("POST", "/api/v1/readings", {**r, "device_id": "rogue-9"}, {"X-Device-Id": "rogue-9", "X-Device-Key": "x"})
    check("AU-04", "unknown device id -> 401", c == 401, str(c))
    c, *_ = s.req("POST", "/api/v1/readings", {**r, "device_id": "soilnode-02"}, SOIL)
    check("AU-05", "body device_id != X-Device-Id -> 400", c == 400, str(c))
    c, *_ = s.req("POST", "/api/v1/readings", {**r, "device_id": "cam-01"}, CAM)
    record("AU-06", "OBS", "camera key accepted on /readings (keys not scoped per endpoint/device type)", f"{c}")


def t_validation(s):
    for tid, kw, desc in [("VA-01", {"soil_moisture_pct": 100.1}, "moisture 100.1"),
                          ("VA-02", {"soil_moisture_pct": -0.1}, "moisture -0.1"),
                          ("VA-03", {"soil_ph": 14.01}, "pH 14.01"),
                          ("VA-04", {"tds_ppm": -1}, "tds -1"),
                          ("VA-05", {"soil_moisture_pct": "wet"}, "moisture as string"),
                          ("VA-06", {"seq": "abc"}, "seq as string")]:
        c, *_ = s.req("POST", "/api/v1/readings", reading(**kw), SOIL)
        check(tid, f"invalid {desc} -> 422", c == 422, str(c))
    r = reading(); r.pop("device_id")
    c, *_ = s.req("POST", "/api/v1/readings", r, SOIL)
    check("VA-07", "missing device_id -> 422", c == 422, str(c))
    c, *_ = s.req("POST", "/api/v1/readings", "{not json", SOIL)
    check("VA-08", "malformed JSON -> 422", c == 422, str(c))
    bad = []
    for tsv in ("not-a-timestamp", "2026-11-20T09:00:00", "2099-01-01T00:00:00Z"):
        c, j, _ = post(s, hdr=SIM, ts=tsv)
        inp = s.req("GET", f"/api/v1/evidence/{j['evidence_id']}")[1]["record"]["input"] if c == 200 else {}
        if not (c == 200 and j["captured_at"] == j["received_at"] and inp.get("ts") is None):
            bad.append((tsv, c, j and j.get("captured_at"), inp.get("ts")))
    c, j, _ = post(s, hdr=SIM, ts="2026-11-01T10:00:00+08:00")
    check("VA-09", "v0.2.3 (S-03 retest): garbage / naive / >24 h-future ts treated as null (captured_at=received_at); "
          "+08:00 normalised to Z", not bad and j["captured_at"] == "2026-11-01T02:00:00Z", f"{bad} {j['captured_at']}")
    c, *_ = post(s, age_s=-1)
    check("VA-13", "age_s -1 -> 422 (v0.2.2: int >= 0)", c == 422, str(c))
    c, j, _ = post(s, soil_moisture_pct=0, soil_ph=0, tds_ppm=0)
    check("VA-10", "edge-valid values 0/0/0 accepted (200)", c == 200, str(c))
    c, j, _ = post(s, soil_moisture_pct=100, soil_ph=14)
    check("VA-11", "edge-valid moisture 100, pH 14 accepted (200)", c == 200, str(c))
    r = {k: v for k, v in reading().items() if k in ("device_id",)}
    c, j, _ = s.req("POST", "/api/v1/readings", r, SOIL)
    check("VA-12", "minimal body (device_id only) accepted, treated as all-null", c == 200 and j["oled"][0] == "NO DATA", f"{c} {j and j.get('oled')}")


def t_thresholds(s):
    cases = [  # tid, kwargs, action, rule_id, led
        ("TH-01", {"soil_moisture_pct": 29.9}, "irrigate", "MOIST_LOW", "red"),
        ("TH-02", {"soil_moisture_pct": 30.0}, "ok", "ALL_OK", "green"),
        ("TH-03", {"soil_moisture_pct": 80.0}, "ok", "ALL_OK", "green"),
        ("TH-04", {"soil_moisture_pct": 80.1}, "drain", "MOIST_HIGH", "amber"),
        ("TH-05", {"soil_ph": 3.99}, "lime", "PH_LIME", "red"),
        ("TH-06", {"soil_ph": 4.0}, "watch", "PH_LOW_WATCH", "amber"),
        ("TH-07", {"soil_ph": 4.19}, "watch", "PH_LOW_WATCH", "amber"),
        ("TH-08", {"soil_ph": 4.2}, "ok", "ALL_OK", "green"),
        ("TH-09", {"soil_ph": 6.5}, "ok", "ALL_OK", "green"),
        ("TH-10", {"soil_ph": 6.51}, "watch", "PH_HIGH", "amber"),
    ]
    for tid, kw, act, rid, led in cases:
        c, j, _ = post(s, **kw)
        check(tid, f"{kw} -> {act}/{rid}/{led}",
              c == 200 and j["action"] == act and j["actions"][0]["rule_id"] == rid and j["led"] == led,
              f"{c} {j and (j['action'], j['actions'][0]['rule_id'], j['led'], j['oled'])}")
    c, j, _ = post(s, soil_ph=5.6)
    check("TH-11", "pH 5.6 -> ok with 'above typical oil-palm band, not harmful' note",
          j["action"] == "ok" and "above the typical" in j["reason"], j["reason"])
    # TDS: no baseline yet
    c, j, _ = post(s, tds_ppm=50)
    check("TH-12", "TDS rules skipped before calibration (note, no fertilise)",
          j["action"] == "ok" and "not calibrated" in j["reason"], j["reason"])
    c, j, _ = s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 600, "tds_margin": 0.30})
    for tid, tds, act, rid, sim in [("TH-13", 419, "fertilise", "TDS_LOW", True), ("TH-14", 420, "ok", "ALL_OK", False),
                                    ("TH-15", 780, "ok", "ALL_OK", False), ("TH-16", 781, "skip_fertiliser", "TDS_HIGH", True)]:
        c, j, _ = post(s, tds_ppm=tds)
        check(tid, f"baseline 600 ±30%: TDS {tds} -> {act}/{rid}, simulated={sim}, led amber/green",
              j["action"] == act and j["actions"][0]["rule_id"] == rid and j["simulated"] is sim and j["led"] == LED_OF[act],
              f"{j['action']} {j['actions'][0]['rule_id']} sim={j['simulated']} {j['oled']}")
    s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 1000, "tds_margin": 0.10})
    c, j1, _ = post(s, tds_ppm=899)
    c, j2, _ = post(s, tds_ppm=900)
    c, j3, _ = post(s, tds_ppm=1101)
    check("TH-17", "custom margin 0.10 on baseline 1000: 899 fertilise, 900 ok, 1101 skip",
          (j1["action"], j2["action"], j3["action"]) == ("fertilise", "ok", "skip_fertiliser"),
          f"{j1['action']},{j2['action']},{j3['action']}")
    s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 600, "tds_margin": 0.30})


def t_priority(s):
    c, j, _ = post(s, soil_moisture_pct=20, soil_ph=3.5, tds_ppm=300)
    check("PR-01", "moist 20 + pH 3.5 + TDS low -> irrigate; actions[] ordered irrigate>lime>fertilise",
          j["action"] == "irrigate" and [a["action"] for a in j["actions"]] == ["irrigate", "lime", "fertilise"],
          str([a["action"] for a in j["actions"]]))
    record("PR-02", "OBS", "simulated=true when TDS finding is present even though primary action is irrigate "
           "(contract: 'whenever the decision uses simulated agronomy' — acceptable, conservative)", f"simulated={j['simulated']}")
    c, j, _ = post(s, soil_ph=3.5, tds_ppm=900)
    check("PR-03", "pH 3.5 + TDS high -> lime > skip_fertiliser", [a["action"] for a in j["actions"]] == ["lime", "skip_fertiliser"],
          str([a["action"] for a in j["actions"]]))
    c, j, _ = post(s, soil_ph=4.1, tds_ppm=300)
    check("PR-04", "pH 4.1 + TDS low -> fertilise > watch, simulated=true",
          [a["action"] for a in j["actions"]] == ["fertilise", "watch"] and j["simulated"] is True,
          str([a["action"] for a in j["actions"]]))
    c, j, _ = post(s, soil_moisture_pct=85, soil_ph=3.5)
    check("PR-05", "moist 85 + pH 3.5 -> drain > lime (led amber per §4 drain row)",
          j["action"] == "drain" and j["actions"][1]["action"] == "lime" and j["led"] == "amber", f"{j['action']} {j['led']}")
    c, j, _ = post(s, soil_ph=6.9, tds_ppm=900)
    check("PR-06", "pH 6.9 + TDS high -> skip_fertiliser > watch(PH_HIGH)",
          [a["rule_id"] for a in j["actions"]] == ["TDS_HIGH", "PH_HIGH"], str([a["rule_id"] for a in j["actions"]]))
    c, j, _ = post(s, soil_moisture_pct=20)
    check("PR-07", "non-ok response has counterfactual + confidence in [0,1]",
          j["counterfactual"].startswith("Would be OK if") and 0 <= j["confidence"] <= 1, f"{j['counterfactual']!r} {j['confidence']}")
    c, j, _ = post(s, soil_moisture_pct=20)
    check("PR-08", "simulated=false for irrigate without TDS finding", j["simulated"] is False, str(j["simulated"]))


def t_nulls_ec(s):
    c, j, _ = post(s, soil_ph=None)
    ok = j["action"] == "ok" and j["oled"] == ["OK (partial)", "no pH reading"]
    inp = s.req("GET", f"/api/v1/evidence/{j['evidence_id']}")[1]["record"]["input"]
    check("NU-01", "pH null -> no pH rule, OLED 'OK (partial)/no pH reading', stored as null (not fabricated)",
          ok and "soil_ph" in inp and inp["soil_ph"] is None, f"{j['oled']} stored={inp.get('soil_ph')}")
    c, j, _ = post(s, soil_moisture_pct=None, soil_ph=None, tds_ppm=None)
    check("NU-02", "all sensors null -> ok/NO DATA/check sensors, led amber",
          j["action"] == "ok" and j["oled"] == ["NO DATA", "check sensors"] and j["led"] == "amber", f"{j['oled']} {j['led']}")
    c, j, _ = post(s, soil_moisture_pct=None, soil_ph=3.5)
    check("NU-03", "moisture null + pH 3.5 -> other rules still fire (lime)", j["action"] == "lime", j["action"])
    c, j, _ = post(s, soil_moisture_pct=None, soil_ph=None)
    record("NU-04", "OBS", "two sensors null: OLED line 2 names only the first missing sensor", str(j["oled"]))
    c, j, _ = post(s, soil_temp_c=None, air_temp_c=None, air_rh_pct=None, rssi_dbm=None)
    check("NU-05", "null temperature/RH/rssi accepted, decision unaffected", c == 200 and j["action"] == "ok", f"{c} {j['action']}")
    c, j, _ = post(s, tds_ppm=620, ec_us_cm=None)
    ev = s.req("GET", f"/api/v1/evidence/{j['evidence_id']}")[1]
    inp = ev["record"]["input"]
    check("EC-01", "ec null + TDS 620 -> derived EC 1240, flagged ec_derived=true (approximate)",
          inp["ec_us_cm"] == 1240.0 and inp["ec_derived"] is True, f"{inp['ec_us_cm']} {inp['ec_derived']}")
    c, j, _ = post(s, tds_ppm=620, ec_us_cm=900)
    inp = s.req("GET", f"/api/v1/evidence/{j['evidence_id']}")[1]["record"]["input"]
    check("EC-02", "ec supplied -> kept, ec_derived=false", inp["ec_us_cm"] == 900 and inp["ec_derived"] is False, str(inp["ec_us_cm"]))
    js = s.req("GET", "/static/app.js")[2]
    check("EC-03", "S-13 retest: EC tile labelled '≈TDS/0.5' only when ec_derived", 'k === "ec_us_cm" && s.reading.ec_derived' in js, "")


def t_oled_led_extremes(s):
    s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 1, "tds_margin": 0.30})
    post(s, soil_moisture_pct=0, soil_ph=0, tds_ppm=99999)
    post(s, soil_moisture_pct=100, soil_ph=14, tds_ppm=0)
    s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 99999, "tds_margin": 0.30})
    post(s, soil_moisture_pct=50, soil_ph=5, tds_ppm=1)
    post(s, soil_moisture_pct=50, soil_ph=5, tds_ppm=12345)
    s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 600, "tds_margin": 0.30})
    bad_len = [r["oled"] for r in RESPONSES if not (isinstance(r["oled"], list) and len(r["oled"]) == 2
                                                    and all(isinstance(x, str) and 0 < len(x) <= 16 for x in r["oled"]))]
    check("OL-01", f"all {len(RESPONSES)} /readings replies: oled = 2 non-empty strings ≤16 chars", not bad_len, str(bad_len[:3]))
    bad_led = [(r["action"], r["led"]) for r in RESPONSES if r["led"] not in ("green", "amber", "red")]
    check("OL-02", "all replies: led ∈ {green, amber, red}", not bad_led, str(bad_led[:3]))
    mism = [(r["action"], r["led"], r["oled"]) for r in RESPONSES
            if r["led"] != LED_OF[r["action"]] and r["oled"][0] != "NO DATA"]
    check("OL-03", "led matches §4 table for the primary action (NO DATA excepted)", not mism, str(mism[:3]))
    am = [r for r in RESPONSES if r["action"] != r["actions"][0]["action"]]
    check("OL-04", "action == actions[0].action (highest priority) in every reply", not am, str(len(am)))
    voc = [r["action"] for r in RESPONSES if r["action"] not in ACTIONS or any(a["action"] not in ACTIONS for a in r["actions"])]
    check("OL-05", "only §4 action vocabulary used", not voc, str(voc[:3]))
    keys = {"action", "reason", "confidence", "actions", "counterfactual", "simulated", "evidence_id", "oled", "led"}
    miss = [sorted(keys - set(r)) for r in RESPONSES if not keys <= set(r)]
    check("OL-06", "every reply carries all §2 response fields", not miss, str(miss[:1]))
    trunc = [r["oled"][1] for r in RESPONSES if len(r["oled"][1]) == 16]
    record("OL-07", "OBS" if trunc else "PASS", "OLED line 2 hard-truncated at 16 chars for extreme values (may cut text)", str(trunc[:3]))
    l1 = sorted({r["oled"][0] for r in RESPONSES})
    check("OL-08", "CLOUD line 1 matches firmware LOCAL wording (no underscores, e.g. 'SKIP FERTILISER')",
          not any("_" in x for x in l1), str(l1))


def t_replay(s):
    c, j, _ = post(s, seq=5000, soil_moisture_pct=55.0)
    live_ev = j["evidence_id"]
    c, j, _ = post(s, seq=4990, buffered=True, soil_moisture_pct=22.0, ts="2026-11-20T08:50:00Z")
    check("RP-01", "buffered replay (buffered=true, older seq) accepted 200", c == 200, str(c))
    _, rows, _ = s.req("GET", "/api/v1/readings?device_id=soilnode-01&limit=2000")
    r4990 = [r for r in rows if r["seq"] == 4990]
    check("RP-02", "replayed row stored with buffered=true and its device ts", r4990 and r4990[0]["buffered"] is True
          and r4990[0]["ts"] == "2026-11-20T08:50:00Z", str(r4990[:1] and {k: r4990[0][k] for k in ("seq", "buffered", "ts")}))
    _, l, _ = s.req("GET", "/api/v1/latest")
    soil = [x for x in l["soil"] if x["device_id"] == "soilnode-01"][0]
    check("RP-03", "/latest (dashboard 'live' panel) still shows the live seq 5000 after an older buffered replay arrives",
          soil["seq"] == 5000, f"latest seq={soil['seq']} action={soil['recommendation']['action']} (live was seq 5000 ok, ev {live_ev})")
    cap = [r["captured_at"] for r in rows]
    check("RP-04", "/readings history (dashboard chart) ordered by captured_at, replay placed at its true time",
          cap == sorted(cap), str([(r["seq"], r["captured_at"][11:19]) for r in rows]))
    c, j, _ = post(s, seq=5001, age_s=120, ts=None, buffered=True)
    rec_at, cap_at = j["received_at"], j["captured_at"]
    from datetime import datetime as _dt
    dt = (_dt.fromisoformat(rec_at.replace("Z", "+00:00")) - _dt.fromisoformat(cap_at.replace("Z", "+00:00"))).total_seconds()
    check("RP-07", "v0.2.2: ts null + age_s 120 -> captured_at = received_at - 120 s", dt == 120, f"{rec_at} - {cap_at} = {dt}")
    c, j, _ = post(s, seq=5002, age_s=999, ts="2026-11-20T09:00:00Z")
    check("RP-08", "ts present -> captured_at = ts (age_s ignored)", j["captured_at"] == "2026-11-20T09:00:00Z", j["captured_at"])
    _, l, _ = s.req("GET", "/api/v1/latest")
    soil = [x for x in l["soil"] if x["device_id"] == "soilnode-01"][0]
    c, j, _ = post(s, seq=3, soil_moisture_pct=33.3)        # device rebooted: seq restarts low, fresh capture
    _, l, _ = s.req("GET", "/api/v1/latest")
    soil = [x for x in l["soil"] if x["device_id"] == "soilnode-01"][0]
    check("RP-09", "v0.2.6 (D-04/D-16): /latest = most recently captured non-buffered row (old-ts row 5002 and replays "
          "ignored; robust to seq reset)", soil["seq"] == 3 and soil["buffered"] is False and soil["reading"]["soil_moisture_pct"] == 33.3,
          f"seq={soil['seq']} buffered={soil['buffered']}")
    _, ev0, _ = s.req("GET", "/api/v1/evidence?limit=1000")
    c1, j1, _ = s.req("POST", "/api/v1/readings", reading(seq=6000), SOIL)
    c2, j2, _ = s.req("POST", "/api/v1/readings", reading(seq=6000), SOIL)
    _, ev1, _ = s.req("GET", "/api/v1/evidence?limit=1000")
    check("RP-05", "v0.2.4 (S-06 retest): identical (device_id, seq) re-POST -> original response, duplicate flag, no new evidence",
          j2["evidence_id"] == j1["evidence_id"] and j2.get("duplicate") is True and len(ev1) == len(ev0) + 1,
          f"{j1['evidence_id']} / {j2['evidence_id']} dup={j2.get('duplicate')} evidence +{len(ev1) - len(ev0)}")
    c3, j3, _ = s.req("POST", "/api/v1/readings", reading(seq=6000, soil_moisture_pct=21.0), SOIL)
    check("RP-10", "v0.2.4: same seq with different values (seq reset after reboot) -> stored as new reading",
          j3["evidence_id"] != j1["evidence_id"] and j3["action"] == "irrigate" and not j3.get("duplicate"), f"{j3['evidence_id']} {j3['action']}")
    c4, j4, _ = s.req("POST", "/api/v1/readings", reading(seq=6000, soil_moisture_pct=21.0, air_temp_c=35.5, buffered=True), SOIL)
    record("RP-11", "OBS", "duplicate test compares only moisture/pH/TDS/soil-temp: same seq with a different air temp / "
           "buffered flag is treated as a duplicate (acceptable for retries)", f"dup={j4.get('duplicate')}")
    check("RP-06", "ts null -> server stamps received_at in reply", isinstance(j2.get("received_at"), str) and j2["received_at"].endswith("Z"),
          str(j2.get("received_at")))


def t_calibration(s):
    p = "/api/v1/devices/sim-01/calibration"
    c, j, _ = s.req("GET", p, headers=SIM)
    check("CA-01", "GET calibration (device) before any set -> baseline null, margin 0.30, updated_at key present",
          c == 200 and j["tds_baseline_ppm"] is None and j["tds_margin"] == 0.30 and "updated_at" in j, f"{c} {j}")
    c, j, _ = s.req("POST", "/api/v1/devices/soilnode-99/calibration", {"use_latest": True})
    check("CA-02", "POST use_latest for a device with no reading -> 409", c == 409, str(c))
    for tid, body in [("CA-03", {"tds_baseline_ppm": 0}), ("CA-04", {"tds_baseline_ppm": -5}),
                      ("CA-05", {"tds_baseline_ppm": 600, "tds_margin": 0}), ("CA-06", {"tds_baseline_ppm": 600, "tds_margin": 1}),
                      ("CA-07", {})]:
        c, *_ = s.req("POST", p, body)
        check(tid, f"POST {body} rejected 422", c == 422, str(c))
    c, j, _ = s.req("POST", p, {"tds_baseline_ppm": 592, "tds_margin": 0.25, "cal_id": "2026-12-09"})
    check("CA-08", "POST baseline 592 / 0.25 -> echoes v0.2.1 body", c == 200 and j["tds_baseline_ppm"] == 592 and j["tds_margin"] == 0.25
          and j["updated_at"], f"{c} {j}")
    c, j, txt = s.req("GET", p, headers=SIM)
    b, m = fw_cal_parse(txt)
    check("CA-09", "GET as device returns stored values; firmware parser caches baseline 592, margin 0.25", (b, m) == (592.0, 0.25), f"{j}")
    c, *_ = s.req("GET", p, headers=SOIL)
    check("CA-10", "GET another device's calibration with own creds -> 401", c == 401, str(c))
    c, *_ = s.req("GET", p, headers={"X-Device-Id": "sim-01", "X-Device-Key": "bad"})
    check("CA-11", "GET with wrong key -> 401", c == 401, str(c))
    c, *_ = s.req("GET", p)
    check("CA-12", "GET without device headers (dashboard, open/local mode) -> 200", c == 200, str(c))
    post(s, hdr=SIM, tds_ppm=640)
    c, j, _ = s.req("POST", p, {"use_latest": True, "tds_margin": 0.3})
    check("CA-13", "POST use_latest takes the last TDS reading (640)", c == 200 and j["tds_baseline_ppm"] == 640, str(j))
    c, j, _ = s.req("POST", p, {"tds_baseline_ppm": None, "tds_margin": 0.3})
    record("CA-14", "OBS", "baseline cannot be cleared back to null via POST (contract allows number|null)", f"{c}")
    _, ev, _ = s.req("GET", "/api/v1/evidence?kind=calibration&limit=5")
    check("CA-15", "each calibration change logged in evidence chain", len(ev) >= 2, f"{len(ev)} calibration records")
    c, j, txt = s.req("GET", "/api/v1/devices/never-seen/calibration")
    b, m = fw_cal_parse(txt, prev_b=555.0, prev_m=0.3)
    check("CA-16", "firmware keeps its cached baseline when backend returns null", b == 555.0, f"{j}")


def t_commands(s):
    p = "/api/v1/devices/cam-01/commands"
    c, j, txt = s.req("GET", p, headers=CAM)
    check("CM-01", "camera poll with empty queue -> 200 {cmd:none}; firmware ignores", c == 200 and j["cmd"] == "none", txt)
    c, j, _ = s.req("POST", p, {"cmd": "capture"})
    check("CM-02", "dashboard POST capture -> queued", c == 200 and j["queued"] is True, str(j))
    c, j, _ = s.req("GET", p, headers=CAM)
    c2, j2, _ = s.req("GET", p, headers=CAM)
    check("CM-03", "poll returns capture once, then none (consumed)", j["cmd"] == "capture" and j2["cmd"] == "none", f"{j} {j2}")
    r1 = s.req("POST", p, {"cmd": "capture"})[1]; r2 = s.req("POST", p, {"cmd": "capture"})[1]
    a, b, cc = (s.req("GET", p, headers=CAM)[1]["cmd"] for _ in range(3))
    check("CM-04", "S-07 retest: repeated Capture clicks coalesce into one pending capture", (a, b, cc) == ("capture", "none", "none")
          and r2.get("coalesced") is True, f"{a},{b},{cc} coalesced={r2.get('coalesced')}")
    s.req("POST", p, {"cmd": "capture"})
    con = sqlite3.connect(s.db); con.execute("UPDATE commands SET created_at='2026-01-01T00:00:00Z' WHERE consumed_at IS NULL"); con.commit(); con.close()
    cmd = s.req("GET", p, headers=CAM)[1]["cmd"]
    check("CM-08", "S-07 retest: a capture older than 60 s expires instead of firing late", cmd == "none", cmd)
    c, *_ = s.req("POST", p, {"cmd": "reboot"})
    check("CM-05", "unknown command 'reboot' -> 422", c == 422, str(c))
    c, *_ = s.req("GET", p, headers=SOIL)
    check("CM-06", "soil node polling camera's queue -> 403", c == 403, str(c))
    c, *_ = s.req("GET", p)
    check("CM-07", "poll without device headers -> 401", c == 401, str(c))


def t_ripeness(s):
    import statistics
    import threading
    p = "/api/v1/infer/ripeness"
    c, *_ = s.req("POST", p, raw=jpeg_bytes())
    check("RI-01", "ripeness without device headers -> 401", c == 401, str(c))
    c, *_ = s.req("POST", p, raw=b"", headers=CAM)
    check("RI-02", "empty body -> 400", c == 400, str(c))
    c, *_ = s.req("POST", p, raw=b"\xff" * 5_000_001, headers=CAM)
    check("RI-03", "body > 5 MB -> 413", c == 413, str(c))
    img = cam_jpeg()
    t0 = time.perf_counter()
    c, j, txt = s.req("POST", p, raw=img, headers=CAM)
    cold = time.perf_counter() - t0
    if c == 503:
        check("RI-04", "model absent -> 503 with clear message", "not found" in txt, txt[:120])
        for tid in ("RI-05", "RI-06", "RI-07", "RI-08", "RI-09", "RI-10", "RI-11"):
            record(tid, "BLOCKED", "needs M1 model", "503")
        return
    check("RI-04", f"model loaded: SVGA JPEG ({len(img) // 1024} KB) from D2 test -> 200 (cold {cold:.2f} s incl. model load)",
          c == 200, f"{c} {j and j.get('model_version')}")
    classes = ["unripe", "underripe", "ripe", "overripe"]
    keys = ["label", "confidence", "probs", "harvest_advice", "explanation", "heatmap_url", "model_version", "evidence_id"]
    ok = (all(k in j for k in keys) and j["label"] in classes and isinstance(j["confidence"], float) and 0 <= j["confidence"] <= 1
          and sorted(j["probs"]) == sorted(classes) and abs(sum(j["probs"].values()) - 1) < 0.01
          and abs(j["probs"][j["label"]] - j["confidence"]) < 1e-6 and j["label"] == max(j["probs"], key=j["probs"].get)
          and isinstance(j["harvest_advice"], str) and j["harvest_advice"] and isinstance(j["explanation"], str) and j["explanation"]
          and j["evidence_id"].startswith("ev_") and j["heatmap_url"] == f"/static/heatmaps/{j['evidence_id']}.png")
    check("RI-05", "§3 response: all 8 fields, types, 4-class probs sum to 1, label=argmax=confidence, heatmap named by evidence_id",
          ok, json.dumps({k: j.get(k) for k in ("label", "confidence", "probs", "heatmap_url", "model_version")}))
    hc, _, _ = s.req("GET", j["heatmap_url"])
    raw = urllib.request.urlopen(s.base + j["heatmap_url"], timeout=10).read()
    from PIL import Image
    hm = Image.open(io.BytesIO(raw))
    ic = s.req("GET", j["image_url"])[0]
    check("RI-06", "heat-map PNG served (image | overlay side by side, 448x224) + uploaded image served",
          hc == 200 and raw[:8] == b"\x89PNG\r\n\x1a\n" and hm.size == (448, 224) and ic == 200, f"{hc} {hm.size} img {ic}")
    c, _, txt = s.req("POST", p, raw=b"this is not a jpeg", headers=CAM)
    check("RI-07", "non-image body -> 400 with message", c == 400 and "decodable" in txt, f"{c} {txt[:80]}")
    d = json.loads(json.dumps(j))
    label, conf, adv, ev = d.get("label", "?"), float(d.get("confidence", 0.0)), d.get("harvest_advice", ""), d.get("evidence_id", "")
    check("RI-08", "cam_node captureAndUpload() parse: label/confidence/harvest_advice/evidence_id typed as the firmware reads them",
          isinstance(label, str) and label != "?" and conf > 0 and adv and ev, f"lastResult='{label} ({conf:.2f}) {adv} {ev} [LAN]'")
    lat = []
    for _ in range(10):
        t0 = time.perf_counter(); s.req("POST", p, raw=img, headers=CAM); lat.append(time.perf_counter() - t0)
    lat.sort()
    p50, p95 = statistics.median(lat), lat[int(0.95 * (len(lat) - 1))]
    check("RI-09", "warm CPU latency over 10 SVGA uploads: p95 < 2 s (live demo budget)", p95 < 2.0, f"p50 {p50:.3f} s, p95 {p95:.3f} s, max {lat[-1]:.3f} s")
    _, l, _ = s.req("GET", "/api/v1/latest")
    c1, *_ = s.req("POST", f"/api/v1/evidence/{j['evidence_id']}/review", {"decision": "override", "override_action": "overripe"})
    c2, *_ = s.req("POST", f"/api/v1/evidence/{j['evidence_id']}/review", {"decision": "override", "override_action": "irrigate"})
    check("RI-10", "ripeness evidence on /latest; override to a ripeness class 200, to a soil action 422 (S-04 retest)",
          l["ripeness"] and l["ripeness"]["evidence_id"].startswith("ev_") and (c1, c2) == (200, 422), f"{c1}/{c2}")
    _, h, _ = s.req("GET", "/api/v1/health")
    check("RI-11", "/health exposes the model_version (provisional build is labelled '-provisional')",
          h["ripeness_model"] == j["model_version"] and "provisional" in j["model_version"], str(h["ripeness_model"]))
    record("RI-12", "OBS", "provisional model still outputs an 'underripe' probability although D2 has no underripe images "
           "(column untrained; final D1 model fixes this)", f"p(underripe)={j['probs']['underripe']}")
    # soil POST latency while ripeness inference holds the global DB lock
    soil_lat = []
    def soil():
        t0 = time.perf_counter(); post(s); soil_lat.append(time.perf_counter() - t0)
    ths = [threading.Thread(target=lambda: s.req("POST", p, raw=img, headers=CAM)) for _ in range(3)]
    for t in ths: t.start()
    time.sleep(0.05); soil()
    for t in ths: t.join()
    record("RI-13", "OBS" if soil_lat[0] > 0.5 else "PASS", "soil POST while 3 ripeness inferences run (inference runs inside db._lock)",
           f"soil reply {soil_lat[0]:.2f} s (alone ≈0.01 s)")
    big = next(iter(sorted((D2 / "FFBtest" / "TestRipe").glob("*"), key=lambda x: -x.stat().st_size)), None)
    if big:
        c, j2, _ = s.req("POST", p, raw=big.read_bytes(), headers=CAM)
        record("RI-14", "PASS" if c in (200, 413) else "FAIL", f"full-size D2 original ({big.stat().st_size // 1024} KB) -> 200 or 413",
               f"{c} {j2 and j2.get('label')}")


def t_evidence(s, tamper: bool):
    _, rows, _ = s.req("GET", "/api/v1/evidence?limit=1000")
    n = len(rows)
    c, v, _ = s.req("GET", "/api/v1/evidence/verify")
    check("EV-01", f"verify chain intact over {n} records", v["ok"] and v["checked"] == n, v["message"])
    e = rows[-1]
    ok = all(re.fullmatch(r"[0-9a-f]{64}", x["hash"]) for x in rows) and all(rows[i]["prev_hash"] == rows[i + 1]["hash"]
                                                                          for i in range(len(rows) - 1))
    check("EV-02", "records linked: prev_hash(n) == hash(n-1), SHA-256 hex", ok and e["prev_hash"] == "0" * 64, "")
    c, j, _ = post(s, soil_moisture_pct=20)
    c, ev, _ = s.req("GET", f"/api/v1/evidence/{j['evidence_id']}")
    check("EV-03", "GET evidence/{id} of a reading -> input, output, calibration, mspo, rules_version",
          c == 200 and ev["record"]["output"]["action"] == "irrigate" and ev["record"]["input"]["soil_moisture_pct"] == 20
          and ev["mspo"] and ev["record"]["rules_version"].startswith("INTERFACES-v0.2"), f"{c} {ev['record'].get('rules_version')} mspo={ev.get('mspo')}")
    c, *_ = s.req("GET", "/api/v1/evidence/ev_999999")
    check("EV-04", "unknown evidence id -> 404", c == 404, str(c))
    c, r, _ = s.req("POST", f"/api/v1/evidence/{j['evidence_id']}/review", {"decision": "approve", "by": "tester", "note": "ok"})
    check("EV-05", "review approve -> new evidence record referencing target", c == 200 and r["target"] == j["evidence_id"], str(c))
    c, *_ = s.req("POST", f"/api/v1/evidence/{j['evidence_id']}/review", {"decision": "override"})
    check("EV-06", "override without override_action -> 422", c == 422, str(c))
    c, r, _ = s.req("POST", f"/api/v1/evidence/{j['evidence_id']}/review", {"decision": "override", "override_action": "banana"})
    check("EV-07", "override_action outside §4 vocabulary rejected (422)", c == 422, f"{c} -> logged as {r and r.get('evidence_id')}")
    c, r, _ = s.req("POST", f"/api/v1/evidence/{j['evidence_id']}/review", {"decision": "override", "override_action": "ok", "by": "agronomist"})
    _, ev, _ = s.req("GET", f"/api/v1/evidence/{j['evidence_id']}")
    check("EV-08", "override flagged retraining_candidate and listed under target's reviews",
          r["retraining_candidate"] is True and len(ev["reviews"]) >= 2, f"{len(ev['reviews'])} reviews")
    c, *_ = s.req("POST", "/api/v1/evidence/ev_999999/review", {"decision": "approve"})
    check("EV-09", "review of unknown id -> 404", c == 404, str(c))
    c, _, md = s.req("GET", "/api/v1/evidence/export")
    check("EV-10", "MSPO audit pack: chain VERIFIED, fertiliser rows marked Simulated=yes",
          "chain: VERIFIED" in md and re.search(r"\| fertilise \|.*\| yes \|", md) is not None, md.splitlines()[2][:90])
    head = s.req("GET", "/api/v1/evidence/verify")[1]["head"]
    check("EV-17", "S-10 retest: audit pack prints the current chain head hash", head in md, head[:16])
    c, cov, _ = s.req("GET", "/api/v1/compliance/coverage")
    check("EV-11", "compliance coverage lists criteria + chain status", c == 200 and cov["criteria"] and cov["chain"]["ok"], str(c))
    if not tamper:
        return
    con = sqlite3.connect(s.db)
    tid = con.execute("SELECT evidence_id, record FROM evidence WHERE kind='soil_recommendation' ORDER BY id LIMIT 1 OFFSET 4").fetchone()
    rec = json.loads(tid[1]); rec["output"]["action"] = "lime" if rec["output"]["action"] != "lime" else "ok"
    con.execute("UPDATE evidence SET record=? WHERE evidence_id=?", (json.dumps(rec, sort_keys=True, separators=(",", ":")), tid[0]))
    con.commit()
    _, v, _ = s.req("GET", "/api/v1/evidence/verify")
    check("EV-12", "tamper: edit one record's action -> verify fails at that record", not v["ok"] and v["first_bad"] == tid[0], v["message"])
    _, _, md = s.req("GET", "/api/v1/evidence/export")
    check("EV-13", "tampered chain -> audit pack says BROKEN", "chain: BROKEN" in md, "")
    con.execute("UPDATE evidence SET record=? WHERE evidence_id=?", (tid[1], tid[0])); con.commit()
    _, v, _ = s.req("GET", "/api/v1/evidence/verify")
    check("EV-14", "restoring the original bytes -> chain verifies again", v["ok"], v["message"])
    mid = con.execute("SELECT evidence_id FROM evidence ORDER BY id LIMIT 1 OFFSET 7").fetchone()[0]
    con.execute("DELETE FROM evidence WHERE evidence_id=?", (mid,)); con.commit()
    _, v, _ = s.req("GET", "/api/v1/evidence/verify")
    check("EV-15", "tamper: delete a middle record -> verify fails", not v["ok"], v["message"])
    last = con.execute("SELECT id FROM evidence ORDER BY id DESC LIMIT 1").fetchone()[0]
    con.close()
    _, v, _ = s.req("GET", "/api/v1/evidence/verify")
    record("EV-16", "OBS", "S-10: audit pack now prints the chain head for external anchoring (checked in EV-17); tail truncation "
           "is detectable only by comparing with a previously quoted head", f"head id {last}")


def t_firmware(s):
    s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 600, "tds_margin": 0.30})
    hdr = {**SOIL, "Content-Type": "application/json"}
    cases = [
        ("FW-01", "boot, no NTP (ts null), cal_id 'uncalibrated', ec null", dict(seq=11)),
        ("FW-02", "NTP time, all sensors OK", dict(seq=12, ts="2026-11-20T09:00:00Z")),
        ("FW-03", "DS18B20 + DHT22 failed (NAN -> null)", dict(seq=13, soil_t=None, air_t=None, rh=None)),
        ("FW-04", "all soil probes failed (NAN -> null)", dict(seq=14, moist=None, ph=None, tds=None)),
        ("FW-05", "buffered replay, no NTP, age_s 95, rssi unknown (0 -> null)", dict(seq=9, buffered=True, rssi=0, age_s=95)),
        ("FW-06", "dry + acidic + TDS low (3 findings)", dict(seq=15, moist=24.04, ph=3.861, tds=300.4)),
    ]
    for tid, desc, kw in cases:
        body = fw_soil_json(**kw)
        c, j, txt = s.req("POST", "/api/v1/readings", body, hdr)
        p = fw_soil_parse(txt) if c == 200 else None
        ok = (c == 200 and p is not None and p["line1"] == p["raw_l1"] and p["line2"] == p["raw_l2"] and p["raw_l1"]
              and p["raw_l2"] and p["led"] in ("green", "amber", "red") and p["evidence"].startswith("ev_"))
        check(tid, f"soil_node toJson() payload [{desc}] -> 200 and applyCloudResponse() accepts", ok,
              f"{c} CLOUD '{p and p['line1']}' / '{p and p['line2']}' led={p and p['led']} {p and p['evidence']}")
    # LOCAL vs CLOUD agreement on boundary values, both sides fed the same r1()-rounded capture (v0.2.3)
    grid = [(m, ph, t) for m in (29.9, 29.96, 30.0, 50, 80.0, 80.04, 80.1) for ph in (3.94, 3.95, 3.99, 4.0, 4.15, 4.2, 6.5, 6.54, 6.55)
            for t in (419, 419.96, 600, 780.04, 781)]
    dis = []
    for i, (m, ph, t) in enumerate(grid):
        _, j, _ = s.req("POST", "/api/v1/readings", fw_soil_json(seq=20000 + i, moist=m, ph=ph, tds=t), hdr)
        a, led, l1, _ = fw_local(m, ph, t, 600, 0.30)
        if (a, led) != (j["action"], j["led"]) or l1 != j["oled"][0]:
            dis.append((m, ph, t, a, j["action"]))
    check("FW-07", f"v0.2.3 (S-12 retest): LOCAL == CLOUD action, LED and OLED line 1 on {len(grid)} raw boundary combos", not dis, str(dis[:4]))
    _, j0, _ = s.req("POST", "/api/v1/readings", fw_soil_json(seq=30002, moist=None, ph=None, tds=None), hdr)
    loc = fw_local(None, None, None, 600)
    check("FW-12", "v0.2.3: all probes failed -> NO DATA / amber in LOCAL and CLOUD", (loc[2], loc[1]) == (j0["oled"][0], j0["led"]) == ("NO DATA", "amber"),
          f"LOCAL {loc[2]}/{loc[1]} CLOUD {j0['oled'][0]}/{j0['led']}")
    record("FW-08", "OBS", "1-dp pH rounding moves the effective edges by half a step (raw 3.95 -> 4.0 = watch, not lime; "
           "raw 6.54 -> 6.5 = ok); within probe accuracy (±0.1 pH), consistent on both sides",
           f"LOCAL(3.95)={fw_local(50, 3.95, 600, 600)[0]}, LOCAL(3.94)={fw_local(50, 3.94, 600, 600)[0]}")
    c, j, txt = s.req("GET", "/api/v1/devices/cam-01/commands", headers=CAM)
    check("FW-10", "cam_node pollCommands(): idle reply parsed, cmd != 'capture' -> no capture", c == 200 and json.loads(txt).get("cmd") != "capture", txt)
    c, j, txt = s.req("POST", "/api/v1/infer/ripeness", raw=cam_jpeg(), headers={**CAM, "Content-Type": "image/jpeg"})
    check("FW-11", "cam_node captureAndUpload(): raw SVGA JPEG + headers -> 200, reply has label/confidence/harvest_advice/evidence_id",
          c == 200 and all(k in j for k in ("label", "confidence", "harvest_advice", "evidence_id")), f"{c} {j and j.get('label')}")


def t_dashboard(s):
    c, _, html = s.req("GET", "/")
    ext = [u for u in re.findall(r"""(?:src|href)=["']([^"']+)""", html) if re.match(r"(https?:)?//", u)]
    check("DB-01", "GET / 200; no external (CDN/font) src/href in index.html", c == 200 and not ext, str(ext))
    assets = re.findall(r"""(?:src|href)=["'](/static/[^"']+)""", html)
    codes = {a: s.req("GET", a)[0] for a in assets}
    check("DB-02", "all referenced local assets served 200 (incl. vendored Chart.js)", all(v == 200 for v in codes.values()), str(codes))
    js = s.req("GET", "/static/app.js")[2] + s.req("GET", "/static/style.css")[2] + s.req("GET", "/harvester")[2]
    ext2 = re.findall(r"https?://[^\s'\"`)]+", js)
    check("DB-03", "app.js / style.css / harvester.html contain no external URLs", not ext2, str(ext2[:3]))
    panels = ["soil-card", "rec-card", "cam-card", "cal-card", "cascade-card", "harvest-card", "ev-card", "mspo-card"]
    check("DB-04", "panels present: readings, recommendation(+reasoning), camera, calibration, satellite cascade, harvest, evidence, MSPO",
          all(f'id="{p}"' in html for p in panels), "")
    credits = ["Kamal", "Rosbi", "CC BY 4.0", "Copernicus Sentinel", "Descals", "Mimboro", "SIMULATED"]
    check("DB-05", "footer attributions: D1 Kamal, D2 Rosbi, D4 Mimboro, Descals mask, Copernicus, CC BY 4.0; SIMULATED labels",
          all(k in html for k in credits), str([k for k in credits if k not in html]))
    m = re.search(r"Contains modified Copernicus Sentinel data[^·<]*", html)
    check("DB-06", "S-11 retest: Copernicus notice has a year and names Earth Engine", bool(m and re.search(r"20\d\d", m.group(0))
          and "Earth Engine" in m.group(0) and "Planetary" not in m.group(0)), m.group(0) if m else "missing")
    lic = s.req("GET", "/static/vendor/LICENSE-chartjs.txt")[0]
    head = s.req("GET", "/static/vendor/chart.umd.min.js")[2][:120]
    check("DB-10", "S-14 retest: Chart.js MIT notice restored (banner or LICENSE file served)", lic == 200 or "MIT" in head, f"LICENSE {lic}; head {head[:60]!r}")
    feeds = {p: s.req("GET", p)[0] for p in ["/api/v1/latest", "/api/v1/harvest/plan?crew=12", "/api/v1/screening",
                                              "/api/v1/satellite", "/api/v1/compliance/coverage",
                                              "/api/v1/evidence?limit=25&non_ok=true", "/api/v1/readings?device_id=soilnode-01&limit=60"]}
    check("DB-07", "every feed the dashboard polls returns 200", all(v == 200 for v in feeds.values()), str(feeds))
    _, hp, _ = s.req("GET", "/api/v1/harvest/plan?crew=12")
    _, sc, _ = s.req("GET", "/api/v1/screening")
    check("DB-08", "harvest + satellite feeds self-label SIMULATED",
          "SIMULATED" in json.dumps(hp).upper() and "SIMULATED" in json.dumps(sc).upper(), sc["stage1_satellite"]["source"])


def t_admin_mode(py, port):
    s = Server(py, port, {"SAWIT_ADMIN_TOKEN": "t0k-verif", "SAWIT_DEVICE_KEYS": "soilnode-01:k-live,cam-01:k-cam",
                          "SAWIT_MODE": "cloud"})
    try:
        c, *_ = s.req("POST", "/api/v1/readings", reading(), SOIL)
        check("AD-01", "SAWIT_DEVICE_KEYS override: demo key rejected (401)", c == 401, str(c))
        live = {"X-Device-Id": "soilnode-01", "X-Device-Key": "k-live"}
        c, *_ = s.req("POST", "/api/v1/readings", reading(), live)
        check("AD-02", "configured key accepted (200)", c == 200, str(c))
        p = "/api/v1/devices/soilnode-01/calibration"
        c, *_ = s.req("POST", p, {"tds_baseline_ppm": 600})
        check("AD-03", "admin token set: calibration POST without token -> 403", c == 403, str(c))
        c, *_ = s.req("POST", p, {"tds_baseline_ppm": 600}, {"X-Admin-Token": "t0k-verif"})
        check("AD-04", "calibration POST with X-Admin-Token -> 200", c == 200, str(c))
        c, *_ = s.req("POST", "/api/v1/devices/cam-01/commands", {"cmd": "capture"})
        check("AD-05", "commands POST without token -> 403", c == 403, str(c))
        c, *_ = s.req("GET", p, headers=live)
        check("AD-06", "device GET calibration still works in token mode", c == 200, str(c))
        c, *_ = s.req("GET", p, headers={"X-Admin-Token": "t0k-verif"})
        c0, *_ = s.req("GET", p)
        js = s.req("GET", "/static/app.js")[2]
        check("AD-07", "S-01 retest: dashboard GET calibration with X-Admin-Token (app.js get() now sends it) -> 200; no token -> 403",
              c == 200 and c0 == 403 and 'headers: TOKEN ? { "X-Admin-Token": TOKEN }' in js, f"{c}/{c0}")
        c, *_ = s.req("GET", p + "?token=t0k-verif")
        record("AD-08", "PASS" if c == 200 else "FAIL", "GET calibration with ?token= query works (fix path for AD-07)", str(c))
        c, *_ = s.req("POST", "/api/v1/evidence/ev_000001/review", {"decision": "approve"})
        check("AD-09", "review POST without token -> 403", c == 403, str(c))
        reads = ["/api/v1/latest", "/api/v1/readings", "/api/v1/evidence", "/api/v1/evidence/export", "/api/v1/evidence/verify",
                 "/api/v1/compliance/coverage", "/api/v1/harvest/plan", "/api/v1/screening", "/api/v1/satellite", "/api/v1/meta"]
        no_tok = {r: s.req("GET", r)[0] for r in reads}
        tok = {r: s.req("GET", r + "?token=t0k-verif")[0] for r in reads}
        check("AD-10", "S-08 retest: cloud mode reads need the token (403 without, 200 with ?token=)",
              set(no_tok.values()) == {403} and set(tok.values()) == {200}, f"{no_tok} / {tok}")
        pub = {r: s.req("GET", r)[0] for r in ["/", "/harvester", "/api/v1/health", "/static/app.js"]}
        check("AD-14", "dashboard shell, harvester shell and /health stay public (page loads, then uses ?token=)",
              set(pub.values()) == {200}, str(pub))
        c, h, _ = s.req("GET", "/api/v1/health")
        check("AD-11", "SAWIT_MODE=cloud reported by /health (dashboard CLOUD pill)", h["mode"] == "cloud", h["mode"])
    finally:
        s.stop()


def t_cloud_failclosed(py, port):
    s = Server(py, port, {"SAWIT_MODE": "cloud", "SAWIT_DEVICE_KEYS": "", "SAWIT_ADMIN_TOKEN": ""})
    try:
        c, *_ = s.req("POST", "/api/v1/readings", reading(), SOIL)
        check("AD-12", "SAWIT_MODE=cloud, no SAWIT_DEVICE_KEYS: demo key rejected (D-12 retest, fail closed)", c == 401, str(c))
        c, *_ = s.req("POST", "/api/v1/devices/soilnode-01/calibration", {"tds_baseline_ppm": 600})
        check("AD-13", "SAWIT_MODE=cloud, no SAWIT_ADMIN_TOKEN: writes refused 403 (fail closed)", c == 403, str(c))
    finally:
        s.stop()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8833)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    py = sys.executable
    s = Server(py, a.port, {})
    try:
        t_health_meta(s); t_auth(s); t_validation(s); t_thresholds(s); t_priority(s); t_nulls_ec(s)
        t_replay(s); t_calibration(s); t_commands(s); t_ripeness(s); t_firmware(s); t_oled_led_extremes(s)
        t_dashboard(s); t_evidence(s, tamper=True)
    finally:
        s.stop()
    t_admin_mode(py, a.port)
    t_cloud_failclosed(py, a.port)
    # server down: dashboard behaviour is a JS path; check the API is really gone (DB-09 manual part in TEST_PLAN)
    try:
        urllib.request.urlopen(f"http://127.0.0.1:{a.port}/api/v1/health", timeout=2)
        check("SV-01", "test servers stopped (port free)", False)
    except Exception:  # noqa: BLE001
        check("SV-01", "test servers stopped (port free)", True)
    counts = {k: sum(1 for r in RESULTS if r[1] == k) for k in ("PASS", "FAIL", "OBS", "BLOCKED")}
    summary = " ".join(f"{k}={v}" for k, v in counts.items())
    print("SUMMARY", summary)
    if a.out:
        lines = [f"# contract_test.py results — {time.strftime('%Y-%m-%d %H:%M:%S')} — {summary}", "",
                 "| ID | Status | Test | Evidence |", "|---|---|---|---|"]
        lines += [f"| {t} | {st} | {d.replace('|', '/')} | {e.replace('|', '/')[:220]} |" for t, st, d, e in RESULTS]
        Path(a.out).write_text("\n".join(lines) + "\n")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
