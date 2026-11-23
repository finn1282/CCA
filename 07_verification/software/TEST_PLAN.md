# SW Verification: Test Plan

> Owner: SW Verification & Testing. Scope: the `03_software` backend, rule engine, evidence chain, dashboard, datasets, models and cloud guides. It also covers the device side of the HW↔SW contract (`02_hardware/firmware/*.ino`).
> Contract under test: **`00_lead/INTERFACES.md` v0.2.2** (v0.2.1 plus `age_s`/`captured_at`, replay-first and `/latest` ignoring buffered rows, D33).
> Rolling passes (D10): Pass 1 = M1 backend smoke test, Pass 2 = M2 model trained, Pass 3 = M3 design docs, Pass 4 = M4 run guides.
> Status values: **pass**, **fail**, **blocked** and **pass (obs)**. "pass (obs)" means the contract is met but something is worth noting.
> Evidence: `tests/pass1_results.md` is the full per-check output of `tests/contract_test.py`. Defect IDs (S-xx) are listed in `PASS_1_REPORT.md`.

Last run: **Pass 1, 23 Nov 2026**, software `b3cb4fe`, firmware `54eea6c`, repo HEAD `4163a6d`, port 8833.

## A. Owner's own suite (re-run in a fresh venv)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| OWN-01 | Backend | `pytest` suite | Fresh venv (Python 3.14) in scratch, `SAWIT_RUNTIME_DIR` set to scratch, `python -m pytest -q -p no:cacheprovider` from `03_software/src` | All pass | pass | 22 passed, 1 deprecation warning (starlette/httpx) |
| OWN-02 | Backend | `smoke_test.sh` end to end | `PY=<venv> PORT=8833 ./smoke_test.sh` | "SMOKE TEST PASSED" and every step plausible | pass (obs) | Output matches `src/tests/smoke_output.txt`. The script has no assertions and prints PASSED unconditionally (S-09) |

## B. Backend and contract (black-box HTTP, `tests/contract_test.py`)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| BE-01…03 | Health/meta | `/health`, and that `/meta` thresholds and action set match §4 | GET | 200; 30/80, 4.0/4.2/6.5, margin 0.30; 7 actions | pass | results BE-* |
| AU-01…05 | Auth | No headers, no key, wrong key, unknown device, body/header device mismatch | POST `/readings` | 401, 401, 401, 401, 400 | pass | AU-* |
| AU-06 | Auth | Camera key used on `/readings` | POST as cam-01 | No rule in the contract | pass (obs) | Keys are not scoped per endpoint |
| VA-01…08, 10…13 | Validation | Out-of-range or typed-wrong fields, missing `device_id`, malformed JSON, `age_s` −1, edge-valid 0/100/14, minimal body | POST | 422 for invalid; 200 for edge-valid; minimal body treated as all-null | pass | VA-* |
| VA-09 | Validation | Non-ISO `ts` | POST `ts:"not-a-timestamp"` | 422 | **fail** | Accepted. Becomes `captured_at` and sorts as the newest chart point (S-03) |
| TH-01…10 | §4 edges | Moisture 29.9/30/80/80.1; pH 3.99/4.0/4.19/4.2/6.5/6.51 | POST | irrigate/ok/ok/drain; lime/watch/watch/ok/ok/watch(PH_HIGH); rule_id and LED per §4 | pass | TH-* |
| TH-11 | §4 note | pH 5.6 | POST | ok plus the "above typical band, not harmful" note | pass | TH-11 |
| TH-12 | TDS | TDS rules before calibration | POST | Skipped, with a note | pass | TH-12 |
| TH-13…17 | TDS edges | Baseline 600 ±30 %: 419/420/780/781; baseline 1000 ±10 %: 899/900/1101 | POST | fertilise / ok / ok / skip_fertiliser, `simulated` true only on TDS findings | pass | TH-13…17 |
| PR-01…08 | Priority | Multi-finding readings | POST | irrigate/drain > lime > fertilise/skip > watch > ok; `action == actions[0]`; counterfactual present | pass | PR-* |
| PR-02 | Simulated flag | irrigate together with a TDS finding | POST | `simulated` true (conservative) | pass (obs) | PR-02 |
| NU-01…05 | Nulls | pH null, all null, moisture null + pH low, two nulls, null temp/RH/rssi | POST and evidence GET | Stored as null, no fabricated value; `OK (partial)` / `NO DATA` (amber); other rules still fire | pass | NU-*. NU-04: line 2 names only the first missing sensor |
| EC-01…02 | EC | `ec_us_cm` null → derived as TDS/0.5 and flagged; when supplied → kept | POST + evidence | 1240 with `ec_derived=true`; 900 with false | pass | EC-* |
| OL-01…08 | OLED/LED | Every `/readings` reply in the run (≈150, including extreme values) | Aggregate | 2 strings of 1–16 chars; LED ∈ {green, amber, red} and matches the §4 row; vocabulary only from §4; all §2 fields present; line 1 has no `_` | pass | OL-*. OL-07: line 2 is hard-truncated at 16 chars for extreme TDS |
| RP-01…09 | Replay/seq | Buffered replay accepted and flagged; `/latest` keeps the highest-seq non-buffered row (D-04 retest); chart ordered by `captured_at`; `age_s` → `captured_at = received − age_s`; `ts` wins over `age_s` | POST + GET | As in v0.2.2 §2 | pass | RP-* |
| RP-05 | Idempotency | Same `seq` posted twice | POST ×2 | No rule in the contract | pass (obs) | 2 evidence records (S-06) |
| CA-01…16 | Calibration | GET before set; POST validation (0, −5, margin 0/1, empty); use_latest (409 with no reading, picks last TDS); device GET (own / other / wrong key); dashboard GET; evidence logged; firmware parser caches the values or clears on null | GET/POST | v0.2.1 body `{tds_baseline_ppm, tds_margin, updated_at}` | pass | CA-*. CA-14: the baseline cannot be cleared to null through the API |
| CM-01…07 | Commands | Empty poll → `{cmd:none}`; queue → capture consumed once; unknown command 422; wrong device 403; no key 401 | GET/POST | As §3 | pass | CM-*. CM-04: repeated clicks queue repeated captures (S-07) |
| EV-01…11 | Evidence | Chain intact; prev_hash links; record content (input/output/calibration/mspo/rules_version); 404; approve/override reviews; retraining flag; audit pack VERIFIED with fertiliser rows `Simulated=yes`; coverage | GET/POST | Explain-to-audit (D18/D28) | pass, except EV-07 | EV-* |
| EV-07 | Evidence | Override to a non-vocabulary action | POST review `override_action:"banana"` | 422 | **fail** | Accepted and logged (S-04) |
| EV-12…15 | Tamper | Edit one record → verify fails at it, audit pack says BROKEN; restore → OK; delete a middle record → fails | Direct SQLite edit on the throw-away DB | Detected | pass | EV-12…15 |
| EV-16 | Tamper | Truncating the tail, or recomputing the whole chain | Analysis | Not detectable without an external head anchor | pass (obs) | Demo limitation; the report target is Confidential Ledger (S-10) |
| AD-01…06, 08, 09, 11…13 | Cloud mode | `SAWIT_DEVICE_KEYS` overrides demo keys; admin token protects calibration/commands/review writes; `?token=` accepted; `SAWIT_MODE=cloud` with no keys/token fails closed (D-12 retest) | Separate server instances | 401/403 as configured | pass | AD-* |
| AD-07 | Cloud mode | Dashboard calibration panel GET when a token is set | GET without device headers or token (the way `app.js` sends it) | 200 | **fail** | 403, so the panel is blank in cloud mode (S-01) |
| AD-10 | Cloud mode | Read endpoints with a token set | GET `/latest`, `/evidence/export` | No rule in the contract | pass (obs) | Unauthenticated (S-08) |
| RI-01…04 | Ripeness | No auth 401, empty 400, >5 MB 413, model absent 503 with a clear message | POST raw JPEG | As stated | pass | RI-* |
| RI-05…09 | Ripeness/model | Response fields, heatmap PNG, non-image 400, cam parser, CPU latency < 2 s | POST | §3 response | **blocked** | M1 not exported yet (503) |

## C. Firmware ↔ backend (exact device payloads, firmware `54eea6c`)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| FW-01…06 | Soil node | `toJson()` shapes: no NTP (`ts:null`, `cal_id:"uncalibrated"`), NTP, DS18B20/DHT failed, all probes failed, buffered + `age_s` 95 + rssi null, 3 findings | POST the byte-exact JSON with the firmware headers; parse with a Python port of `applyCloudResponse()` (ArduinoJson `|` defaults) | 200; parser accepts the reply; lines 1 and 2 are not truncated by `substring(0,16)`; LED valid; `ev_` id | pass | FW-01…06 |
| FW-07 | Fallback | LOCAL `localDecision()` vs CLOUD on 75 boundary combinations (moisture × pH × TDS) | Python port | Same action and LED | pass | FW-07 |
| FW-08 | Fallback | Raw float (LOCAL) vs rounded payload (CLOUD) at edges | Python port | — | pass (obs) | e.g. raw 29.96 %: LOCAL irrigate, CLOUD ok (S-12, Hardware) |
| FW-09, FW-12 | Fallback | LOCAL OLED wording | Python port | — | pass (obs) | `pH 4.0<4.0` at raw 3.96; all probes failed shows green OK on LOCAL vs amber NO DATA on CLOUD (S-12) |
| CA-09, CA-16 | Soil node | `fetchCalibration()` parse of GET calibration (number / null) | Python port | Caches the number; null clears the baseline (v0.2.2 firmware) | pass | CA-09/16 |
| FW-10 | Camera | `pollCommands()` on `{cmd:none}` / `{cmd:capture}` | GET with cam headers | Only `capture` triggers | pass | FW-10, CM-03 |
| FW-11 | Camera | `captureAndUpload()` reply parse | POST JPEG with `Content-Type: image/jpeg` | `label`, `confidence`, `harvest_advice`, `evidence_id` | **blocked** | 503 until M1 exists. A static read of `main.py` shows the fields are present |
| FW-13 | Integration | One device key for both `API_BASE` and `API_BASE_LOCAL` | Config review | The laptop fallback accepts the cloud key | **fail** | The laptop in local mode only knows the demo keys unless `SAWIT_DEVICE_KEYS` is exported (S-02) |
| FW-14 | Integration | Cloud and LAN are two separate databases | Design review | The dashboard and devices use the same backend | pass (obs) | A capture queued on cloud never reaches a camera on LAN. Rehearsal item R-07 (S-05) |

## D. Dashboard

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| DB-01…03 | Offline-safe | No CDN, fonts or external URL in `index.html`, `app.js`, `style.css`, `harvester.html`; all assets served locally (Chart.js 4.4.1 vendored) | Regex over served files plus GET | None external; all 200 | pass | DB-01…03 |
| DB-04 | Panels | Readings, recommendation + reasoning/counterfactual/ML check, camera + heatmap, calibration, satellite→drone→ground cascade, harvest, evidence, MSPO | HTML ids plus an `app.js` read | Present | pass | DB-04 |
| DB-05, DB-08 | Labelling | CC BY 4.0 credits (Kamal D1, Rosbi D2, Mimboro D4, Descals), the Copernicus notice, SIMULATED badges and SIMULATED feed sources | Text check | Present | pass | DB-05/08 |
| DB-06 | Labelling | Copernicus notice wording | Read | "Contains modified Copernicus Sentinel data [year]"; source matches the build (Earth Engine, D16) | pass (obs) | Year missing; says Planetary Computer (S-11) |
| DB-07 | Feeds | Every polled feed returns 200 | GET | 200 | pass | DB-07 |
| DB-09 | Backend down | `tick()` catch sets the pill to "offline" and keeps the last values; other renders use `.catch` | Static read of `app.js:196-220` | Graceful | pass (static) | Cascade is fetched only on the first tick, so it stays empty if the backend was down then; `harvester.html` has no error handling (S-13). A live check is in rehearsal R-10 |
| DB-10 | Licence | Third-party JS licence notice | Read vendor file | MIT notice kept | pass (obs) | Chart.js banner stripped from the minified file (S-14) |

## E. Datasets (D16), as documented so far

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| DS-01 | Sources | D1 Mendeley doi:10.17632/424y96m6sw.1, D2 Zenodo 11114885 / GitHub mirror, D4 Mendeley v2 doi:10.17632/s23jvbpnr3.2, D9 GEE | `03_datasets.md`, `train_m1.py`, `scripts/fetch_d2_github.py` | Documented, with licence | pass | D2 is fetched from the GitHub mirror of the same CC BY 4.0 record |
| DS-02 | Licence | CC BY 4.0 attribution in the dashboard and the model meta (`data` field) | Read | Present | pass | DB-05; `train_m1.py:300` |
| DS-03 | Harmonisation | `map_class()` regex order: damaged/empty excluded; overripe/decay; partial → underripe; immature before mature | Code review plus D2 folder names | 4 classes, no mis-mapping | pass (static) | D2 Test{Unripe,Ripe,Overripe} map correctly. D1 folder names to be confirmed once extracted |
| DS-04 | Split | D1 train/val/test (provided split) → D2 Malaysian test; head fine-tune uses D2 train only, evaluated on D2 test | Code review `train_m1.py:204-290` | No D2-test image in training | pass (static) | Re-check on real counts in Pass 2 |
| DS-05 | Leakage | Near-duplicate images across train/test (same bunch photographed twice) | Perceptual hash across splits | 0 cross-split duplicates | **blocked** | D1 zip incomplete (19 MB of 272 MB); D2 FFBtrain not downloaded |
| DS-06 | Class balance | Per-class counts per split | `train_counts` in `m1_metrics.json` | Documented; class weights used | **blocked** | Waiting for the M1 run. D2 local test copy has 23/41/14 unripe/ripe/overripe (no underripe in D2) |
| DS-07 | D4 split | Geographic split preserved (no reshuffle) | Code review | Provided split | **blocked** | M3 not built yet (stretch, SW-P6) |
| DS-08 | Simulated | M6 data labelled SIMULATED (`m6_tree.json` meta, dashboard, audit pack) | Read + EV-10 | Labelled | pass | `metrics_m6.json` "SIMULATED … n=20000, seed=42" |
| DS-09 | Provisional | A provisional (D2-only) M1 must be labelled as such and not reported as D1→D2 | Code review | `-provisional` suffix, `provisional: true` | pass (static) | `train_m1.py:270,297`. It has no underripe training data (Pass 2 check) |

## F. Models (Pass 2, triggered by M2)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| MD-01 | M1 | Re-run evaluation on D1 test and D2 test with the exported ONNX; compare with `m1_metrics.json` | Own script with onnxruntime | Within ±0.5 pp | blocked | Training in progress |
| MD-02 | M1 | Confusion matrix sane (ordinal errors mostly adjacent) | From MD-01 | Off-diagonal mass mostly ±1 class | blocked | — |
| MD-03 | M1 | ONNX loads in the endpoint; `/health` reports `model_version` | Restart the server with the model | 200 at ripeness | blocked | — |
| MD-04 | M1 | Grad-CAM/CAM heatmap PNG produced and focused on the bunch | RI-06 plus a visual check | Overlay saved and served | blocked | — |
| MD-05 | M1 | CPU latency (laptop) p95 | 20 requests | < 2 s | blocked | — |
| MD-06 | M6 | Tree accuracy reproducible (`train_m6.py` seed 42) | Re-run | 0.884 | blocked → Pass 2 | Needs sklearn in the scratch venv |

## G. Cloud trainability and docs (Passes 3–4)

| ID | Area | Test | Method | Expected | Status |
|---|---|---|---|---|---|
| CL-01 | Kaggle | Notebook/guide: dataset attach paths, GPU flag, `KAGGLE_API_TOKEN` usage, output download, `--d1/--d2` paths | Review only (D31) | Runs as written | blocked (M4) |
| CL-02 | Azure | Deploy guide: resources, region (D29), app settings `SAWIT_MODE=cloud`, `SAWIT_DEVICE_KEYS`, `SAWIT_ADMIN_TOKEN`, startup command, `/api/v1/health` check, persistent DB path | Review only (D31) | Complete for a beginner | blocked (M4) |
| CL-03 | GEE | Satellite export guide → `precomputed/` | Review only | Runs as written | blocked (M4) |
| DOC-01 | D20/D23/D32 | Docs 01–05: no Kaggle/student/price reasons; residency split; RAI scoping (tabular only, Grad-CAM for images) | Read | Compliant | blocked (M3; drafts `01_solution_overview.md`, `02_architecture.md`, `03_ai_models.md` seen, not yet reviewed) |
| DOC-02 | Internal | README/implementation guide documents the actual build honestly | Read | Accurate | pass (obs): README accurate for M1; the local-run section needs the S-02 note |

## H. Presentation-day end-to-end rehearsal checklist

Run this in full at least once before the day, on the presentation laptop and hotspot, and tick each item.

| # | Step | Pass criterion |
|---|---|---|
| R-01 | `git pull`; fresh venv; `pytest -q`; `PORT=<free> ./smoke_test.sh` | All pass |
| R-02 | Run `contract_test.py` on the presentation laptop | 0 FAIL (open defects fixed) |
| R-03 | Cloud: App Service settings `SAWIT_MODE=cloud`, `SAWIT_DEVICE_KEYS`, `SAWIT_ADMIN_TOKEN` set; `GET /api/v1/health` returns `mode:"cloud"` | 200 |
| R-04 | Laptop fallback started with **the same** `SAWIT_DEVICE_KEYS` as the cloud (S-02); `--host 0.0.0.0`; firewall open; `API_BASE_LOCAL` IP matches the hotspot IP | The soil node's POST to the LAN base returns 200 |
| R-05 | Open the dashboard as `https://<app>/?token=<admin>` (and `http://<laptop>:<port>/` for fallback). Check the calibration panel shows the baseline (S-01) | Panel populated |
| R-06 | Soil node boot: OLED shows CLOUD, a reading arrives within 10 s, and the dashboard tiles update | ≤ 10 s |
| R-07 | Single-backend rule: dashboard, soil node and camera all on the same base (CLOUD **or** LAN), because the databases are separate (S-05) | OLED tag matches the dashboard pill |
| R-08 | Demo beats: dry soil → IRRIGATE/red; lime cup → LIME/red; set the TDS baseline from the REFERENCE cup ("Use current reading"); PLAIN → FERTILISE (SIMULATED badge); NUTRIENT → SKIP FERTILISER | Each within one interval, with matching OLED/LED/dashboard |
| R-09 | Camera: dashboard **Capture** once (not repeatedly, S-07) → result, heatmap and harvest advice show in ≤ 10 s; the evidence row appears | ≤ 10 s |
| R-10 | Kill the backend: dashboard pill shows "offline", the node falls back (LAN, then LOCAL), and readings are buffered. Restart the backend → replay; the "live" panel shows the fresh seq, not a replay | As stated |
| R-11 | Evidence: "Verify chain" ✔; open the MSPO audit pack; approve one record, override one | VERIFIED; review rows present |
| R-12 | Wi-Fi off on the laptop and reload the dashboard (local fallback) → no missing assets or fonts | Renders fully |
| R-13 | Before presenting: reset the demo DB (new `SAWIT_RUNTIME_DIR`) so the evidence list starts clean, and seed 3 warm-up readings | Clean log |
| R-14 | After presenting: stop all servers; never commit `secrets.h`, `.env` or DB files | `git status` clean of secrets |
