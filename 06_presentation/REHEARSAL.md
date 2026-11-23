# 06 — Rehearsal: run-of-show, setup, fallback drill

> Links: `02_hardware/05_demo_plan.md` (§4 setup timeline, §6 pre-show checklist), `07_verification/software/TEST_PLAN.md` §H (R-01…R-14), `SCRIPT.md`.

## 1. Run-of-show (15:00 slot)
| Clock | Scene | Speaker | Operator ([Member 3]) |
|---|---|---|---|
| 0:00 | 1 Hook | [Member 1] | Presentation full screen (F11); presenter window on laptop screen |
| 0:35 | 2 Case | [Member 1] | — |
| 1:35 | 3 Problems | [Member 2] | — |
| 3:10 | 4 Why cognitive | [Member 2] | — |
| 4:05 | 5 SawitSense | [Member 3] | — |
| 4:45 | 6 Architecture | [Member 3] | — |
| 6:00 | 7 Integration, roadmap, risks | [Member 4] | Click risk chips if asked |
| 7:30 | 8 **Live demo** | [Member 5] + [Member 3] | Advance beats, Capture, crew 30→20, Verify chain, audit pack; call fallbacks |
| 10:15 | 9 Novelty (tamper) | [Member 5] | Click Tamper, then Undo |
| 11:20 | 10 Extension | [Member 4] | — |
| 12:05 | 11 Close | [Member 1] | — |
| 12:30 | Q&A | all | Leave "Questions?" on screen; B blacks out |
| 15:00 | End | | Stop servers (R-14) |
**Checkpoints:** start of demo ≤ 7:45, end of demo ≤ 10:30, "Questions?" ≤ 12:45. If you're late at the demo, use the skip rule in SCRIPT.md (scene 8).

## 2. One backend at a time (D39)
- At the rehearsal, **pick the primary**: the cloud if it is deployed and stable on the presentation hotspot, otherwise the laptop.
- Set `DASHBOARD_URL` in `config.js` to the primary. `FALLBACK_URL` = the laptop (`http://localhost:8000`). Both boards' `API_BASE` must point at the primary, and `API_BASE_LOCAL` at the laptop.
- Open the dashboard **only on the primary**; the laptop backend runs as a standby with the **same `SAWIT_DEVICE_KEYS`** (S-02).
- A cloud admin token goes in `06_presentation/config.local.js` (git-ignored): `window.SAWIT_LOCAL = { token: "…" };`. Never commit it.
- If the primary fails on stage, the devices switch to LAN by themselves. The operator presses **F**.

## 3. Setup checklist (presentation laptop)
| T− | Task | ✓ |
|---|---|---|
| Day before | Full rehearsal on the same hotspot, power and projector. Run TEST_PLAN §H R-01…R-13 and this file's §4 drill. Time the whole talk with the presenter window | ☐ |
| Day before | Chrome: zoom 100 %, notifications off, bookmarks bar hidden; laptop sleep/power saving off | ☐ |
| 30 min | Start the standby laptop backend: `cd 03_software/src && ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000` with the same `SAWIT_DEVICE_KEYS` as the cloud; check `GET /api/v1/health` on the primary | ☐ |
| 30 min | Fresh demo DB (R-13: new `SAWIT_RUNTIME_DIR`) so the evidence log starts clean; 3 warm-up readings | ☐ |
| 20 min | Start the presentation server: `cd 06_presentation && python -m http.server 8080`; open `http://localhost:8080/` in Chrome | ☐ |
| 15 min | Hardware table per demo plan §4 (cups, probes in REFERENCE, pot dry, FFB print, CAM framing) | ☐ |
| 10 min | Press `8` → demo scene: health light **green**, dashboard visible, beat 1 scrolls to the soil panel. Then `Home` to go back to scene 1 | ☐ |
| 10 min | Press `P` → presenter window opens; drag it to the laptop screen; Chrome full screen (F11) on the projector | ☐ |
| 5 min | Projector check: text readable from the back row. In a bright room press `T` for the daylight theme | ☐ |
| 2 min | Press `Z` (or "Restart clock") just before starting. The talk clock otherwise starts on the first Next | ☐ |

**Keys:** → / Space / PageDown next · ← / PageUp back · `1`–`9`, `0` (scene 10), `-` (scene 11) jump · `Home`/`End` · `P` presenter · `T` theme · `B` or `.` black screen · `Z` restart talk clock · demo only: `F` `O` `S` `Shift+S` `U` · novelty: `R` reset chain.
**Focus:** after clicking inside the dashboard (Capture, crew, Verify), keys go to the dashboard. An orange hint appears; click the beat rail on the left to give control back to the slides. The clicker also works from the presenter window.

## 4. Fallback drill (practise each one at least once)
| Failure | Signal | Operator action | Presenter keeps saying |
|---|---|---|---|
| Primary backend slow/down | Health light red; "Dashboard not reachable" card; OLED tag CLOUD → LAN | Press **F** (frame switches to the laptop backend, label shows FALLBACK). Press F again to go back | "The node has already failed over to the estate's local server, which is exactly what the edge layer is for." |
| Frame blank or refuses (token/TLS) | Health green but white or error frame | Press **U** (reload frame); if still blank, press **O** (new tab on the same panel), then use Alt+Tab to come back | Continue the beat |
| Devices fail, backend up | No new readings after pressing the button | Press **S**, copy the command, run it in a terminal at the repo root (cloud mode: add `--device` and `--key` from `SAWIT_DEVICE_KEYS`). The badge "Simulated device feed" shows on the frame. `Shift+S` clears it | "We'll drive the same block from a simulated node", then narrate the same beats as readings cycle |
| Camera Capture does nothing | No result after 5 s | Open `http://<cam-ip>/capture` (demo plan §5), else skip the beat | "At harvest time the same platform grades bunches…" |
| Sensor reads `--` | NO DATA (amber) | Reseat the wire | "Failed sensors are sent as null, never faked." |
| Running long | Presenter clock amber/red | At 9:40, jump to the Capture beat (click it in the rail) | — |
There is **no video fallback** (D48). If everything fails, finish the beats verbally on the OLED/LEDs (LOCAL mode) and move to scene 9 at 10:15.

## 5. Visual check by stakeholder (first time you open it)
Open `http://localhost:8080/` and step through with →. Check:
1. **Hook:** counters count up smoothly to 20.28 Mt / ~80 % / 30,000; on the second press the title card fades in with the placeholders. Nothing is cut off at the right edge.
2. **Case:** three organisation cards; user chips; the estate map with four brown "manual" stickers that don't hide the block labels.
3. **Problems:**
   - P1: orange bunches appear and some turn red, with two gold harvester figures.
   - P2: the map goes brown and red root circles spread in block B2.
   - P3: the EUDR countdown shows a sensible number of days.
   - Ranking: the table covers the map completely.
4. **Why cognitive:** each press flips one card from brown (today) to green (cognitive); the P3 counterfactual text is readable.
5. **SawitSense:** five coloured tiles in one row; the user chips on the second press.
6. **Architecture:** layers stack from the bottom (1 at the bottom, 5 on top); clicking a layer shows a "why" line; orange particles rise after the cross-cutting box appears; the final line says Azure with Malaysia West / Southeast Asia pins. Check that the wording matches D50.
7. **Roadmap:** hub diagram, then a three-phase timeline, then the risk grid. Risk 1 sits top-right (L3×I3), risk 2 in L3×I2, risk 3 in L2×I3, and risks 4–6 in L2×I2. Clicking a chip shows its mitigation.
8. **Demo:** with the backend running, the dashboard appears in the frame and each → scrolls it to the right panel; the health light is green. Stop the backend: within 5 s the "not reachable" card appears. Try F, O and S.
9. **Novelty:** five records with hashes; "Tamper" types 5.0, record 3 and later turn red and the verdict says "TAMPERED at record 3"; "Undo" returns to VERIFIED.
10. **Extension and close:** rubber highlighted in orange; the arc of three cards; "Questions?" in large orange type.
11. **Presenter window (`P`):** the current cue is highlighted, the clocks run, and its Next/Back buttons move the slides.
12. **Daylight theme (`T`):** everything is still readable on cream.
Tell [Member 3] or the Presentation member about anything that looks off (colours, sizes, wording).
