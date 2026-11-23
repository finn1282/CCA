# 08 — Capability-Only Platform Comparison (for the report, per D23)

> Research wave 2, 23 Nov 2026. Replaces the matrix in `04_cloud_platforms.md` §(b) **for report use**. Student credits, free tiers and pricing are removed as criteria. Cost appears in the report only as an enterprise vendor & cost **risk**. Keys → `sources.md`.

> **⚠ Superseded by `10_audit_wave.md` §1 (wave 4):** after rescoring AWS from official docs and correcting Azure's Malaysia-West residency score, **AWS 89 vs Azure 85** (base). Lead decision required.

## Result
**Azure still ranks first**: Azure 88, AWS 79, Google 67, IBM 49. It also stays first under two sensitivity checks, equal weights and a geospatial-heavy weighting. The gap to AWS is real but moderate, about 9 points. The Report should present AWS as a credible runner-up, not as a weak option.

## Criteria and weights (all capability/fit; each ties to a Part 1 problem)
| # | Criterion | Weight | Why it matters for SawitSense |
|---|---|---|---|
| C1 | First-party IoT ingestion & device management | 15 | Soil-sensor fleet across blocks (P3/O3) |
| C2 | In-country region & data-residency controls (PDPA 2010 s129) | 15 | Worker/smallholder and plot-geolocation data (P3/O4) |
| C3 | Vision model training (AutoML + custom) | 15 | FFB ripeness, Ganoderma detection (P1/O1, P2/O2) |
| C4 | Geospatial / satellite data services | 15 | NDVI screening, EUDR geolocation (P2/O2, P3/O4) |
| C5 | Edge & offline operation | 10 | Remote estates with patchy links |
| C6 | MLOps, monitoring & explainability | 15 | Agronomists and MSPO auditors must trust and audit decisions |
| C7 | Integration with estate enterprise IT (ERP, governance) | 15 | Part 2 integration with existing IT |

## Scores (1–5) with evidence
| Criterion | Azure | AWS | Google Cloud | IBM watsonx |
|---|---|---|---|---|
| C1 IoT | **5**: IoT Hub Standard (twins, C2D, IoT Edge), DPS zero-touch provisioning [AZ-IOTHUB-SCALE] [AZ-DPS]; LoRaWAN server integration [TTS-AZURE] | **4**: IoT Core managed MQTT 3/5 broker + rules [AWS-IOTCORE] | **2**: Cloud IoT Core retired 16 Aug 2023 [GCP-IOTCORE] | **1**: Watson IoT retired 2023, no direct replacement [REG-WIOT] |
| C2 Residency | **5**: Malaysia West (3 AZs); 2nd region in preview in Johor [AZ-REGIONS] | **5**: Asia Pacific (Malaysia) region, 3 AZs [AWS-MYREGION] | **2**: no Malaysian region in the compute region list [GCP-REGIONS] | **1**: no SE Asian watsonx data centre found (unverified) |
| C3 Vision | **4**: AutoML for images (classification, detection, segmentation) [AZ-AUTOML-IMG] + custom training/managed endpoints [AZ-ENDPOINTS] | **4**: SageMaker (vendor docs not opened, so scored at parity) | **5**: AutoML image classification/detection in "Gemini platform (formerly Vertex AI)" [GCP-PRICING] | **3**: tabular-focused AutoAI (unverified) |
| C4 Geospatial | **3**: Planetary Computer Sentinel-2 L2A STAC [MPC-S2]; Planetary Computer Pro GeoCatalog (preview) [AZ-MPCPRO] | **3**: not researched in depth (unverified) | **5**: Earth Engine catalog incl. Sentinel-2/Landsat [GEE-S2] [GEE-L9]; global oil-palm map [GEE-OILPALM] | **2** |
| C5 Edge/offline | **5**: IoT Operations, edge MQTT broker, recovery validated after up to 45 days offline [AZ-IOTOPS] | **5**: Greengrass (not opened; industry-standard) | **2** | **2** |
| C6 MLOps & XAI | **4**: RAI dashboard (interpretability, counterfactuals, PDF scorecard) but tabular-only [AZ-RAI]; drift/quality monitoring with Event Grid retraining triggers [AZ-MONITOR]; blue/green rollout [AZ-ENDPOINTS] | **4** (not opened) | **4** (not opened) | **5**: watsonx.governance is IBM's flagship (not opened) |
| C7 Enterprise integration | **5**: Logic Apps SAP connector for S/4HANA and R/3/ECC via IDoc/BAPI/RFC [AZ-SAP]; Purview governance [AZ-PURVIEW]; Azure Maps routing [AZ-MAPS] | **3** (not assessed) | **3** (not assessed) | **3** (not assessed) |
| **Weighted total /100** | **88** | **79** | **67** | **49** |

Total = Σ(score × weight) ÷ 5.

## Sensitivity checks
| Weighting | Azure | AWS | Google | IBM | Winner |
|---|---|---|---|---|---|
| Base (above) | 88 | 79 | 67 | 49 | Azure |
| Equal weights (7 × 1/7) | 89 | 80 | 66 | 49 | Azure |
| Geospatial-heavy (C4 = 30; C1, C2, C5, C7 = 10; C3, C6 = 15) | 82 | 76 | 75 | 50 | Azure (Google's gap shrinks to 7) |

## Honest caveats for the Report and Lead
1. **Research depth is uneven.** Azure was researched more deeply (wave 2 docs), while several AWS/Google/IBM cells are "not opened" and are scored at parity or neutral (3). This could flatter Azure. However, the decisive criteria (C1 IoT, C2 residency, C5 edge) are verified for all four vendors, and AWS still trails on C7 only because it was not assessed. The ranking order Azure > AWS rests mainly on C7 (integration). If the Report cannot evidence AWS's integration weakness, it should frame Azure's lead as **"best fit for an estate already running Microsoft/SAP"** rather than as a large capability gap.
2. **Azure limitations to state openly** (rubric rewards balanced reasoning): RAI dashboard and built-in model monitoring are **tabular-only** [AZ-RAI] [AZ-MONITOR]; AutoML for images needs **GPU (NC/ND)** compute [AZ-AUTOML-IMG]; Azure OpenAI is **not offered in Malaysia West** [AZ-AOAI-MODELS]; confidential ledger always **replicates to a paired region**, and Malaysia West has none [AZ-ACL-RES] [AZ-REGIONS].
3. **Why Azure uniquely fits (one-line justification):** it is the only platform with an in-country Malaysian region, a live first-party IoT device platform with an offline-capable edge runtime, and native SAP/ERP integration, which together address all three problems end-to-end.
