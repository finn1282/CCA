# Member briefs (subagent prompts)

These are the exact instructions the Lead gives each team member (a Claude Code subagent).
They exist so a **new Claude session can relaunch any member with identical instructions**:
subagents belong to the session that started them and cannot be resumed from another session.

## How to relaunch a member from a new session
1. Check that member's folder `README.md` (Status) and `PLAN.md` to see how far it got.
2. Launch a subagent (Agent tool, `general-purpose`) with the brief file's contents as the prompt, adding at the top:
   *"You are resuming. Read your folder's README.md and PLAN.md first; continue from where it stopped and don't redo finished files."*
3. Members commit after every file, so at most one in-progress file is lost.

| Brief | Member | Launch when |
|---|---|---|
| `research.md` | Research (wave 1 baseline; later waves on demand from `01_research/REQUESTS.md`) | Now / on demand |
| `hardware.md` | Hardware | After baseline gate + stakeholder check-in |
| `software.md` | Software & Cloud AI | After baseline gate + stakeholder check-in |
| `verification_hardware.md` | HW Verification (rolling passes) | Each Hardware milestone |
| _software verification, compliance, report, presentation, technical summary_ | written by the Lead when those stages start | — |

Shared rules for every member live in `00_lead/PROJECT_PLAN.md` (working rules, citations, git, PLAN.md/proposals).
