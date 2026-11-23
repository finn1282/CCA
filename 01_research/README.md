# 01_research — README

## Status
**Research wave 1 complete (23 Nov 2026).** All files committed. Further research on demand via `REQUESTS.md`.

## Inputs used
`00_lead/SPEC.md`, `PROJECT_PLAN.md`, `DECISIONS.md`, `INTERFACES.md`, `components.md`, `CCA Group Assignment.pdf` (rubric p.9); web research (official/vendor pages, journals, MPOB/MSPO documents, dataset repository APIs) — all opened 23 Nov 2026.

## Outputs
| File | Content |
|---|---|
| `00_baseline_brief.md` | Evidence-based direction per team (Hardware, Software, Report, Presentation, Verification) |
| `01_problem_evidence.md` | Malaysian palm oil context, stakeholders, validated & prioritised problems, why cognitive > conventional, mapping to O1–O4 and inputs |
| `02_cognitive_capabilities.md` | Short v1: state of the art + reported accuracies per outcome |
| `03_datasets.md` | Verified datasets (URL, licence, size, classes) ranked per model; gaps and simulated proxies |
| `04_cloud_platforms.md` | (a) student credits available in Malaysia 2026; (b) 4-platform enterprise comparison with weighted matrix + recommendations |
| `05_hardware_notes.md` | ESP32/sensor facts, oil-palm soil thresholds, optional parts (MYR) |
| `sources.md` | 64 Harvard entries with stable keys, grouped by type |
| `REQUESTS.md` | Request log for on-demand research waves |
| `PLAN.md` | Approach, ideas, conflicts, proposals (R-P1…R-P8) for Lead ruling |

## Key findings (must-know)
1. Problem priority by evidence: **P1 labour-constrained harvesting** > **P2 Ganoderma (+ageing)** > **P3 MSPO/EUDR & fertiliser**.
2. Labour: ~80 % foreign workforce; 30,000 short (Oct 2026); harvesting not mechanisable; shortage pushes under-ripe harvesting → OER loss (0.5 pt ≈ RM2.2 bn, our calc.).
3. Ganoderma: 9.2 % of surveyed smallholdings, >20 % in some plantings; asymptomatic until 60–70 % infected → screening/prioritisation is the realistic AI role (published early-detection accuracy only ~64–84 %).
4. MSPO 2022 (mandatory) requires fertilising/soil SOPs + records, traceability and a GHG criterion (N₂O from fertiliser); EUDR applies 30 Dec 2026.
5. Ripeness data: **D1 (4,728 imgs, CC BY)** for training + **D2 (Malaysian, 466 imgs, CC BY)** for testing.
6. Ganoderma data: **D4 UAV RGB, 9,400 crowns, field-confirmed labels, CC BY**; no public multispectral/hyperspectral BSR data.
7. No public oil-palm soil-sensor or harvest-timing data → SIMULATED, labelled.
8. No student cloud credit gives usable GPUs (Azure quota blocked; GCP trial needs card and excludes Vertex since 16 Nov 2026; Studio Lab closed) → **train on Kaggle/Colab, deploy on Azure for Students, satellite in Earth Engine**.
9. Enterprise recommendation: **Azure 83** > AWS 78 > Google 68 > IBM 49 (Malaysian region + live IoT Hub; Google IoT Core and IBM Watson IoT both retired in 2023).
10. ESP32: analog sensors on ADC1 only; pH board needs a divider; probes measure soil slurry; pH OK band 4.2–5.5.

## Assumptions
- Taylor's University email qualifies for Azure for Students (unverified until someone signs up).
- Kaggle GPU quota (~30 h/week) taken from common reports — Kaggle docs not machine-readable.
- Component prices in `05_hardware_notes.md` are approximate/unverified except the Digi-Key figure.
- FGV ownership statement and some vendor features marked "unverified" where pages were not opened.

## Open issues for Lead
1. **R-P1** — re-frame P2 to elevate Ganoderma (contradicts SPEC §3 wording).
2. **R-P2/R-P3** — confirm training (Kaggle) vs deployment (Azure) vs enterprise (Azure) split; update DECISIONS D4.
3. Stakeholder decisions: buy pH buffers (essential) and any optional parts; ask lecturer about Google Cloud education credits / IBM SkillsBuild.
4. Add the demo thresholds (R-P5) to `INTERFACES.md` so Hardware and Software share them.
5. EUDR: EU = 6.8 % of exports — Report should lead P3 with MSPO, EUDR as accelerator.
