# SW Verification: Pass 3 Report (retest of S-16…S-25 + D50)

> Date: 24 Nov 2026. Repo HEAD `3cce551` (software fixes `277b3cc`, `2252139`). Contract: INTERFACES **v0.2.6**.
> Environment: the existing `03_software/.venv` (no downloads, no new venv); local D2 only; port **8833**, with every server stopped afterwards.
> The browser was used under D53: one tab of my own in the Claude tab group, localhost dashboard only. I closed the tab afterwards and did not touch the presentation member's tab.

## 1. Summary

**All 10 Pass 2 defects (S-16…S-25) are closed.**
- The serving-path metric reproduces exactly: **0.9136 on n = 81**, with an identical confusion matrix.
- The dedupe covers all 6 of my leaked pairs, plus 2 genuine extras that I checked by eye.
- The deploy zip runs as the guide says: model inside, inline startup command, DELETE journal in cloud mode.
- A 9 MB photo is downscaled and graded.
- The Earth Engine block IDs match the estate.
- Report-facing docs 01–05 contain no build, demo or cost wording.

There is **1 new minor (S-26)** and **0 majors or blockers**.

| Suite | Result |
|---|---|
| Owner `pytest` | **34 / 34 pass** |
| Owner `smoke_test.sh` (asserted, port 8833) | **pass** |
| `tests/contract_test.py` (v0.2.6, 164 checks) | **156 pass · 0 fail · 8 pass (obs) · 0 blocked** (`tests/pass3_results.md`) |
| `tests/eval_m1.py` (now also scores through the API's own `src/app/preprocess.py`) | Reproduces the reported serving-path metric exactly (`tests/pass3_eval_m1.md`) |
| Deploy package, built from a scratch copy and run as `DEPLOY_AZURE.md` §4 says, in cloud mode | pass |
| Dashboard visual check (D53) | pass |

## 2. Retest of S-16…S-25

| ID | What I checked | Result | Status |
|---|---|---|---|
| S-16 train/serve skew | `src/app/preprocess.py` is shared. `inference._preprocess` and `train_m1` (eval transform, cache and post-export serving evaluation) all call it, and the cache is now lossless PNG. My `eval_m1.py` path C, which calls the API module on the original files, gives **0.9136 on the owner's n = 81, CM `[[25,0,6,1],[0,0,0,0],[0,0,36,0],[0,0,0,13]]`**. That is identical to `m1_metrics_provisional.json` `serving_path` and `d2_malaysia_test`. On all 89 images: 0.9213. The model meta carries `metrics_summary_serving_path`. | Reproduced | **closed** |
| S-17 D2 leakage | `train_m1.dedupe_test` (dHash ≤ 6) drops 8 test images and logs them in `d2_test_duplicates_removed`. It **covers all 6 of my pairs** (0 missing). The 2 extras are genuine: `TestRipe(18)`/`TrainRipe(34)` is the same photo, and `TestUnripe(8)`/`TrainUnripe(98)` is the same bunch from another angle (checked visually). The Kaggle notebook embeds `preprocess.py` and `train_m1.py` byte-identical to the repo, so the full-D2 run dedupes too. | Covered | **closed** |
| S-18 SAS 60 days | Blob/SAS has been removed from the critical path. `make_package.sh` puts `models/m1_ripeness.onnx` + `.json` into the zip (15 MB), and `config.MODEL_PATH` prefers the packaged model. I built the zip from a scratch copy and ran it: `/health` gives `ripeness_model: m1-effb0-0.1-provisional`, and a ripeness POST returns 200. The guide now states the ≤ 6-day user-delegation limit for the optional Blob route. | Works | **closed** |
| S-19 WAL on `/home` | `db.py`: `journal_mode=DELETE` when `SAWIT_MODE=cloud`. On the packaged server's DB, `PRAGMA journal_mode` → `delete`, and the chain verified after 35 records. The SMB share itself can only be exercised on Azure (rehearsal R-03b). | Mode correct | **closed** |
| S-20 startup | The guide uses an inline `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 --proxy-headers`. Running exactly that from the extracted zip root starts cleanly ("Uvicorn running …", the line the guide tells beginners to look for). | Works | **closed** |
| S-21 API spec | `05_api_spec.md` §3 now says "read: open locally, admin token in cloud mode". `SAWIT_MODEL_URL`/`_META_URL` are documented with the ≤ 6-day note. | Aligned | **closed** |
| S-22 report wording | Docs 01–05 no longer contain the demo sequence, provisional/Kaggle results or "cheapest". 02 §4 is now residency and 03 §9 is an evaluation plan. The remaining "App Service" mentions are target-design hosting (D50), and 04's header points build detail to 07, as D20 requires. D50 residency layout (Malaysia West in-country, SEA for IoT Hub/DPS/Azure ML/Ledger/OpenAI on non-personal data) and the D32b RAI scoping are consistent across 02/03/04. | Clean | **closed** |
| S-23 image size | `simulator.py --image` shrinks to ≤ 1600 px. A **9.0 MB** `TestRipe(15).jpg` posted to the cloud-mode server gives `ripe 0.742`. 06 and the Kaggle guide explain this, and 06 §9 lists the 8 duplicate photos not to print. | Works | **closed** |
| S-24 block IDs | `ndvi_estate.block_id()` on a 3×3 grid gives `DEMO-A1, A2, A3, B1, B2, B3, C1, C2, C3`, identical to `estate_blocks.json` (now 9 blocks incl. C3). Harvest table, cascade and evidence all show those IDs on the dashboard. | Consistent | **closed** |
| S-25 Windows note | `RUN_EARTH_ENGINE.md:13` | Present | **closed** |

## 3. Dashboard visual check (D53, localhost:8833, cloud mode `?token=`)

I ran it from the packaged build, seeded with the simulator, a calibration and two camera uploads.
- **Header:** CLOUD and live pills; the evidence count updates.
- **Soil tiles and chart:** render, with the EC label "≈TDS/0.5" shown only when EC is derived. The chart is ordered by capture time.
- **Recommendation card:** FERTILISE with the SIMULATED badge, the rule trace, the counterfactual and the ML check.
- **Camera card:** `m1-effb0-0.1-provisional`; side-by-side heat-map hot on the bunch; probability bars; template explanation; harvest advice.
- **TDS calibration panel:** populated in token mode (S-01 confirmed visually).
- **Cascade:** labelled SIMULATED, 2/9 blocks flagged (B2, C1); the drone stage is honestly "not yet available".
- **Harvest table:** all 9 estate blocks.
- **Evidence:** "Verify chain" gives ✔ "All 35 records intact"; SIM badges shown.
- **MSPO panel:** coverage tiles render.
- **Footer:** Copernicus (2024–2026, Earth Engine) and the CC BY 4.0 credits.
- **Console:** no errors.
- **Backend stopped:** the pill turns red **offline** and the last values stay on screen.

## 4. Defects

| ID | Severity | File:line | Issue | Suggested fix | Owner | Status |
|---|---|---|---|---|---|---|
| S-26 | minor | `03_software/src/app/compliance.py:3,13-…` (shown on the dashboard MSPO panel and in the audit pack) | The code labels every clause "MS 2530:2022 …". D50 and docs 01–04 (and the report) cite **MS 2530-3-2:2022** (estates > 500 ha) and **MS 2530-4-1:2022** (mills). The dashboard on screen during the presentation would therefore disagree with the report. | Change the `ref` strings to `MS 2530-3-2:2022 <clause>` (estate records) and `MS 2530-4-1:2022` where mill-side, then re-run the smoke test. | Software | open |

**Observations (no action required):**
- **Camera card ordering:** probability bars are listed alphabetically (overripe, ripe, underripe, unripe) rather than in ripeness order. Ordinal order would read better on a slide.
- **Untrained underripe column:** the provisional model can show a small "underripe" probability (7 % on one D2 image; RI-12). The final D1 model fixes this.
- **Empty panel area:** while the satellite stage is SIMULATED, the NDVI chart area in the cascade card is empty white space.
- **Carried over from earlier passes:** AU-06, PR-02, NU-04, RP-11, CA-14, FW-08, EV-16 (see TEST_PLAN).

## 5. What the next pass needs

- The S-26 fix.
- The stakeholder's Kaggle D1→D2 outputs (MD-07): re-run `eval_m1.py` path C on D2-test with the final ONNX; the deduped n is in the run log.
- The Azure URL, for rehearsal R-03/R-03b on the real `/home` share.
- The committed `satellite.json` after the Earth Engine run, to confirm the cascade on real data with the matching IDs.

## 6. How to reproduce

```bash
cd /home/zhen/Documents/taylors/CCA; S=<scratch>; PY=03_software/.venv/bin/python
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 $PY 07_verification/software/tests/contract_test.py --port 8833 --out $S/results.md
PYTHONDONTWRITEBYTECODE=1 $PY 07_verification/software/tests/eval_m1.py --out $S/eval_m1.md
# deploy package: copy src/, deploy/make_package.sh and models/m1_ripeness.* into $S/pkg/sw, run make_package.sh there,
# unzip, then start the §4 inline startup command (port 8833) with SAWIT_MODE=cloud, keys, token and SAWIT_RUNTIME_DIR in $S
```
