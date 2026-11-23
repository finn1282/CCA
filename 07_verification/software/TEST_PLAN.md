# SW Verification: Test Plan

> Owner: SW Verification & Testing. Scope: the `03_software` backend, rule engine, evidence chain, dashboard, datasets, models, docs and run guides. It also covers the device side of the HW↔SW contract (`02_hardware/firmware/*.ino`).
> Contract under test: **`00_lead/INTERFACES.md` v0.2.6**. That is v0.2.2 `age_s`/`captured_at`, plus v0.2.3 ts validation, idempotent seq, NO DATA and 1-dp rounding, plus the v0.2.4 seq-reuse rule, plus v0.2.6 `/latest` = most recently captured non-buffered row.
> Rolling passes (D10): Pass 1 = M1 backend; **Pass 2 = M2–M4** (model, design docs, run guides).
> Status values: **pass**, **fail**, **blocked** and **pass (obs)**. "pass (obs)" means the contract is met but something is worth noting.
> Evidence:
> - `tests/pass2_results.md`: per-check output of `tests/contract_test.py`
> - `tests/pass2_eval_m1.md`: output of `tests/eval_m1.py`
> - `tests/pass1_results.md`: the earlier Pass 1 run
>
> Defect IDs (S-xx) are listed in `PASS_1_REPORT.md` (S-01…15, all closed) and `PASS_2_REPORT.md` (S-16…25).

Last run: **Pass 2, 23 Nov 2026**, repo HEAD `345ec07` (software `1ad0560`), existing `03_software/.venv` (D43/D44), port 8833.

## A. Owner's own suite

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| OWN-01 | Backend | `pytest` | `03_software/.venv`, `SAWIT_RUNTIME_DIR` in scratch, `-p no:cacheprovider` | All pass | pass | 33 passed |
| OWN-02 | Backend | `smoke_test.sh` (asserted, `tests/smoke_e2e.py`) | `PY=../.venv/bin/python PORT=8833` | "SMOKE TEST PASSED (all assertions)" | pass | S-09 closed |

## B. Backend and contract (black-box HTTP, `tests/contract_test.py`)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| BE-01…03 | Health/meta | `/health`, plus `/meta` thresholds and actions equal §4 | GET | 200; 30/80, 4.0/4.2/6.5, 0.30; 7 actions | pass | BE-* |
| AU-01…05 | Auth | No headers, no key, wrong key, unknown device, body/header mismatch | POST | 401×4, 400 | pass | AU-* |
| AU-06 | Auth | Camera key used on `/readings` | POST | No rule in the contract | pass (obs) | Keys not scoped per endpoint |
| VA-01…08, 10…13 | Validation | Out-of-range or typed-wrong fields, missing id, malformed JSON, `age_s` −1, edge-valid values, minimal body | POST | 422 / 200 | pass | VA-* |
| VA-09 | Validation | `ts` garbage / naive / >24 h future / `+08:00` | POST | Garbage → null (`captured_at = received_at`); `+08:00` → normalised `Z` (v0.2.3) | pass | S-03 closed |
| TH-01…17 | §4 edges | Moisture 29.9/30/80/80.1; pH 3.99/4.0/4.19/4.2/5.6/6.5/6.51; TDS 600±30 % (419/420/780/781), 1000±10 %; TDS before calibration | POST | Strict `<`/`>` edges, rule_id, LED, `simulated` only on TDS | pass | TH-* |
| PR-01…08 | Priority | Multi-finding readings | POST | irrigate/drain > lime > fertilise/skip > watch > ok; counterfactual | pass (PR-02 obs) | PR-* |
| NU-01…05, EC-01…03 | Nulls / EC | Nulls stored as null; `OK (partial)` / `NO DATA` amber; EC derived and labelled from `ec_derived` | POST + evidence | As §2 | pass (NU-04 obs) | S-13 EC label closed |
| OL-01…08 | OLED/LED | Every reply (~400) | Aggregate | 2 × ≤16 chars, LED matches §4, line 1 without `_` | pass | OL-* |
| RP-01…04, 06…09 | Replay/time | Buffered flag + `ts` kept; `/latest` = most recently captured non-buffered row, including after a seq reset (D-04/D-16); chart ordered by `captured_at`; `age_s` arithmetic | POST + GET | v0.2.6 §2 | pass | RP-* |
| RP-05, RP-10, RP-11 | Idempotency | Identical re-POST; same seq with new values; same seq with a different air temp | POST | Original reply + `duplicate`, no new evidence; new values stored; (obs) only 4 soil fields compared | pass (RP-11 obs) | S-06 closed |
| CA-01…16 | Calibration | GET/POST validation, use_latest, device/other/wrong key, dashboard GET, evidence logged, firmware parse | GET/POST | v0.2.1 body | pass (CA-14 obs) | CA-* |
| CM-01…08 | Commands | Poll none / capture once; coalescing of repeated clicks; 60 s expiry; 422/403/401 | GET/POST + DB-aged row | As §3, S-07 | pass | S-07 closed |
| EV-01…17 | Evidence | Chain links, content, 404, reviews (approve/override, vocabulary 422), audit pack VERIFIED + Simulated=yes + **head hash**, coverage, tamper edit/delete detected | GET/POST + SQLite edit | D18/D28 | pass (EV-16 obs) | S-04, S-10 closed |
| AD-01…14 | Cloud mode | Key override; writes need the token; **reads need the token** (10 endpoints 403 without, 200 with `?token=`); shell and `/health` public; dashboard `get()` sends the token; `SAWIT_MODE=cloud` without secrets fails closed | 3 server instances | 401/403/200 as stated | pass | S-01, S-08, D-12 closed |
| RI-01…03 | Ripeness | No auth 401, empty 400, >5 MB 413 | POST | As stated | pass | RI-* |
| RI-04…11 | Ripeness + model | SVGA JPEG from D2 test → 200; 8 §3 fields and types; probs sum to 1; label = argmax; heat-map PNG 448×224 at `/static/heatmaps/<ev>.png`; image served; non-image 400; cam parser; p95 < 2 s; override vocabulary for ripeness; `/health` model_version | POST/GET | §3 | pass | Cold 0.22 s; warm **p50 0.082 s / p95 0.083 s** |
| RI-12…14 | Ripeness | Underripe column; soil POST during inference; full-size D2 original | — | — | pass (obs) | p(underripe) 0.002 (untrained); soil waits about 0.17 s; 8.6 MB → 413 (S-23) |

## C. Firmware ↔ backend (exact device payloads, firmware v0.2.3+)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| FW-01…06 | Soil node | `toJson()` shapes (1-dp `r1()` rounding, `age_s`, null for NAN): no NTP, NTP, temp/RH failed, all probes failed, buffered, 3 findings | POST byte-shaped JSON; Python port of `applyCloudResponse()` | 200; parser accepts; no truncation | pass | FW-01…06 |
| FW-07 | Fallback | LOCAL `localDecision()` vs CLOUD on **315 raw boundary combinations** | Python port | Same action, LED and OLED line 1 | pass | S-12 closed |
| FW-08 | Fallback | 1-dp pH rounding at edges | Python port | — | pass (obs) | Raw 3.95 → watch (0.05 pH shift, both sides) |
| FW-12 | Fallback | All probes failed | Python port | NO DATA/amber in LOCAL and CLOUD | pass | v0.2.3 |
| FW-10, FW-11 | Camera | `pollCommands()`; `captureAndUpload()` with SVGA JPEG | GET/POST | Only `capture` triggers; reply has label/confidence/harvest_advice/evidence_id | pass | — |
| FW-13 | Integration | One key for cloud and LAN | Doc review | Laptop exports the same `SAWIT_DEVICE_KEYS` | pass | S-02 closed (D39, DEPLOY §7, 06 §4.3) |
| FW-14 | Integration | Separate cloud/LAN databases | Doc review | One backend at a time | pass | S-05 closed (D39) |

## D. Dashboard

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| DB-01…03 | Offline-safe | No external URL in HTML/JS/CSS/harvester; all assets local | Regex + GET | None; 200 | pass | — |
| DB-04, DB-05, DB-07, DB-08 | Panels/labels/feeds | 8 panels; CC BY 4.0 credits; SIMULATED badges; feeds 200 | Text + GET | Present | pass | — |
| DB-06 | Labelling | Copernicus notice | Regex | Year + Earth Engine | pass | S-11 closed |
| DB-09 | Backend down | `tick()` → "offline" pill; cascade retried until loaded; harvester try/catch + offline text | Static read | Graceful | pass (static) | Live check in R-10 |
| DB-10 | Licence | Chart.js MIT notice | GET `vendor/LICENSE-chartjs.txt` | 200 | pass | S-14 closed |

## E. Datasets (D16)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| DS-01 | Sources | D1 Mendeley, D2 Zenodo URLs used by the notebook resolve | HEAD request only (no download, D43) | 200, sizes as documented | pass | D1 272,151,984 B zip; D2 1,159,745,282 B, CC BY 4.0 |
| DS-02 | Licence | CC BY 4.0 credits (dashboard, model meta, Copernicus year) | Read | Present | pass | — |
| DS-03 | Harmonisation | My folder→class mapping vs `train_m1.map_class` / `split_of` on all 312 local D2 files; D1 names | `eval_m1.py` | 0 mismatches | pass | Immature→unripe, Partially Ripe→underripe, Fully Ripe/Mature→ripe, Overripe/Decayed→overripe |
| DS-04 | Split | Provisional: D2-train 85/15 → D2-test; final: D1 split → D2 test; head fine-tune on D2-train | Code review | No test file in training | pass (static) | — |
| DS-05 | Leakage | Cross-split exact (MD5) and near (dHash ≤ 6) duplicates, D2 train × test, plus visual confirmation | `eval_m1.py` | 0 | **fail** | 6/89 test images duplicate train (S-17) |
| DS-06 | Class balance | Counts per split | `eval_m1.py` | Documented | pass (obs) | Local D2 test 34/41/14, train 40/123/60 (partial copy); provisional train 34/105/51 |
| DS-07 | D4 split | Geographic split preserved | — | — | blocked | M3 not built (stretch, D42) |
| DS-08, DS-09 | Labelling | M6 SIMULATED; provisional M1 labelled `-provisional` everywhere (`/health`, meta, README, 03 §9) | Read + RI-11 | Labelled | pass | — |

## F. Models

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| MD-01a | M1 | Reproduce the reported D2-test metric with the training pipeline | Own torchvision path + ONNX | = 0.9326 | pass | Identical CM |
| MD-01b | M1 | Same metric on the **serving** path (`inference._preprocess`) | `eval_m1.py` | Within ±0.5 pp of reported | **fail** | 0.8989 (−3.4 pp) (S-16) |
| MD-01c | M1 | Deduplicated D2 test (S-17 removed) | `eval_m1.py` | Report it | pass (obs) | 0.8916, n = 83 |
| MD-02 | M1 | Confusion matrix sane | `eval_m1.py` | Errors adjacent | pass (obs) | All errors unripe→ripe (adjacent in D2's 3 classes; costly direction) |
| MD-03 | M1 | ONNX loads in the endpoint; `/health` model_version | RI-04/RI-11 | Loaded | pass | — |
| MD-04 | M1 | CAM heat-map focused on the bunch | RI-06 + visual check + CAM centre mass | On the fruit | pass | Centre mass 0.82 |
| MD-05 | M1 | CPU latency p95 | RI-09 | < 2 s | pass | 0.083 s |
| MD-06 | M6 | `train_m6.py` reproducible (run from a scratch copy, nothing written to `03_software`) | Re-run, seed 42 | 0.88375, identical tree | pass | Accuracy and tree structure identical |
| MD-07 | M1 final | D1→D2 Kaggle model: repeat MD-01b/c on D2 test; check the D1-test numbers in the owner's log | After the stakeholder run | — | blocked | Stakeholder step (D31) |

## G. Run guides and docs (desk-check only, D31)

| ID | Area | Test | Method | Expected | Status | Evidence |
|---|---|---|---|---|---|---|
| CL-01 | Kaggle | Notebook equals `train_m1.py`; URLs; GPU/internet/private metadata; `KAGGLE_API_TOKEN` env/file outside the repo; output `-p models`; post-run health | Review + HEAD | Runs as written | pass (obs) | `/kaggle/tmp` vs documented `/kaggle/temp`; step 4 may hit 413 (S-23) |
| CL-02 | Azure | Resources, region fallback, app settings, startup, health version 0.2.6, token URL, clean-up | Review | Complete for a beginner | **fail** | SAS 60 d vs 7 d limit (S-18); SQLite WAL on `/home` (S-19); bare `startup.sh` (S-20) |
| CL-03 | Earth Engine | `EE_PROJECT` env, auth token outside the repo, outputs committed, attribution | Review | Runs as written | pass (obs) | Block-ID mismatch with estate (S-24); no Windows path note (S-25) |
| CL-04 | Alternatives | Fallback ladder, keys, one backend | Review | Consistent with D39 | pass | — |
| DOC-01 | D20/D23/D32 | Docs 01–05: residency split, RAI tabular-only / Grad-CAM for images, no student/price reasons | Grep + read | Compliant | **fail** (minor) | D32 ✔ throughout; build/demo/cost wording in 02/03 (S-22); 05 stale (S-21) |
| DOC-02 | Internal | 06 beginner guide, 07 build-vs-target, README | Read | Accurate | pass (obs) | S-23 |

## H. Presentation-day end-to-end rehearsal checklist

Run this in full at least once before the day, on the presentation laptop and hotspot, and tick each item.

| # | Step | Pass criterion |
|---|---|---|
| R-01 | `git pull`; `pytest -q`; `PORT=<free> ./smoke_test.sh` | 33 passed; SMOKE TEST PASSED |
| R-02 | `contract_test.py` and `eval_m1.py` on the presentation laptop | 0 FAIL; serving-path accuracy recorded |
| R-03 | Cloud: `SAWIT_MODE=cloud`, `SAWIT_DEVICE_KEYS`, `SAWIT_ADMIN_TOKEN`; `/api/v1/health` gives `mode:"cloud"`, version 0.2.6, the model version | 200 |
| R-03b | Cloud DB on `/home/data` (S-19): 50 simulator readings, **Verify chain**, `az webapp restart`, Verify chain again | No "database is locked"; chain VERIFIED and history kept |
| R-04 | Laptop fallback started with the **same** `SAWIT_DEVICE_KEYS` (D39); `--host 0.0.0.0`; firewall open; `API_BASE_LOCAL` = hotspot IP | Node POST to LAN → 200 |
| R-05 | Dashboard opened as `https://<app>/?token=<admin>`; calibration panel shows the baseline; evidence link and audit pack open in a new tab | Panels populated |
| R-06 | Soil node boot: OLED shows CLOUD (or LAN), a reading arrives within 10 s, tiles update | ≤ 10 s |
| R-07 | **One backend at a time (D39):** devices and dashboard on the same base; OLED tag = dashboard pill | Match |
| R-08 | Demo beats: dry → IRRIGATE/red; lime cup → LIME/red; baseline from the **REFERENCE** cup; PLAIN → FERTILISE (SIMULATED); NUTRIENT → SKIP FERTILISER | Within one interval, OLED/LED/dashboard agree |
| R-09 | Camera: one **Capture** click → result, heat-map and advice in ≤ 10 s. Use printed **D2 FFBtest** photos not on the S-17 list | ≤ 10 s |
| R-10 | Kill the backend: pill "offline", node → LAN/LOCAL, buffering. Restart → replay; "live" panel shows the fresh reading | As stated |
| R-11 | Verify chain ✔; audit pack shows the head hash; approve one record, override one | VERIFIED |
| R-12 | Wi-Fi off and reload the local dashboard | All assets render |
| R-13 | Reset the demo DB and seed 3 warm-up readings | Clean log |
| R-14 | After the show: stop servers, rotate keys, `az group delete` if done; no secrets in git | Clean |
