# 01 — Demo Requirements & Component Specifications

> Owner: Hardware. Audience: demo team, Verification, Presentation (D23: not for the report body).
> Contract: `00_lead/INTERFACES.md` v0.2. Application name: **SawitSense** (D24).

## 1. Demo objectives (tied to outcomes)
| # | Objective | Outcome | Evidence the demo shows | Why it matters |
|---|---|---|---|---|
| DO1 | Turn live soil readings into an explained action (irrigate / drain / lime / fertilise / skip / watch / ok) | **O3** fertiliser optimisation, **O4** MSPO | Watering the pot flips IRRIGATE → OK; nutrient solution raises TDS and flips FERTILISE → OK/SKIP | Fertiliser ≈30 % of estate production cost [STAR-FERT2026]; oil-palm yield falls ~10 % per 100 mm soil-water deficit [CARR2011] |
| DO2 | Every reading is traceable (device, seq, calibration date, evidence id) | **O4** MSPO records | Dashboard evidence log row for each reading/decision | MSPO 2022 requires fertilising/soil-fertility SOPs and records [MPOCC-P21] |
| DO3 | Capture a bunch image at the "field edge" and get ripeness + explanation from the cloud model | **O1** ripe FFB harvest windows (and the same capture path serves **O2** imagery inference) | ESP32-CAM photo of a printed FFB → label + confidence + heatmap on dashboard | Labour shortage drives under-ripe harvesting [MA-POEB] [EDGE-LAB2026] |
| DO4 | Keep working when connectivity fails | Credibility | OLED shows LOCAL decision, readings buffered and replayed with `buffered:true` | Rural estates have patchy coverage; estate-wide connectivity is a recent investment [IOI2026] |

Out of scope: on-device ML inference, drone/satellite hardware, real fertiliser dosing.

## 2. Functional requirements
| ID | Requirement | Verified by |
|---|---|---|
| FR1 | Soil node reads moisture, pH, TDS, soil/solution temp, air temp/RH every 10 s (configurable `SEND_INTERVAL_MS`) | Serial log, dashboard |
| FR2 | pH read with TDS module powered **off** (GPIO25 low), TDS read with it on; DS18B20 temperature used for TDS compensation | Serial log shows order; `04_calibration.md` |
| FR3 | POST `application/json` to `{API_BASE}/api/v1/readings` with `X-Device-Id` + `X-Device-Key`, payload fields exactly as INTERFACES §2; failed sensor → `null` | Backend log / Verification |
| FR4 | Parse 200 response: show `oled[0..1]` and `led` tagged **CLOUD** (answered by `API_BASE`) or **LAN** (answered by `API_BASE_LOCAL`) | Demo |
| FR5 | On failure: compute local result from INTERFACES §4 thresholds and priority, show tagged **LOCAL**; TDS rules only if a baseline was received earlier; rules compare the same 1-decimal values the payload sends; moisture, pH and TDS all null → amber **NO DATA** in every mode (v0.2.3) | Unplug WiFi test |
| FR6 | Ring buffer of the last 30 unsent readings, replayed oldest-first with `buffered:true` and `age_s` **before** the fresh reading when the link returns; a 4xx-rejected reading is dropped and logged (never blocks the queue, never buffered) | Offline test |
| FR7 | Cloud URL tried first, `API_BASE_LOCAL` (laptop) second; while on LAN, retry the cloud every 5 min and switch back on success | Fallback drill |
| FR8 | Button short press = send now; long press (≥1.5 s) = next OLED page; very long press (≥5 s) on the calibration page = capture moisture dry/wet raw value to NVS | Demo, calibration |
| FR9 | OLED pages: (1) decision + reason, (2) all readings, (3) network/seq/cal_id | Demo |
| FR10 | Camera captures JPEG on (a) dashboard command poll `GET /api/v1/devices/cam-01/commands` every 2.5 s, (b) local `/capture` page, (c) once on boot; POSTs raw `image/jpeg` to `/api/v1/infer/ripeness` | Demo |
| FR11 | Secrets only in git-ignored `secrets.h` | `git ls-files` check |

## 3. Non-functional requirements
| ID | Requirement |
|---|---|
| NFR1 | All analog inputs on ADC1; no I/O on strapping pins 0/5/12/15 or flash pins 6–11 [ESPFAQ] |
| NFR2 | No ADC pin ever above 3.3 V: pH PO through 10 k/20 k divider (≤ ~2.5 V) [RAW-PH]; moisture on 3.3 V [DFR-SEN0193]; TDS 0–2.3 V [DFR-SEN0244] |
| NFR3 | End-to-end reading → OLED cloud result ≤ 3 s on a phone hotspot |
| NFR4 | Runs ≥ 60 min on the power bank (power budget in `02_system_design.md`) |
| NFR5 | Setup ≤ 10 min from bag to first reading (`05_demo_plan.md`) |
| NFR6 | TLS with pinned root CA for the cloud; plain HTTP only for the local laptop base URL (INTERFACES §1) |
| NFR7 | Rebuildable by a beginner using `06_assembly_guide_beginner.md` |
| NFR8 | Honest labelling: moisture is *relative* % of calibrated span; EC is derived; fertiliser decisions are simulated agronomy |

## 4. Component specifications
| Part (owned) | Role | Supply | Signal / interface | Key limits & notes | Source |
|---|---|---|---|---|---|
| NodeMCU ESP32 (ESP32-WROOM-32) | Soil node MCU, WiFi | 5 V USB → 3.3 V LDO | ADC1 GPIO32–39, I²C, 1-Wire | ADC2 unusable with WiFi; ADC error up to ±6 % → use `analogReadMilliVolts()` + averaging | [ESPFAQ] |
| Capacitive soil moisture v1.2 | Moisture | 3.3 V | Analog 0–3.0 V, inverse (dry = high) | Two-point dry/wet calibration; relative % only; protect PCB edge | [DFR-SEN0193] |
| pH electrode E-201-C + PH-4502C board | Slurry pH | **5 V** (VIN) | PO analog, offset 2.50 V @ pH 7, ≈ −0.18 V/pH | PO may exceed 3.3 V → divider; ±0.1 pH, ≤60 s settling; glass bulb — never into soil; store wet | [RAW-PH] [CIRKIT-PH] |
| TDS module (Gravity-style) | Nutrient proxy | 3.3 V (switched from GPIO25) | Analog 0–2.3 V | 0–1000 ppm, ±10 % FS @ 25 °C; needs external temperature; liquids only | [DFR-SEN0244] |
| DS18B20 waterproof probe | Solution/soil temp (TDS/pH compensation) | 3.3 V | 1-Wire + 4.7 kΩ pull-up | ±0.5 °C typical | [05_hardware_notes §2.4] |
| DHT22 | Air temp / RH | 3.3 V | Single-wire digital | ≥2 s between reads | [05_hardware_notes §2.4] |
| 0.96" OLED SSD1306 128×64 | Local display | 3.3 V | I²C 0x3C | 16 chars × 8 rows at text size 1 | [05_hardware_notes §2.4] |
| LEDs ×3 + on-board LED | Green/amber/red recommendation; WiFi/upload status | — | GPIO + 220–330 Ω | ~5–10 mA each | — |
| Push button | Send / page / calibrate | — | GPIO27 INPUT_PULLUP | Debounced in firmware | — |
| ESP32-CAM (AI-Thinker, OV2640) + USB base | Image capture + upload | 5 V from laptop USB (D26) | WiFi HTTPS | Brownouts on weak supply; VGA/SVGA JPEG; no on-device ML | [RNT-CAM] |
| Power bank (+ 2-port ≥2 A bought, D27) | Soil node supply | 5 V USB | — | Check auto-off at low load | [05_hardware_notes §2.6] |

## 5. Demo → real plantation deployment
Citations from research wave 2 (R-HW1, `01_research/07_field_evidence_and_naming.md`).

| Demo element | Real deployment | Notes |
|---|---|---|
| One breadboard soil node in a pot | Sealed (IP67/IP68) LoRaWAN field node per management block measuring moisture, temperature and EC, sensors at root depth, several per block | Commercial nodes of this class exist [MILESIGHT-EM500]; block-level fertiliser/liming records [MPOCC-P21]; Malaysian oil-palm ESP32 + LoRa soil-node prototype [RUSLAN2021] |
| Capacitive moisture probe | Calibrated volumetric soil-moisture probe (e.g. FDR/TDR) | Demo shows relative %, not VWC |
| Liquid pH/TDS probes in a slurry cup | Periodic lab soil sampling plus in-situ EC sensors; pH by slurry method in lab | Standard agronomic slurry method [05_hardware_notes §2.2] |
| WiFi to phone hotspot | LoRaWAN (AS923) radio to estate gateways, or 4G/NB-IoT where covered | Vendor range up to 15 km rural [MILESIGHT-EM500], but in a Malaysian oil-palm stand **each trunk costs 5.0–7.6 dB and each canopy 5.5–9.3 dB** → plan gateway spacing from plantation measurements [ANZUM2022]; NB-IoT coverage is regional, not nationwide [MAXIS-NBIOT]; IOI has >100 4G/LTE estate sites [IOI2026] |
| Power bank | Long-life battery (or solar) with duty-cycled sensing | Up to ~10 years at a 10-min interval on a 19,000 mAh Li-SOCl₂ cell (vendor lab figure, guideline only) [MILESIGHT-EM500]; optimised low-power agri nodes outlast commercial motes [BORRERO2020] |
| HTTPS POST to App Service | Gateway → LoRaWAN network server → **Azure IoT Hub** (device twins, downlinks) → Azure ML (report-facing, D20) | The Things Stack has a native Azure IoT Hub integration [TTS-AZURE] |
| ESP32-CAM on printed photo | Harvester's phone app / drone camera feeding the same inference API | Harvester allocation from ripeness (D28) |
| OLED + LEDs | Mandor/field supervisor mobile app with the same explained action | Same `oled`/`reason` text, multilingual (D28) |
