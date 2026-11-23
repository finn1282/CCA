# 06 — Presentation Storyboard (Step 1, for stakeholder approval)

> Owner: Presentation member (Outputs Team). Status: **DRAFT v1 — awaiting stakeholder approval (D36). Nothing is built yet.**
> Sources: `05_report/REPORT.md` (content source of truth), `00_lead/DECISIONS.md` (D19, D20, D23, D24, D28, D32, D39, D40, D43),
> `01_research/00_baseline_brief.md` (Presentation hook), `02_hardware/05_demo_plan.md` (demo), `03_software/src/static` (dashboard),
> `07_verification/software/TEST_PLAN.md` §H (rehearsal).

## 0. Ground rules this storyboard follows
- **15 minutes, all 5 members speak, Q&A on any part** (assignment p.2). Planned talk = **14:30**, leaving **0:30 buffer**.
- **Story order follows the report:** hook → case → problems in D19 order (P1 labour & harvest losses > P2 *Ganoderma* > P3 MSPO & fertiliser) → cognitive capability per problem → SawitSense → architecture → platform evaluation → integration, roadmap, risks → **live demo** → novelty (explain-to-audit) → extension → close.
- **Azure-native framing (D20/D23/D32):** the talk describes the professional Azure deployment (Azure ML, IoT Hub + IoT Operations edge, Event Hubs, Data Lake, Logic Apps SAP connector, Azure OpenAI for multilingual explanations, Azure confidential ledger). No Kaggle, student plan, credits or price as a reason for any choice. Cost appears only as a *risk* (scene 8). Platform scores are the capability-only D32 values **Azure 88 / AWS 79 / Google 67 / IBM 49**; Google is named "Gemini platform (formerly Vertex AI)".
- **Hardware appears only in the demo scene** (scene 9), as "the IoT soil-sensing layer". No hardware in any other scene.
- **No prototype accuracy claims (D40, D42):** the demo shows a live grade + confidence + heat-map, never a test-accuracy figure. *Ganoderma* is "screening/prioritisation, not diagnosis" (D32e).
- Every number on screen carries a short Harvard in-text citation (D11), the same ones the report uses. Calculated figures are labelled "authors' calculation".

## 1. Run-of-show at a glance

| # | Scene | Time (start–end) | Dur. | Speaker | Report section |
|---|---|---|---|---|---|
| 1 | Hook: "Record harvest, missing harvesters" | 0:00–0:40 | 0:40 | [Member 1] | Exec summary, Intro |
| 2 | The case: FELDA, SD Guthrie, IOI | 0:40–1:50 | 1:10 | [Member 1] | 1.1 |
| 3 | Three problems, ranked | 1:50–3:35 | 1:45 | [Member 2] | 1.2 |
| 4 | Why cognitive, not conventional | 3:35–4:35 | 1:00 | [Member 2] | 1.3 |
| 5 | Meet SawitSense (F1–F5, users) | 4:35–5:15 | 0:40 | [Member 3] | 2.1 |
| 6 | Architecture build-up | 5:15–6:30 | 1:15 | [Member 3] | 2.2 |
| 7 | Platform matrix (interactive weights) | 6:30–8:00 | 1:30 | [Member 4] | 2.3 |
| 8 | Integration, roadmap & risks | 8:00–9:20 | 1:20 | [Member 4] | 2.4, 2.5 |
| 9 | **Live demo** | 9:20–11:50 | 2:30 | [Member 5] presents · [Member 3] operates laptop | (demo) |
| 10 | Novelty: explain-to-audit (tamper moment) | 11:50–13:20 | 1:30 | [Member 5] | 3.1 |
| 11 | Extension & close | 13:20–14:30 | 1:10 | [Member 1] | 3.2, Conclusion |
| — | Buffer | 14:30–15:00 | 0:30 | — | — |

**Speaker split:** [Member 1] 3:00 (opens and closes, as leader) · [Member 2] 2:45 (Part 1 problems) · [Member 3] 1:55 + demo operator (solution & architecture) · [Member 4] 2:50 (platform, plan, risks) · [Member 5] 4:00 (demo + novelty — one continuous story: the demo's evidence log flows straight into the tamper moment).
Each member owns one coherent part of the report and is the **primary Q&A answerer** for it; `SCRIPT.md` (Step 2) gives every member crisp answers for all parts.

**Recurring visual motif:** one stylised **SawitSense demo estate** — an 8-block plantation map drawn in SVG (block IDs match `03_software/src/static/precomputed/estate_blocks.json`). The same map shows the harvest problem (scene 3), the screening cascade (scenes 4, 10), the data flowing into the architecture (scene 6) and the audit trail per block (scene 10). The audience learns the map once and then reads every scene on it.

## 2. Scenes

### Scene 1 — Hook (0:00–0:40) · [Member 1]
- **On screen:** black screen → palm-frond silhouette sweeps in; three counters tick up one after another: **20.28 Mt** CPO (record 2025), **~80 %** foreign plantation workforce, **30,000** workers short (Oct 2026). Title card fades in: **SawitSense — explained, auditable decisions for Malaysian oil palm**, group `[GroupNo]`, names `[Member 1]…[Member 5]`.
- **Animation:** counters (ease-out), title cross-fade. Sources line: (MPOB, 2026; Ramendran, 2026; The Edge Malaysia, 2026).
- **Key line:** "Malaysia produced a record 20.3 million tonnes of palm oil last year — yet about 80 % of the people who harvest it are foreign workers, and the industry is 30,000 short again."

### Scene 2 — The case (0:40–1:50) · [Member 1]
- **On screen:** three organisation cards slide in — **FELDA** (≈870,000 ha; 112,635 settler families), **SD Guthrie** (13–13.5 ha/worker → 15 ha target; "harvesting has no mechanised solution"), **IOI** (100+ 4G/LTE sites across 100+ estates). Below: stakeholder chips (estate manager, *mandore*, agronomist, plant-health officer, MSPO officer, mill grader; affected: settlers, MPOB, MSPO, EU buyers).
- **Animation:** the estate map draws itself block by block; three "manual" stickers drop onto it: *ripeness by eye*, *Ganoderma by visual census*, *blanket fertiliser*, plus a paper stack "MSPO records".
- **Key line:** "Three operating models — a settler scheme, a multinational and a digitising group — but the same weak point: field decisions depend on scarce human judgement and aren't recorded where they're made."

### Scene 3 — Three problems, ranked (1:50–3:35) · [Member 2]
Three beats on the estate map, then the ranking table.
- **P1 Labour & harvest losses (≈40 s):** ripe bunches on the map turn orange → red (over-ripe) while a small harvester icon can't reach them; counter: **RM2.2 bn per 0.5-pt OER** *(authors' calculation from MPOB, 2026)*; "RM7.5–20 bn/yr — employer estimate" (Ramendran, 2026).
- **P2 *Ganoderma* BSR (≈35 s):** palms look green on the surface; press a key → **"X-ray" reveal** shows infection spreading through roots below ground across 4 rows; caption **"invisible until 60–70 % infected · −43 % in 6 months"** (Khoo and Chong, 2023). Ageing noted in one line (constraint = replanting capital, so not the cognitive target).
- **P3 MSPO & fertiliser (≈20 s):** a countdown clock to **EUDR 30 Dec 2026** (European Commission, 2026); fertiliser ≈30 % of cost (Chong, 2026); MS 2530:2022 clauses 4.1.3 / 4.2.2 / 4.5.4 appear as stamps (MPOCC, 2023).
- **Ranking (≈10 s):** Table 1 builds criterion by criterion (scale, urgency, labour dependence, cognitive addressability) → ranks **1-2-3**; one line on interaction: all three draw on the same scarce field labour, so P1 is the root and one integrated system beats three tools.
- **Key line:** "These aren't three separate problems. Census and compliance paperwork eat the same scarce labour as harvesting."

### Scene 4 — Why cognitive, not conventional (3:35–4:35) · [Member 2]
- **On screen:** three split cards, **Conventional | Cognitive**, one per problem (Table 2): P1 visual grading on fixed rounds → computer vision + harvest window + crew optimisation; P2 visual census → multisource anomaly detection + spatial reasoning (satellite → drone → ground); P3 blanket schedules + paper → knowledge-based reasoning + explainable ML + NLP.
- **Interaction:** a toggle flips each card from "conventional" to "cognitive" (flip animation). P3 card shows the punchline example: a dashboard "pH 3.8" vs SawitSense "**Lime now — pH 3.8 < 4.0. At pH ≥ 4.2 the advice would be to fertilise.**"
- **Honesty note on screen:** early-BSR detection accuracy in research is only 64–84 % (Kwang et al., 2025) → SawitSense *ranks palms for lab confirmation*.
- **Key line:** "Conventional systems store this data. Cognitive systems perceive it, reason over it and explain their conclusion."

### Scene 5 — Meet SawitSense (4:35–5:15) · [Member 3]
- **On screen:** logo animation (*sawit* = oil palm + *sense* = sensing & sense-making). Five function tiles orbit in, each tagged with its problem/outcome: **F1** ripeness & harvest window (P1/O1) · **F2** harvester allocation (P1/O4) · **F3** *Ganoderma* screening cascade (P2/O2) · **F4** explained fertiliser/lime/irrigation advice (P3/O3) · **F5** explain-to-audit evidence log (P3/O4). User strip: manager dashboard, *mandore* mobile app (multilingual), agronomist review queue, plant-health check-list, MSPO audit pack, IT model registry/ERP.
- **Key line:** "Five functions, one per decision that today depends on a scarce person."

### Scene 6 — Architecture build-up (5:15–6:30) · [Member 3]
- **On screen:** Figure 1 adapted from the assignment's Figure 4, built **one layer per key press** from the bottom up: (1) Data sources — Sentinel-2, drone RGB/multispectral, IoT soil sensors (LoRaWAN), bunch photos, SAP ERP, MSPO standards → (2) Ingestion & big data — IoT Hub + DPS, Event Hubs, Data Lake Gen2, Planetary Computer (STAC) → (3) Cognitive services — vision models, NDVI anomaly detection, fertiliser recommender, MSPO knowledge base, NLP (Azure OpenAI) → (4) Cloud & deployment — Azure ML training/registry/endpoints/monitoring, IoT Operations at the estate edge → (5) Application — dashboard, *mandore* app, review queue, audit pack, ERP work orders. Then the **cross-cutting** band slides across: PDPA residency split, Entra ID & Key Vault, Grad-CAM + Responsible AI, confidential-ledger evidence log, human review.
- **Animation:** after the build, data particles flow from the estate map up through the layers into a decision card. Clicking a layer shows a one-line "why this technology" (from report 2.2).
- **Residency mini-map:** two region pins — **Malaysia West** (personal/identifiable data) and **Southeast Asia** (Azure OpenAI, confidential ledger — non-personal/hashed data only, PDPA s129 safeguards) (Microsoft, 2026a; 2026b; Mayer Brown, 2025).
- **Key line:** "Each layer is there because a problem needs it — and personal data never leaves Malaysia."

### Scene 7 — Platform matrix, interactive (6:30–8:00) · [Member 4]
- **On screen:** Table 3 as a live chart: four horizontal bars (Azure, AWS, Gemini platform (formerly Vertex AI), IBM watsonx) and seven **weight sliders** C1–C7 (IoT, in-country region, vision, geospatial, edge/offline, MLOps & explainability, estate-IT integration). Scores 1–5 are fixed from the report; totals = Σ score × weight ÷ (Σ weights) × 20, so the report weights reproduce **88 / 79 / 67 / 49** exactly.
- **Interaction (live, ~30 s):** presenter clicks presets **Report weights → Equal → Geospatial-heavy** (89/80/66/49 and 82/76/75/50) and then drags the geospatial slider up live — the bars re-sort, **Azure stays first**. Hover a cell → evidence one-liner (e.g. "Google Cloud IoT Core retired Aug 2023", "Azure Malaysia West, 3 AZs", "Logic Apps SAP connector: IDoc/BAPI/RFC").
- **Honest framing on screen:** "AWS is a credible runner-up (−9). Azure = best fit for estates already on SAP + Microsoft." Price explicitly excluded: "cost is managed as a risk, not used to choose."
- **Key line:** "Change the weights however you like — Azure stays on top because it's the only one with an in-country region, first-party IoT with an offline edge, and native SAP integration."

### Scene 8 — Integration, roadmap & risks (8:00–9:20) · [Member 4]
- **On screen (part a, 30 s):** integration hub diagram — SAP ERP ↔ (Logic Apps) ↔ SawitSense ↔ mill grading, MSPO reporting; field data via LoRaWAN → IoT Hub; edge cluster for offline blocks.
- **Part b (25 s): roadmap timeline** — a horizontal timeline animates through **Short (0–6 m) pilot** → **Medium (6–18 m) scale & integrate** → **Long (18–36 m) optimise & extend**; each phase expands to scope / functions / integration / success measure (Table 4). "Measure the baseline first" marker at the start of each phase.
- **Part c (25 s): risk heat-map** — 3×3 likelihood × impact grid; the six risks (Table 5) drop into their cells in priority order with category colour (Technical / Operational / Vendor & cost); click a risk → mitigation + owner. Highlight: **top two risks are data (cold start) and people (trust)** → human in every decision during the pilot.
- **Key line:** "The two biggest risks are data and people, not technology — so the pilot keeps a human in every decision." Hand-off: "Let's show you what one of those decisions looks like." → scene 9.

### Scene 9 — Live demo (9:20–11:50) · [Member 5] presents, [Member 3] operates
- **On screen:** the scene embeds the **SawitSense dashboard** in a full-width frame (URL from `config.js`, D39 primary backend; token appended from a git-ignored `config.local.js` when the primary is the cloud). A slim **beat rail** on the left shows the six beats; the operator advances it with a key and the current beat's "say" line is visible only in presenter view. A small status light shows the result of `GET /api/v1/health` on the configured URL (the only network call the presentation makes).
- **Choreography** (from `02_hardware/05_demo_plan.md` §2, timed to 2:30):

| t | Table action ([Member 5]) | Operator ([Member 3]) | Audience sees | Say |
|---|---|---|---|---|
| 0:00 | Point at pot + node; probes in REFERENCE cup | Dashboard on live soil panel | Tiles + chart; OLED "SawitSense" | "This pot stands in for one management block. The node sends moisture, pH, nutrients and temperature every ten seconds." |
| 0:15 | Pot is dry | Scroll to Recommendation card | Red **IRRIGATE**, reason "moisture 24 % < 30 %", counterfactual | "Not just a number — an action, the reason, and what would change it." |
| 0:35 | Pour ~100 mL water, press send button | Evidence table in view | Moisture rises → green **OK**; new evidence row | "Every decision is logged with its reading and calibration — the audit trail MSPO needs." |
| 1:00 | Probes → PLAIN cup, press button | Recommendation card | Amber **FERTILISE** | "A nutrient-depleted block: fertilise." |
| 1:25 | Probes → NUTRIENT cup, press button | Recommendation card | **SKIP FERTILISER** | "After fertiliser, skip the next round — saving cost and runoff." |
| 1:50 | Hold A5 FFB print under ESP32-CAM | Click **Capture** | Ripeness label + confidence + heat-map | "At harvest time, the same platform grades bunches — and the heat-map shows what the model looked at." |
| 2:15 | — | Click **Verify chain** → open MSPO audit pack | "VERIFIED", audit pack with head hash + clauses | "And all of it becomes audit evidence — which is our big idea." → scene 10 |
Optional if ahead of time: ACIDIC cup → red **LIME** "pH 3.8 < 4.0".
- **Panels deliberately not shown in the demo:** satellite/drone cascade and harvester allocation (they are covered by scene 10's animation; the drone stage is not built and the satellite panel is a placeholder until the Earth Engine run).
- **Fallbacks** — operator calls it, presenter keeps talking (ladder, fastest first):
  1. **Primary backend slow/down** → key `F` switches the frame to the fallback URL (laptop `http://localhost:8000`); nodes fall back to LAN by themselves (D39). ~10 s.
  2. **Frame refuses to load** (token/TLS) → key `O` opens the dashboard in a new tab; presenter continues. ~5 s.
  3. **Devices fail but backend is up** → **simulator mode**: operator runs the prepared command `python simulator.py --scenario cycle --interval 2 --base <primary>` (soil readings appear on the same dashboard); the presenter narrates the same beats. Shown on screen as a "Simulated device" badge — no pretending.
  4. **No network/no backend at all** → key `V` plays the **pre-recorded demo video** (`video/demo.mp4`, recorded at the full rehearsal, 2:30) inside the scene. A placeholder card ("Demo video goes here") ships until the file exists.
  5. Scene timer: if the demo passes **12:20** on the master clock, operator skips to the Capture beat, then scene 10.

### Scene 10 — Novelty: explain-to-audit (11:50–13:20) · [Member 5]
- **On screen (a, 40 s): the evidence chain.** Five evidence records (block, reading, decision, explanation, counterfactual, model version, human approval, MS 2530 clause) appear as linked cards, each showing a short SHA-256 hash and the previous hash. Anchor icon: "digests anchored in Azure confidential ledger".
- **The tamper moment (interactive):** presenter clicks into record #3 and changes "**pH 3.8 → 5.0**" (as if someone tidied up the records before an audit) → hashes recompute **in the browser** → record #3 and every later link turn red and the chain visibly snaps; **Verify** shows "TAMPERED at record 3". Undo → chain heals, green "VERIFIED". Real SHA-256, computed locally — the same mechanism as the dashboard's Verify.
- **(b, 30 s): what's new vs off-the-shelf** — five novelty points as quick chips: evidence log · counterfactual plain-language explanations (shown flipping between English and Bahasa Malaysia) · satellite → drone → ground cascade (animated on the estate map: satellite sweep flags a block → drone zooms to crowns → ranked ground check-list; labelled "screening, not diagnosis") · decisions not detections (grades → crew allocation) · planned cross-country validation + learning loop (every override becomes a label).
- **(c, 20 s): new knowledge** — the agree/override rate becomes measurable evidence of human oversight and model quality; MSPO compliance becomes a by-product of operations; it closes the EUDR gap on plot geolocation/traceability (MSPO and EFI, 2025).
- **Key line:** "Anyone can make a prediction. SawitSense turns every decision into evidence an auditor can verify — and you just saw what happens if someone edits it."

### Scene 11 — Extension & close (13:20–14:30) · [Member 1]
- **On screen:** a three-step evolution arc: **estate decision support → shared traceability layer (buyers verify ledger digests instead of re-auditing) → reusable "explained, auditable decision" pattern**. Then an EUDR commodity ring (cattle, cocoa, coffee, oil palm, rubber, soya, wood) with **rubber** lighting up as the natural second sector; FELDA's 112,635 settler families via a simplified co-operative app.
- **Close:** the hook counters return, now with the three SawitSense answers under them (harvest plan / screening cascade / explained advice → evidence log). Final card: "SawitSense — explained, auditable decisions" + "Questions?" + group members.
- **Key line:** "Record output on fragile foundations. SawitSense makes every field decision faster, explained and auditable — starting with one estate, ready for the whole supply chain."

## 3. Likely Q&A per part (preview — full bank with answers in `SCRIPT.md`, Step 2)
| Part (primary answerer) | Likely questions |
|---|---|
| Case & problems ([Member 1], [Member 2]) | Why is labour ranked above *Ganoderma*? Where does RM2.2 bn come from? Isn't the labour shortage easing? Why not address ageing trees? |
| Cognitive capability ([Member 2]) | What exactly makes this "cognitive" and not just analytics? How accurate is early BSR detection, and what happens on false positives? |
| Solution & architecture ([Member 3]) | Why LoRaWAN and IoT Hub? What happens on a remote block with no signal? Why does an LLM sit in the stack — can it make the decision? |
| Platform & plan ([Member 4]) | Why not Google, given it leads on geospatial? Isn't the scoring subjective? What about cost and lock-in? Why is the pilot only 2–3 blocks? |
| Demo & novelty ([Member 5]) | Is the demo running on Azure right now? (truthful answer: "today's backend is [cloud/laptop, decided at rehearsal]; production is the Azure design in scene 6") · Why pH/TDS in a cup, not in soil? · How is the ledger different from a database? · How do you stop someone recomputing the whole chain? (external anchor in the ledger) |

## 4. Tech approach
- **Form:** a single-page, keyboard-driven web story in plain **HTML + CSS + vanilla JS** (ES modules), 16:9 stage scaled to the projector (tested at 1920×1080 and 1280×720). Opens from `file://` or via `python -m http.server` in `06_presentation/`.
- **Libraries: none planned.** Animations use CSS transitions + the Web Animations API; charts (platform bars, risk grid, timeline) and the estate map are hand-written inline SVG; SHA-256 uses `crypto.subtle` with a small own pure-JS fallback (`js/sha256.js`, ~3 KB) for contexts where `crypto.subtle` is unavailable. If a library proves necessary, it is vendored into `06_presentation/vendor/` with a pinned version and licence file (no CDN). System font stack only — no web fonts.
- **Offline guarantee:** no network calls except the configured dashboard URL and its `/api/v1/health` ping. Checked with the browser network panel with Wi-Fi off (Step 2 test).
- **Navigation:** `→`/`Space` next beat, `←` back, `1`–`9`/`0` jump to scene, `P` opens **presenter view** (second window: current + next scene, speaker, key lines, per-scene timer vs target and a master clock; synced via `BroadcastChannel`, works offline), `F`/`O`/`V` demo fallbacks, `R` reset tamper demo, `B` black screen. Honours `prefers-reduced-motion`.
- **Planned files (Step 2):**

| Path | Content |
|---|---|
| `index.html` | The story (11 scenes) |
| `css/style.css` | Theme (dark, high-contrast projector palette; light toggle `T`) |
| `js/main.js` | Scene engine, keyboard nav, timers, presenter sync |
| `js/scenes/*.js` | One module per interactive scene (estate map, architecture, matrix, roadmap/risks, demo, evidence chain) |
| `js/sha256.js` | Own SHA-256 fallback |
| `data/matrix.json`, `data/risks.json`, `data/roadmap.json` | Figures copied from REPORT.md Tables 3–5 (single place to update) |
| `config.js` | `DASHBOARD_URL` (primary), `FALLBACK_URL` (`http://localhost:8000`), `SIMULATOR_CMD`, `VIDEO_PATH` |
| `config.local.js` | **git-ignored**: admin token for a cloud dashboard (never committed) |
| `presenter.html` | Presenter view |
| `video/` | Fallback demo video (git-ignored; README explains how to record it) |
| `SCRIPT.md` | Full 5-speaker script with timings + Q&A bank |
| `REHEARSAL.md` | Run-of-show, setup checklist (links TEST_PLAN §H R-01…R-14 and demo plan §4/§6), fallback drill |

- **Size budget:** whole folder < 1 MB excluding the video. No downloads (D43).

## 5. Questions for the stakeholder
1. **Speaker split:** OK as proposed (M1 opens/closes, M2 Part 1, M3 solution/architecture + demo operator, M4 platform/plan/risks, M5 demo + novelty)? Should the demo presenter instead be [Member 3] (who explains the architecture) with [Member 5] as operator?
2. **Is Q&A inside the 15 minutes or after?** The plan assumes the talk takes ~14:30 and Q&A is separate. If Q&A is inside the 15 minutes, I will cut to ~12:00 (demo 2:00, scenes 2/8 shortened).
3. **Embedding:** dashboard inside the presentation (iframe, preferred: one window, no tab switching) or switch to a browser tab for the demo?
4. **Projector:** 16:9? Dark theme (proposed) or light theme for a bright room? Which browser on the presentation laptop (Chrome assumed)?
5. **Bahasa Malaysia:** scene 10 flips one explanation into BM — can a member check the wording, or keep it English-only?
6. **Demo extras:** include the optional ACIDIC → LIME beat if time allows? Confirm we skip the dashboard's cascade/harvest panels in the live demo (drone stage not built; satellite placeholder).
7. **Fallback video:** who records it at the full rehearsal? It stays out of git (size) — OK?
8. **Title card:** group number and member names stay placeholders `[GroupNo]`, `[Member 1]…[Member 5]` (D8)?
