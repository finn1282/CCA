# Hardware Test Plan (SawitSense soil node + camera node)

> Owner: HW Verification. Contract under test: `00_lead/INTERFACES.md` **v0.2.4**.
> Status values: **pass** · **fail** · **blocked** (missing input) · **needs-hardware** (bench test for the parts holder) · **stakeholder build step** (compile/flash on the stakeholder's machine, D43/D44).
> Per-pass results are in `PASS_<n>_REPORT.md`.

**Last updated: Pass 2, 23 Nov 2026.** Versions checked:
- Firmware: `soil_node` 0.2.3 and `cam_node` 0.2.2 (`02_hardware` at `873a615`).
- Docs: 04–06.
- Backend: `03_software/src` at `47b18ff`.

**Sources:**
- [ESP32-DS]: Espressif (2025) *ESP32 Series Datasheet* v5.3, https://documentation.espressif.com/esp32_datasheet_en.pdf.
  - Allowed input voltage −0.3…3.6 V.
  - ADC atten 3 (11/12 dB): effective range 150–2450 mV.
  - I_OH 40 mA at V_OH ≥ 2.64 V.
- [ESPFAQ]
- [DFR-SEN0244]: 3.3–5.5 V, 3–6 mA, 0–2.3 V out.
- [DFR-SEN0193]
- [RAW-PH]
- [RNT-CAM]
- [AZ-CA]: Microsoft Learn *Azure Certificate Authority details*, https://learn.microsoft.com/en-us/azure/security/fundamentals/azure-ca-details.

## A. Electrical / pin correctness (static)
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| E-01 | ADC | All analog inputs on ADC1 | static | Moisture 34, pH 35, TDS 32 | pass | soil_node.ino:35-37 [ESPFAQ] |
| E-02 | Strapping | No GPIO0/2/5/12/15 misuse | static | GPIO2 is an LED output only; the others are unused | pass | pin map |
| E-03 | Flash pins | GPIO6–11 unused | static | unused | pass | pin map |
| E-04 | pH divider | 10 k/20 k gives 0.667 × PO | static | pH 0 → about 2.51 V at the pin. Worst case 5 V → 3.33 V, which is under 3.6 V [ESP32-DS] | pass | 02_system_design §3 |
| E-05 | pH ADC range | pH 3–8 inside 150–2450 mV | static | pH 4.01 → about 2.02 V | pass | [ESP32-DS] |
| E-06 | Moisture range | Dry point vs the linear ADC range | static | The dry point (2.6–3.0 V) is above 2450 mV. Accepted and documented, with an optional 10 k/33 k divider | pass (accepted, D-07) | 04_calibration.md §1 step 5 |
| E-07 | TDS range | 0–2.3 V ≤ 2450 mV | static | OK | pass | [DFR-SEN0244] |
| E-08 | TDS power on GPIO25 | Current vs GPIO drive | static | 3–6 mA ≪ 40 mA I_OH, so no transistor is needed. Bench check B-04 | pass | [DFR-SEN0244] [ESP32-DS] |
| E-09 | DS18B20 | 4.7 kΩ pull-up | static | present | pass | netlist |
| E-10 | DHT22 | 3V3, GPIO16, 10 k pull-up if bare | static | present. GPIO16 is free on WROOM-32 | pass | netlist |
| E-11 | OLED | I²C 21/22, 0x3C | static | matches | pass | soil_node.ino `setup()` |
| E-12 | LEDs | 220 Ω on 3.3 V GPIO | static | about 6 mA each | pass | pin map |
| E-13 | Button | GPIO27 INPUT_PULLUP to GND | static | OK | pass | soil_node.ino `setup()` |
| E-14 | Power budget | About 260 mA @ 5 V | static | Plausible; ≥ 60 min is easily met | pass | 02_system_design §6 |
| E-15 | CAM power | Laptop USB (D26), spare bank | static | Documented, with a brownout fallback | pass | 05_demo_plan §5 |

## B. Bench tests (needs-hardware: the parts holder runs them and records values here)
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| B-01 | pH PO max | Measure PO in 4.01 buffer and with the BNC shorted, with **PO disconnected** from the ESP32 | multimeter | PO ≤ 4.6 V (pin ≤ 3.1 V); offset 2.50 ± 0.05 V | needs-hardware | |
| B-02 | pH divider | Measure V35 with PO connected | multimeter | 0.667 × PO ± 2 % | needs-hardware | |
| B-03 | 3V3 rail | Measure under WiFi TX + TDS on | multimeter | 3.2–3.4 V | needs-hardware | |
| B-04 | TDS supply | Measure VCC at GPIO25 and the module current | multimeter (series) | ≥ 3.1 V, ≤ 10 mA. If < 3.0 V or > 12 mA, add a high-side PNP/P-MOSFET | needs-hardware | |
| B-05 | Moisture | `raw` in air / water | serial | Spread ≥ 800 mV; note whether dry is > 2450 mV | needs-hardware | |
| B-06 | Moisture % | Dry pot vs watered pot | serial/OLED | < 30 % / > 50 % | needs-hardware | |
| B-07 | pH 2-point | `cal ph686`, `cal ph401`, `cal show` | serial | Slope 0.16–0.19 V/pH; 6.86 re-read ± 0.1. Uncalibrated, PO 2.50 V reads pH ≈ 7.0 | needs-hardware | |
| B-08 | pH/TDS interference | pH in 6.86 buffer with the TDS probe out of the cup vs in the cup but unpowered | serial | Δ ≤ 0.1 pH, else use separate cups | needs-hardware | |
| B-09 | 3 TDS cups | REFERENCE → set baseline; PLAIN; NUTRIENT | OLED + dashboard | PLAIN < 0.7 × base → FERTILISE; NUTRIENT > 1.3 × base → SKIP FERTILISER; REFERENCE → OK. **REFERENCE pH 4.2–6.5** and **PLAIN pH ≥ 4.0** (D-15) | needs-hardware | |
| B-10 | Temperatures | DS18B20 vs DHT22 in still air | serial | within ±1 °C | needs-hardware | |
| B-11 | Null on failure | Unplug each sensor; then all three soil sensors | OLED/payload | `--`/`null` per sensor; all three null → amber **NO DATA** in CLOUD/LAN/LOCAL | needs-hardware | |
| B-12 | Power bank | 15 min idle | observe | Bank does not auto-off | needs-hardware | |
| B-13 | Battery | 60 min, USB meter | meter | ≤ 300 mA average, no resets | needs-hardware | |
| B-14 | CAM brownout | 10 captures on the stage laptop USB | serial | No brownout resets | needs-hardware | |
| B-15 | Boot with wiring | 5 power cycles | observe | Boots every time | needs-hardware | |
| B-16 | Button | Short / 1.5 s / 5 s on CALIB | observe | Send / page / dry-wet capture | needs-hardware | |
| B-17 | Base switching | Kill the cloud (or wrong `API_BASE`), laptop up; then restore the cloud | OLED tag | CLOUD → LAN within 1 cycle; back to CLOUD ≤ 5 min after restore | needs-hardware | |
| B-18 | Offline replay | WiFi off for 60 s, then on | serial + dashboard | `[buf] replayed … via` lines first, then the fresh reading. Dashboard latest = fresh. Chart points at their captured time (age_s) | needs-hardware | |

## C. Firmware vs INTERFACES v0.2.4 (static)
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| C-01 | Paths | readings, infer/ripeness, commands, calibration | static | exact | pass | soil_node.ino `cycle()`/`fetchCalibration()`; cam_node.ino `captureAndUpload()`/`pollCommands()` |
| C-02 | Headers | X-Device-Id/Key on every request | static | both nodes | pass | `httpRequest()` in both sketches |
| C-03 | Payload | 16 §2 fields + `age_s` | static | exact names; `age_s` = seconds since capture (fresh ≈ 2 s+, not literally 0; the backend only uses it when `ts` is null) | pass | soil_node.ino:319-335 |
| C-04 | Null | Failed sensor → null; ts/ec/rssi null rules | static | yes | pass | `jsonNum()`, `toJson()` |
| C-05 | seq | Monotonic over reboots (NVS steps of 10) | static | yes; `cal reset` keeps seq | pass | `loadPrefs()` |
| C-06 | Replay order | Buffer replayed **before** the fresh reading; `buffered:true` | static + INT-13 | yes | pass | soil_node.ino:381-388 |
| C-07 | 4xx handling | A rejected reading is not buffered; a rejected buffered reading is dropped | static | yes, but a 4xx from *either* base outranks a transport error on the other (D-13) | pass with defect D-13 | soil_node.ino:313,318,385,398 |
| C-08 | Tags | CLOUD (`API_BASE`) / LAN (`API_BASE_LOCAL`) / LOCAL | static | yes. If `API_BASE` == laptop URL, the laptop is tagged CLOUD (D-14) | pass with note | soil_node.ino:296-317,350-358 |
| C-09 | Cloud retry | While on LAN, `API_BASE` tried every 5 min | static | `cloudFirst` when `millis()-tLastCloudTry ≥ 300 s` | pass | soil_node.ino:296; cam_node.ino:116 |
| C-10 | NO DATA | All soil sensors null → amber NO DATA in every mode | static + INT-04 | LOCAL via `showNoData`; CLOUD/LAN overridden if the server disagrees | pass | soil_node.ino:228,355 |
| C-11 | Rounding | Values rounded once to 1 dp; LOCAL rules use the same values as the payload | static + INT-27 | yes (`r1()` at capture) | pass | soil_node.ino:213-214 |
| C-12 | LOCAL rules | §4 thresholds, LEDs, priority, strict compares | static | match backend | pass | `localDecision()` |
| C-13 | Calibration GET | Boot + 5 min; null/missing baseline clears the cache | static | yes (D-08 fixed) | pass | soil_node.ino:368-374 |
| C-14 | Camera | 2.5 s poll; `/`, `/capture`, `/preview`; boot capture; raw JPEG; via tag | static | yes | pass | cam_node.ino |
| C-15 | TLS | Pinned roots in the example; `setInsecure` only behind `ALLOW_INSECURE_TLS` | static + openssl | DigiCert Global Root G2 + Microsoft RSA Root CA 2017, both self-signed. SHA-256 fingerprints match the comments. Both examples are identical. G2 alone verifies a live `*.azurewebsites.net` chain (`Verify return code: 0`) | pass | secrets.h.example |
| C-16 | Secrets | `secrets.h` never committed, git-ignored | `git log --all --name-only`, `git check-ignore` | none in history | pass | firmware/.gitignore |
| C-17 | Shared key | One `DEVICE_KEY` for both bases (D39) | static | documented in the examples + guide | pass | secrets.h.example; guide §5 |
| C-18 | pH/TDS sequencing | TDS off during pH | static | yes | pass | `readPh()`/`readTds()` |

## D. Static logic review
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| L-01 | ADC | `analogReadMilliVolts`, 11 dB, averaging | static | per [ESPFAQ] | pass | `readMv()` |
| L-02 | Moisture % | Inverse two-point, clamp | static | correct | pass | `readMoisturePct()` |
| L-03 | pH | Two-point + Nernst T-slope | static | correct | pass | `readPh()` |
| L-05 | pH defaults | Consistent with 2.50 V @ pH 7 | static | V6.86 = 2.525, V4.01 = 3.035 → PO 2.50 V = pH 7.0 | pass (D-02 fixed) | soil_node.ino:60-61 |
| L-06 | TDS | DFRobot cubic + 2 %/°C | static | matches [DFR-SEN0244] | pass | `readTds()` |
| L-07 | Buffer | 30 entries, ring, drop oldest | static | bounded | pass | `bufferPush/Pop` |
| L-08 | Buffer head-of-line | 4xx entry dropped, transport/5xx stops replay until the next cycle | static | yes | pass (D-06 fixed) | soil_node.ino:381-388 |
| L-09 | WiFi reconnect | `wifiMulti.run(3000)` | static | OK | pass | `wifiEnsure()` |
| L-10 | Blocking/WDT | Worst-case cycle with 5 replays | static | No WDT risk; button may be missed during long cycles (accepted) | pass with note | `cycle()` |
| L-11 | Offline timestamps | `age_s` → server `captured_at` | static + INT-28 | yes | pass (D-09 fixed) | soil_node.ino:325 |
| L-12 | CAM buffers | PSRAM SVGA q12, 2 fb | static | OK | pass | `initCamera()` |
| L-13 | Compile-risk review of new code | ternary of string literals → `const char*`, `strcmp`, `prefs.remove`, String concatenation | static | No error found by reading | pass (static only) | soil_node.ino:296-317; cam_node.ino:114-129 |

## E. Compile (stakeholder build step, D43/D44: no ESP32 core is installed on this machine)
Commands run from the repo root on the stakeholder's machine, after copying `secrets.h.example` → `secrets.h` in each sketch folder:
```
arduino-cli config add board_manager.additional_urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core update-index && arduino-cli core install esp32:esp32
arduino-cli lib install "ArduinoJson" "Adafruit SSD1306" "Adafruit GFX Library" "OneWire" "DallasTemperature" "DHT sensor library" "Adafruit Unified Sensor"
arduino-cli compile --fqbn esp32:esp32:esp32    02_hardware/firmware/soil_node
arduino-cli compile --fqbn esp32:esp32:esp32cam 02_hardware/firmware/cam_node
arduino-cli core list; arduino-cli lib list      # record versions in PASS report
```

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| K-01 | soil_node | compile, ESP32 Dev Module | stakeholder build step | Ends with `Sketch uses N bytes (X%) of program storage space. Maximum is 1310720 bytes.` and no `error:`. Deprecation **warnings** (for example `ADC_11db`) are OK. If `Sketch too big`, choose Partition Scheme "Huge APP" (`--fqbn esp32:esp32:esp32:PartitionScheme=huge_app`) | stakeholder build step | record output + `core list`/`lib list` |
| K-02 | cam_node | compile, AI Thinker ESP32-CAM | stakeholder build step | Same success line, no `error:` | stakeholder build step | |
| K-03 | Libraries | Sketch header = guide §1 table | static | match (ArduinoJson **7.x** required: `JsonDocument` without a size) | pass | soil_node.ino:13-14; guide §1 |
| K-04 | Guide supports a first-time compile | Verify step, expected success line, error table | static | See D-17 | fail (D-17) | 06_assembly_guide_beginner.md §3, §5, §6 |

## F. Integration with the backend (`03_software/src` @ `47b18ff`, local uvicorn, port 8899, throw-away runtime dir)
The harness replays the firmware's exact requests:
- `toJson()` field order, including `age_s`
- `r1()` 1-dp rounding
- the replay-first order
- `applyCloudResponse()` parsing, including the NO DATA override

| ID | Area | Test | Expected | Status (Pass 2) |
|---|---|---|---|---|
| INT-01 | health | 200 | pass |
| INT-02 | Cal GET (none) | baseline null, margin 0.3 | pass |
| INT-03 | Dry pot | irrigate/red, `moist 24%<30%` | pass |
| INT-04 | All null | `NO DATA` amber | pass |
| INT-05 | Baseline from REFERENCE (`use_latest`) → device GET | 400.4 | pass |
| INT-21 | REFERENCE cup ≈ baseline | ok/green | pass |
| INT-22 | PLAIN (120 vs 400) | fertilise, amber, simulated | pass |
| INT-23 | NUTRIENT (900) | skip_fertiliser, amber | pass |
| INT-24 | Exactly 0.7×/1.3× | ok (strict compares, same as firmware) | pass |
| INT-25 | REFERENCE at pH 7.2 (tap water) | watch, so green at 0:35 is not guaranteed | pass (confirms D-15) |
| INT-26 | PLAIN with pH drifting to 3.9 | lime outranks fertilise | pass (confirms D-15) |
| INT-08…11 | Priority and bands | as §4 | pass |
| INT-27 | Rounding at thresholds (29.96 %, pH 3.96) | 30.0 ok; 4.0 watch | pass |
| INT-13 | Replay-first then fresh | `/latest` = fresh | pass (D-04 fixed) |
| INT-13b | Late buffered replay | never replaces latest | pass |
| INT-28/29/30 | `age_s` → captured_at; ts wins; bad ts → null | as v0.2.2/v0.2.3 | pass |
| INT-31 | Same seq + same values (retry as buffered, new age_s) | `duplicate:true`, same evidence_id, no new evidence | pass |
| INT-32 | Same seq, different values | new reading + evidence | pass |
| INT-33 | seq restarts low (NVS erased) | `/latest` follows the newest reading | **fail (D-16)** |
| INT-14/18/34 | Wrong key 401; id mismatch 400; moisture 150 → 422 | as stated | pass |
| INT-35 | Dashboard clears the baseline | null accepted | n/a: the backend has no clear operation (422). The firmware D-08 path is reachable only if a future backend returns null |
| INT-15/16 | Command poll idle; one-shot capture | `none`; `capture` once | pass |
| INT-17 | Ripeness raw JPEG (D2 image, 317 kB) | label/confidence/harvest_advice/evidence_id | pass (provisional M1: `ripe`, 0.992) |
| INT-36 | Empty JPEG | 400 | pass |
| INT-19 | TLS to the real Azure URL from the ESP32 | 200 over HTTPS with the pinned roots | blocked (no Azure URL; host-side openssl check passes, C-15) |
| INT-20 | Stage-network end-to-end | Cloud ≤ 3 s, LAN fallback, offline replay | needs-hardware |

## G. Demo & guide review
| ID | Area | Test | Expected | Status | Evidence |
|---|---|---|---|---|---|
| G-01 | Fallbacks | WiFi, cloud down, TLS, no net, capture, brownout, NO DATA, video | present | pass | 05_demo_plan §5 |
| G-02 | 3-cup TDS logic | Baseline cup ≠ trigger cups; matches backend rules | yes | pass (D-01 fixed; INT-21…24) | 04_calibration §3; 05_demo_plan §2 |
| G-03 | Start state | Probes in REFERENCE → post-watering OK/green | Defined. Green depends on REFERENCE pH being 4.2–6.5 (D-15) | pass with note | 05_demo_plan.md:17-19 |
| G-04 | One backend at a time | Primary chosen, same keys, dashboard on primary | documented | pass | 05_demo_plan §3 |
| G-05 | Beginner wiring guide | Sensor-by-sensor expected values | corrected (D-02, D-11) | pass | guide §4 |
| G-06 | Beginner compile guidance | Can a first-time user catch compile errors? | Not yet (D-17) | fail | guide §3, §5, §6 |
