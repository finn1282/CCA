# HW Verification — Pass 1 Report (23 Nov 2026)

## 1. Scope
Contract: `00_lead/INTERFACES.md` v0.2.1 (D25, D30).

Reviewed:
- `02_hardware/` README, PLAN, docs 01–06, `firmware/soil_node`, `firmware/cam_node`, and both `secrets.h.example` files, at `de357ab` (firmware unchanged at `4fc0758`).
- Backend `03_software/src` at `305bb47`, run locally on port 8899 and stopped afterwards.

Test IDs refer to `TEST_PLAN.md`.

## 2. Summary
| Area | Result |
|---|---|
| Electrical / pins (static) | **Pass.** All analog inputs are on ADC1, no strapping pins are misused, and the pH divider is safe (≤ 2.5 V typical, 3.33 V worst case against the 3.6 V abs max [ESP32-DS]). GPIO25 can drive the TDS module without a transistor (3–6 mA [DFR-SEN0244] vs 40 mA I_OH [ESP32-DS]). One minor ADC-range note (D-07). |
| Firmware vs contract | **Pass.** Paths, headers, all 16 payload fields, null handling, seq/buffered/cal_id, response parsing, LOCAL rules and priority, calibration GET, camera poll + `/capture` + boot capture, and TLS pinning all match. Minor deviations: D-05, D-06, D-08, D-09. |
| Secrets | **Pass.** No `secrets.h` anywhere in git history (`git log --all --name-only`). `git check-ignore` confirms both sketch folders are ignored. The only PEM blocks in history are the `REPLACE_WITH_ROOT_CA` placeholders. |
| Compile | **Blocked.** The ESP32 core is not installed yet: Hardware's `arduino-cli core install esp32:esp32` was still downloading into the shared `~/.arduino15`. I did not start a second install, to avoid concurrent writes. |
| Integration (backend) | **16/18 pass, 1 fail (D-04, major), 1 blocked** (ripeness model not trained → 503). |
| Demo plan / guide | Fallbacks are complete. **One major demo-logic defect (D-01)** and minor fixes in the guide. |
| Bench tests | 16 bench tests defined (B-01…B-16, INT-19/20). All are needs-hardware. |

## 3. Defects
| ID | Severity | File:line | Issue | Suggested fix | Owner | Status |
|---|---|---|---|---|---|---|
| D-01 | **major** | `02_hardware/05_demo_plan.md:18,32`; `04_calibration.md:59-61` | The TDS baseline is set from the **PLAIN** cup (T−8 min), and the 1:00 beat then expects that same PLAIN cup to show **FERTILISE**. A reading equal to the baseline is inside ±30 %, so the node shows **OK** and the demo beat fails. | Use three cups. **REFERENCE** (leachate + a small pinch of NPK) sets the baseline. **PLAIN** (distilled water) must read < 0.7 × baseline, giving FERTILISE. **NUTRIENT** must read > 1.3 × baseline, giving SKIP. Update the script, the setup timeline and the calibration §3 steps 1–3, then rehearse with B-09. | Hardware | open |
| D-04 | **major** | `soil_node.ino:367-374` (replay runs *after* the fresh POST); `03_software/src/app/main.py:220` (`/latest` = `MAX(id)` per device) | After a reconnect, the firmware posts the fresh reading first and then replays older buffered ones. The backend treats the last-inserted row as "latest", so the dashboard shows a **stale buffered reading and its recommendation**. Confirmed in INT-13: fresh seq 1550 was sent, `/latest` returned seq 1545. | Backend (primary): exclude `buffered=1` rows from `/latest`, or pick the row with the max `seq` per device. Firmware (optional): replay the buffer before the fresh reading. | Software (+ Hardware optional) | open |
| D-02 | minor | `soil_node.ino:59-60`; `06_assembly_guide_beginner.md:47` | The default pH constants (V6.86 = 2.320, V4.01 = 2.830) put pH 7 at about 2.30 V, but §2.1 sets the offset to 2.50 V at pH 7. An uncalibrated board in the 6.86 buffer at PO 2.48 V computes **pH ≈ 5.97**, not the "pH = 6.9" the guide promises, which will confuse a beginner. | Set `DEF_PH_V686 = 2.525` and `DEF_PH_V401 = 3.035` (0.18 V/pH around 2.50 V @ pH 7 [RAW-PH]), or change the guide's expected value. | Hardware | open |
| D-03 | minor | `firmware/*/secrets.h.example:21-24` | "Copy the LAST certificate in the chain (the root)" is inaccurate. A live `openssl s_client` to `*.azurewebsites.net` on 23 Nov 2026 showed this chain: leaf → *Microsoft TLS G2 RSA CA OCSP 10* → *Microsoft TLS RSA Root G2* **cross-signed by DigiCert Global Root G2**. The last cert sent is therefore a cross-sign, not a self-signed root. Pinning it probably works with mbedTLS, but it is the wrong thing to pin, and it changes when Microsoft re-chains. | Pin **DigiCert Global Root G2** (self-signed, from [AZ-CA]: `https://cacerts.digicert.com/DigiCertGlobalRootG2.crt`, converted to PEM). Optionally concatenate *Microsoft RSA Root Certificate Authority 2017* as a backup ([AZ-CA] lists both as Azure roots). Verify with INT-19. | Hardware | open |
| D-05 | minor | `soil_node.ino:279,288,327`; `cam_node.ino:113,118` | (a) Once the local base answers, `preferLocal` stays true, so the cloud is never tried again while the laptop works. FR7 says "cloud first". (b) Results served by the laptop are tagged **CLOUD** on the OLED. | Retry the cloud first every N cycles (for example every 6th, about 1 min). Tag laptop results as `LAPTOP` (or `CLOUD*`), or record the behaviour in INTERFACES/FR7. | Hardware | open |
| D-06 | minor | `soil_node.ino:355-366,371` | Any non-2xx response, including 4xx validation or auth errors, buffers the reading. The replay loop then `break`s on the first failure. One permanently rejected reading blocks the whole queue until 30 newer ones overwrite it. | Buffer only on transport errors or 5xx. During replay, drop an entry that gets a 4xx (log it). | Hardware | open |
| D-07 | minor | `soil_node.ino:57`; `04_calibration.md:18`; `06_assembly_guide_beginner.md:43` | The moisture dry point (default 2800 mV, expected 2.6–3.0 V) is above the ESP32 ADC's effective 11/12 dB range of **150–2450 mV** [ESP32-DS]. Readings there are compressed and non-linear, so the dry end of the % scale is coarse. | Accept and document it (the % is relative only). Check B-05. If dry is > 2.45 V, either note the reduced resolution near "dry" or add a 10 k/33 k divider on AO. | Hardware | open |
| D-08 | minor | `soil_node.ino:342-345` | If the backend returns `tds_baseline_ppm: null` (baseline cleared), the node keeps the stale NVS baseline and LOCAL mode applies old TDS rules. | If the key is present and null, set `tdsBaseline = NAN` and remove `tdsb` from NVS. | Hardware | open |
| D-09 | minor | `soil_node.ino:133,299` | If NTP never synced, buffered readings carry `ts:null`. The server stamps the *replay* time, so the evidence log records the wrong measurement time for offline readings (audit trail, D18). | Contract question for the Lead: add an optional `age_s` (millis delta) for buffered readings, or have the backend flag `buffered && ts==null` as "time approximate". | Lead (contract) / Hardware / Software | open |
| D-10 | minor | `05_demo_plan.md:16-17` | Probe positions before 1:00 are not defined. After watering, the action depends on where the pH/TDS probes sit. A TDS probe in air reads 0 ppm, which gives FERTILISE once a baseline exists. A pH probe in distilled water may read > 6.5, which gives WATCH. So "green" is not guaranteed. | Start with the pH/TDS/DS18B20 probes in the REFERENCE cup so that the post-watering state is OK/green. | Hardware | open |
| D-11 | minor | `06_assembly_guide_beginner.md:46` | Troubleshooting "0 ppm always → … + wire on 3V3" is wrong: a 3V3 supply keeps the module powered, so it would not read 0. | Change it to "+ not on GPIO25 / GPIO25 wire loose / A wire not on GPIO32". | Hardware | open |
| D-12 | minor | `03_software/src/app/config.py:19` | Default device keys (`demo-soil-key`, `demo-cam-key`) are committed and active unless `SAWIT_DEVICE_KEYS` is set. That is fine locally, but on Azure it is the same as having no key. | Set `SAWIT_DEVICE_KEYS` (and `SAWIT_ADMIN_TOKEN`) as App Service settings, and refuse defaults when `SAWIT_MODE=cloud`. Hand this to SW Verification. | Software | open |

Notes that are not defects:
- The backend sends `oled[0]="SKIP_FERTILISER"` (with underscore) while LOCAL mode shows `SKIP FERTILISER`. This is cosmetic.
- The backend calibration GET adds a `cal_id` field. It is harmless and the firmware ignores it.
- The command poll returns `{"cmd":"none"}` when idle, and the firmware handles it. Clear-on-delivery is confirmed (INT-16), which answers Hardware README open issue 2.

## 4. Integration evidence (backend `305bb47`, uvicorn on 127.0.0.1:8899, fresh runtime dir)
```
INT-01 pass health                                   200
INT-02 pass GET calibration (no baseline)            {"tds_baseline_ppm":null,"tds_margin":0.3,"updated_at":null,"cal_id":null}
INT-03 pass POST reading dry -> irrigate             IRRIGATE / "moist 24%<30%" / red
INT-04 pass POST all-null reading accepted           NO DATA / "check sensors" / amber
INT-05 pass POST baseline then device GET            {"tds_baseline_ppm":400.0,"tds_margin":0.3,...}
INT-06 pass TDS high -> skip_fertiliser              SKIP_FERTILISER / "TDS 900>520" / amber, simulated=true
INT-07 pass TDS low -> fertilise                     FERTILISE / "TDS 100<280"
INT-08 pass priority                                 actions=[irrigate, lime, skip_fertiliser]
INT-09 pass pH 3.8 -> lime red                       "pH 3.80<4.0"
INT-10 pass pH 6.9 / 4.1 -> watch amber
INT-11 pass moist 85 -> drain amber
INT-12 pass all in range -> ok green
INT-13 FAIL latest after buffered replay             latest seq=1545 (fresh 1550 sent before buffered 1545)
INT-14 pass wrong key -> 401
INT-15 pass cam poll idle                            {"cmd":"none"}
INT-16 pass capture one-shot                         poll1 {"cmd":"capture","id":1}; poll2 {"cmd":"none"}
INT-17 BLOCKED ripeness upload                       503 "Ripeness model not found ... m1_ripeness.onnx"
INT-18 pass body/header device mismatch -> 400
```
Every `oled` line returned was ≤ 16 characters, and every `led` value was one of green, amber or red.

## 5. Compile (K-01/K-02)
Not run in Pass 1. `arduino-cli 1.1.1` is at `~/.local/bin`, but `esp32:esp32` was still being installed by Hardware (staging was about 440 MB). Pass 2 will run these commands with `secrets.h` copied from `secrets.h.example`, into a separate build path:
```
arduino-cli compile --fqbn esp32:esp32:esp32    --build-path <scratch>/soil 02_hardware/firmware/soil_node
arduino-cli compile --fqbn esp32:esp32:esp32cam --build-path <scratch>/cam  02_hardware/firmware/cam_node
```
Static API review found no obvious compile errors. Things to watch:
- `ADC_11db` is deprecated in core 3.x, so expect a warning (not an error).
- `max(tds, 0.0f)` compiles because both arguments are float.

## 6. What Pass 2 needs
1. Compile both sketches once the ESP32 core is installed (K-01/02). Record the core version and library versions.
2. Hardware fixes for D-01, D-02, D-03 (and the minors). Software fix for D-04 (and D-12).
3. A trained `m1_ripeness.onnx` to unblock INT-17. An Azure URL for INT-19 (TLS pin test).
4. Bench results B-01…B-16 and INT-20 from the person holding the parts.
