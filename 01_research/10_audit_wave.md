# 10 — Audit Wave (C-01/C-02, C-03, C-16, C-18)

> Research wave 4, 23 Nov 2026, driven by `07_verification/compliance/REPORT_AUDIT_1.md`. No large downloads were made (D43). Keys refer to `sources.md`.

## 1. C-01/C-02 — AWS rescored from official docs

### 1a. What the AWS docs say (verified 23 Nov 2026)
| Area | AWS evidence | Key |
|---|---|---|
| IoT ingestion & provisioning | Fleet provisioning: AWS IoT generates and delivers device certificates on first connect. Two modes: **by claim** (shared claim certificate swapped for a unique one) and **by trusted user**. Pre-provisioning hooks are also supported. IoT Core is a managed MQTT 3/5 broker with a rules engine. | [AWS-FLEETPROV] [AWS-IOTCORE] |
| Edge | Greengrass v2 is an open-source edge runtime. Devices "act locally on the data", run ML predictions, filter/aggregate data and "react autonomously to local events". The opened page gives **no validated maximum offline duration**. | [AWS-GG] |
| Vision | **Rekognition Custom Labels** trains custom classifiers/detectors from "a few hundred images or less"; its own example is distinguishing healthy and infected plants. SageMaker AI supports custom training. | [AWS-RCL] [AWS-SMTRAIN] |
| Explainability | **SageMaker Clarify** gives SHAP feature attributions and partial-dependence plots, and **explains computer-vision models (image classification and object detection)** and NLP models with the same SHAP method. The opened page shows no counterfactual feature. | [AWS-CLARIFY] |
| SAP integration | **AppFlow SAP OData connector** works through OData V2/V4 on SAP Gateway. It needs **NetWeaver 7.40 SP02+**, and ODP is not supported as a destination. **AWS SDK for SAP ABAP** lets ABAP code (BADIs, reports, OData services) call AWS services on NetWeaver 7.4+ or BTP. | [AWS-APPFLOW-SAP] [AWS-SDK-ABAP] |
| Malaysia region service list | AWS regional services table, source version 2025-11-13. **ap-southeast-5 (Malaysia)** lists AWS IoT Core, IoT Device Management, IoT Device Defender, **IoT Greengrass**, **SageMaker AI**, **Rekognition**, Kinesis Data Streams and Lambda. **AppFlow is not listed.** | [AWS-REGTABLE] |

### 1b. New finding on the Azure side (C2 also needs correcting)
The **Azure Retail Prices API** for `malaysiawest` (checked 23 Nov 2026) shows **no price entries for IoT Hub, Azure Machine Learning, Azure Maps or confidential ledger**. Southeast Asia (Singapore) does have IoT Hub and Azure ML entries. Malaysia West does list **Event Grid (which includes an MQTT broker), Event Hubs, Functions, App Service, Storage, Data Explorer, Fabric, Logic Apps, AKS and Foundry Models** [AZ-PRICES-API].

This is an **indicative** check, not an official availability statement. It still means the claim "Azure = in-country region + IoT Hub" is **probably not true for IoT Hub and Azure ML today**. AWS, by contrast, lists IoT Core, Greengrass and SageMaker in its Malaysian region.

### 1c. Rescoring (1–5)
| Criterion (weight) | Azure (08 → now) | AWS (08 → now) | Reason for change |
|---|---|---|---|
| C1 IoT (15) | 5 → 5 | 4 → **5** | Fleet provisioning matches DPS zero-touch provisioning [AWS-FLEETPROV] [AZ-DPS] |
| C2 Residency (15) | 5 → **4** | 5 → 5 | Azure IoT Hub/AML absent from Malaysia West pricing (indicative) [AZ-PRICES-API]; AWS lists IoT Core, Greengrass, SageMaker in ap-southeast-5 [AWS-REGTABLE] |
| C3 Vision (15) | 4 → 4 | 4 → **5** | Rekognition Custom Labels works from a few hundred images, plus SageMaker custom training [AWS-RCL] [AWS-SMTRAIN]; Azure AutoML images needs GPU NC/ND [AZ-AUTOML-IMG] |
| C4 Geospatial (15) | 3 → 3 | 3 → 3 | Unchanged (AWS geospatial not researched) |
| C5 Edge/offline (10) | 5 → 5 | 5 → **4** | Greengrass acts locally, but no validated offline duration found [AWS-GG]; IoT Operations validated recovery after up to 45 days offline [AZ-IOTOPS] |
| C6 MLOps & XAI (15) | 4 → 4 | 4 → **5** | Clarify explains **image** classifiers and detectors [AWS-CLARIFY]; Azure RAI dashboard is tabular-only [AZ-RAI] |
| C7 Enterprise integration (15) | 5 → 5 | 3 → **4** | AppFlow OData + SDK for SAP ABAP are real [AWS-APPFLOW-SAP] [AWS-SDK-ABAP]; Logic Apps adds IDoc/BAPI/RFC incl. ECC [AZ-SAP] |

### 1d. Recomputed totals (/100)
| Weighting | Azure (C2 = 5, as in 08) | Azure (C2 = 4, corrected) | AWS (rescored) | Google | IBM |
|---|---|---|---|---|---|
| Base (C1, C2, C3, C4, C6, C7 = 15; C5 = 10) | 88 | **85** | **89** | 67 | 49 |
| Equal weights | 89 | 86 | **89** | 66 | 49 |
| Geospatial-heavy (C4 = 30; C1, C2, C5, C7 = 10; C3, C6 = 15) | 82 | 80 | **84** | 75 | 50 |

### 1e. Plain answer: **Azure no longer ranks first on capability scores. AWS does.**
- With AWS rescored from its own docs, AWS edges Azure even before the Azure correction (89 vs 88 base). After correcting Azure C2, AWS leads under every weighting: **+4 base, +3 equal, +4 geo-heavy**.
- The margin is small (3–4 points), within the subjectivity of 1–5 scoring. Both are credible, and Google and IBM remain clearly behind.

**Verified differentiators (each with a source on both sides)**
| Where Azure is better | Azure evidence | AWS evidence |
|---|---|---|
| Validated long offline operation at the edge | IoT Operations recovery validated after **up to 45 days offline** [AZ-IOTOPS] | Greengrass "acts locally"; no validated duration on the opened page [AWS-GG] |
| Native SAP ECC/S/4HANA integration (IDoc, BAPI, RFC) | Logic Apps SAP connector: **IDoc, BAPI, RFC/tRFC; ECC and S/4HANA** [AZ-SAP] | AppFlow uses **OData only** (NetWeaver 7.40 SP02+), and AppFlow is **not in the AWS Malaysia service list**; SDK for SAP ABAP needs ABAP development inside SAP [AWS-APPFLOW-SAP] [AWS-REGTABLE] [AWS-SDK-ABAP] |
| Counterfactual ("what would change the decision") explanations + compliance PDF scorecard | RAI dashboard: DiCE counterfactuals, PDF scorecard (tabular) [AZ-RAI] | Clarify: SHAP + PDP; no counterfactuals on the opened page [AWS-CLARIFY] |

| Where AWS is better | AWS evidence | Azure evidence |
|---|---|---|
| In-country hosting of IoT + edge + ML services | IoT Core, Greengrass, SageMaker, Rekognition in ap-southeast-5 [AWS-REGTABLE] | IoT Hub, Azure ML absent from Malaysia West pricing (indicative) [AZ-PRICES-API] |
| Explainability for the **image** models (ripeness, Ganoderma) | Clarify explains image classification and object detection [AWS-CLARIFY] | RAI dashboard tabular-only; images need the open-source toolbox [AZ-RAI] |
| Low-data vision training | Custom Labels: few hundred images [AWS-RCL] | AutoML images needs GPU NC/ND compute [AZ-AUTOML-IMG] |

**Options for the Lead (decision needed; this contradicts D15):**
1. **Switch the recommendation to AWS.** This best follows the evidence and the rubric's demand for rigour. Software's report-facing architecture would need re-mapping: IoT Core, Greengrass, SageMaker, Clarify, Rekognition. The build can stay on Azure for Students as an internal workaround (D20 already separates build from report).
2. **Keep Azure, but re-justify it as a conditional fit:** "for an estate whose ERP is SAP ECC/S/4HANA and whose remote estates need weeks of offline operation". This is defensible only if C-03 shows the target companies run SAP (see §2). The report must then show the AWS-leading matrix honestly and argue the deciding criteria explicitly. Raising weights just to make Azure win would be visible to markers.
3. **Present a weighted tie with a decision rule.** Not recommended, because the rubric asks for a single recommendation.

Research's view: **Option 2 is viable if §2's SAP evidence is accepted. Otherwise use Option 1.** Either way, the report must drop the claim that Azure hosts IoT Hub and ML in Malaysia West, unless Microsoft's official products-by-region page confirms it.

## 2. C-03: Which ERP do the case companies run?
| Company | Evidence | Strength | Key |
|---|---|---|---|
| **IOI Corporation** | Rolled out **SAP S/4HANA** to its corporate office, mills, refinery **and estates** (implementation partners HCL Technologies and Wilmar Consultancy Services). Fiori front end; SAP Cloud Platform links satellite apps to S/4HANA. | **Strong**: IOI's own news page republishing NST (29 Jul 2020), also on MPOB Palm News | [IOI-S4HANA2020] |
| **SD Guthrie** (ex-Sime Darby Plantation) | A BSI RSPO certification audit report (2023) states estate hectarage "taken from SEMUA Field – Master listing in **SAP System**". The same report verifies RSPO metrics against the "**SAP accounting system**". The SAP product/version is not stated. | **Medium–strong**: independent certification-body audit document | [BSI-SDG-RSPO2023] |
| SD Guthrie (version) | A vendor-tracking database lists "SAP ERP ECC 6.0 for ERP Financial". | **Weak**: lead-generation site, unsourced. Do not cite in the report. | — |
| **FELDA / FGV** | FGV Prodata Systems, an FGV Holdings subsidiary that grew out of FELDA's IT unit, is an **SAP Silver partner** offering "ERP – SAP solutions". The profile does **not** say FGV itself runs SAP. | **Indirect only** | [SAP-FGVPRODATA] |

**Conclusion:** at least **two of the three named producers (IOI, SD Guthrie) run SAP**. The report can say: "major Malaysian planters such as IOI (SAP S/4HANA across estates and mills) and SD Guthrie (SAP-based estate master data and accounting) run SAP ERP". FGV is unconfirmed; the report should not claim it. This supports **Option 2** in §1e (Azure Logic Apps SAP connector with IDoc/BAPI/RFC as a deciding integration criterion). Note that IOI is on S/4HANA, which AWS can also reach via OData (AppFlow) or the SDK for SAP ABAP. Azure's advantage is breadth (IDoc/BAPI/RFC) and in-region availability, not exclusivity.

Naming note: MPOB has a mill-grading system called **SawitSCAN** (June 2026) [MPOB-TT698]. "SawitSense" does not clash with it, but the report could mention SawitSCAN as related work.

## 3. C-16: Which MSPO part applies to large estates?
- **MS 2530-3-1:2022 is the wrong part for large estates.** It covers plantations of **40.46–500 ha** [MPOCC-P31]. Large estates (FELDA/FGV, SD Guthrie, IOI) fall under **MS 2530-3-2:2022, "General Principles for Oil Palm Plantations (more than 500 hectares)"** [MPOCC-P32]. Mills, including supply-chain/traceability obligations, fall under **MS 2530-4-1:2022** [MPOCC-P41]. Independent smallholders use Part 2-1 [MPOCC-P21].
- **The clause numbers hold in Part 3-2** (checked in the guidance text) [MPOCC-P32]:
  - **4.1.3** Existing site management (4.1.3.1: SOPs, with records of implementation maintained)
  - **4.1.4** Replanting (a useful link to P2 ageing trees)
  - **4.2.2** Traceability
  - **4.5.4** GHG emissions (4.5.4.1–4.5.4.3: MSPO GHG Calculator, Jan–Dec reporting)
  - **4.5.5** Water resources
- **Part 4-1 (mills)** also uses **4.2.2 Traceability** and **4.5.4 GHG** [MPOCC-P41].
- Caveat: the explicit SOP list naming "**Fertilising**" and "managing soil fertility" appears in the Part 2-1 guidance [MPOCC-P21]. The Part 3-x guidance states the SOP requirement generically (4.1.3.1). The report should cite fertiliser SOPs as "4.1.3 site-management SOPs (e.g. fertilising, per MPOCC guidance)".
- **Report fix:** replace "MS 2530-3-1" with "**MS 2530-3-2:2022** (estates >500 ha) and **MS 2530-4-1:2022** (mills)". Clause numbers are unchanged.
- Context: SD Guthrie estates (Bukit Benut) were audited against the earlier 2013 parts MS 2530-3:2013 (plantations) and MS 2530-4:2013 (mills) in visits 2022–2024 (final report Oct 2024) [BSI-SDG-MSPO2024]. This confirms the Part 3/Part 4 split for large companies.

## 4. C-18: Recent (2023+) sources on current estate practice
| Practice | Evidence (2023 or later) | Key |
|---|---|---|
| **Manual ripeness grading** | MPOB (June 2026): FFB grading at mills "is still largely performed manually by human workers". Only **50–100 bunches are sampled per 5–20 t consignment (0.1–0.4 % of the load)**, which causes grading disputes. MPOB is developing SawitSCAN (imaging + AI) as the alternative. | [MPOB-TT698] |
| | JOPR review (2023): grading "is commonly conducted using visual inspection by trained workers" using colour and loose-fruit count. It is labour-intensive, and misclassification comes from tree height, miscounted loose fruit, poor visibility and lighting. | [MANSOUR2023] |
| | JOPR (2026): conventional FFB monitoring "relies heavily on manual inspection, which is labour-intensive" | [HASSAN2026] |
| **Visual Ganoderma census** | Review (2023): palms are asymptomatic early, and symptoms are noticed visually on foliage only when infection is ~60–70 % developed. Lab diagnostics (PCR/ELISA/GSM) are costly or slow for large-scale use. | [KHOO2023] |
| | Smartphone study (2025, Malaysia and Thailand): most model errors were between early-infected and healthy palms, the same distinction human visual census struggles with. | [DARANAGAMA2025] |
| | (Older but official method) MPOB national surveillance identified BSR by **visual symptoms**, confirmed with selective media. | [IBRAHIM2020] |
| **Uniform fertiliser rates** | Sabah growers (Aug 2026) apply a fixed **kg per palm** (e.g. cut from ~12 kg to ~9 kg per palm) and cut rates across the board when prices rise. Planters call for "nutrient-use efficiency, precision agriculture". | [STAR-FERT2026] |
| | Thesis (2024): yield gaps "often stem from inadequate nutrient management practices and limited agronomic knowledge"; it proposes a site-specific decision-support tool | [FARRASATI2024] |

Gap: no 2023+ source quantifies how common blanket schedules are on large estates. The report should phrase this as "uniform per-palm rates adjusted by price/age" with [STAR-FERT2026], not as "all estates use blanket schedules".
