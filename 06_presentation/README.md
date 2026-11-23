# 06_presentation — README

## Status (23 Nov 2026)
| Step | State |
|---|---|
| Step 1 — Storyboard (`STORYBOARD.md`) | **Done, awaiting stakeholder approval (D36).** |
| Step 2 — Build (`index.html` + assets, `SCRIPT.md`, `REHEARSAL.md`) | Not started — begins only after approval |

## What this is
The 15-minute group presentation for SawitSense (Case #4), built as an **interactive, animated web story** that runs **offline** in the presenter's laptop browser. It has a live-demo scene that embeds the SawitSense dashboard, with fallbacks (laptop backend, simulator, pre-recorded video). All 5 members speak; the script includes a Q&A bank so every member can answer on any part.

## Inputs used
`CCA Group Assignment.pdf` p.2 · `00_lead/SPEC.md` · `00_lead/DECISIONS.md` (D19, D20, D23, D24, D28, D32, D36, D39, D40, D43) · `05_report/REPORT.md` (content source of truth) · `01_research/00_baseline_brief.md` (Presentation section) · `01_research/08_platform_comparison_capability.md` (sensitivity weights) · `02_hardware/05_demo_plan.md` · `03_software/README.md` + `src/static/` · `07_verification/software/TEST_PLAN.md` §H.

## Outputs
| Path | Content | State |
|---|---|---|
| `STORYBOARD.md` | 11 scenes with timing, speaker, on-screen content + animation/interaction, key lines, demo choreography, fallback ladder, tech approach, questions | Draft v1 |
| `index.html`, `css/`, `js/`, `data/`, `config.js`, `presenter.html` | The presentation | Step 2 |
| `SCRIPT.md` | 5-speaker script + Q&A bank | Step 2 |
| `REHEARSAL.md` | Run-of-show, setup checklist, fallback drill | Step 2 |

## How to run (after Step 2)
```bash
cd 06_presentation && python -m http.server 8080   # open http://localhost:8080 (file:// also works)
```
Set the demo backend in `config.js` (`DASHBOARD_URL` = primary chosen at rehearsal, D39). A cloud admin token goes only in the git-ignored `config.local.js`.

## Rules followed
- Offline: no CDN, no web fonts; any library vendored locally with a pinned version (none planned). Only network call = configured dashboard URL.
- Azure-native framing; no Kaggle/student/price talk (D20, D23); D32 platform scores; hardware only in the demo scene.
- Small assets, no large downloads (D43); demo video kept out of git.

## Open issues for Lead
- Stakeholder questions listed in `STORYBOARD.md` §5 (speaker split, Q&A inside/outside 15 min, iframe vs tab, theme/projector, BM wording, demo extras, video owner, title placeholders).
