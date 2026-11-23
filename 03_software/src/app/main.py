"""SawitSense backend (FastAPI) — actual build of the ingestion, cognitive and application layers.

Run locally:  uvicorn app.main:app --host 0.0.0.0 --port 8000   (from 03_software/src)
Contract:     00_lead/INTERFACES.md v0.2.1, full spec in 03_software/05_api_spec.md
"""
from __future__ import annotations

import json
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import analytics, config as C, db, evidence, inference, recommender

APP_VERSION = "0.2.1"
app = FastAPI(title="SawitSense API", version=APP_VERSION,
              description="Smart palm oil plantation decision support — explain-to-audit build")
# The presentation embeds the dashboard/API from another origin (06_presentation).
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
C.ensure_dirs()


# ---------------------------------------------------------------- auth
def device_auth(x_device_id: str | None = Header(None), x_device_key: str | None = Header(None)) -> str:
    if not x_device_id:
        raise HTTPException(401, "Missing X-Device-Id header")
    if C.REQUIRE_DEVICE_KEY and C.DEVICE_KEYS.get(x_device_id) != x_device_key:
        raise HTTPException(401, "Unknown device or wrong X-Device-Key")
    return x_device_id


def admin_auth(request: Request, x_admin_token: str | None = Header(None)) -> None:
    """Dashboard write actions. Open when SAWIT_ADMIN_TOKEN is unset (local demo)."""
    if C.ADMIN_TOKEN and (x_admin_token or request.query_params.get("token")) != C.ADMIN_TOKEN:
        raise HTTPException(403, "Admin token required")


def device_or_admin(request: Request, device_id: str, x_device_id: str | None = Header(None),
                    x_device_key: str | None = Header(None), x_admin_token: str | None = Header(None)) -> None:
    if x_device_id:
        if x_device_id != device_id or (C.REQUIRE_DEVICE_KEY and C.DEVICE_KEYS.get(x_device_id) != x_device_key):
            raise HTTPException(401, "Unknown device or wrong X-Device-Key")
        return
    admin_auth(request, x_admin_token)


# ---------------------------------------------------------------- models
class SoilReading(BaseModel):
    device_id: str
    seq: int | None = None
    ts: str | None = None
    buffered: bool = False
    block_id: str | None = "DEMO-A1"
    soil_moisture_pct: float | None = Field(None, ge=0, le=100)
    soil_ph: float | None = Field(None, ge=0, le=14)
    tds_ppm: float | None = Field(None, ge=0)
    ec_us_cm: float | None = None
    soil_temp_c: float | None = None
    air_temp_c: float | None = None
    air_rh_pct: float | None = None
    rssi_dbm: int | None = None
    cal_id: str | None = None
    fw_version: str | None = None


class Calibration(BaseModel):
    tds_baseline_ppm: float | None = Field(None, gt=0)
    tds_margin: float = Field(C.TDS_DEFAULT_MARGIN, gt=0, lt=1)
    use_latest: bool = False          # dashboard: "use current TDS reading as baseline"
    cal_id: str | None = None


class Command(BaseModel):
    cmd: Literal["capture"] = "capture"


class Review(BaseModel):
    decision: Literal["approve", "override"]
    by: str = "agronomist"
    note: str = ""
    override_action: str | None = None


# ---------------------------------------------------------------- ingestion: soil node
@app.post("/api/v1/readings")
def post_reading(r: SoilReading, device: str = Depends(device_auth)) -> dict:
    if r.device_id != device:
        raise HTTPException(400, "device_id in body does not match X-Device-Id")
    payload = r.model_dump()
    ec_derived = payload["ec_us_cm"] is None and payload["tds_ppm"] is not None
    if ec_derived:
        payload["ec_us_cm"] = round(payload["tds_ppm"] / 0.5, 1)   # approximation (DFR-SEN0244)
    payload["ec_derived"] = ec_derived
    received = db.now()
    dev = db.get_device(device)
    rec = recommender.recommend(payload, dev.get("tds_baseline"), dev.get("tds_margin"))
    record = {
        "input": payload, "received_at": received,
        "calibration": {"device_cal_id": r.cal_id, "tds_baseline_ppm": dev.get("tds_baseline"),
                        "tds_margin": dev.get("tds_margin"), "tds_cal_id": dev.get("cal_id")},
        "output": rec, "rules_version": "INTERFACES-v0.2.1",
    }
    ev = evidence.append("soil_recommendation", record, device, r.block_id)
    db.x("INSERT INTO readings(device_id, block_id, seq, ts, received_at, buffered, payload, recommendation, evidence_id)"
         " VALUES(?,?,?,?,?,?,?,?,?)",
         (device, r.block_id, r.seq, r.ts, received, int(r.buffered), db.dumps(payload), db.dumps(rec), ev))
    db.touch_device(device, r.rssi_dbm, r.fw_version)
    out = {k: rec[k] for k in ("action", "reason", "confidence", "actions", "counterfactual", "simulated")}
    out.update(evidence_id=ev, oled=rec["oled"], led=rec["led"], received_at=received)
    return out


@app.get("/api/v1/readings")
def list_readings(device_id: str | None = None, limit: int = Query(120, le=2000)) -> list[dict]:
    sql, args = "SELECT * FROM readings", []
    if device_id:
        sql += " WHERE device_id=?"; args.append(device_id)
    rows = db.q(sql + " ORDER BY id DESC LIMIT ?", (*args, limit))
    return [{"id": x["id"], "device_id": x["device_id"], "received_at": x["received_at"], "seq": x["seq"],
             "buffered": bool(x["buffered"]), "evidence_id": x["evidence_id"], **json.loads(x["payload"]),
             "action": json.loads(x["recommendation"])["action"]} for x in reversed(rows)]


# ---------------------------------------------------------------- devices: calibration + commands
def _cal_body(device_id: str) -> dict:
    d = db.get_device(device_id)
    return {"tds_baseline_ppm": d.get("tds_baseline"),
            "tds_margin": d.get("tds_margin") if d.get("tds_margin") is not None else C.TDS_DEFAULT_MARGIN,
            "updated_at": d.get("updated_at"), "cal_id": d.get("cal_id")}


@app.get("/api/v1/devices/{device_id}/calibration")
def get_calibration(device_id: str, _=Depends(device_or_admin)) -> dict:
    return _cal_body(device_id)


@app.post("/api/v1/devices/{device_id}/calibration")
def set_calibration(device_id: str, c: Calibration, _=Depends(admin_auth)) -> dict:
    baseline = c.tds_baseline_ppm
    if c.use_latest:
        rows = db.q("SELECT payload FROM readings WHERE device_id=? ORDER BY id DESC LIMIT 1", (device_id,))
        tds = json.loads(rows[0]["payload"]).get("tds_ppm") if rows else None
        if tds is None:
            raise HTTPException(409, "No recent TDS reading for this device")
        baseline = float(tds)
    if baseline is None:
        raise HTTPException(422, "Provide tds_baseline_ppm or use_latest=true")
    cal_id = c.cal_id or db.now()[:10]
    db.set_calibration(device_id, baseline, c.tds_margin, cal_id)
    last = db.q("SELECT block_id FROM readings WHERE device_id=? ORDER BY id DESC LIMIT 1", (device_id,))
    evidence.append("calibration", {"output": {"action": "calibrate",
                                               "reason": f"TDS baseline {baseline:.0f} ppm ±{c.tds_margin:.0%}"},
                                    "tds_baseline_ppm": baseline, "tds_margin": c.tds_margin, "cal_id": cal_id},
                    device_id, last[0]["block_id"] if last else None)
    return _cal_body(device_id)


@app.post("/api/v1/devices/{device_id}/commands")
def queue_command(device_id: str, c: Command, _=Depends(admin_auth)) -> dict:
    cid = db.x("INSERT INTO commands(device_id, cmd, created_at) VALUES(?,?,?)", (device_id, c.cmd, db.now()))
    return {"queued": True, "id": cid, "cmd": c.cmd}


@app.get("/api/v1/devices/{device_id}/commands")
def poll_command(device_id: str, device: str = Depends(device_auth)) -> dict:
    if device != device_id:
        raise HTTPException(403, "Device may only poll its own commands")
    db.touch_device(device_id)
    with db._lock:
        rows = db.q("SELECT id, cmd FROM commands WHERE device_id=? AND consumed_at IS NULL ORDER BY id LIMIT 1", (device_id,))
        if not rows:
            return {"cmd": "none"}
        db.x("UPDATE commands SET consumed_at=? WHERE id=?", (db.now(), rows[0]["id"]))
    return {"cmd": rows[0]["cmd"], "id": rows[0]["id"]}


# ---------------------------------------------------------------- cognitive: ripeness
@app.post("/api/v1/infer/ripeness")
async def infer_ripeness(request: Request, device: str = Depends(device_auth)) -> dict:
    body = await request.body()
    if not body:
        raise HTTPException(400, "Empty body — send raw image/jpeg")
    if len(body) > 5_000_000:
        raise HTTPException(413, "Image larger than 5 MB")
    block = C.DEVICE_BLOCKS.get(device, "DEMO-A1")
    try:
        with db._lock:   # reserve the next evidence id so heatmap name == evidence id
            nxt = (db.q("SELECT COALESCE(MAX(id),0)+1 AS n FROM evidence")[0]["n"])
            name = f"ev_{nxt:06d}"
            res = inference.predict(body, heatmap_name=name)
            (C.IMAGE_DIR / f"{name}.jpg").write_bytes(body)
            ev = evidence.append("ripeness", {"output": res, "image": f"/media/images/{name}.jpg",
                                              "harvest_rule": "M2 rule-based schedule (SIMULATED)"}, device, block)
    except inference.ModelUnavailable as e:
        raise HTTPException(503, str(e)) from e
    except ValueError as e:
        raise HTTPException(400, str(e)) from e
    db.touch_device(device)
    return {**{k: res[k] for k in ("label", "confidence", "probs", "harvest_advice", "explanation",
                                   "heatmap_url", "model_version")}, "evidence_id": ev,
            "needs_review": res["needs_review"], "image_url": f"/media/images/{name}.jpg"}


# ---------------------------------------------------------------- application: dashboard feeds
def _latest_ripeness() -> dict | None:
    e = evidence.listing(limit=1, kind="ripeness")
    if not e:
        return None
    r = e[0]
    return {"evidence_id": r["evidence_id"], "created_at": r["created_at"], "block_id": r["block_id"],
            "device_id": r["device_id"], "image_url": r["record"].get("image"), **r["record"]["output"]}


@app.get("/api/v1/latest")
def latest() -> dict:
    rows = db.q("SELECT * FROM readings WHERE id IN (SELECT MAX(id) FROM readings GROUP BY device_id) ORDER BY id DESC")
    soil = []
    for x in rows:
        ev = evidence.get(x["evidence_id"])
        soil.append({"device_id": x["device_id"], "block_id": x["block_id"], "received_at": x["received_at"],
                     "seq": x["seq"], "reading": json.loads(x["payload"]), "recommendation": json.loads(x["recommendation"]),
                     "evidence_id": x["evidence_id"], "reviews": [r["record"] for r in evidence.reviews_for(x["evidence_id"])],
                     "calibration": ev["record"]["calibration"] if ev else None})
    devices = [dict(d) for d in db.q("SELECT device_id, last_seen, last_rssi, fw_version, tds_baseline, tds_margin, cal_id FROM devices")]
    return {"server_time": db.now(), "mode": C.DEPLOYMENT_MODE, "soil": soil, "ripeness": _latest_ripeness(),
            "devices": devices, "evidence_count": db.q("SELECT COUNT(*) n FROM evidence")[0]["n"]}


@app.get("/api/v1/evidence")
def evidence_list(limit: int = Query(50, le=1000), block_id: str | None = None, kind: str | None = None,
                  non_ok: bool = False) -> list[dict]:
    return evidence.listing(limit, block_id, kind, non_ok)


@app.get("/api/v1/evidence/verify")
def evidence_verify() -> dict:
    return evidence.verify()


@app.get("/api/v1/evidence/export", response_class=PlainTextResponse)
def evidence_export(block_id: str | None = None, since: str | None = None) -> str:
    return evidence.audit_pack(block_id, since)


@app.get("/api/v1/evidence/{evidence_id}")
def evidence_get(evidence_id: str) -> dict:
    e = evidence.get(evidence_id)
    if not e:
        raise HTTPException(404, "No such evidence record")
    e["reviews"] = evidence.reviews_for(evidence_id)
    return e


@app.post("/api/v1/evidence/{evidence_id}/review")
def evidence_review(evidence_id: str, rv: Review, _=Depends(admin_auth)) -> dict:
    target = evidence.get(evidence_id)
    if not target:
        raise HTTPException(404, "No such evidence record")
    if rv.decision == "override" and not rv.override_action:
        raise HTTPException(422, "override_action required when overriding")
    orig = target["record"].get("output", {})
    rec = {"target": evidence_id, "decision": rv.decision, "by": rv.by, "note": rv.note,
           "original": orig.get("action") or orig.get("label"), "override_action": rv.override_action,
           "output": {"action": rv.override_action or orig.get("action") or orig.get("label"),
                      "reason": f"{rv.decision} by {rv.by}: {rv.note}".strip(": ")},
           # Overrides become labelled examples for the retraining queue (human-in-the-loop, D28).
           "retraining_candidate": rv.decision == "override"}
    ev = evidence.append("review", rec, target["device_id"], target["block_id"])
    return {"evidence_id": ev, **rec}


@app.get("/api/v1/compliance/coverage")
def compliance_coverage(block_id: str | None = None) -> dict:
    from . import compliance
    rows = list(reversed(evidence.listing(limit=100000, block_id=block_id)))
    return {"block_id": block_id, "records": len(rows), "criteria": compliance.coverage(rows),
            "chain": evidence.verify()}


@app.get("/api/v1/harvest/plan")
def harvest_plan(crew: int | None = Query(None, ge=1, le=500)) -> dict:
    return analytics.harvest_plan(crew, _latest_ripeness())


@app.get("/api/v1/screening")
def screening(z: float = -1.5, p: float = 0.3) -> dict:
    return analytics.cascade(z, p)


@app.get("/api/v1/satellite")
def satellite() -> dict:
    return analytics.satellite()


@app.get("/api/v1/meta")
def meta() -> dict:
    return {"app": "SawitSense", "version": APP_VERSION, "mode": C.DEPLOYMENT_MODE,
            "thresholds": {"moisture_low": C.MOISTURE_LOW, "moisture_high": C.MOISTURE_HIGH, "ph_lime": C.PH_LIME,
                           "ph_watch_top": C.PH_WATCH_TOP, "ph_high": C.PH_HIGH, "tds_default_margin": C.TDS_DEFAULT_MARGIN},
            "actions": list(recommender.rules.PRIORITY), "ripeness_model": inference.model_info(),
            "fertiliser_model": (recommender._tree() or {}).get("meta")}


@app.get("/api/v1/health")
def health() -> dict:
    db.q("SELECT 1")
    m = inference.model_info()
    return {"status": "ok", "version": APP_VERSION, "mode": C.DEPLOYMENT_MODE, "time": db.now(),
            "ripeness_model": m.get("model_version") if m.get("available", True) else None,
            "fertiliser_model": bool(recommender._tree())}


# ---------------------------------------------------------------- static
app.mount("/static/heatmaps", StaticFiles(directory=C.HEATMAP_DIR), name="heatmaps")
app.mount("/media/images", StaticFiles(directory=C.IMAGE_DIR), name="images")
app.mount("/static", StaticFiles(directory=C.STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(C.STATIC_DIR / "index.html")


@app.get("/harvester", include_in_schema=False)
def harvester():
    return FileResponse(C.STATIC_DIR / "harvester.html")
