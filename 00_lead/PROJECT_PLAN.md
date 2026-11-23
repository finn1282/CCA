# Project Plan — Smart Palm Oil Plantation Cognitive System

Lead: Project Lead (Claude, orchestrator — verifies, directs, owns `SPEC.md`; produces no deliverables).
Deadline: **15 Dec 2026 00:00**. Start: 23 Nov 2026.

## Team (each member = a subagent working in its own folder)
| Team | Member | Folder | Main deliverables |
|---|---|---|---|
| Technical | Research | `01_research/` | Problem evidence, sources (Harvard), datasets, cloud platform/credits study, platform comparison, MSPO/Ganoderma/FFB facts, hardware facts |
| Technical | Hardware | `02_hardware/` | Specs, block/wiring/schematic diagrams, pin map, power budget, BOM (+ optional purchases in MYR), firmware, demo plan, beginner assembly guide |
| Technical | Software & Cloud AI | `03_software/` | Architecture (adapted Fig. 4), cloud AI design, data pipeline, dataset prep, model training notebooks, API + dashboard, HW integration, beginner implementation guide |
| Technical | (Software+Research, Lead-verified) | `04_technical/` | Final technical summary report of the whole system |
| Outputs | Report | `05_report/` | Final report in Markdown, structured exactly to Parts 1–3 + progress report |
| Outputs | Presentation | `06_presentation/` | Interactive/animated web presentation (runs in laptop browser, embeds live demo) + 15-min script split for 5 speakers |
| Verification | HW tester | `07_verification/hardware/` | HW test plan, firmware compile check, pin/power/interface validation |
| Verification | SW tester | `07_verification/software/` | SW test plan, dataset validity, training run check, end-to-end integration dry run |
| Verification | Compliance | `07_verification/compliance/` | Rubric scorecard for report + presentation, gap list |

## Phases & gates
| # | Phase | Runs | Gate (Lead verifies before next phase) |
|---|---|---|---|
| 0 | Setup | Lead | SPEC, PLAN, OVERVIEW, HANDOFF, INTERFACES, DECISIONS pushed |
| 1 | Research | Research | Sources real & citable (≥15 to have margin); problems validated with evidence (not assumed); datasets downloadable + licensed; cloud credits for Malaysian students verified; platform comparison ready. **Stakeholder check-in.** |
| 2 | Build | Hardware ∥ Software | Both conform to `INTERFACES.md`; HW stays a small demo; model trains on a real dataset |
| 3 | Verify | HW tester ∥ SW tester | Tests executed with recorded results; defects fixed by owners |
| 4 | Outputs | Technical summary → Report ∥ Presentation | Every rubric sub-task covered with evidence |
| 5 | Audit | Compliance | Every criterion argued at "Outstanding" band; fix loop until clean |

Target dates: P1 by 26 Nov · P2 by 3 Dec · P3 by 6 Dec · P4 by 10 Dec · P5 by 12 Dec · buffer to 14 Dec.

## Working rules (all members)
1. Read `00_lead/SPEC.md`, `00_lead/DECISIONS.md`, `00_lead/INTERFACES.md`, and the `README.md` of any folder you depend on, **before** starting.
2. Write only inside your own folder (Lead owns `00_lead/`).
3. Keep `<your folder>/README.md` current: Status · Inputs used · Outputs (file list + one line each) · Assumptions · Open issues for Lead.
4. After each meaningful step: `git add <your folder> && git commit -m "<folder>: <what>" && git pull --rebase && git push`. Commit message ends with the Co-Authored-By line.
5. No unverifiable claims: every fact gets a source; every dataset gets a URL + licence; simulated data is labelled as such.
6. Markdown + Mermaid; concise.

## Lead verification checklist (applied at each gate)
- Consistent with SPEC and other teams' outputs (names, numbers, platform, interfaces)?
- Maps to a rubric sub-task in SPEC §2?
- Evidence real (spot-check URLs) and code actually runs?
- README handoff complete?
Results are recorded in `PROJECT_OVERVIEW.md`.
