# 03_software — README

## Status
**Step 1 done (23 Nov 2026):** `PLAN.md` written; waiting for Lead rulings on SW-P1…SW-P8. No build work started yet.

## Inputs used
`00_lead/SPEC.md`, `PROJECT_PLAN.md`, `DECISIONS.md` (D1–D23), `INTERFACES.md` v0.1, `CCA Group Assignment.pdf` pp.5–8, `01_research/00_baseline_brief.md`, `01`–`05`, `sources.md`.

## Outputs
| File | Content |
|---|---|
| `PLAN.md` | Approach, models M1–M7, task breakdown + dependencies, Part 3 ideas, conflicts, proposals SW-P1…P8 |
| `README.md` | This file |

Planned (Step 2): `01_solution_overview.md`, `02_architecture.md`, `03_ai_models.md`, `04_cloud_design.md`, `05_api_spec.md`, `06_implementation_guide_beginner.md`, `07_actual_build_vs_target.md` (internal), `src/`, `training/`.

## Interface changes requested
- SW-P2: recommendation response v0.2 (`actions[]`, wider action enum, `counterfactual`, `simulated`, `evidence_id`, `oled`, `led`).
- SW-P3: transport/payload v0.2 (HTTPS POST returns recommendation, `X-Device-Key`, `ec_us_cm`/`ts` optional, `seq`, `rssi_dbm`, backend-held TDS calibration, ESP32-CAM endpoint + optional command poll).

## Assumptions
- Training runs on Kaggle (stakeholder account) or, failing that, on the CPU-only path on a laptop (no GPU on the build machine).
- Azure for Students subscription and an Earth Engine noncommercial project will be created by the stakeholder.

## Open issues for Lead
1. Rule on SW-P1…SW-P8 (`PLAN.md` §5).
2. Accounts needed (stakeholder action): Kaggle (phone-verified, for GPU notebook), Azure for Students (for deployment; need `az login` or publish profile), Google Earth Engine noncommercial project (for NDVI pre-compute). Without them: CPU training, local-laptop deployment, Copernicus Browser export.
3. App-name collision check for SW-P1.

## Research requests
- R1 (appended to `01_research/REQUESTS.md`): Azure service docs for the target design, MS 2530:2022 criterion numbers, PDPA 2010 cross-border section, Ganoderma neighbour-spread evidence, harvesting round interval / harvester productivity.

## New sources used
None yet.
