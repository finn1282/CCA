# Handoff Plan — read this to take over the project

**Last updated:** 2026-11-23 (Phase 0 complete, Phase 1 started)

## 1. What this project is
ITS69404 Cognitive Computing group assignment (30%), Case #4 Smart Palm Oil Plantation Management.
Deliverables: Markdown report (Parts 1–3 + progress report), interactive presentation + script (15 min, 5 speakers), small hardware demo (ESP32 soil node + ESP32-CAM on a potted plant), technical summary. Deadline **15 Dec 2026 00:00**.

## 2. Where everything is
| Path | What |
|---|---|
| `initial_plan.md` | Original stakeholder brief (unchanged) |
| `CCA Group Assignment.pdf` | Assignment brief and rubric (the target) |
| `components.md` | Hardware already owned |
| `00_lead/SPEC.md` | **Source of truth** — requirements, rubric, scope, confirmed facts |
| `00_lead/DECISIONS.md` | All stakeholder/lead decisions |
| `00_lead/INTERFACES.md` | HW↔SW data contract |
| `00_lead/PROJECT_PLAN.md` | Team, phases, gates, working rules |
| `00_lead/PROJECT_OVERVIEW.md` | Live status + rubric tracker + risks |
| `00_lead/briefs/` | Exact prompts for each team member (to relaunch subagents in a new session) |
| `0X_<team>/README.md` | Each team's status, inputs, outputs, open issues |

## 3. How to continue
1. Read `PROJECT_OVERVIEW.md` to see the current phase and anything blocked.
2. Read `SPEC.md` + `DECISIONS.md`.
3. Open the README of the team in the current phase; its "Status" and "Open issues" say exactly what's left.
4. Continue that phase following `PROJECT_PLAN.md` working rules (commit + push after every step).
4a. Check each team's `PLAN.md` Proposals table for rows with no Lead ruling — rule on them first (see PROJECT_PLAN.md "Team plans & change proposals").
5. When a phase finishes, run the Lead checklist in `PROJECT_PLAN.md`, update OVERVIEW, SPEC §8 and this file.

**Subagents do not survive the session that launched them.** A new session must relaunch members using the saved prompts in `00_lead/briefs/` (see `briefs/README.md`); each member resumes from its folder's README/PLAN. Any member that was mid-task when the old session ended has at most one unpushed file lost.

If using Claude Code: start a session in this repo and say *"You are the project lead. Read 00_lead/HANDOFF.md and continue from the current phase."*

## 4. Current state (2026-11-23, wrapping up — stakeholder low on usage; no new tasks)
| Member | Status | Next action on resume |
|---|---|---|
| Research | Waves 1–3 done (101 sources). Idle | Only on new `01_research/REQUESTS.md` rows |
| Hardware | Docs 01–06 + firmware pushed; stopped (D43) before compile. Pass-1 fixes + v0.2.3/v0.2.4 changes: check `git log -- 02_hardware` and README for which landed | Resume `briefs/hardware.md`: confirm D-01/D-02/D-03 + v0.2.3 (NO DATA, rounding, shared keys) are in the code/docs; **no compile here** — compile happens on stakeholder's machine (assembly guide step 1) |
| Software | ✅ Step 2 complete (D42): docs 01–05, 32/32 tests, provisional M1 (not reportable), run guides `training/RUN_ON_KAGGLE.md`, `deploy/DEPLOY_AZURE.md`, `deploy/ALTERNATIVES.md`, `gee/RUN_EARTH_ENGINE.md`, `06_implementation_guide_beginner.md`, `07_actual_build_vs_target.md` | Only if stretch drone YOLO wanted, or fixes from SW verif pass 2 |
| HW Verification | Pass 1 ✅ (2 major/10 minor) | Pass 2 (deferred): static re-check of fixes vs v0.2.4; compile is a stakeholder build step (D43) |
| SW Verification | Pass 1 ✅ (132/154; 2 major/13 minor — all fixed by SW in 9bd2e04) | **Pass 2 (deferred):** re-test fixes, provisional M1 endpoint + heatmap, docs 01–05 vs D20/D23/D32, run guides for beginner correctness |
| Report | ✅ Full draft v1 done & Lead-gated (D41): `05_report/REPORT.md`, ~4,270 words, 26 refs | Stakeholder review; fill placeholders; optional ledger citation; then compliance audit |
| Technical summary (04_technical), Presentation (06_presentation, storyboard approval first per D36), Compliance audit | **Not started** — Lead writes briefs | — |

**Stakeholder to-dos:** regenerate Kaggle token (was pasted in chat); run Kaggle training via `03_software/training/RUN_ON_KAGGLE.md` (gives the real D1→D2 M1 model); Earth Engine project ID → `EE_PROJECT` + `03_software/gee/RUN_EARTH_ENGINE.md` when written; resolve Azure for Students sign-up (else laptop backend is primary per D39); buy demo items (D21, D27); run hardware bench tests B-01…B-16 (B-01 pH board voltage **before** wiring to GPIO35).
**Relaunch note:** a new session must relaunch members from `00_lead/briefs/` with the resume preamble (subagents don't survive sessions).

## 5. Phase log
| Date | Event |
|---|---|
| 2026-11-23 | SW verif pass 1 (D39), report outline approved (D40); wrap-up requested by stakeholder |
| 2026-11-23 | HW verification pass 1 (D33), report Part 1 gate (D34), research wave 3 (101 sources) |
| 2026-11-23 | Research wave 2 (D32), SW smoke test, verification + report started; all paused at usage limit |
| 2026-11-23 | HW/SW plans ruled, INTERFACES v0.2, Step 2 + research wave 2 started |
| 2026-11-23 | Research gate passed; D14–D22; Hardware + Software launched (PLAN step) |
| 2026-11-23 | Member briefs saved to `00_lead/briefs/` for cross-session relaunch |
| 2026-11-23 | Team PLAN.md + proposal/ruling process added (D13) |
| 2026-11-23 | Baseline research must finish before other teams start (D12) |
| 2026-11-23 | Switched to parallel pipeline + on-demand research + citations in every section (D10, D11) |
| 2026-11-23 | Brief saved, assignment read, stakeholder Q&A done (D1–D9), Phase 0 files pushed |
