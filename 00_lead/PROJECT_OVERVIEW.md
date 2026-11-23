# Project Overview — Stakeholder Status Page

**Project:** Cognitive Smart Palm Oil Plantation Management (ITS69404 Group Assignment, Case #4)
**Deadline:** 15 Dec 2026 00:00 · **Last updated:** 2026-11-23 — ▶ resumed after pause

## Status at a glance
| Phase | Owner | Target | Status | Gate result |
|---|---|---|---|---|
| 0 Setup | Lead | 23 Nov | ✅ Done | Lead files pushed |
| 1 Baseline research wave (then on demand) | Research | 26 Nov | ✅ Wave 1 done 23 Nov | ✅ Passed (D14) — 4 proposals awaiting stakeholder |
| 2 Build (HW ∥ SW, parallel with on-demand research) | Hardware, Software | 3 Dec | 🟡 Building (plans ruled 23 Nov) | PLAN gate ✅ |
| 3 Verify (rolling passes per milestone) | HW/SW testers | 6 Dec | 🟡 HW pass 1 + SW pass 1 running (SW smoke test 17/17 ✅) | — |
| 4 Outputs (Tech summary, Report, Presentation) | Report, Presentation | 10 Dec | 🟡 Report Part 1 drafting | — |
| 5 Rubric audit & fixes | Compliance | 12 Dec | ⚪ Not started | — |

> Workflow is a parallel pipeline (D10) — see diagram in `PROJECT_PLAN.md`.

## Rubric coverage tracker
| Rubric item | Where it will be evidenced | Status |
|---|---|---|
| P1 Describe case (2) | Research → Report §1 | ⚪ |
| P1 ≥3 problems + evidence (4) | Research `01_…` → Report §1 | 🟡 evidence ready |
| P1 Cognitive capability per problem (4) | Research `02_…` v2 → Report §1 | 🟡 evidence ready |
| P2 App proposal (2) | Software → Report §2 — **SawitSense** | 🟡 |
| P2 Technologies justified (3) | Software/Hardware → Report §2 | ⚪ |
| P2 Compare ≥3 platforms + recommend (5) | Research `08_…` → Report §2 | 🟡 evidence ready |
| P2 Integration + phased plan (3) | Software → Report §2 | ⚪ |
| P2 Risks + mitigation (2) | Software/Verification → Report §2 | ⚪ |
| P3 Novelty (3) | All → Report §3 | ⚪ |
| P3 Future extension (2) | All → Report §3 | ⚪ |
| ≥10 Harvard sources | Research | ✅ 95 collected |
| Progress report (member contributions) | Report | ⚪ |
| 15-min presentation, 5 speakers, demo | Presentation + Hardware | ⚪ |

## Team proposals (D13)
| ID | Team | Proposal | Lead ruling |
|---|---|---|---|
| R-P1 | Research | Re-frame P2 as Ganoderma (primary) + ageing; rank P1 > P2 > P3 | ✅ D19 |
| R-P2 | Research | Train on Kaggle/Colab; deploy on Azure for Students; Earth Engine for satellite | ✅ D20 (report shows full Azure) |
| R-P3 | Research | Azure as enterprise recommendation | ✅ D15 |
| R-P4 | Research | Primary datasets D1+D2, D4, Sentinel-2, simulated fertiliser | ✅ D16 |
| R-P5 | Research | Shared demo thresholds | ✅ D17 |
| R-P6 | Research | Buy pH buffer sachets (~RM5–10) | ✅ D21 |
| R-P7 | Research | Ask lecturer about GCP edu credits / IBM SkillsBuild | ❌ D22 skipped |
| R-P8 | Research | "Explain-to-audit" MSPO evidence log as Part 3 anchor | ✅ D18 |
| HW-P1–P5, P7 / SW-P2–P3 | HW + SW | Interface changes, merged into INTERFACES v0.2 | ✅ D25 |
| HW-P6 | Hardware | Power: node on power bank, CAM on laptop USB | ✅ D26 |
| HW-P8 | Hardware | Demo purchases | ✅ D27 (stakeholder) |
| SW-P1 | Software | App name SawitSense | ✅ D24 |
| SW-P4/P5 | Software | Part 3 package; O4 scope; NLP layer | ✅ D28 |
| SW-P6/P7 | Software | Training scope; build platform | ✅ D29 |
| HW-P9 / SW-P8 | HW + SW | Research wave 2 requests | ✅ answered (D32) |

## Open decisions for stakeholder
Accounts for the build (Kaggle, Azure for Students, Earth Engine) — asked 23 Nov.

## Risks
| Risk | Impact | Mitigation |
|---|---|---|
| No free cloud credits usable from Malaysia | Can't train in cloud | Research verifies early; fallback local training + light cloud deploy (D4) |
| No public Ganoderma dataset | O2 model weak | Research finds proxy (UAV/hyperspectral, leaf disease) or documents simulated approach |
| Live demo fails on stage (WiFi) | Presentation marks | Offline/local fallback mode + recorded backup video (Verification to test) |
