# Interface Contract (HW ↔ SW) — DRAFT v0

> Owner: Lead. Hardware and Software must both conform. Proposals for change go in your README
> "Open issues for Lead"; the Lead bumps the version here. Finalised at the Phase 2 gate.

## Transport (draft)
- ESP32 soil node → WiFi → **HTTPS POST JSON** (or MQTT if Software justifies it) to the ingestion endpoint chosen by Software.
- Interval: every 10 s in demo mode (configurable).
- Offline fallback: buffer last N readings, show status on OLED, red LED on failure.

## Soil node payload (draft)
```json
{
  "device_id": "soilnode-01",
  "ts": "2026-12-10T09:00:00Z",
  "block_id": "DEMO-A1",
  "soil_moisture_pct": 41.2,
  "soil_ph": 5.4,
  "tds_ppm": 620,
  "ec_us_cm": 1240,
  "soil_temp_c": 27.8,
  "air_temp_c": 30.1,
  "air_rh_pct": 78.5,
  "fw_version": "0.1.0"
}
```

## ESP32-CAM (draft)
- Captures JPEG on button press / HTTP trigger → POST `image/jpeg` to the inference endpoint → response `{ "label": "...", "confidence": 0.0-1.0, "explanation": "..." }` shown on dashboard.

## Recommendation response (draft)
`{ "action": "fertilise|irrigate|lime|ok", "reason": "...", "confidence": 0.0-1.0 }` → dashboard and optionally back to the node (OLED/LED).
