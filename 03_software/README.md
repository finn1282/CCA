# 03_software — README

## Status (23 Nov 2026)
| Milestone | State |
|---|---|
| Plan (SW-P1…P8) | All accepted (D24–D29) |
| M1 milestone: backend + simulator + rules + dashboard | **Done.** INTERFACES **v0.2.5** implemented. 32/32 pytest pass. Asserted smoke test passes (`src/tests/smoke_output.txt`) |
| HW verification pass 1 defects (D-04, D-12) | **Fixed** (b3cb4fe) with tests |
| SW verification pass 1 defects (S-01…S-15) | **Fixed** (9bd2e04), see table below |
| M2 milestone: M1 ripeness model | **Provisional model trained on CPU** (D2-only, see Training results). The full D1→D2 run is the stakeholder's Kaggle step (D31) |
| Design docs 01–05 | **Done** (D32 applied). M1 numbers filled in 03 §9 |
| Run guides (D31) | `training/RUN_ON_KAGGLE.md`, `deploy/DEPLOY_AZURE.md` + `deploy/ALTERNATIVES.md`, `gee/RUN_EARTH_ENGINE.md` |
| 06 implementation guide, 07 build-vs-target | Done |
| Open stretch | M3/M4 drone YOLO not trained (SW-P6) |

## Inputs used
`00_lead/SPEC.md`, `PROJECT_PLAN.md`, `DECISIONS.md` (D1–D39), `INTERFACES.md` v0.2.5, assignment PDF pp.5–8, `01_research/00`–`08`, `sources.md`, `07_verification/hardware/PASS_1_REPORT.md`, `07_verification/software/PASS_1_REPORT.md`.

## Outputs
| Path | Content |
|---|---|
| `PLAN.md` | Approach, models M1–M7, tasks, ideas, conflicts, proposals (all ruled) |
| `01_solution_overview.md` | Name (SawitSense), problems → functions, users, user stories — report-facing |
| `02_architecture.md` | Adapted Fig. 4 layers, components, data flow, demo sequence, deployment + PDPA residency, explainability per model — report-facing |
| `03_ai_models.md` | M1–M7 + NLP: inputs, algorithm vs alternatives, data, metrics, explainability, MLOps; measured results — report-facing |
| `04_cloud_design.md` | Why Azure, services per layer, residency, cost drivers (as risk), ERP integration, short/medium/long roadmap, prioritised risks — report-facing |
| `05_api_spec.md` | API v0.2.5 (devices, dashboard, evidence, config) |
| `06_implementation_guide_beginner.md` | Install, run, connect devices, calibrate, train, deploy, demo-day checklist |
| `07_actual_build_vs_target.md` | **Internal**: demo component → production Azure equivalent; Q&A lines |
| `src/app/` | FastAPI backend: `main.py` (endpoints), `rules.py`, `recommender.py` (rules + M6), `evidence.py` (hash chain, audit pack), `compliance.py` (M7, MS 2530 clauses), `inference.py` (M1 ONNX + CAM, M2), `analytics.py` (allocation, cascade), `db.py`, `config.py` |
| `src/static/` | Dashboard (`index.html`, `app.js`, `style.css`, vendored Chart.js + licence), `harvester.html`, `precomputed/estate_blocks.json` (SIMULATED) |
| `src/simulator.py` | Soil-node simulator (stdlib), 7 scenarios + cycle, optional camera image |
| `src/smoke_test.sh` + `src/tests/smoke_e2e.py` | Asserted end-to-end smoke test (own server, temp DB, port 8791) |
| `src/tests/test_api.py` | 32 tests (rules, contract, auth, calibration, commands, evidence tamper, v0.2.2/0.2.3, defects) |
| `training/ripeness/train_m1.py` | M1 training (CPU or GPU; provisional D2-only mode), ONNX export + parity check |
| `training/ripeness/m1_metrics_provisional.json`, `m1_ripeness_provisional.json` | Metrics + metadata of the provisional model (weights are git-ignored) |
| `training/kaggle/` | `sawitsense_m1.ipynb` + `kernel-metadata.json` (built by `build_notebook.py`) |
| `training/fertiliser/train_m6.py`, `metrics_m6.json` | M6 SIMULATED dataset + tree → `src/app/assets/m6_tree.json` |
| `training/estate/make_demo_estate.py` | SIMULATED estate (productivity by palm age from AHMAD2020) |
| `gee/ndvi_estate.py`, `gee/ndvi_estate_codeeditor.js` | M5 Sentinel-2 NDVI anomaly pre-compute (stakeholder runs) |
| `deploy/make_package.sh` | Builds the App Service zip |
| `scripts/fetch_d2_github.py` | D2 download from the GitHub mirror (optional per-class cap) |

## How to run (local)
```bash
cd 03_software && python -m venv .venv && .venv/bin/pip install -r src/requirements.txt
cd src && ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000     # dashboard: http://localhost:8000
../.venv/bin/python simulator.py --scenario cycle --interval 2              # second terminal
../.venv/bin/python -m pytest -q && PY=../.venv/bin/python ./smoke_test.sh
```

**Device keys (S-02).** Each device has **one** key, which it uses for both the cloud and the laptop. Locally, the demo keys (`soilnode-01:demo-soil-key`, `cam-01:demo-cam-key`, `sim-01:demo-sim-key`) are active unless `SAWIT_DEVICE_KEYS` is set. If the firmware carries the real cloud keys, export the **same** `SAWIT_DEVICE_KEYS` before starting the laptop backend, or the LAN fallback answers 401. In cloud mode (`SAWIT_MODE=cloud`), the demo keys are disabled and `SAWIT_ADMIN_TOKEN` is required for dashboard reads and writes.

**One backend at a time (D39).** The laptop and the cloud keep separate databases and command queues.

## Smoke test result
Latest run (`src/tests/smoke_output.txt`): **all assertions pass.**
- Health.
- Calibration from the latest reading.
- dry → irrigate/MOIST_LOW/red, wet → drain/MOIST_HIGH/amber, acidic → lime/PH_LIME/red.
- low_nutrient → fertilise/TDS_LOW/amber (simulated), over_fertilised → skip_fertiliser/TDS_HIGH/amber (simulated).
- Null pH → `OK (partial)/no pH reading`.
- Idempotent repeat of (device_id, seq).
- Calibration GET as the device; command delivered once.
- Ripeness inference (or 503 when no model is loaded).
- Evidence chain verified; audit pack has the head hash and clauses.
- Harvest plan, cascade, and dashboard assets all return 200.

## Training results
- **M6 (SIMULATED data):** hold-out accuracy against noisy labels **0.88**. Per class: irrigate F1 0.94, drain 0.92, lime 0.88, skip 0.88, ok 0.87, fertilise 0.82, watch 0.58. See `training/fertiliser/metrics_m6.json`.
- **M1 provisional (CPU, D2-only):** see `training/ripeness/m1_metrics_provisional.json` and the summary in `03_ai_models.md` §9.
  - Trained on a subset of D2-train (Malaysia) because the D1 download from Mendeley's S3 bucket runs at a few KB/s from this machine.
  - **No underripe class in D2**, so the model never predicts "underripe" reliably.
  - The **full model** (D1 train → D2 cross-country test, GPU fine-tune) is produced by the stakeholder's Kaggle run (`training/RUN_ON_KAGGLE.md`). The notebook downloads D1 at datacentre speed.

## Verification defect log (Software-owned)
| ID | Fix |
|---|---|
| D-04 | `/latest` = non-buffered reading with the highest seq; chart ordered by `captured_at` |
| D-12 | Demo keys disabled in cloud mode; admin token mandatory (fail closed) |
| S-01 | Dashboard `get()` sends `X-Admin-Token` |
| S-02 | Documented here, in 06 §4.3, DEPLOY_AZURE §7 and ALTERNATIVES |
| S-03 | `ts` validated as ISO-8601 with a timezone, normalised to UTC `…Z`; unparseable or > 24 h in the future → null (warning logged) |
| S-04 | `override_action` validated against the soil action vocabulary or the ripeness classes, depending on the record kind |
| S-05 | "One backend at a time" rule in 06, DEPLOY_AZURE, ALTERNATIVES |
| S-06 | Repeat `(device_id, seq)` with identical sensor values → original response, `duplicate: true`, no new evidence. **Deviation, flagged for the Lead:** if the same seq arrives with *different* values (device restarted and seq reset), it is stored as new rather than silenced, and a warning is logged. This is not a DB unique constraint |
| S-07 | Pending captures are coalesced; commands expire after 60 s |
| S-08 | In cloud mode all reads except `/health` need the admin token (header or `?token=`). The dashboard and harvester view pass it on. Image/heat-map paths stay unauthenticated (documented) |
| S-09 | Smoke test asserts every result; exits non-zero on failure |
| S-10 | Audit pack prints the chain head hash as an external anchor |
| S-11 | Footer: "Contains modified Copernicus Sentinel data (2024–2026), processed in Google Earth Engine" |
| S-13 | Cascade retries until loaded; harvester page handles offline; EC tile label depends on `ec_derived` |
| S-14 | Chart.js MIT banner restored + `vendor/LICENSE-chartjs.txt` |
| S-15 | Image-cache names use md5 (stable across runs) |
| S-12 | Hardware-owned (firmware LOCAL rounding). No backend change needed |

## Interface changes requested
None open. v0.2.5 implemented. Backend-only additions:
- `ALL_OK` rule ID.
- `received_at`, `captured_at` and `duplicate` in the POST response.
- `cal_id` in the calibration body.
- `coalesced` on command POST.

## Assumptions
- Harvest round default 10 days (AHMAD2020; MPOB-NEWS2020).
- Harvester productivity by palm age, derived from team figures (AHMAD2020).
- Crew of 30 and the 8-block demo estate are SIMULATED.
- Neighbour-spread scale of 36 m, about 4 rows (KHOO2023).

## Open issues for Lead
1. **D1 not downloadable here** (Mendeley S3 at a few KB/s). The provisional M1 is D2-only. The final M1 depends on the stakeholder's Kaggle run, which is ready to go.
2. The S-06 deviation described above: please confirm.
3. M3/M4 (drone YOLO) not trained: a stretch item. The cascade's stage 2 shows "not yet available" until it exists.
4. Satellite panel shows a labelled SIMULATED placeholder until the stakeholder runs `gee/ndvi_estate.py`.
5. Brief item 4 (student build and cost table in 04) conflicts with D23. Resolved by moving that content to 07 and `deploy/`, and keeping enterprise cost drivers as risk only in 04.

## Research requests
- R1: answered (wave 2).

## New sources used
None beyond `01_research/sources.md`. Keys used in 01–05 include AZ-*, MPC-S2, MPOCC-P31, MAYER-PDPA2025, AHMAD2020, MPOB-NEWS2020, COOPER2011, HASSAN2026, TTS-AZURE, ANZUM2022, MPOB-APPS2025.
