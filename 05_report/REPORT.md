## Executive Summary

Malaysia's palm oil sector produced record output in 2025 (MPOB, 2026), yet those gains depend on scarce harvesters, healthy palm stands and certified practice. This report analyses the case of FELDA, SD Guthrie and IOI and ranks three problems: (P1) labour shortage and harvest losses; (P2) declining stand productivity, driven mainly by *Ganoderma* basal stem rot; and (P3) MSPO compliance and fertiliser efficiency. It proposes **SawitSense**, a cognitive decision-support application. SawitSense fuses satellite, drone and IoT soil-sensor data through computer vision, multisource anomaly detection and knowledge-based reasoning. It plans harvests, screens for disease and gives explained fertiliser advice. A capability-only evaluation of four enterprise platforms ranks Microsoft Azure first (88/100) for its Malaysian region, first-party IoT with an offline edge, and SAP integration. A three-phase roadmap runs from a one-estate pilot to group-wide use. The main novelty is an explain-to-audit evidence log that turns every decision into tamper-evident MSPO and EUDR evidence.

---

## 1 Introduction

In 2025 Malaysia's 5.70 million hectares of oil palm produced a ten-year high of 20.28 million tonnes of crude palm oil (CPO). Palm product exports earned RM112.4 billion (Malaysian Palm Oil Board (MPOB), 2026). The case concerns three producers that typify the sector: the FELDA settlement scheme, the multinational SD Guthrie and the digitising IOI Corporation. They share one difficulty. Key field decisions depend on human judgement over images, sensor readings and regulations: when to harvest, which palms are diseased, how much fertiliser to apply. The workforce that supplies that judgement is shrinking (The Edge Malaysia, 2026). Cognitive computing systems perceive patterns, reason over domain knowledge and explain their conclusions, which makes them suited to this task. Part 1 analyses the case and ranks the problems. Part 2 proposes SawitSense, evaluates platforms and plans integration. Part 3 explains its novelty and how it can be extended.

---

# Part 1 — Case Analysis & Problem Identification

## 1.1 The Case: Organisations, Stakeholders and Current Situation

**Organisations.** FELDA, the national land-settlement agency, controls about 870,000 ha. Around 490,000 ha are worked by settlers, and about 330,000 ha of commercial estates are run by FGV, which FELDA has taken private (The Edge Malaysia, n.d.). The scheme supports 112,635 settler families (New Straits Times, 2019). SD Guthrie (formerly Sime Darby Plantation) has raised its land-to-labour ratio from 10.7 to 13–13.5 ha per worker and is targeting 15 ha by 2028. It states that harvesting still has no mechanised solution (The Edge Malaysia, 2025). IOI has built more than 100 4G/LTE sites across more than 100 estates to support IoT and data-led management (IOI Corporation Berhad, 2026). These are three distinct operating models: a settler scheme, a multinational estate group and a digitising estate group. A useful solution must therefore serve smallholders as well as well-connected estates.

**Stakeholders.** The direct users are estate managers, harvest supervisors (*mandores*), agronomists, plant-health and MSPO officers, and mill graders. Affected parties include settlers and smallholders, the regulators MPOB and MSPO, and EU buyers subject to deforestation due diligence (MSPO and EFI, 2025; European Commission, 2026).

**Current situation.** MPOB attributes the 2025 gains to better labour supply and a higher share of ripe bunches reaching mills (MPOB, 2026). Field decisions remain manual, however:
- ripeness is judged by eye on fixed harvesting rounds (Ma, n.d.);
- *Ganoderma* is found by visual census (Khoo and Chong, 2023);
- fertiliser follows blanket schedules (Chong, 2026).

MSPO records are compiled as separate paperwork. MSPO data also lack the plot polygons and plot-level traceability that the EUDR requires (MSPO and EFI, 2025). The sector is therefore high-performing but fragile. Its gains rest on scarce labour and on decisions that are not recorded where they are made.

## 1.2 Key Problems, Evidence and Prioritisation

The problems in the case brief were tested against published evidence. Each was then ranked on four criteria:
- scale of loss;
- urgency;
- how far today's remedy depends on scarce labour;
- *cognitive addressability*, meaning whether the binding constraint is information and judgement (Table 1).

*Table 1: Problem prioritisation*

| Problem | Scale of loss | Urgency | Labour dependence of current remedy | Cognitive addressability | Rank |
|---|---|---|---|---|---|
| P1 Labour shortage & harvest losses | RM7.5–20 bn/yr (employer estimate); ≈RM2.2 bn per 0.5-pt OER | High: 30,000 workers short (2026) | Very high: grading by scarce harvesters | High | **1** |
| P2 *Ganoderma* BSR (+ ageing) | 43 % loss within 6 months; 860,610 ha at risk by 2040 | Medium–high: progressive, hidden | High: visual census | High for BSR; low for ageing | **2** |
| P3 MSPO compliance & fertiliser | Fertiliser ≈30 % of cost; market access | High: EUDR from Dec 2026 | Medium: clerical | High | **3** |

**P1 Labour shortage and harvest losses.**
- *Workforce.* About 80 % of plantation workers are foreign, and employers estimate the cost of shortages at RM7.5–20 billion a year (Ramendran, 2026).
- *The current shortfall.* In October 2026 the sector was 30,000 workers short, and replacing a worker takes about six months. Policy aims to cut foreign workers to 10 % of the workforce by 2030. In 2021 about RM1 billion of ripe fruit went unharvested (The Edge Malaysia, 2026).
- *Quality as well as volume.* Short of labour, estates cut more under-ripe bunches to avoid collecting loose fruit, which lowers the oil extraction rate (OER) (Ma, n.d.).
- *The cost of lost OER.* Mills processed about 103 Mt of fresh fruit bunches (FFB) in 2025 (20.28 Mt CPO ÷ 19.74 % OER). Each 0.5-point loss of OER is therefore about 0.51 Mt of CPO, or RM2.2 billion at the 2025 average price of RM4,292.50/t (authors' calculation from MPOB, 2026).

The shortage eased in 2024–25 and is now returning (The Edge Malaysia, 2026). The need is therefore structural resilience, not crisis response.

**P2 Declining stand productivity: *Ganoderma* (primary) and ageing.**
- *Scale.* Basal stem rot (BSR) can cut a plantation's economic return by 43 % within six months. Modelling suggests it could destroy 860,610 ha of Malaysian mature palms by 2040 (Khoo and Chong, 2023).
- *Detection.* Palms show no symptoms until infection is about 60–70 % advanced, and laboratory tests are too slow and costly to apply to every palm (Khoo and Chong, 2023).
- *Ageing.* Ageing stands also depress yield, but the constraint there is replanting capital. Blocks that miss the replanting window stay unsuited to mechanisation for decades (The Edge Malaysia, 2025).

BSR is therefore the cognitively addressable part of P2.

**P3 MSPO compliance and fertiliser efficiency.**
- *MSPO.* Certification is mandatory and covers 87 % of planted area. The MS 2530:2022 standard adds a deforestation cut-off of 31 December 2019 and tighter traceability (MSPO and EFI, 2025).
- *Records required.* The standard requires records for fertilising and soil fertility (criterion 4.1.3), FFB traceability (4.2.2), and GHG reporting that includes nitrous oxide from fertiliser (4.5.4) (MPOCC, 2023).
- *Fertiliser.* Fertiliser is about 30 % of production cost, and a 40 % cut can reduce yields by at least 20 % (Chong, 2026).
- *EUDR.* The EUDR applies to large operators from 30 December 2026 (European Commission, 2026). However, the EU takes only 6.8 % of Malaysian palm oil exports (MPOB, 2026), so MSPO is the driver that applies to every producer.

**Interaction.** *Ganoderma* census and compliance paperwork draw on the same scarce field and supervisory labour as harvesting (Khoo and Chong, 2023; The Edge Malaysia, 2026). P1 is therefore the root priority, and one integrated system is preferable to three separate tools.

## 1.3 Cognitive Computing Capabilities for Each Problem

Each problem is matched to the capability that removes its binding constraint (Table 2).

**P1: computer-vision pattern recognition with scheduling.**
- *Capability.* Deep-learning detectors classify bunch ripeness from drone and ground images. A YOLO11 model trained on 11,613 drone images reached 98.3 % mAP at about 7.7 ms per frame and logged results for each tree (Che Hassan et al., 2026).
- *From grades to a plan.* Counts of ripe bunches per block feed a harvest-window forecast and an optimiser that assigns the available crew.
- *Why conventional methods fall short.* Human grading cannot scale this way. It needs the workers who are missing, varies between graders (which feeds estate–mill disputes over oil content), and sees nothing between rounds (Ma, n.d.). An ERP or scheduling system cannot read images at all.
- *Explanation.* Each grade comes with a Grad-CAM heat-map and a confidence score.

**P2: multisource machine-learning anomaly detection with spatial reasoning.**
- *Capability.* A screening cascade fuses weak signals. Sentinel-2 NDVI time series flag blocks that are losing vigour. A drone-image detector flags suspect crowns. A rule then raises the risk of palms within the four-row root-contact zone (Khoo and Chong, 2023).
- *Why conventional methods fall short.* Visual census finds palms only once symptoms show. Learned spectral patterns can flag stress earlier, and satellite screening covers every palm.
- *Limits.* Published early-detection accuracy is only 64–84 % (Kwang et al., 2025), and spectral signals can confuse disease with nutrient deficiency (Khoo and Chong, 2023). SawitSense therefore ranks palms for laboratory confirmation; it does not diagnose them.

**P3: knowledge representation and reasoning with explainable machine learning.**
- *Capability.* A knowledge base encodes agronomic thresholds and the MS 2530:2022 criteria (MPOCC, 2023). A recommender reads soil-sensor data (moisture, pH, conductivity, temperature) and proposes fertilise, lime, irrigate or skip. The knowledge base constrains each proposal and explains it. Natural language processing (NLP) renders the explanations in Bahasa Malaysia and English.
- *Why conventional methods fall short.* A conventional dashboard can display a pH of 3.8. It cannot infer that the block needs lime before fertiliser, or record why.
- *Explanation.* Counterfactual explanations let agronomists challenge the model; for example, "had pH been 4.2 or higher, the advice would be to fertilise". The Azure Responsible AI dashboard provides these explanations for tabular models such as this one (Microsoft, 2025).
- *Audit evidence.* Each recommendation is stored with its data and the MSPO clause it supports, so compliance evidence becomes a by-product of normal work.

*Table 2: Conventional and cognitive approaches compared*

| Problem | Conventional method and its limit | Cognitive capability | Why it is better suited |
|---|---|---|---|
| P1 | Visual grading on fixed rounds: needs scarce harvesters, inconsistent, blind between rounds | Computer vision + harvest-window forecasting + crew optimisation | Grades every visible bunch consistently without extra labour and produces a harvest plan |
| P2 | Visual census + laboratory tests: finds BSR only at 60–70 % infection | Multisource anomaly detection + spatial reasoning | Screens all palms continuously and sends experts to the highest-risk palms first |
| P3 | Blanket schedules + paper records: blind between samples | Knowledge-based reasoning + explainable ML + NLP | Site-specific, explained advice; MSPO evidence produced automatically |

In all three problems the constraint is the same. Judgement over unstructured, fast-changing evidence must be applied at a scale the workforce cannot supply. Conventional systems store such data; cognitive systems perceive it, reason over it and explain their conclusions.

---

# Part 2 — Technology Evaluation & Solution Proposal

*[In progress.]*

---

# Part 3 — Creative Thinking & Innovation

*[In progress.]*

---

## Conclusion

*[In progress.]*

---

## References

Che Hassan, C.A.Z., Muhammad Razif, M.R., Mohd, M.N., Abd Halim, A., Mohd Mustapha, N.H. and Azman, M.N. (2026) 'Real-time oil palm fresh fruit bunch drone image classification using YOLO11 architecture', *Journal of Oil Palm Research* (article in press, published online 17 August). doi:10.21894/jopr.2026.0033 (Accessed: 23 November 2026).

Chong, R. (2026) 'Lower palm oil yields loom as Sabah growers cut fertiliser', *The Star*, 20 August. Available at: https://www.thestar.com.my/news/nation/2026/08/20/lower-palm-oil-yields-loom-as-sabah-growers-cut-fertiliser (Accessed: 23 November 2026).

European Commission (2026) *Regulation on deforestation-free products* (Regulation (EU) 2023/1115). Available at: https://environment.ec.europa.eu/topics/forests/deforestation/regulation-deforestation-free-products_en (Accessed: 23 November 2026).

IOI Corporation Berhad (2026) *IOI accelerates digital transformation across our plantations with estate-wide high-speed connectivity* [Media release], 15 January. Available at: https://www.ioigroup.com/media-releases/ioi-accelerates-digital-transformation-across-our-plantations-with-estate-wide-high-speed-connectivity (Accessed: 23 November 2026).

Khoo, Y.W. and Chong, K.P. (2023) '*Ganoderma boninense*: general characteristics of pathogenicity and methods of control', *Frontiers in Plant Science*, 14, 1156869. doi:10.3389/fpls.2023.1156869 (Accessed: 23 November 2026).

Kwang, C.S., Razak, S.F.A., Yogarayan, S., Bin Muhammad, A.M.M., Ling, C.A., Bakar, S.A. and Abidin, H. (2025) 'Ganoderma detection in oil palm plantations using UAV hyperspectral imaging and AI', *TENCON 2025 – IEEE Region 10 Conference*, Kota Kinabalu, 27–30 October. Available at: https://shdl.mmu.edu.my/15767/ (Accessed: 23 November 2026).

Ma, A.N. (n.d.) 'Challenges facing the palm oil industry', *Palm Oil Engineering Bulletin*, No. 94, pp. 19–22. Bangi: MPOB. Available at: https://palmoilis.mpob.gov.my/publications/POEB/poeb94-ma2.pdf (Accessed: 23 November 2026).

Malaysian Palm Oil Board (MPOB) (2026) *Overview of the Malaysian Oil Palm Industry in 2025*. Bangi: MPOB. Available at: https://bepi.mpob.gov.my/images/overview/Overview2025.pdf (Accessed: 23 November 2026).

Malaysian Palm Oil Certification Council (MPOCC) (2023) *Guidance document for MS2530-3-1:2022 General principles for oil palm plantations (40.46 hectares to 500 hectares)*, Version 1.0, May. Available at: https://mspo.org.my/wp-content/uploads/2025/08/Guidance-document-for-MSPO-Part-3-1.pdf (Accessed: 23 November 2026).

Malaysian Sustainable Palm Oil (MSPO) and European Forest Institute (EFI) (2025) *Joint gap assessment of the EUDR information needs and information availability from the Malaysian Sustainable Palm Oil (MSPO) certification*. Available at: https://www.forest-trends.org/wp-content/uploads/2022/01/2025-MSPO_EUDR-Joint_Gap_Assessment.pdf (Accessed: 23 November 2026).

Microsoft (2025) *Assess AI systems and make data-driven decisions with Azure Machine Learning Responsible AI dashboard*. Microsoft Learn. Available at: https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai-dashboard (Accessed: 23 November 2026).

New Straits Times (2019) 'Felda seeking investors for hitech agriculture and cash cropping', 25 February; republished by MPOB Palm News. Available at: https://prestasisawit.mpob.gov.my/en/palmnews/news/27078 (Accessed: 23 November 2026).

Ramendran, C. (2026) 'Plantation sector hit hard by labour shortage', *The Star*, 1 March. Available at: https://www.thestar.com.my/news/nation/2026/03/01/plantation-sector-hit-hard-by-labour-shortage (Accessed: 23 November 2026).

The Edge Malaysia (2025) 'Cover Story: Positioning SD Guthrie for next stage of growth', *The Edge Malaysia Weekly*, 15–21 December. Available at: https://theedgemalaysia.com/node/786139 (Accessed: 23 November 2026).

The Edge Malaysia (2026) 'Cover Story 1: Can Malaysian planters avert another migrant worker crunch?', *The Edge Malaysia Weekly*, 9–15 November. Available at: https://theedgemalaysia.com/node/825330 (Accessed: 23 November 2026).

The Edge Malaysia (n.d.) 'Felda's road ahead in the spotlight', *The Edge Malaysia*, 6 October (year not stated in text; displayed 2026). Available at: https://theedgemalaysia.com/node/820636 (Accessed: 23 November 2026).

---

## Appendix A — Progress Report

Group: [GroupNo] · Lecturer: [Lecturer name]

*Table A1: Project timeline*

| Date (2026) | Milestone | Owner |
|---|---|---|
| 23 Nov | Case selected; problems validated with evidence; sources compiled | [Member 1 – Leader], [Member 2] |
| 23–26 Nov | Problem prioritisation and cognitive-capability analysis (Part 1) | [Member 2] |
| 26 Nov – 3 Dec | Solution design, architecture and AI models (Part 2.1–2.2) | [Member 3] |
| 3–6 Dec | Platform evaluation, integration plan and risks (Part 2.3–2.5) | [Member 4] |
| 6–10 Dec | Novelty and extension (Part 3); report drafting | [Member 5] |
| 10–12 Dec | Compliance review against rubric; revisions | [Member 1 – Leader] |
| 14 Dec | Final report submitted; presentation rehearsal | All |

*Table A2: Member contributions*

| Member | Student ID | Role | Main contribution |
|---|---|---|---|
| [Member 1 – Leader] | [ID] | Project lead | [Contribution] |
| [Member 2] | [ID] | [Role] | [Contribution] |
| [Member 3] | [ID] | [Role] | [Contribution] |
| [Member 4] | [ID] | [Role] | [Contribution] |
| [Member 5] | [ID] | [Role] | [Contribution] |
