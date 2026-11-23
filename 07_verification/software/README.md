# 07_verification/software: README

## Status
**Pass 2 is complete (23 Nov 2026).** It covered milestones M2–M4 and was tested at HEAD `345ec07` (software `1ad0560`) against INTERFACES **v0.2.6**. It used the existing `03_software/.venv` and local D2 images only (D43/D44).

Results:
- **Pass 1:** all 15 defects (S-01…S-15) are **closed**.
- **Owner suite:** 33/33 `pytest` pass, and the asserted smoke test passes.
- **`contract_test.py`:** 164 checks, giving **156 pass · 0 fail · 8 pass (obs) · 0 blocked**. This includes the ripeness endpoint with the provisional model: p95 0.08 s on CPU, heat-map served.
- **`eval_m1.py`:** the class mapping is correct. The reported 0.9326 reproduces only on the training pipeline; the **serving path gives 0.8989**. 6/89 D2-test images duplicate D2-train images.
- **M6:** retrained from a scratch copy and reproduces exactly (0.88375, identical tree).
- **Docs 01–05:** D32 residency and RAI scoping are correct. Build/demo/cost wording appears in 02/03.
- **Run guides:** Kaggle OK. Azure has 3 issues. Earth Engine is OK, with 2 minor issues.

## Latest pass
`PASS_2_REPORT.md`. The previous pass is in `PASS_1_REPORT.md`.

## Open defects
**10 open: 4 major, 6 minor, 0 blockers.** All are owned by Software.

| ID | Sev | One line |
|---|---|---|
| S-16 | major | Mismatch between training and serving preprocessing: reported D2-test 0.93 vs **0.90** on the deployed inference path |
| S-17 | major | D2 split leakage: 6/89 test images are the same photos as train images (pair list in `tests/pass2_eval_m1.md`) |
| S-18 | major | DEPLOY_AZURE: user-delegation SAS asked for 60 days, but the limit is 7 days, so step 3 fails |
| S-19 | major (risk) | SQLite WAL on App Service `/home` (SMB share) risks "database is locked"; use `journal_mode=DELETE` in cloud |
| S-20 | minor | `--startup-file "startup.sh"` relies on a bare file name and the exec bit; use `bash startup.sh` |
| S-21 | minor | `05_api_spec` says cloud reads are open and omits `SAWIT_MODEL_URL`/`_META_URL` |
| S-22 | minor | Report-facing 02/03 contain build/demo/cost wording (03 §9 provisional/Kaggle, 02 §4 demo, "cheapest") |
| S-23 | minor | Guides post D2 originals that are > 5 MB (413); printed photos should come from FFBtest minus the leaked ones |
| S-24 | minor | GEE block IDs `B01–B16` don't match the estate/drone IDs used by the cascade and demo story |
| S-25 | minor | `RUN_EARTH_ENGINE.md` has no Windows `.venv\Scripts` note |

## Outputs
| File | Content |
|---|---|
| `TEST_PLAN.md` | All test cases with status and evidence, plus the presentation-day rehearsal checklist (§H, now with R-03b cloud DB check) |
| `PASS_1_REPORT.md`, `PASS_2_REPORT.md` | Pass results, defects, retests, what the next pass needs |
| `tests/contract_test.py` | Black-box v0.2.6 tests: endpoints, §4 edges, auth/cloud mode, idempotency, commands, tamper, firmware payload/parser emulation (v0.2.3 rounding), ripeness endpoint with the model, dashboard offline checks |
| `tests/eval_m1.py` | Independent M1 re-evaluation on local D2 (serving vs training preprocessing, deduplicated test), class-mapping cross-check, MD5/dHash leakage scan |
| `tests/pass1_results.md`, `tests/pass2_results.md`, `tests/pass2_eval_m1.md` | Raw outputs of each run |

## How to rerun
```bash
cd /home/zhen/Documents/taylors/CCA
S=<your scratch dir>                      # never inside the repo
PY=03_software/.venv/bin/python           # use the existing venv; do not create new ones (D43/D44)
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 $PY 07_verification/software/tests/contract_test.py --port 8833 --out $S/results.md
PYTHONDONTWRITEBYTECODE=1 $PY 07_verification/software/tests/eval_m1.py --out $S/eval_m1.md        # ~2 min, local D2 only
cd 03_software/src && PYTHONDONTWRITEBYTECODE=1 SAWIT_RUNTIME_DIR=$S/rt TMPDIR=$S ../.venv/bin/python -m pytest -q -p no:cacheprovider
PY=../.venv/bin/python PORT=8833 TMPDIR=$S ./smoke_test.sh
```
- Use a free port. Do not use 8765 or 8791.
- `contract_test.py` starts and stops its own servers (3 instances, one after another) and exits with 0 when there is no FAIL.
- Never download datasets or packages for these tests (D43).

## Inputs used
- 00_lead: SPEC, DECISIONS (D16, D20, D23, D31–D33, D39–D47), INTERFACES v0.2.6
- 01_research: `03_datasets.md`
- 03_software: README, docs 01–07, `src/`, `training/` (incl. `kaggle/`), `deploy/`, `gee/`, `models/` (provisional), `data/raw/d2`
- 02_hardware: `firmware/*.ino`
- 07_verification/hardware: PASS_2 (coordination only; firmware internals not duplicated)

## Next pass
It is triggered by either of these:
- fixes for S-16…S-19
- the stakeholder's Kaggle D1→D2 model, Azure URL or EE export (MD-07, R-03/R-03b, S-24)

## Open issues for Lead
1. **S-16/S-17:** any M1 number that reaches the report or slides should be the serving-path, deduplicated figure. D40 already keeps prototype results out of the report, but the presentation may quote them.
2. **S-18/S-19:** fix these before the stakeholder runs the Azure guide (D31), so the first account-bound attempt does not fail.
