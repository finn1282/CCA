# 03_software — README

## Status
- **Step 1 (plan):** done; all of SW-P1–P8 accepted (D24–D29). INTERFACES v0.2.1 (D30) is implemented.
- **Milestone 1: backend + simulator + rule engine + dashboard.** Done 23 Nov 2026. 17/17 tests pass and the end-to-end smoke test passes (results below). **Ready for SW verification.**
- **Milestone 2: M1 ripeness training.** In progress (CPU path locally; Kaggle path is for the stakeholder, D31).
- Next: design docs 01–05 → implementation guide → 07.

## Inputs used
`00_lead/SPEC.md`, `PROJECT_PLAN.md`, `DECISIONS.md` (D1–D31), `INTERFACES.md` v0.2.1, `CCA Group Assignment.pdf` pp.5–8, `01_research/00_baseline_brief.md`, 01–05, `sources.md`.

## Outputs
| Path | Content |
|---|---|
| `PLAN.md` | Approach, models M1–M7, tasks, ideas, conflicts, proposals (all ruled) |
| `src/app/main.py` | FastAPI app: ingestion, recommendation, calibration GET/POST, commands, ripeness inference, evidence log, compliance, harvest, screening, dashboard |
| `src/app/rules.py` | Explainable rule engine (INTERFACES §4 rule IDs, priority, counterfactual, OLED/LED) |
| `src/app/recommender.py` | Hybrid: rules (authoritative) + M6 tree (confidence + Saabas attributions); M6 trained on SIMULATED data |
| `src/app/evidence.py` | Explain-to-audit log with a SHA-256 hash chain, reviews, MSPO audit pack |
| `src/app/compliance.py` | M7 MSPO knowledge base + coverage reasoner (criterion numbers pending R1b) |
| `src/app/inference.py` | M1 ONNX inference + CAM heatmap + template explanation; M2 harvest-advice rule |
| `src/app/analytics.py` | Harvester allocation (SIMULATED estate) + satellite → drone → ground cascade |
| `src/app/assets/m6_tree.json` | M6 decision tree as JSON (simulated training data, test accuracy 0.88 against noisy labels) |
| `src/static/` | Dashboard (`index.html`, `app.js`, `style.css`, Chart.js stored locally), `harvester.html` mobile view, `precomputed/` panels |
| `src/simulator.py` | Soil-node simulator (stdlib only), 7 scenarios + cycle; can also post a camera image |
| `src/smoke_test.sh` | End-to-end smoke test (starts its own server on port 8791 with a temp DB) |
| `src/tests/test_api.py` | 17 tests: rule table, TDS + simulated flag, priority, nulls, contract, auth, calibration, commands, tamper detection, feeds, ripeness |
| `training/fertiliser/train_m6.py` | Simulated dataset generator + tree training → `m6_tree.json`, `metrics_m6.json` |
| `training/estate/make_demo_estate.py` | SIMULATED demo estate for the harvest/cascade panels |

## How to run (local)
```bash
cd 03_software && python -m venv .venv && .venv/bin/pip install -r src/requirements.txt
cd src && ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000     # dashboard: http://localhost:8000
../.venv/bin/python simulator.py --scenario cycle --interval 2              # second terminal
../.venv/bin/python -m pytest -q && PY=../.venv/bin/python ./smoke_test.sh
```
Demo device keys (local only, overridden by the `SAWIT_DEVICE_KEYS` env var in the cloud): `soilnode-01:demo-soil-key`, `cam-01:demo-cam-key`, `sim-01:demo-sim-key`.

## Smoke test result (23 Nov 2026, laptop CPU, Python 3.14)
Full log in `src/tests/smoke_output.txt`. Summary:
- `/health` ok; 3 warm-up readings → TDS baseline calibrated from the current reading (592 ppm ±30 %).
- A 40-reading scenario cycle produced every action with the correct rule, LED and OLED text: `irrigate` (MOIST_LOW, red), `watch` (PH_LOW_WATCH, amber), `lime` (PH_LIME, red, "pH 3.86<4.0"), `fertilise` (TDS_LOW, amber, simulated), `skip_fertiliser` (TDS_HIGH, amber, simulated), `drain` (MOIST_HIGH, amber). A null pH sensor gave "OK (partial) / no pH reading", with no value invented.
- Calibration GET as the device returned `{"tds_baseline_ppm":592.0,"tds_margin":0.3,...}`.
- Evidence chain: "All 44 records intact (SHA-256 chain)". The MSPO audit pack shows coverage of soil, fertiliser, GHG and traceability; disease, harvest and oversight show as gaps until those events occur. The tamper test in pytest detects an edited record.
- Harvest plan and cascade feeds respond (SIMULATED satellite until the stakeholder runs the GEE export). `/`, `/harvester` and the static assets return 200.
- Ripeness endpoint returns 503 with a clear message until the M1 model file exists (tested).

## Interface changes requested
None open. v0.2.1 implemented in full. Notes for Hardware:
- Rule IDs added beyond §4: `ALL_OK` (ok entry).
- For missing sensors, `oled` = `["OK (partial)","no pH reading"]`.
- `/api/v1/readings` response also carries `received_at`.

## Assumptions
- Harvest round interval of 10 days, harvester productivity of 90 bunches/day and a crew of 12 are placeholders pending R1(e). All three are labelled.
- The demo estate (blocks, ripe-bunch estimates) is SIMULATED.

## Open issues for Lead
1. MSPO criterion numbers, Ganoderma neighbour-spread distance and harvest intervals all wait on research R1. Placeholders are marked `[criterion TBC — R1b]` etc.
2. Something else was running a server on port 8765 during my run (not mine), perhaps the SW tester. The smoke test now uses port 8791.

## Research requests
- R1 (open, wave 2).

## New sources used
None yet.
