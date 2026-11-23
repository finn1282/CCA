# REPORT OUTLINE (for stakeholder approval, D36)

## Changelog (D37)
| Ver | Date | What changed | Trigger |
|---|---|---|---|
| v1 | 2026-11-23 | First full outline within the D35 budget (≈4,300 body words, 6 tables/figures, 20 references) | D35, D36, D37 |

Keys refer to `01_research/sources.md`. "(pending: …)" marks points that may change when that team's output arrives. Rules applied throughout: D20 (Azure-native target design only), D23 (capability-only justification; cost only as a risk), D32 (residency split, explainability scope, Ganoderma = screening).

---

## Front matter (outside the word budget)
- **Cover page:** title, module, ITS69404+[GroupNo], [Member 1 – Leader]…[Member 5] with [ID], lecturer, submission date. **TOC.**
- **Executive summary (150 words):** three ranked problems → SawitSense → Azure (88/100) → three-phase roadmap → explain-to-audit novelty.

## 1 Introduction (150)
- Sector scale: 5.70 M ha, 20.28 Mt CPO (a ten-year high), RM112.4 bn exports [MPOB2025]. The case covers FELDA, SD Guthrie and IOI.
- Tension: the record output depends on scarce labour and on bunches being harvested ripe [MPOB2025]. Harvesting is unmechanised [EDGE-SDG2025], and MSPO and the EUDR are tightening [MSPO-EFI2025] [EC-EUDR].
- Thesis: these problems need judgement over images, sensor data and rules at a scale the workforce cannot supply, which is the job a cognitive system does. Then the report roadmap.

## Part 1 — Case Analysis & Problem Identification (~1,400)

### 1.1 Case, organisations, stakeholders, situation (300) — *sub-task 1a [2]*
- **FELDA:** ≈870,000 ha; ≈490,000 ha worked by more than 100,000 settler families; ≈330,000 ha of estates run by FGV, which FELDA has now taken private [EDGE-FELDA].
- **SD Guthrie:** raised land per worker from 10.7 ha to 13–13.5 ha (target 15 ha by 2028); says harvesting "still lacks mechanisation" [EDGE-SDG2025]. **IOI:** estate-wide 4G (no core reference; see open question 1).
- **Stakeholders** (a single prose sentence, no table): estate managers, harvest supervisors, agronomists, MSPO officers, mill graders, smallholders, MPOB/MSPO regulators, EU buyers.
- **Current situation:** ripeness judged by eye on fixed rounds; Ganoderma found by visual census; blanket fertiliser schedules; MSPO records kept as separate paperwork. MSPO data lack EUDR polygon geolocation and plot-level traceability [MA-POEB] [KHOO2023] [MSPO-EFI2025].
- *Outstanding:* we contrast the three operating models (settler scheme, multinational, digitising estate) to show that one solution must serve all three.

### 1.2 Prioritised problems with evidence (550) — *sub-task 1b [4]*
- **Ranking criteria (REP-P1, D34):** scale of loss · urgency · labour dependence of today's fix · cognitive addressability.
- **P1 Labour and harvest losses (rank 1):**
  - 30,000 workers short (Oct 2026); target of 10 % foreign workers by 2030; RM1 bn of ripe FFB left unharvested in 2021 [EDGE-LAB2026].
  - The shortage drives under-ripe harvesting and so OER loss [MA-POEB].
  - Each 0.5 pt of OER ≈ RM2.2 bn (our calculation, working shown) [MPOB2025]. Nuance: the shortage is cyclical, so the case is about structural resilience.
- **P2 Ganoderma BSR (primary) + ageing (rank 2):**
  - BSR can cause a 43 % loss within 6 months and could reach 860,610 ha by 2040.
  - It is asymptomatic until 60–70 % infected, and lab tests are too slow to apply to every palm [KHOO2023].
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
- **Integration:**
  - Logic Apps SAP connector (IDoc/BAPI/RFC) reads blocks and HR data and writes back approved fertiliser actions as work orders [AZ-SAP];
  - LoRaWAN network server → IoT Hub; edge cluster on the estate network [AZ-IOTOPS].
- **Residency split:**
  - personal data stays in Malaysia West;
  - Azure OpenAI and Confidential Ledger run in Southeast Asia with only non-personal or hashed data, under s129 safeguards (Transfer Impact Assessment, transfer record) [AZ-REGIONS] [AZ-AOAI-MODELS] [MAYER-PDPA2025].
- **Roadmap:**
  - **Short term (0–6 months):** pilot on 2–3 estates: soil nodes, M1 ripeness, evidence log, SAP read-only.
  - **Medium term (6–18 months):** drone/satellite cascade, crew allocation, retraining with humans in the loop, ERP write-back, M6 retrained on estate data, yield forecasting.
  - **Long term (18–36 months):** group-wide edge rollout, smallholder/co-operative app, EUDR due-diligence export, other crops.
- (pending: `03_software/04_cloud_design.md`, phase durations and integration detail)
- **Table 4: Phased roadmap (PDF Fig. 6).** Columns: Phase · Scope / functions · Integration step · Exit KPI.

### 2.5 Risks and mitigations, prioritised (350) — *2e [2]*
Ranked by likelihood × impact (pending: `03_software/05_…` risk list):
1. **Technical — model generalisation and data gaps.** M6 is trained on simulated data, there is no harvest-time data, and estates differ. *Mitigation:* cross-country validation, human review, drift alerts that trigger retraining.
2. **Operational — adoption by a multilingual, mostly foreign crew, and Ganoderma false positives.** *Mitigation:* plain-language multilingual explanations, a "screening, not diagnosis" label, ground confirmation, mandore champions.
3. **Technical — connectivity under the canopy.** *Mitigation:* offline edge processing [AZ-IOTOPS] and LoRaWAN gateway planning.
4. **Vendor & cost — lock-in and consumption cost at group scale** (GPU training, message volumes). *Mitigation:* open formats (ONNX, COCO, STAC, Kafka-compatible streaming), FinOps budgets, phased scaling, AWS as a documented fallback [AWS-MYREGION].
5. **Compliance constraint — PDPA cross-border transfer.** *Mitigation:* the residency split [MAYER-PDPA2025].
- **Table 5: Risk register.** Columns: # · Category · Risk · Likelihood/Impact · Mitigation · Owner.

## Part 3 — Creative Thinking & Innovation (~600)

### 3.1 Novelty vs off-the-shelf (400) — *3a [3]*
- **Explain-to-audit evidence log (anchor, D18/D28).** Each decision is stored with its inputs, model version, explanation, counterfactual, human approval or override, geolocation and MSPO clause. Records are hash-chained into Azure Confidential Ledger, and a one-click audit pack is produced [MPOCC-P31] [MSPO-EFI2025]. Compliance becomes a by-product of operations.
- **Counterfactual explanations** a supervisor can read, e.g. "if pH ≥ 4.2 → fertilise" [AZ-RAI].
- The **satellite → drone → ground cascade** with neighbour-risk reasoning [KHOO2023], and **crew allocation** that turns ripeness grades into decisions [HASSAN2026].
- **Cross-country validation:** trained on Indonesian data, tested on Malaysian data, and the drop is reported honestly (pending: `03_software/03_ai_models.md` §9, M1 metrics). The human-review queue feeds retraining.
- No table; a contrast sentence against single-function tools.

### 3.2 Future extension (200) — *3b [2]*
- **Organisation:** FELDA settler co-operatives get a simplified advisory app and evidence log [EDGE-FELDA]; yield forecasting comes from logged data; N₂O/GHG accounting comes from the fertiliser log [MPOCC-P31].
- **Other sectors:** the EUDR also covers rubber and cocoa [EC-EUDR], so plot geolocation and the evidence log transfer directly. Malaysian rubber is about 90 % smallholder-grown, which raises the same traceability problem (optional reference; see open question 1).

## Conclusion (150)
- Restates the ranked problems, how SawitSense answers each, why Azure fits, and how the solution evolves.

---

## Tables and figures (6)
Table 1 prioritisation · Table 2 conventional vs cognitive · Figure 1 architecture · Table 3 platform matrix · Table 4 roadmap · Table 5 risk register.

## Core reference list (20)
In-text form is given first, then the full Harvard entry.

1. **(Amazon, 2024)** Amazon (2024) *AWS launches infrastructure region in Malaysia* [Press release], 21 August. Available at: https://press.aboutamazon.com/2024/8/aws-launches-infrastructure-region-in-malaysia (Accessed: 23 November 2026).
2. **(Chong, 2026)** Chong, R. (2026) 'Lower palm oil yields loom as Sabah growers cut fertiliser', *The Star*, 20 August. Available at: https://www.thestar.com.my/news/nation/2026/08/20/lower-palm-oil-yields-loom-as-sabah-growers-cut-fertiliser (Accessed: 23 November 2026).
3. **(Che Hassan et al., 2026)** Che Hassan, C.A.Z., Muhammad Razif, M.R., Mohd, M.N., Abd Halim, A., Mohd Mustapha, N.H. and Azman, M.N. (2026) 'Real-time oil palm fresh fruit bunch drone image classification using YOLO11 architecture', *Journal of Oil Palm Research* (in press). doi:10.21894/jopr.2026.0033 (Accessed: 23 November 2026).
4. **(Clark, 2022)** Clark, L. (2022) 'IBM to fire Watson IoT Platform from its cloud', *The Register*, 15 November. Available at: https://www.theregister.com/2022/11/15/ibm_set_to_retire_watson/ (Accessed: 23 November 2026).
5. **(European Commission, 2026)** European Commission (2026) *Regulation on deforestation-free products* (Regulation (EU) 2023/1115). [URL as in sources.md] (Accessed: 23 November 2026).
6. **(Google Cloud, n.d.)** Google Cloud (n.d.) *Google.Cloud.Iot.V1 .NET client library reference* (deprecation notice). Available at: https://docs.cloud.google.com/dotnet/docs/reference/Google.Cloud.Iot.V1/latest (Accessed: 23 November 2026).
7. **(Khoo and Chong, 2023)** Khoo, Y.W. and Chong, K.P. (2023) '*Ganoderma boninense*: general characteristics of pathogenicity and methods of control', *Frontiers in Plant Science*, 14, 1156869. doi:10.3389/fpls.2023.1156869 (Accessed: 23 November 2026).
8. **(Ma, n.d.)** Ma, A.N. (n.d.) 'Challenges facing the palm oil industry', *Palm Oil Engineering Bulletin*, No. 94, pp. 19–22. Bangi: MPOB. Available at: https://palmoilis.mpob.gov.my/publications/POEB/poeb94-ma2.pdf (Accessed: 23 November 2026).
9. **(MPOB, 2026)** Malaysian Palm Oil Board (MPOB) (2026) *Overview of the Malaysian Oil Palm Industry in 2025*. Bangi: MPOB. Available at: https://bepi.mpob.gov.my/images/overview/Overview2025.pdf (Accessed: 23 November 2026).
10. **(MPOCC, 2023)** Malaysian Palm Oil Certification Council (MPOCC) (2023) *Guidance document for MS2530-3-1:2022 General principles for oil palm plantations (40.46 hectares to 500 hectares)*, Version 1.0. Available at: https://mspo.org.my/wp-content/uploads/2025/08/Guidance-document-for-MSPO-Part-3-1.pdf (Accessed: 23 November 2026).
11. **(MSPO and EFI, 2025)** Malaysian Sustainable Palm Oil (MSPO) and European Forest Institute (EFI) (2025) *Joint gap assessment of the EUDR information needs and information availability from the MSPO certification*. Available at: https://www.forest-trends.org/wp-content/uploads/2022/01/2025-MSPO_EUDR-Joint_Gap_Assessment.pdf (Accessed: 23 November 2026).
12. **(Mayer Brown, 2025)** Mayer Brown (2025) *From legislative reform to practical guidance: key amendments to Malaysia's PDPA and the launch of cross-border transfer guidelines*, 25 July. Available at: https://www.mayerbrown.com/en/insights/publications/2025/07/from-legislative-reform-to-practical-guidance-key-amendments-to-malaysias-pdpa-and-the-launch-of-cross-border-transfer-guidelines (Accessed: 23 November 2026).
13. **(Microsoft, 2025)** Microsoft (2025) *Assess AI systems and make data-driven decisions with Azure Machine Learning Responsible AI dashboard*. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai-dashboard (Accessed: 23 November 2026).
14. **(Microsoft, 2026a)** Microsoft (2026a) *Azure OpenAI models and region availability*. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models (Accessed: 23 November 2026).
15. **(Microsoft, 2026b)** Microsoft (2026b) *List of Azure regions*. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/reliability/regions-list (Accessed: 23 November 2026).
16. **(Microsoft, 2026c)** Microsoft (2026c) *What is Azure IoT Operations?* Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/iot-operations/overview-iot-operations (Accessed: 23 November 2026).
17. **(Microsoft, n.d.)** Microsoft (n.d.) *Access SAP from workflows* (Azure Logic Apps SAP connector). Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/logic-apps/logic-apps-using-sap-connector (Accessed: 23 November 2026).
18. **(The Edge Malaysia, 2025)** The Edge Malaysia (2025) 'Cover Story: Positioning SD Guthrie for next stage of growth', *The Edge Malaysia Weekly*, 15–21 December. Available at: https://theedgemalaysia.com/node/786139 (Accessed: 23 November 2026).
19. **(The Edge Malaysia, 2026)** The Edge Malaysia (2026) 'Cover Story 1: Can Malaysian planters avert another migrant worker crunch?', *The Edge Malaysia Weekly*, 9–15 November. Available at: https://theedgemalaysia.com/node/825330 (Accessed: 23 November 2026).
20. **(The Edge Malaysia, n.d.)** The Edge Malaysia (n.d.) 'Felda's road ahead in the spotlight', *The Edge Malaysia*, 6 October. [URL as in sources.md] (Accessed: 23 November 2026).

**Left out to stay at 20 (each a one-for-one swap):** [IOI2026] (IOI connectivity) · [AZ-ACL-RES] (ledger replication) · [STAR-LAB2026] (~80 % foreign workforce) · [EDGE-RUBBER2026] (rubber traceability) · [KWANG2025] (Ganoderma detection accuracy of 64–84 %).

## Appendix A — Progress report (≤1 page)
- **Table A1: Timeline.** Columns: Date · Milestone · Owner (6–8 rows, 23 Nov – 14 Dec; from git history and PROJECT_PLAN phases).
- **Table A2: Contribution.** Columns: Member · Role · Sections / artefacts · Contribution %. Names are placeholders ([Member 1 – Leader]…[Member 5]).
- The rubric cross-reference has moved to `05_report/RUBRIC_MAP.md` (D35) and is not part of the report.

## Open questions for the stakeholder
1. **References are capped at 20.** Should any of the five left-out sources replace one in the core list? I recommend swapping in IOI2026 for 1.1, as IOI is one of the three named organisations.
2. **Section owners:** which members owned which sections, for Table A2 and the presentation split?
3. **Lecturer name** and **group number** for the cover page.
4. **FELDA settlers:** the core source gives ">100,000 settlers" [EDGE-FELDA]. The exact count of 112,635 families (2019) would need [NST-FELDA2019] as a 21st reference. Is "more than 100,000" enough?
