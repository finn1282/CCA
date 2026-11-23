# 02_hardware — README

## Status
**Step 2 deliverables written and pushed (23 Nov 2026).** Contract: `00_lead/INTERFACES.md` **v0.2.3** (D25, D30, D33, D39). Soil firmware 0.2.3, camera 0.2.2. Verification Pass 1 fixes applied (see below).
Compile check: see "Verification notes" below. Bench test on real hardware still needed (only the person holding the parts can do it).
Audience (D23): demo, Verification and presentation — hardware detail does not go into the report.

## Inputs used
`00_lead/SPEC.md`, `PROJECT_PLAN.md`, `DECISIONS.md` (D17, D20, D21, D23–D39), `INTERFACES.md` v0.2.3, `07_verification/hardware/PASS_1_REPORT.md`, `components.md`,
`01_research/00_baseline_brief.md`, `05_hardware_notes.md`, `sources.md`.

## Outputs
| File | Content |
|---|---|
| `PLAN.md` | Approach, tasks, ideas, conflicts, proposals HW-P1…P9 with Lead rulings |
| `01_requirements_and_specs.md` | Demo objectives → O1/O3/O4, FR/NFR, component specs, demo → real deployment mapping (`[R-HW1]` placeholders) |
| `02_system_design.md` | Block + data-flow + wiring diagrams, pin map, netlist, pH divider, CAM role, power budget, placement |
| `03_bom.md` | Owned parts, approved purchases (D21, D27) ≈ RM44–84 |
| `firmware/soil_node/soil_node.ino` + `secrets.h.example` | All sensors, NVS calibration, OLED pages, LEDs, button, HTTPS POST + CLOUD/LOCAL decision, cloud→local base fallback, 30-reading offline buffer with replay, TDS baseline fetch |
| `firmware/cam_node/cam_node.ino` + `secrets.h.example` | Command-poll capture, local `/capture` + `/preview` page, capture on boot, raw JPEG POST, same cloud/LAN logic; both examples pin DigiCert Global Root G2 + Microsoft RSA Root CA 2017 |
| `firmware/.gitignore` | Keeps `secrets.h` out of git |
| `04_calibration.md` | Moisture dry/wet, pH 6.86/4.01 two-point + temperature slope, TDS compensation + backend baseline, log table |
| `05_demo_plan.md` | 2:30 script, setup timeline, fallbacks, pre-show checklist |
| `06_assembly_guide_beginner.md` | Tools, IDE/core/libraries, breadboard basics, one-sensor-at-a-time tests, flashing, troubleshooting |

## Pin map summary (NodeMCU ESP32)
Moisture 34 · pH (10 k/20 k divider) 35 · TDS 32 (power switched by 25) · DS18B20 4 · DHT22 16 · OLED 21/22 ·
LEDs G/A/R 18/19/23 · status LED 2 · button 27. Analog only on ADC1; no strapping pins used for inputs.

## Interface assumptions
- INTERFACES v0.2.2 as written; `GET /api/v1/devices/{id}/calibration` → `{tds_baseline_ppm, tds_margin, updated_at}` (D30); `tds_baseline_ppm: null` clears the node's cached baseline.
- Commands endpoint: `{"cmd":"capture"}` triggers a capture, `{"cmd":"none"}` = idle; clear-on-delivery confirmed by Verification INT-16.
- `age_s` is sent on every reading (0 when fresh).
- Node sends `ec_us_cm: null` (backend derives).

## Assumptions
- Default calibration constants are placeholders until bench calibration.
- Power figures in `02_system_design.md` §6 are estimates; verify with a USB meter.
- Purchase prices approximate/unverified.
- Root CA for the Azure endpoint must be exported on the day the URL exists (instructions in `secrets.h.example`).

## Verification notes
- Compile status: see the latest commit message / section below.
- Bench checks for the Verification pass: ADC1-only analog, pH pin ≤ 3.1 V, CAM brownouts on laptop USB, power-bank auto-off, offline buffer replay.

## Verification Pass 1 fixes (D33)
| ID | Fix | Files |
|---|---|---|
| D-01 | Three TDS cups: REFERENCE sets baseline, PLAIN → FERTILISE, NUTRIENT → SKIP | `04_calibration.md` §3, `05_demo_plan.md` |
| D-02 | Default pH constants 2.525 V (6.86) / 3.035 V (4.01); guide expects pH≈7.0 at PO 2.50 V | `soil_node.ino`, `06_…md` |
| D-03 | Pin self-signed DigiCert Global Root G2 (+ Microsoft RSA Root CA 2017 backup) with SHA-256 fingerprints, checked against the system trust store [AZ-CA] | both `secrets.h.example` |
| D-04 (HW side) | Buffer replayed before the fresh reading | `soil_node.ino` `cycle()` |
| D-05 | CLOUD/LAN/LOCAL tags; cloud retried every 5 min while on LAN (both nodes) | firmware, FR4/FR7, demo fallbacks |
| D-06 | 4xx: fresh reading not buffered; buffered entry dropped and logged | `soil_node.ino` |
| D-07 | Documented ADC accurate range 150–2450 mV [ESP32-DS] vs dry point; optional 10 k/33 k divider | `04_calibration.md` §1 |
| D-08 | Null/missing baseline clears cache + NVS | `fetchCalibration()` |
| D-09 | `age_s` added (v0.2.2) | `toJson()` |
| D-10 | Defined start state: probes in REFERENCE, pot dry → IRRIGATE only | `05_demo_plan.md` |
| D-11 | TDS troubleshooting line corrected | `06_…md` |

## v0.2.3 changes (D39)
- All soil sensors null → amber `NO DATA` in CLOUD/LAN/LOCAL (`showNoData()`).
- Readings rounded once at capture to 1 decimal; payload and LOCAL rules use the same values (pH and TDS now sent with 1 decimal).
- One key for both backends documented in both `secrets.h.example` files and the guide; one-backend-at-a-time demo rule in `05_demo_plan.md` §3.

## Open issues for Lead
1. R-HW1 citations pending → fill `[R-HW1]` placeholders in `01_requirements_and_specs.md` §5.
2. [ESP32-DS] and [AZ-CA] are cited in Hardware docs but not yet in `01_research/sources.md` (D33: Research to add).
3. Bench tests B-01…B-16 need the person holding the hardware.

## Research requests
- R-HW1 (LoRaWAN/cellular field soil-node sources) — open in `01_research/REQUESTS.md`.

## New sources used
- [ESP32-DS] Espressif *ESP32 Series Datasheet* v5.3 (ADC effective range) — key from `07_verification/hardware/TEST_PLAN.md`.
- [AZ-CA] Microsoft Learn *Azure Certificate Authority details* — key from `07_verification/hardware/TEST_PLAN.md`; root certificates fetched from cacerts.digicert.com and the Microsoft PKI repository on 23 Nov 2026.
