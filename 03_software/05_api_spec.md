# 05 — SawitSense API Specification (v0.2.2)

> Implements `00_lead/INTERFACES.md` v0.2.2 (D25, D30, D33). Base path `/api/v1`. All bodies are JSON (UTF-8), except the camera upload, which is raw `image/jpeg`. Interactive OpenAPI docs are served at `/docs`.
> - In the target design this API runs on Azure Container Apps behind API Management, and device traffic arrives through IoT Hub (`04_cloud_design.md`).
> - In the build, devices call it directly over HTTPS (INTERFACES §1).

## 1. Conventions

| Item | Rule |
|---|---|
| Device auth | `X-Device-Id` + `X-Device-Key` on every device call. Unknown pair → `401`. Body `device_id` ≠ header → `400`. A device may only read or poll its own resources → `401`/`403` |
| Admin (dashboard write) auth | `X-Admin-Token` header, or `?token=`, when `SAWIT_ADMIN_TOKEN` is set. **Cloud mode (`SAWIT_MODE=cloud`):** the token is mandatory (writes are refused if it is unset), and the demo device keys are disabled. Only keys from `SAWIT_DEVICE_KEYS` are accepted (D-12) |
| Time | ISO-8601 UTC `YYYY-MM-DDTHH:MM:SSZ`. The server stamps `received_at`; `captured_at` = `ts` if given, else `received_at − age_s`, else `received_at` |
| Nulls | A failed sensor is `null` and is never replaced by a value. Rules for that sensor are skipped and noted |
| IDs | Evidence IDs are `ev_` + 6 digits, sequential, hash-chained |
| Errors | `{"detail": "..."}` with status 400 / 401 / 403 / 404 / 409 / 413 / 422 / 503 |
| CORS | Open (`*`), so the presentation can embed the dashboard |

## 2. Device endpoints

### 2.1 `POST /api/v1/readings` — soil node → recommendation (synchronous)

**Request**

| Field | Type | Req | Notes |
|---|---|---|---|
| `device_id` | string | ✔ | Must equal `X-Device-Id` |
| `seq` | int | | Monotonic per device |
| `ts` | string\|null | | Device clock (NTP); null if no time |
| `age_s` | int ≥ 0 \| null | | v0.2.2: seconds between capture and send (0 if fresh) |
| `buffered` | bool | | `true` for replays from the offline buffer |
| `block_id` | string | | Default `DEMO-A1` |
| `soil_moisture_pct` | 0–100 \| null | | |
| `soil_ph` | 0–14 \| null | | |
| `tds_ppm` | ≥0 \| null | | |
| `ec_us_cm` | number\|null | | If null, the server derives EC ≈ TDS/0.5 and flags `ec_derived` |
| `soil_temp_c`, `air_temp_c`, `air_rh_pct` | number\|null | | Context; soil temp feeds M6 |
| `rssi_dbm` | int\|null | | |
| `cal_id` | string\|null | | Date of last probe calibration (logged as evidence) |
| `fw_version` | string\|null | | |

**Response 200**
```json
{
  "action": "lime",
  "reason": "Soil pH 3.86 < 4.0 — strongly acidic, apply lime [KANANG2026]",
  "confidence": 0.86,
  "actions": [
    {"action": "lime", "severity": "high", "rule_id": "PH_LIME", "reason": "..."},
    {"action": "fertilise", "severity": "medium", "rule_id": "TDS_LOW", "reason": "... (SIMULATED agronomy)"}
  ],
  "counterfactual": "Would be OK if pH ≥ 4.2 and TDS ≥ 414 ppm",
  "simulated": true,
  "evidence_id": "ev_000023",
  "oled": ["LIME", "pH 3.86<4.0"],
  "led": "red",
  "received_at": "2026-12-10T09:00:03Z",
  "captured_at": "2026-12-10T09:00:03Z"
}
```

**Rule table (INTERFACES §4).** The backend applies these rules; firmware uses the same thresholds in LOCAL mode.

| rule_id | Condition | action | severity | led |
|---|---|---|---|---|
| `MOIST_LOW` | moisture < 30 | irrigate | high | red |
| `MOIST_HIGH` | moisture > 80 | drain | medium | amber |
| `PH_LIME` | pH < 4.0 | lime | high | red |
| `PH_LOW_WATCH` | 4.0 ≤ pH < 4.2 | watch | low | amber |
| `PH_HIGH` | pH > 6.5 | watch | low | amber |
| `TDS_LOW` | TDS < baseline × (1 − margin) | fertilise (simulated) | medium | amber |
| `TDS_HIGH` | TDS > baseline × (1 + margin) | skip_fertiliser (simulated) | medium | amber |
| `ALL_OK` | none triggered | ok | info | green |

**Rule details:**
- **Priority:** irrigate/drain > lime > fertilise/skip_fertiliser > watch > ok. Ties go to the higher severity, then the larger distance from the threshold.
- **pH 5.5–6.5** is OK, with a note: above the typical oil-palm band, not harmful.
- **No TDS baseline set** → TDS rules are skipped (noted).
- **`simulated: true`** whenever a TDS rule fired.
- **`oled[0]`** is the upper-case action with `_` replaced by a space (e.g. `SKIP FERTILISER`). For partial data it reads `OK (partial)` / `no pH reading`; when all sensors are null it reads `NO DATA` / `check sensors` with an amber LED.
- **Confidence** comes from the rules (distance from the threshold in sensor-error units, minus 0.1 per missing sensor), blended 50/50 with the M6 tree's probability for the chosen action. `needs_review` (visible on `/latest`) is set when M6 disagrees or confidence is below 0.6.

**`/latest` semantics (D-04).** The dashboard shows the **non-buffered** reading with the highest `seq` per device. A buffered replay never replaces a fresh reading. A device that has sent only buffered rows shows its newest row.

### 2.2 `GET /api/v1/devices/{device_id}/calibration` (v0.2.1, D30)
Callable by the device itself (device headers), or by the dashboard (admin token, or open in local mode). Called by the soil node at boot and hourly to cache the baseline for LOCAL mode.
```json
{"tds_baseline_ppm": 592.0, "tds_margin": 0.30, "updated_at": "2026-12-10T08:40:00Z", "cal_id": "2026-12-10"}
```
If no baseline is set: `{"tds_baseline_ppm": null, "tds_margin": 0.30, "updated_at": null, "cal_id": null}`.

### 2.3 `POST /api/v1/devices/{device_id}/calibration` (admin)
Body `{"tds_baseline_ppm": 600, "tds_margin": 0.30}`, or `{"use_latest": true, "tds_margin": 0.30}`, which takes the device's latest TDS reading. Optional `cal_id` (defaults to today). Returns the same body as GET.
- `409` if `use_latest` is set and the device has no TDS reading.
- `422` if neither field is given, or the margin is outside 0–1.
- Every change is written to the evidence log (`kind: calibration`).

### 2.4 `GET /api/v1/devices/{device_id}/commands` — camera poll (every 2–3 s)
Returns the oldest unconsumed command and marks it consumed (clear on delivery): `{"cmd": "capture", "id": 12}`, or `{"cmd": "none"}`.

### 2.5 `POST /api/v1/devices/{device_id}/commands` (admin)
Body `{"cmd": "capture"}` → `{"queued": true, "id": 12, "cmd": "capture"}`.

### 2.6 `POST /api/v1/infer/ripeness` — camera → M1
Body: raw JPEG (≤ 5 MB) with device headers. The block comes from the device mapping (`cam-01` → `DEMO-A1`).
```json
{
  "label": "ripe", "confidence": 0.87,
  "probs": {"unripe": 0.03, "underripe": 0.06, "ripe": 0.87, "overripe": 0.04},
  "harvest_advice": "Harvest this round",
  "explanation": "Model attends to the upper of the image (top-20% heat), where the dominant colour is red/orange; 87% ripe vs 6% underripe.",
  "heatmap_url": "/static/heatmaps/ev_000124.png",
  "model_version": "m1-effb0-0.1",
  "evidence_id": "ev_000124",
  "needs_review": false,
  "image_url": "/media/images/ev_000124.jpg"
}
```
- **Final class list:** `unripe, underripe, ripe, overripe`.
- **Heat-map PNG:** original crop and CAM overlay side by side.
- **Errors:** `400` empty or undecodable image; `413` > 5 MB; `503` model not loaded (message says how to train it).
- **Harvest advice (M2 rule, round interval `SAWIT_HARVEST_ROUND_DAYS`, default 10):**
  - unripe → "Not ready — re-check in about two harvest rounds (~20 days)"
  - underripe → "Nearly ready — re-check next round (~10 days)"
  - ripe → "Harvest this round"
  - overripe → "Harvest immediately — loose-fruit and FFA risk; flag block for a shorter round"

## 3. Dashboard / application endpoints (read: open; write: admin)

| Method & path | Purpose | Response (main fields) |
|---|---|---|
| `GET /latest` | Dashboard poll (2 s) | `mode`, `server_time`, `soil[]` (`device_id, block_id, seq, buffered, received_at, captured_at, reading, recommendation, evidence_id, reviews, calibration`), `ripeness` (last result), `devices[]`, `evidence_count` |
| `GET /readings?device_id=&limit=` | Chart series, ordered by `captured_at` (buffered replays fall into place) | list of readings + `action` |
| `GET /evidence?limit=&block_id=&kind=&non_ok=` | Evidence log (newest first) | `evidence_id, created_at, kind, device_id, block_id, record, mspo[], prev_hash, hash` |
| `GET /evidence/{id}` | One record + its reviews | as above + `reviews[]` |
| `POST /evidence/{id}/review` (admin) | Human approve/override; appended as a new record (`kind: review`); overrides are flagged `retraining_candidate` | `{"decision":"approve|override","by":"...","note":"...","override_action":"watch"}` |
| `GET /evidence/verify` | Recompute the SHA-256 chain | `{"ok":true,"checked":44,"head":"…","message":"All 44 records intact"}` or `{"ok":false,"first_bad":"ev_000017",...}` |
| `GET /evidence/export?block_id=&since=` | **MSPO audit pack** (Markdown): chain status, clause coverage, decision table | `text/plain` |
| `GET /compliance/coverage?block_id=` | M7 clause coverage | `criteria[]` (`criterion, title, ref, records, last, status`), `chain` |
| `GET /harvest/plan?crew=` | Harvester allocation (SIMULATED estate) | `blocks[]` (`assigned_harvesters, harvester_days_needed, bunches_at_risk, status`), `bunches_at_risk_total`, `method`, `assumptions` |
| `GET /screening?z=-1.5&p=0.3` | Satellite → drone → ground cascade | `stage1_satellite.flagged[]`, `stage2_drone`, `stage3_ground.ranked[]` (`priority, dist_to_confirmed_m`) |
| `GET /satellite` | Pre-computed M5 NDVI panel | `blocks[]`, `months[]`, `estate_ndvi[]`, `image`, `source` |
| `GET /meta` | Thresholds, action list, model info | — |
| `GET /health` | Liveness | `{"status":"ok","version":"0.2.2","mode":"local","ripeness_model":…,"fertiliser_model":true}` |
| `GET /`, `GET /harvester` | Dashboard, mobile harvester view | HTML |

## 4. Evidence record (stored, hashed)

```json
{
  "evidence_id": "ev_000023", "created_at": "2026-12-10T09:00:03Z", "kind": "soil_recommendation",
  "device_id": "soilnode-01", "block_id": "DEMO-A1",
  "record": {"input": {...payload, "captured_at": "...", "ec_derived": true}, "received_at": "...",
             "calibration": {"device_cal_id": "2026-12-09", "tds_baseline_ppm": 592, "tds_margin": 0.3},
             "output": {...recommendation, "ml": {"model_version": "m6-tree-0.1", "probs": {...}, "attributions": [...]}},
             "rules_version": "INTERFACES-v0.2.2"},
  "mspo": ["TRACEABILITY", "SOIL_FERTILITY", "FERTILISER_RECORDS"],
  "prev_hash": "…", "hash": "sha256(prev_hash + canonical JSON of the fields above)"
}
```
`kind` ∈ `soil_recommendation | ripeness | calibration | review | ganoderma_screening`. MSPO tags map to MS 2530:2022 clauses (`compliance.py`): 4.1.3.1, 4.1.3.4, 4.1.3.5, 4.2.2, 4.5.4, 4.5.5.

## 5. Configuration (environment variables)

| Variable | Default (local) | Cloud |
|---|---|---|
| `SAWIT_MODE` | `local` | `cloud` (dashboard shows CLOUD; enables fail-closed auth) |
| `SAWIT_DEVICE_KEYS` | demo keys (local only) | **required**: `soilnode-01:<key>,cam-01:<key>` |
| `SAWIT_ADMIN_TOKEN` | empty (open) | **required** |
| `SAWIT_RUNTIME_DIR` / `SAWIT_DB` | `src/runtime/` | persistent path, e.g. `/home/data` on App Service |
| `SAWIT_MODEL` | `models/m1_ripeness.onnx` (+ `.json`) | deployed model path |
| `SAWIT_HARVEST_ROUND_DAYS` | 10 | — |
