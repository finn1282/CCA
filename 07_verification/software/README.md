# 07_verification/software: README

## Status
**Pass 3 is complete (24 Nov 2026).** It retested S-16…S-25 and D50 at HEAD `3cce551` (software `277b3cc` + `2252139`) against INTERFACES **v0.2.6**. It used the existing `03_software/.venv`, local D2 only, and no downloads.

Results:
- **Pass 2 defects:** all 10 (S-16…S-25) are **closed**. Pass 1's 15 were closed earlier.
- **Owner suite:** 34/34 `pytest` pass, and the asserted smoke test passes.
- **`contract_test.py`:** 164 checks, giving **156 pass · 0 fail · 8 pass (obs) · 0 blocked**.
- **M1 serving-path metric:** reproduced exactly, **0.9136 on n = 81**, identical confusion matrix. The dedupe covers all of my leaked pairs.
- **Deploy package:** built from a scratch copy and run with the guide's startup command in cloud mode. The model is in the zip, the journal is DELETE, and a 9 MB photo is downscaled and graded.
- **Dashboard:** checked visually in the browser (D53, own tab, closed afterwards). Everything renders, Verify chain ✔, and "offline" shows when the backend stops.

## Latest pass
`PASS_3_REPORT.md`. Earlier passes: `PASS_2_REPORT.md`, `PASS_1_REPORT.md`.

## Open defects
**1 open: 0 major, 1 minor, 0 blockers.**

| ID | Sev | Owner | One line |
|---|---|---|---|
| S-26 | minor | Software | Dashboard and audit pack label clauses "MS 2530:2022"; D50 and docs cite MS 2530-3-2:2022 / 4-1:2022 (`src/app/compliance.py`) |

## Outputs
| File | Content |
|---|---|
| `TEST_PLAN.md` | All test cases with status and evidence, plus the presentation-day rehearsal checklist (§H) |
| `PASS_1_REPORT.md`, `PASS_2_REPORT.md`, `PASS_3_REPORT.md` | Pass results, defects, retests, next-pass needs |
| `tests/contract_test.py` | Black-box v0.2.6 suite: endpoints, §4 edges, auth/cloud mode, idempotency, commands, tamper, firmware payload/parser emulation, ripeness endpoint with the model, dashboard offline checks |
| `tests/eval_m1.py` | Independent M1 re-evaluation on local D2. It scores a legacy path and the API's shared `preprocess.py` path, on the full set and the owner-deduped set, cross-checks the class mapping, and scans for leakage (MD5/dHash), including whether the owner's dedupe covers my list |
| `tests/pass{1,2,3}_results.md`, `tests/pass{2,3}_eval_m1.md` | Raw outputs of each run |

## How to rerun
```bash
cd /home/zhen/Documents/taylors/CCA
S=<your scratch dir>; PY=03_software/.venv/bin/python     # existing venv only (D43/D44)
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 $PY 07_verification/software/tests/contract_test.py --port 8833 --out $S/results.md
PYTHONDONTWRITEBYTECODE=1 $PY 07_verification/software/tests/eval_m1.py --out $S/eval_m1.md
cd 03_software/src && PYTHONDONTWRITEBYTECODE=1 SAWIT_RUNTIME_DIR=$S/rt TMPDIR=$S ../.venv/bin/python -m pytest -q -p no:cacheprovider
PY=../.venv/bin/python PORT=8833 TMPDIR=$S ./smoke_test.sh
```
- Use a free port. Do not use 8765, 8791 or 8844/8845, which the presentation uses.
- Never download datasets or packages (D43).
- To test the deploy zip, build it from a **scratch copy** so nothing is written into `03_software/deploy/` (PASS_3 §6).

## Inputs used
- 00_lead: DECISIONS (D20, D23, D31–D33, D39, D43–D53), INTERFACES v0.2.6
- 03_software: docs 01–07, `src/` (incl. `app/preprocess.py`), `training/` (incl. `kaggle/`), `deploy/`, `gee/`, `models/` (provisional), `data/raw/d2`
- 02_hardware: `firmware/*.ino`

## Next pass
It is triggered by any of these:
- the S-26 fix
- the stakeholder's Kaggle D1→D2 model (MD-07)
- the Azure URL (R-03/R-03b on the real `/home` share)
- the Earth Engine `satellite.json`

## Open issues for Lead
1. S-26 matters for the presentation: the MSPO panel on screen should cite the same standard parts as the report (D50).
