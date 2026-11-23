# 02_hardware — README

## Status
**Step 2 deliverables written and pushed (23 Nov 2026).** Contract: `00_lead/INTERFACES.md` v0.2.1 (D25, D30).
Compile check: see "Verification notes" below. Bench test on real hardware still needed (only the person holding the parts can do it).
Audience (D23): demo, Verification and presentation — hardware detail does not go into the report.

## Inputs used
`00_lead/SPEC.md`, `PROJECT_PLAN.md`, `DECISIONS.md` (D17, D20, D21, D23–D30), `INTERFACES.md` v0.2.1, `components.md`,
`01_research/00_baseline_brief.md`, `05_hardware_notes.md`, `sources.md`.

## Outputs
| File | Content |
|---|---|
| `PLAN.md` | Approach, tasks, ideas, conflicts, proposals HW-P1…P9 with Lead rulings |
| `01_requirements_and_specs.md` | Demo objectives → O1/O3/O4, FR/NFR, component specs, demo → real deployment mapping (`[R-HW1]` placeholders) |
| `02_system_design.md` | Block + data-flow + wiring diagrams, pin map, netlist, pH divider, CAM role, power budget, placement |
| `03_bom.md` | Owned parts, approved purchases (D21, D27) ≈ RM44–84 |
| `firmware/soil_node/soil_node.ino` + `secrets.h.example` | All sensors, NVS calibration, OLED pages, LEDs, button, HTTPS POST + CLOUD/LOCAL decision, cloud→local base fallback, 30-reading offline buffer with replay, TDS baseline fetch |
| `firmware/cam_node/cam_node.ino` + `secrets.h.example` | Command-poll capture, local `/capture` + `/preview` page, capture on boot, raw JPEG POST |
| `firmware/.gitignore` | Keeps `secrets.h` out of git |
| `04_calibration.md` | Moisture dry/wet, pH 6.86/4.01 two-point + temperature slope, TDS compensation + backend baseline, log table |
| `05_demo_plan.md` | 2:30 script, setup timeline, fallbacks, pre-show checklist |
| `06_assembly_guide_beginner.md` | Tools, IDE/core/libraries, breadboard basics, one-sensor-at-a-time tests, flashing, troubleshooting |

## Pin map summary (NodeMCU ESP32)
Moisture 34 · pH (10 k/20 k divider) 35 · TDS 32 (power switched by 25) · DS18B20 4 · DHT22 16 · OLED 21/22 ·
LEDs G/A/R 18/19/23 · status LED 2 · button 27. Analog only on ADC1; no strapping pins used for inputs.

## Interface assumptions
- INTERFACES v0.2.1 as written; `GET /api/v1/devices/{id}/calibration` → `{tds_baseline_ppm, tds_margin, updated_at}` (D30).
- Commands endpoint: 200 with `{"cmd":"capture"}` triggers a capture; 204/empty/other = nothing. Server clears the command after delivery (assumed; no ack call).
- Node sends `ec_us_cm: null` (backend derives).

## Assumptions
- Default calibration constants are placeholders until bench calibration.
- Power figures in `02_system_design.md` §6 are estimates; verify with a USB meter.
- Purchase prices approximate/unverified.
- Root CA for the Azure endpoint must be exported on the day the URL exists (instructions in `secrets.h.example`).

## Verification notes
- Compile status: see the latest commit message / section below.
- Bench checks for the Verification pass: ADC1-only analog, pH pin ≤ 3.1 V, CAM brownouts on laptop USB, power-bank auto-off, offline buffer replay.

## Open issues for Lead
1. R-HW1 citations pending → fill `[R-HW1]` placeholders in `01_requirements_and_specs.md` §5.
2. Software: please confirm the command-endpoint semantics above (clear-on-delivery).

## Research requests
- R-HW1 (LoRaWAN/cellular field soil-node sources) — open in `01_research/REQUESTS.md`.

## New sources used
None (only keys from `01_research/sources.md`).
