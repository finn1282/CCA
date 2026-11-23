# Interface Contract (HW ↔ SW) — v0.2.5 (agreed)

> Owner: Lead. v0.2 reconciles HW-P1–P5/P7 and SW-P2/P3 (D25). Hardware and Software MUST both conform.
> Change requests → your PLAN.md Proposals table; the Lead bumps the version here.
> Scope note: this is the **actual build**. Report-facing design may describe IoT Hub/MQTT (D20).

## 1. Transport & security
- Devices → **HTTPS POST** (JSON for soil node, raw JPEG for camera) to the backend (Azure App Service in the build; laptop local fallback).
- Headers on every device request: `X-Device-Id: <device_id>`, `X-Device-Key: <key>`.
- Secrets (WiFi, key, root CA, endpoint URL) live in **`secrets.h` (git-ignored)**; repo holds `secrets.h.example` only.
- TLS with pinned root CA certificate. Plain HTTP allowed **only** for the local-fallback base URL.
- Base URL configurable in `secrets.h`: `API_BASE` (cloud) and `API_BASE_LOCAL` (fallback).

## 2. Soil node → `POST /api/v1/readings`
Interval 10 s in demo mode (configurable); short button press = send now.
```json
{
  "device_id": "soilnode-01",
  "seq": 1532,
  "ts": "2026-12-10T09:00:00Z",
  "buffered": false,
  "block_id": "DEMO-A1",
  "soil_moisture_pct": 41.2,
  "soil_ph": 5.4,
  "tds_ppm": 620,
  "ec_us_cm": null,
  "soil_temp_c": 27.8,
  "air_temp_c": 30.1,
  "air_rh_pct": 78.5,
  "rssi_dbm": -61,
  "cal_id": "2026-12-09",
  "fw_version": "0.2.0"
}
```
- `ts` optional/null (no NTP) → server stamps `received_at`. `seq` monotonic; buffered replays send `buffered: true`.
- **v0.2.2:** optional `age_s` (int, seconds between capture and send; 0 for fresh readings). Server sets `captured_at = received_at − age_s` when `ts` is null. Firmware **replays the buffer before posting the fresh reading**; backend `/latest` uses the non-buffered reading with the highest `seq` (never a buffered replay).
- **v0.2.3:** `ts` must be ISO-8601 UTC (`…Z`); an unparseable `ts` is treated as null (server logs a warning), never stored as-is. `(device_id, seq)` with **identical values** is idempotent (returns the original response, no new evidence); the same `seq` with **different values** is stored as a new reading (so a device whose seq resets after reboot is not silenced) (v0.2.4).
- **Failed sensor → `null`, never a fabricated value.** `ec_us_cm` optional; backend derives EC ≈ TDS/0.5 and labels it approximate.
- `cal_id` = date of last calibration (feeds the evidence log audit trail, D18).

### Response (200) — recommendation returned synchronously
```json
{
  "action": "irrigate",
  "reason": "Soil moisture 24% < 30% threshold",
  "confidence": 0.9,
  "actions": [
    {"action": "irrigate", "severity": "high", "rule_id": "MOIST_LOW", "reason": "..."},
    {"action": "watch", "severity": "low", "rule_id": "PH_LOW_WATCH", "reason": "..."}
  ],
  "counterfactual": "Would be OK if moisture ≥ 30%",
  "simulated": false,
  "evidence_id": "ev_000123",
  "oled": ["IRRIGATE", "moist 24%<30%"],
  "led": "red"
}
```
- `action` = highest-priority entry of `actions[]`. `simulated: true` whenever the decision uses simulated agronomy (fertiliser).
- `oled`: 2 lines, ≤16 chars each. `led`: `green|amber|red`.
- Node tags the result by who answered: **CLOUD** (`API_BASE`), **LAN** (`API_BASE_LOCAL`, the laptop), or **LOCAL** (on-device §4 thresholds when both fail) (HW-P1, v0.2.2).
- Cloud-first: while on LAN, the node retries `API_BASE` every 5 min and switches back on success.
- A 4xx-rejected buffered reading is dropped and logged; it must not block the replay queue.
- If **all** sensors are null, the node shows amber `NO DATA` (never green OK) in every mode. LOCAL rules compare the same rounded values the payload sends (1 decimal), so LOCAL and CLOUD agree at thresholds.
- **One backend at a time (demo, D39):** the cloud and the laptop use the **same `SAWIT_DEVICE_KEYS`**; only one is the primary during the show and the dashboard is opened on that one.

## 3. Camera → `POST /api/v1/infer/ripeness`
- Body: raw `image/jpeg`; headers as §1.
- Triggers: (a) dashboard "Capture" button → camera polls `GET /api/v1/devices/{device_id}/commands` every 2–3 s and captures on `{"cmd":"capture"}`; (b) camera's local `/capture` web page (fallback, from the laptop); (c) one capture on boot/reset.
- Response:
```json
{
  "label": "ripe",
  "confidence": 0.87,
  "probs": {"unripe": 0.03, "underripe": 0.06, "ripe": 0.87, "overripe": 0.04},
  "harvest_advice": "Harvest this round",
  "explanation": "Heatmap focuses on fruitlet colour on the bunch surface",
  "heatmap_url": "/static/heatmaps/ev_000124.png",
  "model_version": "m1-effb0-0.1",
  "evidence_id": "ev_000124"
}
```
(Class names follow the trained dataset; Software publishes the final list.)

## 4. Shared thresholds & action vocabulary (D17 corrected, D25)
Actions: `ok | irrigate | drain | lime | fertilise | skip_fertiliser | watch`
**Priority:** `irrigate`/`drain` > `lime` > `fertilise`/`skip_fertiliser` > `watch` > `ok`

| Reading | Rule ID | Condition | Action | LED |
|---|---|---|---|---|
| soil_moisture_pct | MOIST_LOW | < 30 | irrigate | red |
| soil_moisture_pct | MOIST_HIGH | > 80 | drain | amber |
| soil_ph | PH_LIME | < 4.0 | lime | red |
| soil_ph | PH_LOW_WATCH | 4.0–4.2 | watch | amber |
| soil_ph | — | 4.2–6.5 | ok (5.5–6.5 noted "above typical oil-palm band, not harmful") | green |
| soil_ph | PH_HIGH | > 6.5 | watch ("check / stop liming") | amber |
| tds_ppm | TDS_LOW | below device baseline × (1 − margin) | fertilise (simulated agronomy) | amber |
| tds_ppm | TDS_HIGH | above device baseline × (1 + margin) | skip_fertiliser (simulated agronomy) | amber |

- Moisture thresholds are demo calibration values; pH bands from [KANANG2026] [AAR-SOIL] (see `01_research/05_hardware_notes.md`).
- TDS baseline + margin stored **per device in the backend**, set from the dashboard on the day (Software owns; default margin 30 %). Firmware LOCAL mode uses the last baseline received or skips TDS rules.
- pH and TDS probes read a soil-water slurry; firmware powers TDS off (GPIO25) while reading pH.

## 5. Other endpoints (Software publishes full spec in `03_software/05_api_spec.md`)
`GET /api/v1/latest`, `GET /api/v1/evidence/{id}`, `POST` **and `GET`** `/api/v1/devices/{id}/calibration` (v0.2.1: body/response `{"tds_baseline_ppm": number|null, "tds_margin": 0.30, "updated_at": "..."}`; GET used by the soil node at boot and **every 5 minutes** (v0.2.5, matches firmware `CAL_FETCH_MS`) to cache the baseline for LOCAL mode), `POST /api/v1/devices/{id}/commands`, `GET /api/v1/health`.
