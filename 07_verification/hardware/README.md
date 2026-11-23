# 07_verification/hardware: README

## Status
**Pass 1 complete (23 Nov 2026).** This pass was a static, contract and integration review. Compile is blocked until the ESP32 core is installed. All bench tests are waiting for the person holding the parts.

## Latest pass
`PASS_1_REPORT.md` covers:
- `02_hardware` at `4fc0758` (firmware at `de357ab`)
- the backend `03_software/src` at `305bb47`
- INTERFACES v0.2.1

## Open defects
**12 open: 2 major, 10 minor, 0 blockers.**

| ID | Sev | Owner | One line |
|---|---|---|---|
| D-01 | major | Hardware | Demo TDS beat: the baseline is set from the same PLAIN cup that is expected to show FERTILISE, so it will show OK |
| D-04 | major | Software (+HW) | Buffered replays posted after the fresh reading become the dashboard "latest" |
| D-02…D-03, D-05…D-11 | minor | Hardware / Lead | pH defaults, CA pin instruction, sticky local base and CLOUD tag, buffer head-of-line, moisture ADC range, null baseline, buffered timestamps, demo start state, guide text |
| D-12 | minor | Software | Default device keys stay active in cloud mode |

## Outputs
| File | Content |
|---|---|
| `TEST_PLAN.md` | All test cases (electrical, bench, contract, logic, compile, integration, demo) with status and evidence |
| `PASS_1_REPORT.md` | Pass 1 results, defects table, integration log, what Pass 2 needs |
| `README.md` | This file |

## Inputs used
SPEC, PROJECT_PLAN, DECISIONS (D17, D21, D25–D30), INTERFACES v0.2.1, `01_research/05_hardware_notes.md`, `00_baseline_brief.md` §Verification, `02_hardware/*`, `03_software/src`.

New sources cited, to be added to `01_research/sources.md`:
- [ESP32-DS]: Espressif *ESP32 Series Datasheet* v5.3, https://documentation.espressif.com/esp32_datasheet_en.pdf
- [AZ-CA]: Microsoft Learn *Azure Certificate Authority details*, https://learn.microsoft.com/en-us/azure/security/fundamentals/azure-ca-details

## Handoff notes
- **Integration harness:** a Python script replays the firmware's exact requests. It is kept outside the repo because writes here are limited to this folder's docs. To reproduce, start the backend on a free port with a throw-away `SAWIT_RUNTIME_DIR`, then run the INT-xx cases in `TEST_PLAN.md` §F. Default demo keys: `soilnode-01:demo-soil-key`, `cam-01:demo-cam-key`. Always stop the server afterwards.
- **Compile:** run it in Pass 2 with `--build-path` in a scratch dir and a `secrets.h` copied from the example. Do not run a second `core install` into the shared `~/.arduino15` while Hardware's install is running.
- **Bench tests:** B-01 (pH PO max with PO disconnected) must happen **before** PO is wired to GPIO35.
- **Next pass trigger:** Hardware compile result or fixes for D-01/D-02/D-03, the Software D-04 fix, a trained M1 model, or an Azure URL.

## Open issues for Lead
1. D-09: the contract has no way to timestamp offline readings without NTP. Consider an optional `age_s`, or a backend "time approximate" flag.
2. D-05: decide whether a laptop-served result should be tagged CLOUD and whether the local base may stay sticky. FR7 currently says cloud first.
