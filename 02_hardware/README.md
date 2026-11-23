# 02_hardware — README

## Status
**Step 1 complete (23 Nov 2026): `PLAN.md` written; awaiting Lead rulings on HW-P1…HW-P9.** Step 2 deliverables not started.
Audience (D23): demo, Verification and presentation — hardware detail does not go into the report.

## Inputs used
`00_lead/SPEC.md`, `PROJECT_PLAN.md`, `DECISIONS.md` (D17, D20, D21, D23), `INTERFACES.md` v0.1, `components.md`,
`01_research/00_baseline_brief.md`, `05_hardware_notes.md`, `sources.md`.

## Outputs
| File | Status |
|---|---|
| `PLAN.md` | Done — approach, draft pin map, tasks, ideas, conflicts, proposals, purchases |
| `01_requirements_and_specs.md` | Planned (Step 2) |
| `02_system_design.md` | Planned |
| `03_bom.md` | Planned |
| `firmware/soil_node/soil_node.ino`, `firmware/cam_node/cam_node.ino`, `config.h.example` | Planned |
| `04_calibration.md` | Planned |
| `05_demo_plan.md` | Planned |
| `06_assembly_guide_beginner.md` | Planned |

## Interface assumptions (pending HW-P1…P5, P7)
- HTTPS POST JSON per INTERFACES v0.1, 10 s demo interval, recommendation returned in POST response (HW-P1).
- CAM posts raw `image/jpeg`; local HTTP trigger (HW-P4).
- Thresholds exactly D17.

## Assumptions
- Pin map in `PLAN.md` §1.4 is a draft until bench-tested.
- Component prices are approximate marketplace ranges, unverified.
- `arduino-cli` not installed here; compile check attempted in Step 2 or handed to Verification.

## Open issues for Lead
1. Rule on HW-P1…HW-P9 (`PLAN.md` §4); HW-P8 (purchases) needs stakeholder.
2. Software endpoint URLs + response formats needed for INTERFACES v0.2.

## Research requests
- R-HW1 (LoRaWAN/cellular field soil-node sources) — appended to `01_research/REQUESTS.md`.

## New sources used
None yet (only keys from `01_research/sources.md`).
