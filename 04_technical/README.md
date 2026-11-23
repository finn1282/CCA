# 04_technical — README

## Status
**The technical summary is written (23 Nov 2026).** It is an internal document (D20) that covers both the target design and the actual build, with each section labelled [TARGET], [BUILD] or [BOTH].
- **Length:** ≈ 2,750 words of prose, plus tables and 3 Mermaid diagrams (≈ 4,250 words in total).
- **Citations:** every key cited resolves in `01_research/sources.md`.
- **Checks re-run for this summary:** owner tests, 32/32 pass.

## Outputs
| File | Content |
|---|---|
| `TECHNICAL_SUMMARY.md` | Nine sections, one per brief item: (1) overview; (2) target Azure architecture; (3) actual build; (4) hardware demo; (5) interfaces v0.2.4; (6) datasets & models; (7) verification status; (8) build & run order; (9) limitations & next steps |
| `README.md` | This file |

## Inputs used
- **00_lead:** SPEC, DECISIONS (D1–D44), INTERFACES v0.2.4, PROJECT_PLAN.
- **01_research:** README, `00_baseline_brief.md`, `03_datasets.md` (D4 facts), `sources.md`.
- **02_hardware:** README, docs 01–06, both `.ino` files and `secrets.h.example`.
- **03_software:** README, docs 01–07, `models/README.md` + metrics, `metrics_m6.json`, `estate_blocks.json`, the RUN_ON_KAGGLE, DEPLOY_AZURE, ALTERNATIVES and RUN_EARTH_ENGINE guides, and the `main.py` route list.
- **07_verification:** hardware and software READMEs, TEST_PLANs (B-01…B-16, §H R-01…R-14).

## Assumptions
- Defects that owners report as fixed (D-01…D-12, S-01…S-15) are shown as "fixed, not independently retested". Pass 2 is deferred (D42), and there has been no compile (D43).
- The M1 final metrics, the Azure URL and the GEE export are shown as pending, because they are stakeholder steps (D31).

## Inconsistencies found (for the Lead)
| # | Where | Inconsistency | Suggested fix |
|---|---|---|---|
| 1 | Calibration fetch interval | INTERFACES §5 and `03_software/05_api_spec.md` §2.2 / `06_…` §5 say the soil node fetches its TDS baseline **hourly**. The firmware (`CAL_FETCH_MS = 300000`) and `02_hardware/02_system_design.md` §2 use **every 5 min** | Harmless, but align the text: either INTERFACES says "boot + periodically (firmware: 5 min)", or the firmware changes to 1 h |
| 2 | Version labels | INTERFACES is **v0.2.4** (D42). However, `03_software/README.md` and `07_actual_build_vs_target.md` say v0.2.3, `05_api_spec.md` is titled **v0.2.2**, `APP_VERSION`/`rules_version` = 0.2.3 / "INTERFACES-v0.2.3", and `02_hardware/README.md` says v0.2.3 | Bump the doc headers to v0.2.4 (the content already implements the S-06 behaviour) |
| 3 | `07_verification/*/README.md` | Both still list all HW (D-xx) and SW (S-xx) defects as **open**, although D33, D39 and D42 and the owner READMEs record them as fixed | Expected until pass 2 runs. Add a status note ("fixed by owner, retest pending") so readers are not misled |
| 4 | `02_hardware/README.md` open issue 2 | Says [ESP32-DS] and [AZ-CA] are not yet in `sources.md`. **Both are now present** | Close the issue |
| 5 | `02_hardware/README.md` "Verification notes" | "Compile status: see the latest commit message", but per D43 no compile has run | State "not compiled (D43); compile on the builder's machine" |
| 6 | Function numbering | The technical-summary brief names **F1–F5**. `03_software/01_solution_overview.md` defines **F1–F6** (F6 = analytics) | Confirm which list the report/presentation use. The summary shows F1–F5 plus F6 |
| 7 | Platform scores in research files | `01_research/README.md` key finding 9 and `00_baseline_brief.md` still quote **83/78/68/49**. D15's row says 83/100. D32d supersedes these with **88/79/67/49** | Add a "superseded by D32d" note in those two places (the README's wave-2 section already gives 88/79/67/49) |
| 8 | TDS baseline wording | `03_software/06_…` §5 step 2 says set the baseline from the "normal" soil-water slurry. The hardware demo plan (D-01, D33) uses the **REFERENCE cup** | Reword 06 §5 to "REFERENCE cup" so the three-cup beat works |
| 9 | MSPO clause list | D32f lists 4.1.3, 4.1.3.4, 4.2.2, 4.5.4, 4.5.5. `03_ai_models.md` M7 and `compliance.py` also use **4.1.3.1** and **4.1.3.5** (sub-clauses of 4.1.3) | An extension, not a contradiction. Confirm the report uses the same clause numbers as the code's audit pack |

None of these affects the system design or the decisions; items 1, 6 and 8 are the ones worth fixing before rehearsal or the report freeze.

## Open issues for Lead
- Once the stakeholder's Kaggle run finishes, update `TECHNICAL_SUMMARY.md` §6 and §9 with the final M1 metrics. Do the same after the Azure deployment, the GEE export and HW/SW pass 2.

## New sources used
None. Every key comes from `01_research/sources.md`.
