# HW Verification: Pass 2 Report (23 Nov 2026)

## 1. Scope
Contract: `00_lead/INTERFACES.md` **v0.2.4**.

Reviewed:
- `02_hardware` at `873a615`: `soil_node.ino` 0.2.3, `cam_node.ino` 0.2.2, both `secrets.h.example`, docs 04–06, and the 02 changes.
- The fix commits `54eea6c` and `873a615`.
- Backend `03_software/src` at `47b18ff`. I ran it with `03_software/.venv` on 127.0.0.1:8899 with a throw-away runtime dir, and **stopped it afterwards**.

Rule D43/D44 applies: nothing was installed, and compiling is recorded as a **stakeholder build step**. Test IDs refer to `TEST_PLAN.md`.

## 2. Summary
| Area | Result |
|---|---|
| Pass 1 defects | **11 of 12 closed.** D-01…D-06 and D-08…D-12 are verified fixed. D-07 is accepted and documented (resolution note in 04_calibration §1). |
| Firmware vs v0.2.4 | **Pass.** Checked: replay-first, `age_s`, CLOUD/LAN/LOCAL tags, 5-min cloud retry, 4xx drop, NO DATA in all modes, 1-dp rounding shared by LOCAL and payload, baseline clear, one shared key, pinned roots. One new minor issue in the 4xx precedence (D-13) and one tag note (D-14). |
| TLS pin | **Pass (host-side).** Both examples carry DigiCert Global Root G2 + Microsoft RSA Root CA 2017. Both are self-signed, and the SHA-256 fingerprints match the comments. `openssl s_client -CAfile <G2 only>` against a live `*.azurewebsites.net` returns `Verify return code: 0 (ok)`. The on-device check (INT-19) waits for the Azure URL. |
| 3-cup TDS demo | **Pass.** REFERENCE→OK, PLAIN→FERTILISE, NUTRIENT→SKIP against the real backend rules (INT-21…24, strict compares at 0.7×/1.3×). Residual demo risk from pH in the cups (D-15). |
| Integration | **30/32 pass.** One fail (INT-33 → D-16, Software). INT-35 is not applicable: the backend cannot clear a baseline, so it is information only. Ripeness is now unblocked: the provisional M1 returned `ripe` 0.992 on a D2 image. |
| Compile | **Stakeholder build step** (K-01/K-02). The exact commands and expected output are in TEST_PLAN §E. My static review of the new code found no compile errors. |
| Beginner guide, compile part | **Not yet enough** for a first-time user to catch and fix compile errors themselves (D-17). |

## 3. Pass 1 defects: re-check
| ID | Status | Evidence |
|---|---|---|
| D-01 3-cup TDS | **closed** | 04_calibration §3 table + steps; 05_demo_plan §2 (0:00–1:25) and T−8 min; INT-21…24 |
| D-02 pH defaults | **closed** | soil_node.ino:60-61 (2.525/3.035 → PO 2.50 V = pH 7.0); guide step 7 says pH ≈ 7.0 |
| D-03 CA pin | **closed** | secrets.h.example; openssl verification as in §2 |
| D-04 buffered latest | **closed** | Firmware replays first (soil_node.ino:381-388). Backend `/latest` uses non-buffered rows only. INT-13, INT-13b |
| D-05 sticky local / tag | **closed** | CLOUD/LAN/LOCAL, retry every 300 s (soil_node.ino:296; cam_node.ino:116). See D-14 |
| D-06 head-of-line | **closed** | soil_node.ino:385 drops a 4xx entry; transport/5xx stops replay. See D-13 |
| D-07 moisture ADC range | **accepted** | Documented with an optional 10 k/33 k divider (04_calibration §1 step 5; guide step 3) |
| D-08 null baseline | **closed (firmware)** | soil_node.ino:372. The backend has no clear operation (INT-35), so the path is dormant but correct |
| D-09 offline time | **closed** | `age_s` (soil_node.ino:325); INT-28/29 |
| D-10 start state | **closed** | 05_demo_plan.md:15 |
| D-11 guide TDS text | **closed** | guide step 6 |
| D-12 default keys | **closed** | config.py: demo keys only in local mode; cloud fails closed |

## 4. New defects (Pass 2)
| ID | Severity | File:line | Issue | Suggested fix | Owner | Status |
|---|---|---|---|---|---|---|
| D-17 | **major** | `02_hardware/06_assembly_guide_beginner.md` §3 (l.31-34), §5 CLI block (l.58-63), §6 (l.65+) | Compiling is now a stakeholder build step (D43), so the firmware's **first compile ever** will happen on the stakeholder's machine. The guide doesn't yet let a first-time user find and fix compile errors:<br>(a) No "Verify (✓) first, then Upload" step, so compile errors and upload errors get mixed up.<br>(b) No expected success line (`Sketch uses … bytes … Maximum is …`), and no note that warnings are OK but `error:` is not.<br>(c) No compile-error rows in §6: `ArduinoJson.h`/`DHT.h`/`Adafruit_SSD1306.h: No such file` → library missing; `'JsonDocument' does not name a type` / `StaticJsonDocument` hints → ArduinoJson 6 installed instead of 7; `esp_camera.h: No such file` → wrong board or no ESP32 core; `Sketch too big` → Partition Scheme "Huge APP"; `secrets.h` constants undeclared → old or incomplete `secrets.h` copy.<br>(d) The CLI block lacks `core install`, `lib install` and the `secrets.h` copy step, and says "as used for the compile check" although no compile was run.<br>(e) No instruction to record the core and library versions that worked. | Add a short "Compile first (Verify)" step for each sketch with the expected success line. Add the error rows above to §6. Replace the CLI block with the full sequence in TEST_PLAN §E. Add "write down Tools → Board version and the library versions in the calibration log". | Hardware | open |
| D-13 | minor | `soil_node.ino:313,318,385,398` | `requestAny()` returns any 4xx over a transport error from the other base, and `isRejected()` then drops the reading (or the buffered entry). Example: the cloud app is stopped, so Azure answers **403**, while the laptop is unreachable. The fresh reading is then *not buffered*, and a buffered one is *deleted*, which loses data the buffer was meant to keep. 401/403/404/408/429 are not "this payload is bad". | Treat only **400/413/422** as permanent rejects (drop). For any other 4xx, buffer or keep the entry (log it), as for transport errors. Optionally, require both bases to agree before dropping. | Hardware | open |
| D-14 | minor | `soil_node.ino:300-301`; `05_demo_plan.md` §3 ("both can point at the laptop") | If the laptop is the primary and `API_BASE` = the laptop URL, `isCloud` is true, so the OLED says **CLOUD** for a laptop result. The presenter would then be telling the audience something untrue. A failure also retries the same URL twice. | Tag by scheme (`https://` → CLOUD, `http://` → LAN), or set `API_BASE_LOCAL ""` when the laptop is primary and tag `http` bases as LAN. Mention this in demo plan §3. | Hardware | open |
| D-15 | minor | `04_calibration.md:63`; `05_demo_plan.md:17` | The 3-cup logic is right for TDS, but green at 0:35 also needs the REFERENCE pH to be in 4.2–6.5. REFERENCE "(or tap water)" can read pH > 6.5, which gives **WATCH** amber (INT-25). In PLAIN (distilled water) a glass electrode often drifts; if it reads < 4.0, **LIME** outranks FERTILISE (INT-26). | Use pot leachate (not tap water) for REFERENCE. Add to calibration §3 step 2 and the pre-show checklist: "REFERENCE shows OK (pH 4.2–6.5), PLAIN shows FERTILISE (not LIME)", and give PLAIN 60 s to settle. | Hardware | open |
| D-16 | minor | `03_software/src/app/main.py:288-293` (`/latest` picks the non-buffered row with the **highest seq**) | If the node's seq restarts lower (NVS erased: "Erase All Flash" upload option, or a replacement board), `/latest` stays on the old high-seq row and the dashboard freezes on a stale reading. INT-33: posted seq 5 after seq 150, and `/latest` still showed 150. | Since firmware v0.2.2 sends the fresh reading last, pick the newest non-buffered row by `id` (or `received_at`) instead of `seq`. | Software | open |
| D-18 | minor (trivial) | `soil_node.ino:3`; `cam_node.ino:3` | Header comments say "Firmware 0.2.0", while `FW_VERSION` is 0.2.3 / 0.2.2. | Align the comments. | Hardware | open |

Notes (not defects):
- `age_s` for a fresh reading is the real time since capture: about 2 s, more after replays. INTERFACES says "0 for fresh". This is harmless, because the backend uses `age_s` only when `ts` is null, and the real value is more correct.
- The backend `oled[0]` is now `SKIP FERTILISER` (with a space), which matches LOCAL.
- `/latest` and other dashboard reads need the admin token in cloud mode (S-08). Devices never call them.

## 5. Integration evidence (backend `47b18ff`, 127.0.0.1:8899)
```
INT-01  pass  health  version 0.2.3, ripeness_model m1-effb0-0.1-provisional
INT-02  pass  device GET calibration (none)        {"tds_baseline_ppm":null,"tds_margin":0.3,...}
INT-03  pass  dry -> IRRIGATE / "moist 24%<30%" / red
INT-04  pass  all-null -> ["NO DATA","check sensors"] amber
INT-05  pass  baseline from REFERENCE via use_latest -> device reads 400.4
INT-21  pass  REFERENCE 395 -> OK / green
INT-22  pass  PLAIN 120 -> FERTILISE "TDS 120<280" amber simulated=true
INT-23  pass  NUTRIENT 900 -> SKIP FERTILISER "TDS 900>521" amber
INT-24  pass  280.3 (0.7x) -> ok ; 520.5 (1.3x) -> ok
INT-25  pass  REFERENCE pH 7.2 -> WATCH "pH 7.20>6.5"   (demo risk D-15)
INT-26  pass  PLAIN pH 3.9 -> lime outranks fertilise    (demo risk D-15)
INT-08  pass  [irrigate, lime, skip_fertiliser]
INT-09..11 pass lime/red, watch/amber (6.9, 4.1), drain/amber
INT-27  pass  29.96% / pH 3.96 -> rounded 30.0 / 4.0 -> watch only (matches LOCAL)
INT-13  pass  replay 130,131 (buffered) then fresh 132 -> latest 132
INT-13b pass  fresh 140 then late buffered 135 -> latest 140
INT-28  pass  age_s 120, ts null -> captured_at = received_at - 120 s
INT-29  pass  ts given -> captured_at = ts
INT-30  pass  ts "not-a-time" -> 200, treated as null
INT-31  pass  seq 150 retried as buffered (age_s 12) -> duplicate:true, same ev_000026, evidence 25->26->26
INT-32  pass  seq 150 with different values -> new ev_000027
INT-33  FAIL  seq 5 posted after seq 150 -> /latest still 150   (D-16)
INT-14  pass  wrong key 401 ; INT-18 id mismatch 400 ; INT-34 moisture 150 -> 422
INT-35  n/a   {"tds_baseline_ppm":null} -> 422 (no clear operation in backend)
INT-15/16 pass {"cmd":"none"} ; capture delivered once
INT-17  pass  TrainRipe(139).jpg 316828 B -> ripe 0.992 "Harvest this round" ev_000029
INT-36  pass  empty body -> 400
SUMMARY 30 / 32
```

## 6. Stakeholder build step (compile and flash)
See TEST_PLAN §E for the exact commands. The expected result for each sketch is a final line `Sketch uses N bytes (X%) of program storage space. Maximum is …` with no `error:` lines.

Please send back:
1. Both compile logs.
2. `arduino-cli core list` and `lib list`.
3. Bench results B-01…B-18.

Pass 3 will review those.

## 7. What Pass 3 needs
1. Hardware fixes for D-17 (guide), D-13, D-14, D-15, D-18. Software fix for D-16.
2. The stakeholder's compile logs (K-01/K-02) and version list.
3. The Azure URL for INT-19, plus bench results B-01…B-18 and INT-20 from the parts holder.
