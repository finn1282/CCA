# 01 — Solution Overview: SawitSense

> Report-facing (Part 2: application name, core functions, target users). Citation keys refer to `01_research/sources.md`. Rules applied: D19 problem order, D23 capability-based justification, D28 scope.

## 1. Name

| Option | Meaning | Verdict |
|---|---|---|
| **SawitSense** | "Sawit" is Malay for oil palm; "Sense" covers both sensing (satellite, drone, soil, camera) and sense-making (explained decisions) | **Recommended (D24).** No existing product found under this name. Clearly different from MPOB's *MySawit* and *Tekno Sawit* apps (MPOB-APPS2025) |
| PalmPulse | Continuous health signal of the estate | Generic; already used by unrelated brands |
| Sawit360 | All-round view | Too close to existing "Sawit360" search results (MPOB-APPS2025 context) |

**Tagline:** *From sensor to signed-off decision.*

**One-sentence pitch.** SawitSense is a cognitive decision-support platform for Malaysian oil palm estates. It fuses Sentinel-2 satellite imagery, drone surveys, IoT soil sensors and bunch photos into four explained decisions:
- where to harvest and with which crew;
- which palms to check for *Ganoderma* first;
- what to apply to each block;
- an audit-ready MSPO evidence trail.

## 2. Problems → outcomes → core functions

The problem order is the one ruled in D19; the evidence base is in `01_research/01_problem_evidence.md`.

| Problem (D19) | Evidence (short) | Outcome | SawitSense core function | Cognitive capability |
|---|---|---|---|---|
| **P1 Labour shortage & harvest losses** | ~80 % foreign workforce and 30,000 workers short (STAR-LAB2026; EDGE-LAB2026). Harvesting is not mechanised (EDGE-SDG2025). Rounds stretch to 20–25 days against a 7–13-day recommendation (AHMAD2020). Under-ripe harvesting loses oil (MA-POEB) | **O1** predict ripe-FFB harvest windows | **F1 Ripeness grading & harvest window**: a vision model grades bunches from camera or drone images. A harvest-window rule turns grades into "harvest now / next round" (RAMLI2026)<br>**F2 Harvester allocation**: assigns the limited crew to the blocks where each harvester saves the most ripe bunches, weighted by over-ripening risk (AHMAD2020; MPOB-NEWS2020) | Computer vision; optimisation |
| **P2 Declining stand productivity: Ganoderma BSR (primary) + ageing** | BSR affects 9.2 % of surveyed smallholdings and >20 % of some plantings (IBRAHIM2020; BORNEO-GANO2025). It is asymptomatic until 60–70 % of the palm is infected (KHOO2023). Replanting runs at 2 % vs a 4–5 % target (SARMIDI2025) | **O2** detect Ganoderma early | **F3 Satellite → drone → ground screening cascade**: <br>1. Sentinel-2 NDVI anomaly selects blocks. <br>2. A drone detector scores palms. <br>3. Ground checks are ranked by suspicion and closeness to confirmed cases, because root contact spreads BSR within about 4 rows (KHOO2023) while spores cause scattered cases (COOPER2011). <br>Positioned as **screening and prioritisation, not diagnosis** (D32e; KWANG2025; AHMADI2023) | Multisource ML; anomaly detection; spatial reasoning |
| **P3 MSPO sustainability & fertiliser compliance** | MSPO is mandatory; MS 2530:2022 requires SOP records for fertilising and soil fertility (4.1.3), traceability (4.2.2), GHG including N₂O from fertiliser (4.5.4) and water management (4.5.5) (MPOCC-P31; MPOCC-P21). Fertiliser is ≈30 % of production cost (STAR-FERT2026). EUDR applies from 30 Dec 2026 (HL-EUDR2026) | **O3** optimise fertiliser use · **O4** yield + MSPO | **F4 Explained fertiliser / lime / irrigation advice**: a rule engine based on agronomic thresholds (KANANG2026; AAR-SOIL; CARR2011), plus an ML confidence check and a counterfactual ("would be OK if pH ≥ 4.2")<br>**F5 Explain-to-audit evidence log**: every AI decision is stored with inputs, model version, explanation, human approval and block. The log is tamper-evident and mapped to MSPO clauses, and exports as an audit pack (D18, D28)<br>**F6 Productivity & compliance analytics**: NDVI trends, MSPO clause coverage and evidence KPIs | Knowledge representation & reasoning; explainable ML; NLP (multilingual explanations) |

**Data gap: yield forecasting.** No public data exists for yield forecasting, so it is a **medium-term roadmap item** fed by the estate's own logged data (D28). The same applies to the harvest-timing and soil-sensor datasets, which do not exist publicly either (`01_research/03_datasets.md`).

## 3. Target users

| User | Where they work | What SawitSense gives them | Interface |
|---|---|---|---|
| **Estate manager** | Estate office | Daily block priorities for harvest, screening and fertiliser; MSPO coverage; KPIs | Web dashboard (Power BI for group reporting) |
| **Harvest mandore** (crew supervisor) | Field | Today's crew allocation per block; bunch grades | Mobile harvester app; plain-language, multilingual text for a largely foreign workforce (STAR-LAB2026) |
| **Agronomist** | Regional / HQ | Explained recommendations, a review queue for low-confidence results, approve/override | Dashboard review queue |
| **Plant-health / IPM officer** | Field + office | Ranked palm check-lists from the cascade, with confirmation feedback | Dashboard + mobile |
| **Sustainability / MSPO officer** | HQ | Evidence pack per block and period; chain-verification status | Audit-pack export |
| **IT / data team** | HQ | Model registry, monitoring, ERP integration | Azure ML studio, Logic Apps |
| **Smallholder cooperative** (extension) | Village | A simplified advisory and evidence log for MSPO Part 2 certification (MPOCC-P21) | Mobile (long-term phase) |

## 4. User stories (acceptance-style)

1. **Manager (P1).** As an estate manager, I want each morning's crew allocation ranked by the ripe bunches each harvester can save, so that the fewest bunches over-ripen when I am short of workers.
   - *Accept when* the plan lists blocks, harvesters assigned, bunches at risk, and the rule used.
2. **Mandore (P1).** As a harvest mandore, I want to photograph a bunch and get "ripe — harvest this round" with a heat-map, so that I can grade consistently without an experienced grader.
   - *Accept when* the result shows the class, the confidence, the region of the image the model attended to, and the harvest advice.
3. **IPM officer (P2).** As an IPM officer, I want a ranked list of palms to check, starting with drone-flagged palms near confirmed BSR cases, so that a scarce field team visits the most likely infections first.
   - *Accept when* each palm shows its suspicion score, its distance to the nearest confirmed case and the satellite block flag. The list says "screening, not diagnosis".
4. **Agronomist (P3).** As an agronomist, I want each fertiliser or lime recommendation to show the rule, the reading, a counterfactual and the model's agreement, so that I can approve or override it in one click.
   - *Accept when* an override is logged as a new record and queued as a retraining example.
5. **MSPO officer (P3/O4).** As a sustainability officer, I want an evidence pack for block X covering last quarter, with clause references (4.1.3, 4.2.2, 4.5.4, 4.5.5) and proof that no record was altered, so that I can satisfy an MSPO auditor quickly.
   - *Accept when* the pack shows clause coverage and gaps, a decision table, and a "chain verified" result.
6. **IT lead.** As the IT lead, I want approved fertiliser actions posted to the ERP work-order module, so that operations and audit records do not diverge.
   - *Accept when* an approved action creates an ERP work order through the integration layer (`04_cloud_design.md` §5).

## 5. What makes it different (summary — full argument in Report Part 3)

| SawitSense | Off-the-shelf |
|---|---|
| **Explain-to-audit**: each decision becomes tamper-evident MSPO evidence (D18) | Dashboards show predictions; compliance stays manual paperwork |
| **Cascade across scales**: satellite → drone → ground, with neighbour-spread reasoning (KHOO2023) | Single-sensor tools |
| **Decision, not just detection**: ripeness grades become crew allocation | Ripeness graders stop at the grade (HASSAN2026) |
| **Counterfactual explanations** a supervisor can read, in the worker's language | Feature-importance charts for data scientists |
| **Human-in-the-loop learning**: overrides feed retraining | Static models |
| None of the Malaysian tools found combine satellite + drone + IoT with an MSPO evidence log (MPOB-APPS2025) | — |
