# REPORT OUTLINE (for stakeholder approval, D36)

## Changelog (D37)
| Ver | Date | What changed | Trigger |
|---|---|---|---|
| v3 | 2026-11-23 | Stakeholder changes applied: validation is a planned step (no prototype results); risk 1 is now cold start / data gap; roadmap wording changed; references raised to 26 (+KWANG2025, IOI2026, NST-FELDA2019, STAR-LAB2026, GCP-REGIONS, GEE-S2 — the last two evidence Google's residency and geospatial scores in 2.3; EDGE-RUBBER2026 and AZ-ACL-RES left out to stay at 26); FELDA 112,635 families; no cover page or TOC; rubric map moved to RUBRIC_MAP.md | D40 (outline v2 approved with changes) |
| v2 | 2026-11-23 | 2.4 and 2.5 rebuilt from Software design docs 01–05 (integration table, Fig. 6 roadmap with KPIs, nine risks condensed to six); only the M1 metrics remain pending | 03_software docs 01–05 pushed and Lead-checked |
| v1 | 2026-11-23 | First full outline within the D35 budget (≈4,300 body words, 6 tables/figures, 20 references) | D35, D36, D37 |

Keys refer to `01_research/sources.md`. "(pending: …)" would mark points awaiting another team; none remain in v3. Rules applied throughout: D20 (Azure-native target design only), D23 (capability-only justification; cost only as a risk), D32 (residency split, explainability scope, Ganoderma = screening).

---

## Front matter (outside the word budget)
- No cover page, TOC or formatting in REPORT.md (D40): the stakeholder adds them.
- **Executive summary (150 words):** three ranked problems → SawitSense → Azure (88/100) → three-phase roadmap → explain-to-audit novelty.

## 1 Introduction (150)
- Sector scale: 5.70 M ha, 20.28 Mt CPO (a ten-year high), RM112.4 bn exports [MPOB2025]. The case covers FELDA, SD Guthrie and IOI.
- Tension: the record output depends on scarce labour and on bunches being harvested ripe [MPOB2025]. Harvesting is unmechanised [EDGE-SDG2025], and MSPO and the EUDR are tightening [MSPO-EFI2025] [EC-EUDR].
- Thesis: these problems need judgement over images, sensor data and rules at a scale the workforce cannot supply, which is the job a cognitive system does. Then the report roadmap.

## Part 1 — Case Analysis & Problem Identification (~1,400)

### 1.1 Case, organisations, stakeholders, situation (300) — *sub-task 1a [2]*
- **FELDA:** ≈870,000 ha; ≈490,000 ha of settler land, ≈330,000 ha of estates run by FGV, which FELDA has now taken private [EDGE-FELDA]; 112,635 settler families [NST-FELDA2019].
- **SD Guthrie:** raised land per worker from 10.7 ha to 13–13.5 ha (target 15 ha by 2028); says harvesting "still lacks mechanisation" [EDGE-SDG2025]. **IOI:** more than 100 4G/LTE sites across more than 100 estates for IoT [IOI2026].
- **Stakeholders** (a single prose sentence, no table): estate managers, harvest supervisors, agronomists, MSPO officers, mill graders, smallholders, MPOB/MSPO regulators, EU buyers.
- **Current situation:** ripeness judged by eye on fixed rounds; Ganoderma found by visual census; blanket fertiliser schedules; MSPO records kept as separate paperwork. MSPO data lack EUDR polygon geolocation and plot-level traceability [MA-POEB] [KHOO2023] [MSPO-EFI2025].
- *Outstanding:* we contrast the three operating models (settler scheme, multinational, digitising estate) to show that one solution must serve all three.

### 1.2 Prioritised problems with evidence (550) — *sub-task 1b [4]*
- **Ranking criteria (REP-P1, D34):** scale of loss · urgency · labour dependence of today's fix · cognitive addressability.
- **P1 Labour and harvest losses (rank 1):**
  - About 80 % of workers are foreign, and losses are put at RM7.5–20 bn a year (an employer estimate) [STAR-LAB2026].
  - 30,000 workers short (Oct 2026); target of 10 % foreign workers by 2030; RM1 bn of ripe FFB left unharvested in 2021 [EDGE-LAB2026].
  - The shortage drives under-ripe harvesting and so OER loss [MA-POEB].
  - Each 0.5 pt of OER ≈ RM2.2 bn (our calculation, working shown) [MPOB2025]. Nuance: the shortage is cyclical, so the case is about structural resilience.
- **P2 Ganoderma BSR (primary) + ageing (rank 2):**
  - BSR can cause a 43 % loss within 6 months and could reach 860,610 ha by 2040.
  - It is asymptomatic until 60–70 % infected, and lab tests are too slow to apply to every palm [KHOO2023].
  - Published early-detection accuracy is only 64–84 % [KWANG2025] (in 1.3).
  - Ageing is capital-bound; missed replanting locks blocks out of mechanisation [EDGE-SDG2025].
- **P3 MSPO compliance and fertiliser (rank 3):**
  - MSPO is mandatory (87 % of area certified), and the MS 2530:2022 cut-off is 31 Dec 2019 [MSPO-EFI2025].
  - Records are required for fertilising (4.1.3), traceability (4.2.2), and GHG including N₂O from fertiliser (4.5.4) [MPOCC-P31].
  - Fertiliser is ≈30 % of production cost; a 40 % cut means ≥20 % yield loss [STAR-FERT2026].
  - EUDR applies from 30 Dec 2026 [EC-EUDR]. Nuance: the EU takes only 6.8 % of exports [MPOB2025].
- **Interaction (REP-P2), 1–2 sentences:** census and paperwork use the same scarce labour, and tall old palms lower harvester output, so P1 is the root problem and the solution must be integrated.
- **Table 1: Problem prioritisation.** Columns: Problem · Scale of loss · Urgency · Labour dependence · Cognitive addressability · Rank (3 rows).
- *Outstanding:* the ranking is argued against explicit criteria, and the counter-evidence is stated.

### 1.3 Cognitive capability per problem (550) — *sub-task 1c [4]*
- **P1 → computer-vision pattern recognition + scheduling/optimisation.** A YOLO11 drone model reaches mAP 98.3 % at 7.7 ms/frame with per-tree logging [HASSAN2026]. Its outputs drive the harvest window and crew allocation.
- **P2 → multisource ML anomaly detection + spatial reasoning.**
  - Satellite NDVI flags blocks, the drone detector flags crowns, and a 4-row root-contact rule raises neighbour risk [KHOO2023].
  - Spectral methods can confuse disease with nutrient deficiency [KHOO2023], so the system is framed as screening and prioritisation, not diagnosis.
- **P3 → knowledge representation and reasoning + explainable ML + NLP.**
  - The knowledge base holds the MSPO clauses [MPOCC-P31] and agronomic thresholds.
  - A recommender works on soil-sensor data, and NLP produces explanations in BM and English.
  - The RAI dashboard covers the tabular model only [AZ-RAI].
- **Why better than conventional:** the system scales without labour, grades consistently, and turns perception into a decision. It produces audit evidence as a by-product of work.
- **Table 2: Conventional vs cognitive.** Columns: Problem · Conventional method · Its limit · Cognitive capability · Why better (3 rows; Figure 1 and the old Tables 4–5 are dropped).
- *Outstanding:* each problem gets a specific capability, an explicit "why better" and stated limits.

## Part 2 — Technology Evaluation & Solution Proposal (~2,000)

### 2.1 SawitSense: name, functions, users (250) — *2a [2]*
- **Name:** "sawit" (Malay for oil palm) + sense. Tagline: "From sensor to signed-off decision".
- **Functions:**
  - F1 ripeness grading and harvest window;
  - F2 crew allocation;
  - F3 satellite → drone → ground screening cascade;
  - F4 explained fertiliser, lime and irrigation advice;
  - F5 MSPO evidence log and audit pack.
- **Users:** estate manager, harvest mandore (mobile, multilingual), agronomist (review queue), IPM officer, MSPO officer, IT team, smallholder co-operatives (later phase).
- Prose only, no table. *Outstanding:* every function is traced to P1–P3 and O1–O4.

### 2.2 Underlying technologies + adapted architecture (350) — *2b [3]*
- Each layer is justified by capability:
  - Data sources: Sentinel-2, UAV, IoT soil nodes over LoRaWAN, bunch images, estate ERP, MSPO documents.
  - Ingestion: IoT Hub, Event Hubs, Data Lake Gen2, Planetary Computer STAC.
  - Cognitive: models M1–M6, knowledge base M7, reasoning, NLP.
  - Cloud: Azure ML endpoints and monitoring; IoT Operations edge, which keeps working offline and was validated after 45 days offline [AZ-IOTOPS].
  - Application: dashboard, mobile app, audit pack.
- Cross-cutting: PDPA residency split, Entra ID / Key Vault, Grad-CAM for images and RAI for tabular models [AZ-RAI].
- **Figure 1: SawitSense layered architecture (adapted from PDF Fig. 4).** A compact Mermaid diagram with 5 layers and a cross-cutting bar (from `03_software/02_architecture.md` §1).

### 2.3 Platform evaluation and recommendation (650) — *2c [5]*
- **Four platforms:** Azure, AWS, Google "Gemini platform (formerly Vertex AI)", IBM watsonx. Seven capability criteria (weights): C1 IoT 15, C2 residency 15, C3 vision 15, C4 geospatial 15, C5 edge/offline 10, C6 MLOps/XAI 15, C7 enterprise integration 15.
- **Totals: Azure 88 · AWS 79 · Google 67 · IBM 49** (D32). Azure stays first under the equal-weight and geospatial-heavy sensitivity checks.
- **Evidence:**
  - Malaysia West region [AZ-REGIONS]; AWS Malaysia region [AWS-MYREGION];
  - Google IoT Core retired [GCP-IOTCORE]; IBM Watson IoT retired [REG-WIOT];
  - SAP connector [AZ-SAP]; IoT Operations [AZ-IOTOPS].
- **Balanced reasoning:**
  - Google leads on geospatial and AWS is a credible runner-up.
  - Azure's caveats: RAI is tabular-only, and Azure OpenAI is not offered in Malaysia West [AZ-AOAI-MODELS].
  - Research depth on AWS was uneven, so the lead is framed as best fit for an estate already running SAP/Microsoft.
- **Recommendation:** Azure, linked to each problem. P1 and P2 are served by vision plus IoT/edge; P3 by residency, explainability and ERP integration.
- **Table 3: Weighted capability matrix.** Columns: Criterion (weight) · Azure · AWS · Google · IBM, plus a totals row and a sensitivity row.

### 2.4 Integration with existing IT + phased plan (400) — *2d [3]*
Source: `03_software/04_cloud_design.md` §3, §5, §6.
- **Integration with the estate IT already in place:**
  - **SAP ERP (S/4HANA or ECC)**, via the Logic Apps SAP connector (IDoc/BAPI/RFC) behind API Management [AZ-SAP]. Block master and planting dates seed the MSPO block reference (4.1.3.4). Approved fertiliser and lime actions become work orders. Harvest tickets close the yield loop.
  - **Mill weighbridge and grading** feeds come in for ripeness feedback and OER KPIs.
  - **Outbound:** the MSPO evidence pack, and N quantities into the GHG calculation (4.5.4) [MPOCC-P31].
  - **Microsoft 365:** Power BI and Teams alerts.
  - **Field data:** the drone vendor uploads into the data lake; LoRaWAN network server → IoT Hub; an edge cluster runs on the estate network [AZ-IOTOPS].
- **Residency split (D32), the only place PDPA appears:**
  - personal data stays in Malaysia West [AZ-REGIONS];
  - Azure OpenAI and the Confidential Ledger run in Southeast Asia and receive only non-personal or hashed data [AZ-AOAI-MODELS];
  - s129 safeguards apply: a Transfer Impact Assessment and transfer records [MAYER-PDPA2025].
- **Roadmap (PDF Fig. 6 structure):**
  - **Short term (0–6 months), pilot.** One estate, 2–3 blocks including one with a BSR history. Models M1, M5, M6, M7, with M3 as a screening trial. ERP read-only. Human approval of every action. Baseline KPIs first.
  - **Medium term (6–18 months), scale and integrate.** One region of estates, with LoRaWAN plus edge processing on each estate. The rule-based baseline is replaced by estate-trained models. M2 learns time-to-ripe from logged grades. SAP work-order write-back, drift monitoring and ledger anchoring go live.
  - **Long term (18–36 months), optimise and extend.** Group-wide rollout plus smallholder co-operatives. Yield forecasting from logged history. Multispectral BSR detection. EUDR geolocation package.
- **Table 4: Phased roadmap.** Columns: Phase · Scope · Models / functions · Integration · Success measure. Three rows, with KPIs per phase:
  - short term: agronomist agreement ≥80 %, and the audit pack accepted by an internal auditor;
  - medium term: harvest rounds back within 10–15 days;
  - long term: a measurable OER gain and MSPO audits with zero record findings.

### 2.5 Risks and mitigations, prioritised (350) — *2e [2]*
Source: `04_cloud_design.md` §4, §7. The nine risks there, scored likelihood × impact on 1–3 scales, are condensed to six rows in Fig. 6 categories, highest first:
1. **Technical: cold start and data gaps (3×3).** No labelled estate data exists at launch: no public soil-sensor, harvest-timing or multispectral BSR data, and early-BSR accuracy in the literature is only 64–84 % [KWANG2025]. *Mitigation:* launch on a rule-based agronomic baseline with human review of every action; frame Ganoderma as screening, not diagnosis, with ground confirmation; collect labelled pilot data; validate across countries before go-live; retrain on pilot data, triggered by drift.
2. **Operational: adoption and trust (3×2).** The field workforce is largely foreign, with mixed literacy [EDGE-LAB2026]. *Mitigation:* multilingual counterfactual explanations, one-tap approve or override, mandore champions, and a paper fallback during the pilot.
3. **Technical: legacy ERP and connectivity (2×3).** Customised SAP ECC with inconsistent block codes, and blocks with poor coverage. *Mitigation:* the SAP connector with read-only first and write-back later, a block-master clean-up [AZ-SAP], and edge buffering with local rules [AZ-IOTOPS].
4. **Vendor & cost: lock-in (2×2).** *Mitigation:* open formats (ONNX, STAC, Kafka protocol, MLflow), a containerised API, and AWS as a documented fallback because it also has a Malaysian region [AWS-MYREGION].
5. **Vendor & cost: enterprise spend growth (2×2).** Drivers are GPU training, always-on endpoints and message volume. *Mitigation:* budgets and alerts, edge aggregation, autoscale schedules, drift-triggered rather than calendar retraining, and a quarterly FinOps review.
6. **Vendor / compliance: service residency and PDPA transfer (2×2, 1×3).** *Mitigation:* the residency split, a template fallback if the LLM is unavailable, and DPO sign-off before phase 2 [AZ-AOAI-MODELS] [MAYER-PDPA2025].
- **Table 5: Risk register.** Columns: # · Category · Risk · L×I · Mitigation · Owner.

## Part 3 — Creative Thinking & Innovation (~600)

### 3.1 Novelty vs off-the-shelf (400) — *3a [3]*
- **Explain-to-audit evidence log (anchor, D18/D28).** Each decision is stored with its inputs, model version, explanation, counterfactual, human approval or override, geolocation and MSPO clause. Records are hash-chained into Azure Confidential Ledger, and a one-click audit pack is produced [MPOCC-P31] [MSPO-EFI2025]. Compliance becomes a by-product of operations.
- **Counterfactual explanations** a supervisor can read, e.g. "if pH ≥ 4.2 → fertilise" [AZ-RAI].
- The **satellite → drone → ground cascade** with neighbour-risk reasoning [KHOO2023], and **crew allocation** that turns ripeness grades into decisions [HASSAN2026].
- **Cross-country validation (planned):** train on another country's public data and test on Malaysian data before go-live, then report any drop. The human-review queue feeds retraining.
- No table; a contrast sentence against single-function tools.

### 3.2 Future extension (200) — *3b [2]*
- **Organisation:** FELDA settler co-operatives get a simplified advisory app and evidence log [EDGE-FELDA]; yield forecasting comes from logged data; N₂O/GHG accounting comes from the fertiliser log [MPOCC-P31].
- **Other sectors:** the EUDR also covers rubber and cocoa [EC-EUDR], so plot geolocation and the evidence log transfer directly. Rubber shares the smallholder geolocation and traceability problem (the 90 % smallholder figure was dropped with EDGE-RUBBER2026), which raises the same traceability problem (optional reference; see open question 1).

## Conclusion (150)
- Restates the ranked problems, how SawitSense answers each, why Azure fits, and how the solution evolves.

---

## Tables and figures (6)
Table 1 prioritisation · Table 2 conventional vs cognitive · Figure 1 architecture · Table 3 platform matrix · Table 4 roadmap · Table 5 risk register.

## Core reference list (26)
The 20 entries of v2 plus six added under D40. Full entries are in the REPORT.md reference list. Added: Kwang et al. (2025), IOI Corporation Berhad (2026), New Straits Times (2019), Ramendran (2026), Google Cloud (2026) [GCP-REGIONS], Google Earth Engine (n.d.) [GEE-S2]. Letters: Microsoft (2026a/b/c) = AOAI models / regions / IoT Operations; The Edge Malaysia 2025 / 2026 / n.d. need no letters.

- **Industry and government:** MPOB (2026) · MPOCC (2023) · MSPO and EFI (2025) · Ma (n.d.) · IOI Corporation Berhad (2026) · European Commission (2026) · Mayer Brown (2025)
- **News and trade press:** Chong (2026) · Ramendran (2026) · The Edge Malaysia (2025; 2026; n.d.) · New Straits Times (2019) · Clark (2022)
- **Academic:** Khoo and Chong (2023) · Che Hassan et al. (2026) · Kwang et al. (2025)
- **Vendor:** Amazon (2024) · Google Cloud (n.d.) · Google Cloud (2026) · Google Earth Engine (n.d.) · Microsoft (2025; 2026a; 2026b; 2026c; n.d.)

## Appendix A — Progress report (≤1 page)
- **Table A1: Timeline.** Columns: Date · Milestone · Owner (6–8 rows, 23 Nov – 14 Dec; from git history and PROJECT_PLAN phases).
- **Table A2: Contribution.** Columns: Member · Role · Sections / artefacts · Contribution %. Names are placeholders ([Member 1 – Leader]…[Member 5]).
- The rubric cross-reference is in `05_report/RUBRIC_MAP.md` (D35, D40) and is not part of the report.
- Placeholders: [Member 1 – Leader]…[Member 5], [ID], [GroupNo], [Lecturer name].

## Open questions for the stakeholder
- Resolved in D40. Still open: section owners for Table A2, lecturer name and group number (placeholders in Appendix A).
