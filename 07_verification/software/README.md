# 07_verification/software: README

## Status
**Pass 1 is complete (23 Nov 2026).** It was triggered by M1 (backend smoke test).

What was tested:
- software `b3cb4fe`
- firmware `54eea6c`
- INTERFACES **v0.2.2**

Results:
- Owner's suite: 22/22 `pytest` pass, and the smoke test passes.
- Independent contract and firmware script: 154 checks, giving **132 pass · 3 fail · 13 pass (obs) · 6 blocked**.
- The model tests are blocked: M1 is still training and `/infer/ripeness` returns 503.

HW defects D-04, D-12 and D-09 were retested and are **fixed**.

## Latest pass
`PASS_1_REPORT.md`: backend and contract, firmware↔backend payloads, dashboard, and datasets as documented so far.

## Open defects
**15 open: 2 major, 13 minor, 0 blockers.**

| ID | Sev | Owner | One line |
|---|---|---|---|
| S-01 | major | Software | Cloud/token mode: the dashboard's calibration GET sends no token → 403, so the TDS panel is blank |
| S-02 | major | Software (+HW) | Laptop fallback only accepts demo keys unless `SAWIT_DEVICE_KEYS` is exported; nodes have one key for both bases → LAN answers 401 |
| S-03 | minor | Software | `ts` not validated; a bad string becomes `captured_at` and sorts as the newest chart point |
| S-04 | minor | Software | `override_action` accepts any string (pollutes the audit trail and retraining queue) |
| S-05 | minor | Lead/SW/HW | Cloud and LAN are separate DBs and command queues; demo needs a single-backend rule |
| S-06 | minor | Software | No `(device_id, seq)` idempotency, so retries duplicate evidence |
| S-07 | minor | Software | Command queue has no de-dup or expiry |
| S-08 | minor | Software | Read endpoints are unauthenticated in cloud mode |
| S-09 | minor | Software | `smoke_test.sh` prints PASSED without assertions |
| S-10 | minor | Software | Hash chain has no external head anchor (tail truncation is undetectable) |
| S-11 | minor | Software | Copernicus notice has no year and names Planetary Computer instead of Earth Engine |
| S-12 | minor | Hardware | LOCAL vs CLOUD: rounding at edges, all-null shown as green OK, 1-dp pH on the OLED (coordination with HW verification) |
| S-13 | minor | Software | Cascade is fetched only once; harvester page has no offline handling; EC tile label |
| S-14 | minor | Software | Chart.js MIT banner stripped from the vendored file |
| S-15 | minor | Software | `train_m1.py` cache names use the randomised `hash()`, so the cache is never reused |

## Outputs
| File | Content |
|---|---|
| `TEST_PLAN.md` | Every test case with ID, method, expected result, status and evidence, plus the **presentation-day rehearsal checklist** (§H) |
| `PASS_1_REPORT.md` | Pass 1 results, defects table, retests, what Pass 2 needs |
| `tests/contract_test.py` | Independent black-box tests: v0.2.2 endpoints, §4 edges, auth, cloud fail-closed, tamper detection, firmware payloads and parser emulation, dashboard offline checks |
| `tests/pass1_results.md` | Per-check output of the Pass 1 run |

## How to rerun
```bash
cd /home/zhen/Documents/taylors/CCA
S=<your scratch dir>                     # never inside the repo; don't commit venvs
python3 -m venv $S/venv && $S/venv/bin/pip install -r 03_software/src/requirements.txt
# independent suite: starts and stops its own servers (3 instances, one after another) on the given port
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 $S/venv/bin/python 07_verification/software/tests/contract_test.py --port 8833 --out $S/results.md
# owner suite (writes runtime files to $S only)
cd 03_software/src && PYTHONDONTWRITEBYTECODE=1 SAWIT_RUNTIME_DIR=$S/rt TMPDIR=$S $S/venv/bin/python -m pytest -q -p no:cacheprovider
PY=$S/venv/bin/python PORT=8833 TMPDIR=$S ./smoke_test.sh
```
- Use a free port. Do not use 8765 or 8791, which other members use.
- Exit code 0 means no FAIL.
- When the M1 model exists (`03_software/models/m1_ripeness.onnx` + `.json`), RI-04 reports OBS. The RI-05…09 model checks are added in Pass 2.

## Inputs used
- 00_lead: SPEC, PROJECT_PLAN, DECISIONS (D16, D20, D23, D28, D29, D31–D33), INTERFACES v0.2.1 → v0.2.2
- 01_research: `03_datasets.md`, `00_baseline_brief.md` §Verification
- 03_software: README, PLAN, `src/`, `training/`, `scripts/`
- 02_hardware: `firmware/*.ino`, `secrets.h.example`
- 07_verification/hardware: README and PASS_1_REPORT, read for coordination; HW firmware internals were not duplicated

## Next pass
**Pass 2** is triggered by M2 (M1 model trained). It needs:
- the ONNX model, its meta and `m1_metrics.json`
- D1 fully extracted and D2 FFBtrain present
- fixes for S-01…S-04

Passes 3 and 4 follow M3 (design docs 01–05) and M4 (Kaggle/Azure/GEE run guides).

## Open issues for Lead
1. S-02 and S-05 affect the demo's fallback story. Please add "same `SAWIT_DEVICE_KEYS` on the laptop" and "one backend at a time" to the demo plan and run guide, or rule otherwise.
2. INTERFACES §2 could state that `ts` must be ISO-8601 UTC (`…Z`) (S-03) and that `(device_id, seq)` is unique (S-06).
