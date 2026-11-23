# 06 — Presentation Storyboard

> Owner: Presentation member (Outputs Team). Status: **v2: approved with changes (D48), built (Step 2).**

## Changelog
| Date | Version | Change | Trigger |
|---|---|---|---|
| 2026-11-24 | v2 | Talk cut to **12:30** (Q&A inside the 15 min). **Platform-comparison scene dropped**; Azure appears as the chosen platform with one line in the architecture scene. Its time is redistributed: [Member 4] also takes the extension scene, and [Member 3] narrates the harvest and cascade panels in the demo. **Palm-plantation theme** (estate greens, FFB orange/red, soil browns, frond motif), plus a daylight variant. Dashboard embedded with a one-key new-tab fallback. **No pre-recorded video and no V key**: fallbacks are F (laptop backend), O (new tab) and S (simulator). No Bahasa Malaysia line. No lime beat. **Harvester-allocation and screening-cascade panels added to the demo**, honestly labelled. Placeholders kept. Residency wording per D50. No ripeness-model accuracy figure anywhere (D51). Cascade animation moved out of the novelty scene because the demo now shows the real panel | D48, D50, D51 |
| 2026-11-23 | v1 | First storyboard (11 scenes, 14:30, platform matrix scene, video fallback) | Brief Step 1 |

## 0. Ground rules
- 15-minute slot, **talk 12:30, Q&A 2:30**, all 5 members speak (assignment p.2; D48).
- Story order follows the report: hook → case → problems (D19: P1 labour & harvest losses > P2 *Ganoderma* > P3 MSPO & fertiliser) → cognitive capability → SawitSense → architecture → integration, roadmap, risks → **live demo** → novelty → extension → close.
- **Azure-native framing (D20/D23):** Azure is presented as the chosen platform, with no comparison matrix and no justification on the slides (D48). Residency (D50): personal data stays in **Malaysia West** (Event Grid MQTT, Event Hubs, Storage, App Service). **Azure ML, IoT Hub/DPS, confidential ledger and Azure OpenAI run in Southeast Asia** and receive only non-personal or hashed data. We never claim IoT Hub or Azure ML run in Malaysia West.
- **Hardware appears only in the demo.** No Kaggle, student, credit or price talk.
- **No ripeness-model accuracy figure** in the slides, script or Q&A (D51). The demo shows the live grade, its confidence and the heat-map only. The only accuracy number shown is the *literature* range for early *Ganoderma* detection (64–84 %, Kwang et al., 2025), used to justify "screening, not diagnosis".
- Every number on screen carries a short Harvard citation (D11). RM2.2 bn is labelled "authors' calculation".

## 1. Run-of-show (12:30)

| # | Scene | Time | Dur. | Speaker | Steps |
|---|---|---|---|---|---|
| 1 | Hook | 0:00–0:35 | 0:35 | [Member 1] | 2 |
| 2 | The case | 0:35–1:35 | 1:00 | [Member 1] | 3 |
| 3 | Three problems, ranked | 1:35–3:10 | 1:35 | [Member 2] | 4 |
| 4 | Why cognitive | 3:10–4:05 | 0:55 | [Member 2] | 4 |
| 5 | Meet SawitSense | 4:05–4:45 | 0:40 | [Member 3] | 2 |
| 6 | Architecture (+ Azure line, residency) | 4:45–6:00 | 1:15 | [Member 3] | 8 |
| 7 | Integration, roadmap, risks | 6:00–7:30 | 1:30 | [Member 4] | 4 |
| 8 | **Live demo** | 7:30–10:15 | 2:45 | [Member 5]; [Member 3] operates and narrates 1:55–2:30 | 9 |
| 9 | Novelty: explain-to-audit (tamper moment) | 10:15–11:20 | 1:05 | [Member 5] | 3 |
| 10 | Extension | 11:20–12:05 | 0:45 | [Member 4] | 3 |
| 11 | Close + "Questions?" | 12:05–12:30 | 0:25 | [Member 1] | 2 |
| — | Q&A | 12:30–15:00 | 2:30 | all | — |

**Speaking time:** [Member 1] 2:00 · [Member 2] 2:30 · [Member 3] 2:30 (plus operating the laptop) · [Member 4] 2:15 · [Member 5] 3:15. Total 12:30.

**Recurring motif:** an 8-block demo estate drawn in SVG (block IDs from `03_software/src/static/precomputed/estate_blocks.json`). Scene 2 shows the manual practices on it. In scene 3, ripe bunches go over-ripe (P1) and an X-ray reveals the hidden *Ganoderma* infection (P2).

## 2. Scenes (as built)
1. **Hook.** Three counters run: 20.28 Mt record CPO, ~80 % foreign workforce, 30,000 short. Then the SawitSense title card with the placeholders `[GroupNo]` and `[Member 1]…[Member 5]`.
2. **Case.** FELDA, SD Guthrie and IOI cards. Then user and affected chips. Then the estate map with "manual" stickers (ripeness by eye, visual census, blanket fertiliser, paper MSPO records).
3. **Problems.** One step per problem:
   - P1: ripe bunches turn red on the map, with RM2.2 bn per 0.5-pt OER labelled as our calculation.
   - P2: soil X-ray showing root infection spreading in block B2; invisible until 60–70 %, −43 % in 6 months.
   - P3: a live EUDR countdown to 30 Dec 2026, fertiliser ≈30 % of cost, and MS 2530 clause stamps.
   - Then the Table 1 ranking overlay with the interaction line.
4. **Why cognitive.** Three cards flip from conventional to cognitive (P1, P2, P3). P3 shows the counterfactual "Lime now: pH 3.8 < 4.0; at pH ≥ 4.2, fertilise".
5. **SawitSense.** Name meaning, functions F1–F5 with their problem and outcome, then the user strip.
6. **Architecture.** Five layers build bottom-up, one per key press. Clicking a layer shows "why this technology". The cross-cutting band follows, with data particles flowing upward. The last step shows "Built on **Microsoft Azure**, our chosen platform" and two region pins with the D50 residency split.
7. **Integration, roadmap and risks.**
   - Integration hub: SAP ERP, mill grading, MSPO reporting, field data.
   - Short/medium/long timeline (Table 4).
   - 3×3 likelihood × impact risk grid (Table 5); clicking a chip shows its mitigation and owner.
   - Final step: "Top risks are data and people → a human approves every decision in the pilot."
8. **Live demo.** The dashboard is embedded beside a 9-beat rail. Each beat scrolls the dashboard to its panel, and a health light pings `GET /api/v1/health`. The choreography is in §3.
9. **Novelty.**
   - Five evidence records, chained with real SHA-256 hashes computed in the browser.
   - **Tamper** types pH 3.8 → 5.0 into record 3. Record 3 and every later record turn red and the verdict reads "TAMPERED at record 3". **Undo** (or R) restores "VERIFIED".
   - Then five novelty chips.
10. **Extension.** Co-operative app for FELDA settlers. EUDR's seven commodities with rubber highlighted. The three-step evolution arc.
11. **Close.** Each hook problem is paired with SawitSense's answer, then the closing line and "Questions?".

## 3. Demo choreography (2:45)
| t | Who | Table / laptop action | Dashboard panel |
|---|---|---|---|
| 0:00 | M5 | Point at the pot and node; probes in the REFERENCE cup | Live soil node |
| 0:15 | M5 | Pot is dry | Recommendation: red IRRIGATE, reason + counterfactual |
| 0:35 | M5 | Pour ~100 mL water, press the send button | Evidence log: new row, OK |
| 0:55 | M5 | Probes → PLAIN cup, press send | Recommendation: FERTILISE (SIMULATED agronomy badge) |
| 1:15 | M5 | Probes → NUTRIENT cup, press send | Recommendation: SKIP FERTILISER |
| 1:35 | M5 + M3 | FFB print under the ESP32-CAM; M3 clicks Capture | Camera: label + confidence + heat-map (**no accuracy figure**, D51) |
| 1:55 | M3 | Change crew 30 → 20 | Harvester allocation (**SIMULATED estate** badge) |
| 2:15 | M3 | — | Screening cascade: satellite stage flags B2 and C1 (**placeholder until the Earth Engine run**); drone stage "**not yet available**"; so the ground list is empty |
| 2:30 | M5 | M3 clicks Verify chain, then opens the MSPO audit pack | Evidence: VERIFIED + audit pack |

**Fallbacks (operator calls it, presenter keeps talking):**
- **F:** switch the frame to the laptop backend (`FALLBACK_URL`, D39); the devices fall back to LAN by themselves.
- **O:** open the current panel in a new tab.
- **S:** simulator mode. Shows the prepared `simulator.py` command and a "Simulated device feed" badge on the frame.
- **U:** reload the frame.
- No video fallback (D48).

## 4. Tech approach (as built)
- Plain HTML/CSS/JS, **no third-party libraries, no CDN, no web fonts**. Classic scripts, so it also opens from `file://`. 1920×1080 stage scaled to the window.
- Hand-written SVG and CSS animations. Own SHA-256 implementation (`js/sha256.js`), self-tested at load and cross-checked against `crypto.subtle` when that is available.
- Network: only the configured dashboard URL (iframe + `/api/v1/health`). The admin token is read from the git-ignored `config.local.js`.
- Presenter window (`P`): cues per step, talk clock vs plan, scene timer, time left in the slot. Synced by `postMessage` and `BroadcastChannel`.
- Files: `index.html`, `presenter.html`, `config.js`, `css/style.css`, `js/data.js` (timings, cues, report figures), `js/main.js`, `js/sha256.js`. The whole folder is well under 1 MB.
