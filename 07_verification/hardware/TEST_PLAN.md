# Hardware Test Plan (SawitSense soil node + camera node)

> Owner: HW Verification. Contract under test: `00_lead/INTERFACES.md` **v0.2.1**.
> Items checked: `02_hardware/` docs 01–06 and `firmware/` at commit `de357ab` (firmware unchanged at `4fc0758`), backend `03_software/src` at `305bb47`.
> Status values: **pass** · **fail** · **blocked** (missing input) · **needs-hardware** (bench test the person holding the parts must run).
> Last updated: Pass 1, 23 Nov 2026. The results per pass are in `PASS_<n>_REPORT.md`.

Sources for the electrical limits:
- [ESP32-DS]: Espressif (2025) *ESP32 Series Datasheet* v5.3, Table 5-1 and Table 5-3, and the ADC characteristics. https://documentation.espressif.com/esp32_datasheet_en.pdf. Figures used here: allowed input −0.3…3.6 V; ADC atten 3 (11/12 dB) effective range **150–2450 mV**; I_OH 40 mA at V_OH ≥ 2.64 V.
- [ESPFAQ] (ADC2 is not usable while WiFi runs; strapping pins).
- [DFR-SEN0244]: TDS module, 3.3–5.5 V supply, **3–6 mA** working current, 0–2.3 V output.
- [DFR-SEN0193]: capacitive moisture sensor.
- [RAW-PH]: PH-4502C board, 5 V, about 2.5 V at pH 7, about 0.18 V/pH.
- [RNT-CAM]: ESP32-CAM brownouts.
- [AZ-CA]: Microsoft (2026) *Azure Certificate Authority details*. https://learn.microsoft.com/en-us/azure/security/fundamentals/azure-certificate-authority-details.

New keys still to be added to `01_research/sources.md`: [ESP32-DS] and [AZ-CA].

## A. Electrical / pin correctness (static)
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| E-01 | ADC | Every analog input is on ADC1 | static | Moisture 34, pH 35 and TDS 32 are all ADC1 | pass | soil_node.ino:35-37; 02_system_design §3 [ESPFAQ] |
| E-02 | Strapping | Nothing drives GPIO0/2/5/12/15 at boot | static | GPIO2 is used only as the on-board LED output. 0, 5, 12 and 15 are unused | pass | soil_node.ino:44; pin map |
| E-03 | Flash pins | GPIO6–11 unused | static | unused | pass | pin map |
| E-04 | pH divider | 10 k/20 k gives V_pin = 0.667 × PO | static | PO at pH 0 is about 3.76 V, giving about 2.51 V at the pin. PO at 5 V (rail) gives 3.33 V, still under the 3.6 V abs max [ESP32-DS]. LM358-class output cannot reach 5 V | pass | 02_system_design §3 |
| E-05 | pH ADC range | pH 3–8 sits inside the 150–2450 mV ADC range | static | pH 4.01 (about 3.03 V PO) gives about 2.02 V at the pin, which is inside the range | pass | [ESP32-DS] ADC table |
| E-06 | Moisture range | Dry point inside the linear ADC range | static | The default and expected dry point is 2.6–3.0 V. That is above 2450 mV, where the ADC is non-linear | fail (minor, D-07) | soil_node.ino:57; 04_calibration.md:18 |
| E-07 | TDS range | Output 0–2.3 V is ≤ 2450 mV | static | OK | pass | [DFR-SEN0244] |
| E-08 | TDS power from GPIO25 | Module current vs GPIO drive | static | 3–6 mA [DFR-SEN0244] is well under the 40 mA I_OH [ESP32-DS], so **no transistor is needed**. V_OH may sag slightly below the module's 3.3 V minimum. Check this in B-04 | pass | soil_node.ino:38,183 |
| E-09 | DS18B20 | 4.7 kΩ pull-up DQ→3V3 | static | Present | pass | netlist; guide step 4 |
| E-10 | DHT22 | 3V3, GPIO16, 10 k pull-up if bare sensor | static | Present. GPIO16 is free on the WROOM-32 (it is PSRAM only on WROVER) | pass | netlist; guide step 5 |
| E-11 | OLED | I²C SDA 21 / SCL 22, 0x3C | static | Matches | pass | soil_node.ino:498-499 |
| E-12 | LEDs | 220 Ω from a 3.3 V GPIO | static | (3.3 − about 2.0 V)/220 Ω ≈ 6 mA per LED, which is within drive limits | pass | 02_system_design §3 |
| E-13 | Button | GPIO27 INPUT_PULLUP to GND; GPIO27 is not a strapping pin | static | OK | pass | soil_node.ino:489 |
| E-14 | Power budget | Soil node about 260 mA at 5 V on the bank | static | Plausible. pH board about 0.5 W = 100 mA [RAW-PH]. ≥ 60 min is easily met | pass | 02_system_design §6 |
| E-15 | CAM power | ESP32-CAM on laptop USB (D26), with a spare 2-port bank | static | Documented. Brownout fallback is in the demo plan | pass | 05_demo_plan §4 |

## B. Bench tests (needs-hardware: run by the parts holder, record values here)
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| B-01 | pH PO max | With the pH board on 5 V and PO **disconnected**, measure PO in the 4.01 buffer and with the BNC shorted | bench (multimeter) | PO ≤ 4.6 V, so the pin stays ≤ 3.1 V. Offset is 2.50 ± 0.05 V with the BNC shorted | needs-hardware | |
| B-02 | pH divider | With PO connected, measure GPIO35 | bench | V35 = 0.667 × PO ± 2 % | needs-hardware | |
| B-03 | 3V3 rail | Measure 3V3 at full load (WiFi TX + TDS on) | bench | 3.2–3.4 V | needs-hardware | |
| B-04 | TDS supply | Measure TDS VCC at GPIO25 while it is on, and the module current | bench (multimeter in series) | ≥ 3.1 V, ≤ 10 mA. If VCC is < 3.0 V or the current is > 12 mA, add a PNP/P-MOSFET high-side switch | needs-hardware | |
| B-05 | Moisture | Raw mV in air and in water (`raw` command) | bench | Spread ≥ 800 mV. Note whether dry is > 2450 mV (D-07) | needs-hardware | |
| B-06 | Moisture % | Dry pot / just watered | bench | < 30 % / > 50 % | needs-hardware | |
| B-07 | pH 2-point | `cal ph686`, `cal ph401`, `cal show` | bench | Slope 0.16–0.19 V/pH. Re-reading the 6.86 buffer gives 6.86 ± 0.1 | needs-hardware | |
| B-08 | pH/TDS interference | Read pH in the 6.86 buffer with the TDS probe (a) out of the cup, (b) in the cup unpowered | bench | Difference ≤ 0.1 pH. If it is larger, use separate cups | needs-hardware | |
| B-09 | TDS | PLAIN (distilled), REFERENCE and NUTRIENT cups | bench | Monotonic rise. NUTRIENT > 1.3 × REFERENCE. Distilled < 0.7 × REFERENCE (see D-01) | needs-hardware | |
| B-10 | Temperatures | DS18B20 vs DHT22 in still air after 5 min | bench | Within ±1 °C | needs-hardware | |
| B-11 | Null on failure | Unplug each sensor in turn | bench | OLED shows `--` and the payload field is `null`, with no other field affected | needs-hardware | |
| B-12 | Power bank | Soil node on the bank, idle 15 min | bench | Bank does not auto-off | needs-hardware | |
| B-13 | Battery | 60 min run on the bank, USB meter | bench | ≤ 300 mA average, no resets | needs-hardware | |
| B-14 | CAM brownout | CAM on the stage laptop USB, 10 captures with WiFi on | bench | No "Brownout detector" resets | needs-hardware | |
| B-15 | Boot with wiring | Power-cycle the fully wired node 5× | bench | Boots every time (no strapping problem) | needs-hardware | |
| B-16 | Button | Short / 1.5 s / 5 s on the CALIB page | bench | Send / page / dry-wet capture | needs-hardware | |

## C. Firmware vs INTERFACES v0.2.1 (static)
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| C-01 | Paths | `/api/v1/readings`, `/infer/ripeness`, `/devices/{id}/commands`, `/devices/{id}/calibration` | static | Exact | pass | soil_node.ino:338,354; cam_node.ino:132,150 |
| C-02 | Headers | X-Device-Id and X-Device-Key on every request | static | Both nodes, all requests | pass | soil_node.ino:268-269; cam_node.ino:103-104 |
| C-03 | Payload fields | All 16 §2 fields, same names | static | Exact match | pass | soil_node.ino:296-311 |
| C-04 | Types/null | Failed sensor gives NAN, which becomes `null`. `ts` is null without NTP. `ec_us_cm` is null. `rssi_dbm` is null when disconnected | static | Yes | pass | soil_node.ino:119-121,299,305,309 |
| C-05 | seq | Monotonic across reboots (NVS, steps of 10) | static | Yes. Reasoned through the reboot cases | pass | soil_node.ino:147-151,196 |
| C-06 | buffered | Replays send `buffered:true`, oldest first | static | Yes | pass | soil_node.ino:368-374 |
| C-07 | cal_id | Sent every time. Default is `"uncalibrated"` | static | Accepted by the backend (free string) | pass | soil_node.ino:63,310; INT-04 |
| C-08 | Response parse | action, oled[0..1], led, evidence_id, reason fallback | static + integration | Yes | pass | soil_node.ino:319-333; INT-03…12 |
| C-09 | LOCAL rules | §4 thresholds, LEDs, priority irrigate/drain > lime > fertilise/skip > watch > ok | static | Match. TDS rules only run when a baseline is cached | pass | soil_node.ino:67-68,213-236 |
| C-10 | CLOUD vs LOCAL tag | CLOUD on a 200 response, LOCAL on failure | static | Yes. However, a laptop-served result is also tagged CLOUD, and the local base stays preferred (D-05) | pass with note | soil_node.ino:279,288,327 |
| C-11 | Base order | Cloud first, then `API_BASE_LOCAL` | static | Cloud first only until local succeeds once. After that local is "sticky" (D-05) | fail (minor) | soil_node.ino:279-289; cam_node.ino:113-118 |
| C-12 | Calibration GET | At boot + every 5 min, cached in NVS | static | Yes. A null baseline does not clear the cache (D-08) | pass with note | soil_node.ino:334-347,510,525 |
| C-13 | Camera poll | Poll every 2.5 s, capture on `{"cmd":"capture"}` | static | Yes | pass | cam_node.ino:46,147-156 |
| C-14 | Camera triggers | Local `/capture` page and capture on boot | static | Yes (`/`, `/capture`, `/preview`) | pass | cam_node.ino:159-195 |
| C-15 | JPEG upload | Raw `image/jpeg` body | static | Yes | pass | cam_node.ino:106 |
| C-16 | TLS | Pinned root CA; `setInsecure` only behind the `ALLOW_INSECURE_TLS` switch; plain HTTP only for non-https bases | static | Yes. The CA export instruction is misleading (D-03) | pass with note | soil_node.ino:255-264; secrets.h.example:21-24 |
| C-17 | Secrets | `secrets.h` is git-ignored and never committed | static (`git log --all --name-only`, `git check-ignore`) | No `secrets.h` anywhere in history. Ignored in both sketch folders | pass | firmware/.gitignore:2 |
| C-18 | pH/TDS sequencing | TDS is unpowered while pH is read | static | GPIO25 LOW and 300 ms wait before pH. TDS is powered only for its own read | pass | soil_node.ino:168-169,183-186 |

## D. Static logic review
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| L-01 | ADC | `analogReadMilliVolts`, 11 dB, 32–128 samples | static | Follows [ESPFAQ] | pass | soil_node.ino:113-118,490-493 |
| L-02 | Moisture % | (dry − mV)/(dry − wet) × 100, clamped | static | Correct for inverse output | pass | soil_node.ino:154-160 |
| L-03 | pH 2-point | slope = (V4.01 − V6.86)/2.85; pH = 6.86 + (V6.86 − V)/slope_T | static | Correct, checked by hand: V = V4.01 gives 4.01 | pass | soil_node.ino:167-181 |
| L-04 | pH temp comp | slope × (T+273.15)/(Tcal+273.15) | static | Correct Nernst scaling | pass | soil_node.ino:177 |
| L-05 | pH defaults | Default constants agree with the 2.50 V @ pH 7 offset | static | They do not. The defaults put pH 7 at about 2.30 V (D-02) | fail (minor) | soil_node.ino:59-60 |
| L-06 | TDS formula | DFRobot cubic × 0.5, 2 %/°C compensation, DS18B20 T (25 °C if T fails) | static | Matches [DFR-SEN0244] | pass | soil_node.ino:182-193 |
| L-07 | Buffer | 30 entries, ring, drop oldest | static | Bounded | pass | soil_node.ino:91-93,315-318 |
| L-08 | Buffer HOL | A 4xx-rejected reading is buffered and blocks the replay queue | static | It should be dropped (D-06) | fail (minor) | soil_node.ino:355-374 |
| L-09 | WiFi reconnect | `wifiMulti.run(3000)` every cycle when down | static | Reconnects. Blocks ≤ 3 s | pass | soil_node.ino:239-247 |
| L-10 | Blocking / WDT | Worst-case cycle: sensors ~2.2 s + WiFi 3 s + 2 bases × (4+4) s + 5 replays | static | No task-WDT trip (the loop task is not WDT-subscribed by default; HTTP yields). The button can be missed during long cycles | pass with note | soil_node.ino:50,348-375 |
| L-11 | Buffered timestamps | Buffered readings without NTP get the server time of the replay | static | Audit-trail time is wrong (D-09) | fail (minor) | soil_node.ino:133,299 |
| L-12 | CAM frame buffers | PSRAM → SVGA q12, 2 fb, GRAB_LATEST | static | OK on the AI-Thinker board (has PSRAM) | pass | cam_node.ino:67-68 |

## E. Compile
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| K-01 | soil_node | `arduino-cli compile --fqbn esp32:esp32:esp32 02_hardware/firmware/soil_node` with `secrets.h` copied from the example | compile | 0 errors | blocked (Pass 1) | ESP32 core not yet installed: Hardware's `core install esp32:esp32` was still downloading into the shared `~/.arduino15` |
| K-02 | cam_node | `arduino-cli compile --fqbn esp32:esp32:esp32cam 02_hardware/firmware/cam_node` | compile | 0 errors | blocked (Pass 1) | same |
| K-03 | Libraries | Names/versions in the sketch header = guide §1 table | static | ArduinoJson 7.x, Adafruit SSD1306/GFX, OneWire, DallasTemperature, DHT sensor library, Adafruit Unified Sensor | pass | soil_node.ino:13-14; 06_guide §1 |

## F. Integration with the backend (`03_software/src`, local uvicorn)
Harness: a Python script that sends the firmware's exact payload (field order and rounding copied from `toJson()`) and headers, then parses the response with the same rules as `applyCloudResponse()`, `fetchCalibration()` and `pollCommands()`. The server ran with default demo keys and a throw-away runtime dir.

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| INT-01 | health | `GET /api/v1/health` | integration | 200 | pass | PASS_1 §4 |
| INT-02 | Cal GET (none) | Device GET before a baseline is set | integration | 200 `{tds_baseline_ppm:null, tds_margin:0.3, updated_at}` | pass | |
| INT-03 | Dry pot | moist 24 | integration | irrigate / red / `IRRIGATE`,`moist 24%<30%` | pass | |
| INT-04 | All null | All sensors null, cal_id "uncalibrated" | integration | 200, parseable | pass | `NO DATA` / amber |
| INT-05 | Cal POST→GET | Dashboard sets 400 ppm, device reads it back | integration | 400 / 0.30 | pass | |
| INT-06/07 | TDS rules | 900 / 100 ppm vs 400 | integration | skip_fertiliser / fertilise, amber, `simulated:true` | pass | |
| INT-08 | Priority | moist 20 + pH 3.8 + TDS 900 | integration | irrigate, actions [irrigate, lime, skip] | pass | |
| INT-09…12 | Bands | lime / watch (6.9, 4.1) / drain / ok | integration | Colours as §4 | pass | |
| INT-13 | Buffered replay | Fresh seq 1550, then buffered seq 1545 (the firmware's order) | integration | `/latest` shows 1550 | **fail (major, D-04)** | `/latest` shows 1545 |
| INT-14 | Auth | Wrong key | integration | 401 | pass | |
| INT-15/16 | Commands | Idle poll, then queue → poll → poll | integration | `none`, then `capture` once, then `none` | pass | |
| INT-17 | Ripeness | Raw JPEG upload | integration | 200 with label/confidence/evidence_id | blocked | 503: `m1_ripeness.onnx` not trained yet |
| INT-18 | Mismatch | Body device_id ≠ header | integration | 400 | pass | |
| INT-19 | TLS to Azure | Node → real `API_BASE` with the pinned CA | needs-hardware | 200 over HTTPS | blocked | No Azure URL yet |
| INT-20 | Stage network E2E | Both nodes on the presenter's hotspot, cloud + local fallback drill, WiFi-off buffer drill | needs-hardware | Cloud 200 in ≤ 3 s (NFR3); LOCAL tag when the cloud is down; buffered replay appears with `buffered:true` | needs-hardware | |

## G. Demo & guide review
| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| G-01 | Fallbacks | WiFi loss, cloud down, TLS error, no network, CAM brownout, capture failure, video | static | All present | pass | 05_demo_plan §4 |
| G-02 | TDS demo logic | The baseline cup and the "FERTILISE" cup are different | static | They are the same cup (PLAIN), so the beat shows OK | **fail (major, D-01)** | 05_demo_plan.md:18,32; 04_calibration.md:59-61 |
| G-03 | Demo start state | Probe positions defined before 1:00 | static | Undefined: the post-watering action is not deterministic (D-10) | fail (minor) | 05_demo_plan.md:16-17 |
| G-04 | Beginner guide | One sensor at a time, expected values, troubleshooting | static | Complete. Two wrong expected values (D-02, D-11) | pass with notes | 06_assembly_guide_beginner.md:43-47 |
| G-05 | Soil node power fallback | Bank auto-off / brownout on stage | static | Covered by the checklist (15 min test) but not in the fallback table | pass with note | 05_demo_plan §5 |
