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
