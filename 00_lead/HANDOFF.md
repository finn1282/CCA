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

## 4. Current state (2026-11-24) — ALL TEAM WORK COMPLETE; waiting on stakeholder
Decisions through **D58**; INTERFACES **v0.2.6**; no members running.
| Deliverable | Status | Location |
|---|---|---|
| Report | ✅ Content final (~4,560 words, 34 refs, est. ~27–28/30; audits 1–2) | `05_report/REPORT.md` |
| Presentation | ✅ Built + audit fixes (12:30 talk, 5 speakers, Q&A bank, drills) | `06_presentation/` (index.html, SCRIPT.md, REHEARSAL.md) |
| Technical summary | ✅ Current to D57 | `04_technical/TECHNICAL_SUMMARY.md` |
| Software | ✅ 35/35 tests; SW verification pass 3 clean | `03_software/` |
| Hardware | ✅ fw 0.2.6; HW verification pass 2 fixes landed (D-13…D-18 await retest after compile) | `02_hardware/` |
| Research | ✅ 119 sources | `01_research/` |

**Stakeholder to-dos (in order):**
1. **Report:** fill Appendix A contributions; add the cover page, TOC and declaration forms; export Figure 1 (Mermaid) as an image; format (TNR 12, 1.5 spacing, justified).
2. **Presentation:**
   - Open `06_presentation` via `python -m http.server 8080` and run the visual checklist in REHEARSAL.md §5.
   - Set `config.js` (DASHBOARD_URL, RESTART_CMD, CAMERA_CMD).
   - Prepare the FFB photo.
   - Fill the contribution lines; run the Q&A cross-training drill (§6).
3. **Software:**
   - Regenerate the Kaggle token, then follow `03_software/training/RUN_ON_KAGGLE.md`.
   - Run `gee/RUN_EARTH_ENGINE.md`.
   - Deploy with `deploy/DEPLOY_AZURE.md`, or use the laptop as primary (D39).
4. **Hardware:**
   - Buy the demo items.
   - First compile per `02_hardware/06_assembly_guide_beginner.md` §3.1.
   - Run bench tests B-01… (B-01 pH voltage first).
5. **Verification (after steps 3–4):** HW verification pass 3 (compile logs + bench results), SW verification pass 4 (Kaggle model, Azure URL, satellite.json). Relaunch from `00_lead/briefs/`.

**Relaunch:** subagents don't survive sessions; relaunch from `00_lead/briefs/` with the resume preamble.

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
