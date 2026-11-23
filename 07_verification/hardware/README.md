# 07_verification/hardware: README

## Status
**Pass 2 complete (23 Nov 2026).** This pass re-ran the static review and the backend integration checks against INTERFACES **v0.2.4**.

Not done here:
- **Compiling** is a **stakeholder build step** (D43/D44: no ESP32 core is installed on this machine).
- **Bench tests** wait for the person holding the parts.

## Latest pass
`PASS_2_REPORT.md` covers:
- `02_hardware` at `873a615` (soil_node 0.2.3, cam_node 0.2.2)
- backend `03_software/src` at `47b18ff`

Results:
- 11 of 12 Pass 1 defects closed; D-07 accepted.
- Integration: 30/32 (1 fail → D-16, 1 n/a).
- 3-cup TDS demo logic matches the backend rules.

## Open defects
**6 open: 1 major, 5 minor, 0 blockers.**

| ID | Sev | Owner | One line |
|---|---|---|---|
| D-17 | major | Hardware | Beginner guide can't yet carry a first-time compile: no Verify step, no success line, no compile-error table, incomplete CLI |
| D-13 | minor | Hardware | Any 4xx outranks a transport error, so readings are dropped (for example a stopped Azure app returns 403) |
| D-14 | minor | Hardware | If the laptop is the primary in `API_BASE`, laptop results are tagged CLOUD |
| D-15 | minor | Hardware | 3-cup demo: the REFERENCE pH must be 4.2–6.5 (tap water → WATCH); PLAIN pH drift < 4 → LIME |
| D-16 | minor | Software | `/latest` picks by highest seq, so it freezes after a seq restart (NVS erase) |
| D-18 | minor | Hardware | Header comments say fw 0.2.0 |

Closed in Pass 2: D-01…D-06 and D-08…D-12. Accepted: D-07.

## Outputs
| File | Content |
|---|---|
| `TEST_PLAN.md` | All test cases with current status, including the stakeholder compile commands (§E) and bench tests B-01…B-18 |
| `PASS_1_REPORT.md` | Pass 1 (v0.2.1) results and defects D-01…D-12 |
| `PASS_2_REPORT.md` | Pass 2 (v0.2.4) re-check, new defects D-13…D-18, integration log |
| `README.md` | This file |

## Inputs used
- SPEC, PROJECT_PLAN, DECISIONS (D17, D21, D25–D44), INTERFACES v0.2.4
- `01_research/05_hardware_notes.md`
- `02_hardware/*`, `03_software/src`

New source keys, still to be added to `01_research/sources.md`:
- [ESP32-DS]: Espressif *ESP32 Series Datasheet* v5.3, https://documentation.espressif.com/esp32_datasheet_en.pdf
- [AZ-CA]: Microsoft Learn *Azure Certificate Authority details*, https://learn.microsoft.com/en-us/azure/security/fundamentals/azure-ca-details

## Handoff notes
- **Integration harness.** It is a Python script kept outside the repo; it replays the firmware's exact requests. To reproduce:
  1. Run `SAWIT_RUNTIME_DIR=<tmp> ../.venv/bin/uvicorn app.main:app --port 8899` from `03_software/src`.
  2. Run the INT cases in TEST_PLAN §F. Demo keys: `soilnode-01:demo-soil-key`, `cam-01:demo-cam-key`.
  3. Always stop the server afterwards.
- **TLS check (host side).** Extract the PEM blocks from `secrets.h.example`, then run `openssl s_client -connect example.azurewebsites.net:443 -CAfile <pem>`. It should report `Verify return code: 0`.
- **Compile.** Do not install the ESP32 core here (D43). The stakeholder runs TEST_PLAN §E and sends back the logs plus `core list`/`lib list`.
- **Bench order.** B-01 (pH PO max, with PO disconnected) must come **before** PO is wired to GPIO35.
- **Next pass trigger.** Any of: the D-17/D-13/D-14/D-15 fixes, the Software D-16 fix, the stakeholder's compile logs, the Azure URL, or bench results.

## Open issues for Lead
1. D-17 is rated major because, under D43, the stakeholder's compile is the firmware's first ever. The guide is the only safety net.
2. INTERFACES says `age_s` is "0 for fresh readings", but the firmware sends the true time since capture (≈2 s or more). This is harmless; consider rewording it to "seconds since capture".
