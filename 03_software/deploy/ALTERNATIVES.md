# If Azure for Students access fails (internal only)

> The report and presentation still describe the Azure design (D15, D20). This page only covers how the **demo** runs if the student subscription is not available in time. Under D23 the report never mentions this.

## Decision ladder (use the first one that works)

| # | Option | What you get | Effort | Notes |
|---|---|---|---|---|
| **1** | **Laptop-local backend (first-class, already tested)** | Dashboard, API and evidence log on the presenting laptop. Devices use `API_BASE_LOCAL` over the venue/phone Wi-Fi | 5 min | No internet dependency. This is the default fallback in INTERFACES §1. Steps: `06_implementation_guide_beginner.md` §3–4 |
| 2 | Laptop + phone hotspot | Same as 1, but the devices and laptop join a phone hotspot you control. This avoids venue Wi-Fi client isolation | +5 min | Recommended even when Azure works, as plan B |
| 3 | Laptop + HTTPS tunnel (e.g. Cloudflare quick tunnel: `cloudflared tunnel --url http://localhost:8000`) | A temporary public HTTPS URL that forwards to the laptop, so remote viewers can open the dashboard | 10 min | The URL changes each run. Devices still use the LAN address. Set `SAWIT_MODE=cloud` with a token if the URL is shared |
| 4 | Another free container host (e.g. Render free web service, Hugging Face Spaces Docker) | A public URL without Azure | 30–60 min | Free tiers sleep when idle (cold start), and disks may not persist (the evidence log resets). Use the same env vars as `DEPLOY_AZURE.md` §4 |
| — | Paid cloud | — | — | Not allowed: no spending beyond confirmed free credits (brief) |

## What changes in each case
- **Firmware:** `API_BASE` stays as configured. If the cloud is unreachable, the node falls back to `API_BASE_LOCAL`, and its OLED shows LAN/LOCAL (INTERFACES v0.2.2).
- **Keys (S-02):** export the same `SAWIT_DEVICE_KEYS` on the laptop as in `secrets.h`. With no export, the laptop accepts only the demo keys `demo-soil-key` and `demo-cam-key`. That is fine only if the firmware was flashed with those keys.
- **One backend at a time (D39):** if you fall back to the laptop, also open the dashboard from the laptop (`http://localhost:8000`). A cloud dashboard cannot see readings sent to the LAN.
- **Model:** copy `models/m1_ripeness.onnx` and `.json` to the laptop. The backend loads them from `03_software/models/`.
- **Satellite panel:** once `gee/ndvi_estate.py` has run, `src/static/precomputed/satellite.json` and the PNG are committed, so the panel works offline. Until then it shows the labelled SIMULATED placeholder.

## What to tell the audience
Nothing changes in the story. The demo is "the SawitSense API". The report's deployment section describes the Azure target, and the demo is a scaled-down instance of the same API.
