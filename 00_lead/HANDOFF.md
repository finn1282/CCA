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

## 4. Current state
- Running: baseline Research wave 1 only (D12). Hardware/Software were briefly started then stopped (no output) so they begin from the baseline brief.
- After the baseline gate + stakeholder check-in: launch Hardware ∥ Software, then rolling verification. The full Hardware/Software briefs used are reproducible from PROJECT_PLAN.md + SPEC.md.
- Research requests from any team go in `01_research/REQUESTS.md`; Lead dispatches waves.
- Next: stakeholder check-in on datasets, training platform, extra parts → Software adopts them → rolling verification passes.

## 5. Phase log
| Date | Event |
|---|---|
| 2026-11-23 | Member briefs saved to `00_lead/briefs/` for cross-session relaunch |
| 2026-11-23 | Team PLAN.md + proposal/ruling process added (D13) |
| 2026-11-23 | Baseline research must finish before other teams start (D12) |
| 2026-11-23 | Switched to parallel pipeline + on-demand research + citations in every section (D10, D11) |
| 2026-11-23 | Brief saved, assignment read, stakeholder Q&A done (D1–D9), Phase 0 files pushed |
