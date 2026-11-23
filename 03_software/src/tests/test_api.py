"""Backend tests: rule table (INTERFACES v0.2.1 §4), ingestion, calibration, evidence chain, commands.
Run from 03_software/src:  python -m pytest -q
"""
import json
import os
import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("SAWIT_RUNTIME_DIR", str(Path(__file__).resolve().parent / "_runtime"))

from fastapi.testclient import TestClient  # noqa: E402

from app import db, rules  # noqa: E402
from app.main import app  # noqa: E402

SOIL = {"X-Device-Id": "soilnode-01", "X-Device-Key": "demo-soil-key"}
CAM = {"X-Device-Id": "cam-01", "X-Device-Key": "demo-cam-key"}


@pytest.fixture(autouse=True)
def fresh_db(tmp_path):
    db.reset_for_tests(tmp_path / "t.db")
    yield


@pytest.fixture
def client():
    return TestClient(app)


def reading(**kw):
    base = {"device_id": "soilnode-01", "seq": 1, "ts": None, "buffered": False, "block_id": "DEMO-A1",
            "soil_moisture_pct": 50, "soil_ph": 5.0, "tds_ppm": 600, "ec_us_cm": None, "soil_temp_c": 27.5,
            "air_temp_c": 30, "air_rh_pct": 78, "rssi_dbm": -60, "cal_id": "2026-12-09", "fw_version": "0.2.0"}
    base.update(kw)
    return base


# ---------------- rule table
@pytest.mark.parametrize("kw,action,rule,led", [
    ({"soil_moisture_pct": 24}, "irrigate", "MOIST_LOW", "red"),
    ({"soil_moisture_pct": 85}, "drain", "MOIST_HIGH", "amber"),
    ({"soil_ph": 3.8}, "lime", "PH_LIME", "red"),
    ({"soil_ph": 4.1}, "watch", "PH_LOW_WATCH", "amber"),
    ({"soil_ph": 6.8}, "watch", "PH_HIGH", "amber"),
    ({"soil_ph": 6.0}, "ok", "ALL_OK", "green"),
    ({}, "ok", "ALL_OK", "green"),
])
def test_rule_table(kw, action, rule, led):
    r = rules.recommend(reading(**kw))
    assert r["action"] == action and r["actions"][0]["rule_id"] == rule and r["led"] == led
    assert all(len(line) <= 16 for line in r["oled"]) and len(r["oled"]) == 2


def test_tds_rules_and_simulated_flag():
    low = rules.recommend(reading(tds_ppm=300), 600, 0.3)
    high = rules.recommend(reading(tds_ppm=900), 600, 0.3)
    mid = rules.recommend(reading(tds_ppm=600), 600, 0.3)
    assert (low["action"], low["simulated"]) == ("fertilise", True)
    assert (high["action"], high["simulated"]) == ("skip_fertiliser", True)
    assert mid["action"] == "ok" and not mid["simulated"]
    assert rules.recommend(reading(tds_ppm=300))["action"] == "ok"   # no baseline → TDS rules skipped


def test_priority_and_counterfactual():
    r = rules.recommend(reading(soil_moisture_pct=20, soil_ph=3.7, tds_ppm=300), 600, 0.3)
    assert [a["action"] for a in r["actions"]] == ["irrigate", "lime", "fertilise"]
    assert r["counterfactual"].startswith("Would be OK if moisture ≥ 30%")


def test_null_sensor_never_fabricated():
    r = rules.recommend(reading(soil_ph=None))
    assert "soil_ph" in " ".join(r["notes"]) and r["action"] == "ok"
    allnull = rules.recommend(reading(soil_ph=None, soil_moisture_pct=None, tds_ppm=None))
    assert allnull["oled"][0] == "NO DATA" and allnull["led"] == "amber"


# ---------------- API
def test_post_reading_contract(client):
    r = client.post("/api/v1/readings", json=reading(soil_moisture_pct=24), headers=SOIL)
    assert r.status_code == 200, r.text
    j = r.json()
    for k in ("action", "reason", "confidence", "actions", "counterfactual", "simulated", "evidence_id", "oled", "led"):
        assert k in j
    assert j["action"] == "irrigate" and j["evidence_id"].startswith("ev_")
    ev = client.get(f"/api/v1/evidence/{j['evidence_id']}").json()
    assert ev["record"]["input"]["ec_us_cm"] == 1200.0 and ev["record"]["input"]["ec_derived"] is True


def test_auth(client):
    assert client.post("/api/v1/readings", json=reading(), headers={"X-Device-Id": "soilnode-01", "X-Device-Key": "bad"}).status_code == 401
    assert client.post("/api/v1/readings", json=reading(device_id="other"), headers=SOIL).status_code == 400


def test_calibration_get_post_and_tds(client):
    g = client.get("/api/v1/devices/soilnode-01/calibration", headers=SOIL).json()
    assert g == {"tds_baseline_ppm": None, "tds_margin": 0.30, "updated_at": None, "cal_id": None}
    client.post("/api/v1/readings", json=reading(tds_ppm=640), headers=SOIL)
    p = client.post("/api/v1/devices/soilnode-01/calibration", json={"use_latest": True}).json()
    assert p["tds_baseline_ppm"] == 640 and p["tds_margin"] == 0.30 and p["updated_at"]
    r = client.post("/api/v1/readings", json=reading(tds_ppm=300), headers=SOIL).json()
    assert r["action"] == "fertilise" and r["simulated"] is True
    assert client.get("/api/v1/devices/soilnode-01/calibration", headers=CAM).status_code == 401


def test_commands_queue(client):
    assert client.get("/api/v1/devices/cam-01/commands", headers=CAM).json() == {"cmd": "none"}
    client.post("/api/v1/devices/cam-01/commands", json={"cmd": "capture"})
    assert client.get("/api/v1/devices/cam-01/commands", headers=CAM).json()["cmd"] == "capture"
    assert client.get("/api/v1/devices/cam-01/commands", headers=CAM).json() == {"cmd": "none"}
    assert client.get("/api/v1/devices/cam-01/commands", headers=SOIL).status_code == 403


def test_evidence_chain_review_and_tamper(client):
    ids = [client.post("/api/v1/readings", json=reading(seq=i, soil_ph=3.8), headers=SOIL).json()["evidence_id"] for i in range(3)]
    rv = client.post(f"/api/v1/evidence/{ids[0]}/review", json={"decision": "override", "override_action": "watch", "note": "recent liming"})
    assert rv.status_code == 200 and rv.json()["retraining_candidate"] is True
    assert client.get("/api/v1/evidence/verify").json()["ok"] is True
    pack = client.get("/api/v1/evidence/export").text
    assert "VERIFIED" in pack and "FERTILISER_RECORDS" in pack
    # tamper with a stored record → verification must fail at that record
    con = sqlite3.connect(db.C.DB_PATH)
    con.execute("UPDATE evidence SET record=replace(record,'lime','ok') WHERE evidence_id=?", (ids[1],))
    con.commit(); con.close()
    v = client.get("/api/v1/evidence/verify").json()
    assert v["ok"] is False and v["first_bad"] == ids[1]


def test_latest_harvest_screening_health(client):
    client.post("/api/v1/readings", json=reading(), headers=SOIL)
    l = client.get("/api/v1/latest").json()
    assert l["soil"][0]["device_id"] == "soilnode-01"
    h = client.get("/api/v1/harvest/plan?crew=5").json()
    assert h["simulated"] and sum(b["assigned_harvesters"] for b in h["blocks"]) <= 5
    assert client.get("/api/v1/screening").json()["available"]
    assert client.get("/api/v1/health").json()["status"] == "ok"
    assert client.get("/").status_code == 200 and client.get("/harvester").status_code == 200


def test_ripeness_endpoint(client):
    from app import inference
    import io
    from PIL import Image
    buf = io.BytesIO(); Image.new("RGB", (320, 240), (180, 60, 20)).save(buf, "JPEG")
    r = client.post("/api/v1/infer/ripeness", content=buf.getvalue(), headers={**CAM, "Content-Type": "image/jpeg"})
    if not inference.C.MODEL_PATH.exists():
        assert r.status_code == 503
        return
    assert r.status_code == 200, r.text
    j = r.json()
    assert j["label"] in j["probs"] and abs(sum(j["probs"].values()) - 1) < 0.01
    assert client.get(j["heatmap_url"]).status_code == 200
    assert client.post("/api/v1/infer/ripeness", content=b"notajpeg", headers=CAM).status_code == 400
