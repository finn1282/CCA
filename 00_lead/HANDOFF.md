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

## 4. Current state (2026-11-24)
Decisions through **D51**. INTERFACES **v0.2.6**.
| Member | Status | Next on resume |
|---|---|---|
| Research | Waves 1–4 done (119 sources; `10_audit_wave.md` = AWS rescoring, ERP, MSPO Part 3-2) | On demand only |
| Hardware | ✅ All verification fixes through pass 2 (345ec07); fw 0.2.6. Compile = stakeholder build step (D43) | Only if HW verif pass 3 finds issues |
| Software | 🔄 D50 residency/platform edits to docs 02–04, then S-16…S-25 fixes (D51) | Resume `briefs/software.md` with D50 + D51 lists |
| HW Verification | ✅ Pass 2 (30/32; fixes since landed) | Pass 3 after stakeholder compile + bench tests |
| SW Verification | ✅ Pass 2 (156/164, 0 fail; S-16…S-19 major) | Pass 3 after S-16…S-25 fixes |
| Technical summary | ✅ `04_technical/TECHNICAL_SUMMARY.md` | Refresh after D50/D51 changes |
| Report | 🔄 Revision: audit fixes C-01…C-23 + D49/D50/D51 (OUTLINE v4 → REPORT.md) | Resume `briefs/report.md` with `07_verification/compliance/REPORT_AUDIT_1.md` |
| Presentation | 🔄 Step 2 build (storyboard approved D48; D50 residency, D51 no accuracy figures) | Resume `briefs/presentation.md` Step 2 |
| Compliance | ✅ Report audit 1 (24.5 → ~28/30) | Re-audit report after revision; audit presentation after build |

**Stakeholder to-dos:** regenerate the Kaggle token, then run RUN_ON_KAGGLE; Earth Engine run; Azure deploy (after S-18/S-19 fixes) or laptop fallback; buy demo items; bench tests B-01… (B-01 first); fill the placeholders.
**Relaunch:** subagents don't survive sessions. Relaunch from `00_lead/briefs/` with the resume preamble.

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
