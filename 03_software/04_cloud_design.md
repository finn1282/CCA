# 04 — Cloud Design on Microsoft Azure, Integration, Roadmap and Risks

> Report-facing (Part 2: technologies 3 marks, platform 5, integration + phased plan 3, risks 2).
> - Platform per D15. Capability-only reasoning per D23: cost appears only as a vendor & cost **risk** (§7).
> - Residency, explainability, DPS and AutoML scope per D32.
> - The demonstration build and its mapping to these services are internal (`07_actual_build_vs_target.md`, D20).
> - Keys refer to `01_research/sources.md`.

## 1. Why Azure (summary of the capability comparison)

The capability-only matrix is in `01_research/08_platform_comparison_capability.md`. Scores: Azure 88, AWS 79, Google Cloud 67, IBM watsonx 49. Azure also stays first under equal weights and under a geospatial-heavy weighting.

**Azure is the only one of the four that combines all three of:**
1. An **in-country Malaysian region**: Malaysia West with 3 availability zones, and a second region in preview in Johor (AZ-REGIONS).
2. A **live first-party IoT device platform with an offline-capable edge runtime**:
   - IoT Hub Standard with device twins and cloud-to-device messaging (AZ-IOTHUB-SCALE);
   - DPS for zero-touch provisioning (AZ-DPS);
   - IoT Operations, with recovery validated after up to 45 days offline (AZ-IOTOPS).
3. **Native ERP integration**: the Logic Apps SAP connector supports S/4HANA and ECC through IDoc, BAPI and RFC (AZ-SAP), with Purview governance alongside (AZ-PURVIEW).

Together these cover P1–P3 end to end.

**How the other platforms compare:**
- **Google Cloud** is the strongest in geospatial (Earth Engine) and vision AutoML. However, it has no Malaysian region (GCP-REGIONS) and retired IoT Core in 2023 (GCP-IOTCORE).
- **IBM** retired Watson IoT without a replacement (REG-WIOT).
- **AWS** is a credible runner-up, with a Malaysian region (AWS-MYREGION) and IoT Core (AWS-IOTCORE). It is the fallback named in the lock-in mitigation (§7).

**Azure limitations, stated openly:**
- The Responsible AI dashboard and built-in monitoring are tabular-only (AZ-RAI; AZ-MONITOR).
- AutoML for images needs GPU compute (AZ-AUTOML-IMG).
- Azure OpenAI is not offered in Malaysia West (AZ-AOAI-MODELS).
- Confidential ledger always replicates to a paired region, and Malaysia West has none (AZ-ACL-RES).

The design below works around each of these.

## 2. Services per architecture layer

| Layer (Fig. 4) | Azure service | Role in SawitSense | Capability that justifies it | Region (D32a) |
|---|---|---|---|---|
| 1 Sources → 2 | **Azure IoT Operations** on Arc-enabled Kubernetes (estate edge) | Edge MQTT broker; local rule engine during outages; data flows to Event Hubs/ADLS | Offline processing, 45-day recovery validated (AZ-IOTOPS) | Estate (on-premises) |
| 2 Ingestion | **IoT Hub Standard** | Per-device identity, telemetry, **device twins + cloud-to-device** (recommendation back to node), routing | Standard tier needed for twins/C2D; 400k msgs/day per S1 unit (AZ-IOTHUB-SCALE) | Malaysia West where offered, otherwise Southeast Asia |
| 2 | **Device Provisioning Service** | Zero-touch X.509 provisioning of the node fleet | Attestation, allocation policies (AZ-DPS) | **Southeast Asia, single-region data residency + private endpoint** (D32c) |
| 2 | **Event Hubs** | Streams from weather feeds, ERP change events, drone upload notifications | Kafka-compatible, millions of events/s (AZ-EVENTHUBS) | Malaysia West where offered, otherwise SEA |
| 2 | **Data Lake Storage Gen2** | Bronze/silver/gold lake: raw readings, images, orthomosaics, NDVI rasters, curated training sets | Hierarchical namespace, file-level ACLs (AZ-ADLS) | Malaysia West |
| 2 | **Planetary Computer STAC** (+ Planetary Computer Pro GeoCatalog when GA) | Sentinel-2 L2A search and ingest; estate geospatial catalogue | Global L2A archive, STAC standard (MPC-S2; AZ-MPCPRO) | Data source / Malaysia West copy |
| 3 Cognitive | **Azure Machine Learning** (workspace, pipelines, registry, data labelling) | Train M1/M3/M6; scheduled M5 pipeline; versioned models and data | Managed MLOps; MLflow models | Malaysia West where offered, otherwise SEA |
| 3 | **AutoML for images** (enterprise design only, D32d) | Benchmark/accelerate M1 and M3 against custom models | Classification, detection, segmentation with sweeps; needs NC/ND GPU (AZ-AUTOML-IMG) | As above |
| 3 | **Responsible AI dashboard** (M6 only) + **RAI Toolbox (open source)** for images | Interpretability, DiCE counterfactuals, error analysis, PDF scorecard (M6); Grad-CAM for M1/M3 | Dashboard is tabular/sklearn only (AZ-RAI) | — |
| 3 | **Azure OpenAI** | Multilingual rewording of structured explanations; audit-pack narrative | Model availability in Southeast Asia (AZ-AOAI-MODELS) | **Southeast Asia, non-personal prompts only** |
| 3 | **Azure Maps** | Block maps, satellite basemap, **matrix routing** for crew movement | Multipoint optimisation, matrix routing, geofencing (AZ-MAPS) | — |
| 4 Deployment | **Azure ML managed online endpoints** | Real-time M1/M3 inference | Blue/green split, traffic mirroring, autoscale, private network (AZ-ENDPOINTS) | Malaysia West where offered |
| 4 | **Azure Container Apps** (API, rule engine, M6, reasoners) + **Azure Functions** (event handlers) | SawitSense API and dashboard back-end | Serverless containers, scale-to-zero | Malaysia West |
| 4 | **Azure Cosmos DB** | Latest state per block/device; evidence records | Low-latency document store | Malaysia West |
| 4 | **Azure ML model monitoring** + **Azure Monitor** + **Event Grid** | Drift, data quality (M6); custom class-shift signal (M1/M3); retrain triggers | Built-in tabular signals + Event Grid alerts (AZ-MONITOR) | — |
| 5 Application | Static Web Apps / Container Apps (dashboard), **Power BI** (group reporting), mobile app (harvester) | User surfaces | — | Malaysia West |
| Cross-cutting | **Azure confidential ledger** | Anchor SHA-256 digests of evidence records → tamper-evidence for MSPO auditors | Append-only, tamper-evident (AZ-ACL); paired-region replication (AZ-ACL-RES) | **Southeast Asia, digests only** |
| Cross-cutting | **Microsoft Purview**, **Entra ID**, **Key Vault**, Private Link | Lineage, classification of personal data, RBAC, secrets, private networking | Unified governance & sensitive-data protection (AZ-PURVIEW) | Malaysia West |
| Integration | **Logic Apps** (SAP connector), **API Management** | ERP work orders, master data, MPOB/MSPO exports | IDoc/BAPI/RFC to S/4HANA & ECC (AZ-SAP) | Malaysia West |

## 3. Data residency & PDPA 2010 (constrains integration only)

The 2024 amendment replaced the old s129 "whitelist" with a test: the destination must have a substantially similar law or adequate protection, or a listed exception must apply. Guidelines from April 2025 require a Transfer Impact Assessment (valid for up to 3 years) and a record of every transfer. A DPO and breach notification have applied since June 2025 (MAYER-PDPA2025).

**Integration constraints that follow (D32a):**
1. **Personal data stays in Malaysia West.** This covers worker and smallholder identities, IC numbers and individually linked plot locations: ADLS, Cosmos DB and the ERP extracts. Purview classifies these fields.
2. **Services outside Malaysia receive only non-personal or hashed data:**
   - Azure OpenAI gets block IDs, readings and rule text.
   - The confidential ledger gets SHA-256 digests.
   - DPS uses the SEA single-region option with a private endpoint (AZ-DPS).
3. **Where Azure ML, IoT Hub or Event Hubs must run in Southeast Asia** because the service is not offered in Malaysia West, the transfer is covered by a TIA, a transfer record, and pseudonymised device and block IDs. Personal fields never enter training datasets.
4. **ML datasets contain no personal identifiers.** Harvester IDs in allocation plans are pseudonymised; the mapping to real identities stays in the ERP.

## 4. Enterprise cost drivers (context for the vendor & cost risk in §7)

Cost was **not** a selection criterion (D23). The table only shows which design choices drive enterprise spend, so that the risk in §7 can be managed.

| Driver | Why it grows | Design control |
|---|---|---|
| GPU training (AutoML for images, M1/M3 fine-tunes) | NC/ND compute required (AZ-AUTOML-IMG) | Scheduled retrains triggered by drift only; low-priority compute; custom transfer learning before AutoML sweeps |
| Online endpoints (always-on instances) | ≥3 instances recommended for HA (AZ-ENDPOINTS) | Autoscale on schedule (harvest hours); batch scoring for drone tiles |
| IoT message volume | Units are sized by messages per day (AZ-IOTHUB-SCALE) | Edge aggregation in IoT Operations (send changes and anomalies, not every sample) |
| Image/orthomosaic storage | Drone surveys are large | Lifecycle tiers in ADLS (hot → cool → archive) |
| Azure OpenAI calls | Per-request usage | Cache per rule ID and language; LLM only for user-facing text |

## 5. Integration with existing estate IT

| Existing system | Integration | Direction | Mechanism |
|---|---|---|---|
| **ERP (SAP S/4HANA or ECC)**: block master, planting dates, harvest tickets, fertiliser stock and work orders, HR rosters | Block master and planting dates seed the block reference (MSPO 4.1.3.4). Approved fertiliser/lime actions become **work orders**. Harvest tickets close the loop for yield KPIs | Both | Logic Apps SAP connector over IDoc/BAPI/RFC (AZ-SAP); API Management facade |
| **Mill weighbridge / grading** | FFB grades and tonnage per block, used for ripeness-model feedback and OER KPIs | In | Event Hubs / batch file to ADLS |
| **MSPO traceability & GHG reporting** | Evidence pack per block and period; N quantities → MSPO GHG Calculator input (4.5.4) | Out | Export from the evidence service (Markdown/PDF/CSV) |
| **MPOB e-submission** (monthly returns) | Production figures pre-filled from ERP + SawitSense KPIs | Out | Report export; manual submission retained |
| **Microsoft 365 / Power BI** | Management reporting, Teams alerts ("Block B2 flagged") | Out | Power BI dataset on gold layer; Logic Apps → Teams |
| **Existing drone vendor** | Orthomosaics uploaded to ADLS; detection results returned as GeoJSON | In/Out | SAS-scoped upload; STAC catalogue |
| **Estate network** (4G/LTE where available (IOI2026); LoRaWAN for sensors) | LoRaWAN network server → IoT Hub integration (TTS-AZURE) | In | Device twins, downlinks |

## 6. Phased implementation plan (Fig. 6 structure)

```mermaid
flowchart LR
  S["SHORT-TERM (0–6 months)<br/><b>Pilot / proof of concept</b><br/>1 estate, 2–3 blocks"] --> M["MEDIUM-TERM (6–18 months)<br/><b>Scale & integrate</b><br/>region of estates"] --> L["LONG-TERM (18–36 months)<br/><b>Optimise & extend</b><br/>group-wide + smallholders"]
```

| | Short-term: pilot | Medium-term: scale & integrate | Long-term: optimise & extend |
|---|---|---|---|
| **Scope** | One estate (e.g. Johor), 2–3 blocks incl. one with known BSR history | All estates in one region; drone programme quarterly | Whole group; smallholder cooperatives (MSPO Part 2) |
| **Data** | Install soil nodes; monthly Sentinel-2 pipeline; one drone survey; collect graded bunch images | LoRaWAN + IoT Operations edge per estate; weather and mill feeds; M6 rule-based baseline replaced by estate-trained data | Multispectral drone data; leaf-nutrient lab results; yield history → **yield forecasting model** |
| **Models** | M1, M5, M6 (rules + tree), M7; M3 as screening trial | Retrain M1/M3 on estate data (AutoML benchmark); M2 learns time-to-ripe from logged grades; drift monitoring live | Satellite nutrient mapping (KOK2021); multispectral BSR detection; LLM audit narrative in 4 languages |
| **Integration** | Read-only ERP block master; evidence pack exported manually | **SAP work orders** from approved actions; Power BI; Teams alerts; confidential-ledger anchoring | MSPO GHG Calculator export; EUDR geolocation package; partner APIs for cooperatives |
| **People** | Train 1 manager, 2 mandores, 1 agronomist; human approval required for every action | Review queue only for low confidence or disagreement; champions per estate | Extension officers; multilingual harvester app |
| **Success measures (baseline first)** | Baseline: round length, under-ripe share at mill, fertiliser kg/ha, BSR found per survey hour. Target: agronomist agreement ≥ 80 %; audit pack accepted by internal MSPO auditor | Round length back within 10–15 days (AHMAD2020; MPOB-NEWS2020); fewer over-ripe bunches; fertiliser rounds skipped where EC is high | Measurable OER gain; BSR found earlier per hectare surveyed; MSPO audits with zero record findings |

## 7. Integration & implementation risks (prioritised)

Each risk is scored likelihood × impact (1–3); the highest are listed first.

| # | Risk (Fig. 6 category) | L×I | Concrete mitigation | Owner |
|---|---|---|---|---|
| 1 | **Technical: model accuracy and data gaps.** Early BSR detection is moderate even in research (64–84 %) (AHMADI2023; KWANG2025); no public soil-sensor or harvest-timing data; Indonesia → Malaysia domain shift in M1 | 3×3 | Position M3 as **screening, not diagnosis**, with ground confirmation for every positive. Report cross-country accuracy honestly and fine-tune on estate images in the pilot. Rules stay authoritative for M6, and human review is required until agreement ≥ 80 %. Overrides feed retraining | Data science lead |
| 2 | **Operational: user adoption and trust.** A largely foreign field workforce (STAR-LAB2026) with mixed literacy; supervisors distrust black boxes | 3×2 | Counterfactual, plain-language explanations in BM, English, Bahasa Indonesia and Nepali. One-tap approve/override. Mandore champions. Paper fallback during the pilot. Measure agreement weekly | Estate manager |
| 3 | **Technical: legacy ERP compatibility.** Customised SAP ECC, inconsistent block codes | 2×3 | Integrate through the Logic Apps SAP connector (IDoc/BAPI) behind API Management (AZ-SAP). Block-master clean-up in phase 1. Read-only first, write-back in phase 2 | IT lead |
| 4 | **Technical: connectivity at remote blocks** | 2×3 | IoT Operations edge with local rules and buffering (AZ-IOTOPS). LoRaWAN planned with plantation-specific canopy loss of 5–9 dB (ANZUM2022). Store-and-forward with capture timestamps | IoT engineer |
| 5 | **Vendor & cost: lock-in** | 2×2 | Open formats: ONNX models, STAC catalogues, Kafka protocol on Event Hubs, MLflow. Containerised API. AWS identified as fallback (Malaysian region + IoT Core) (AWS-MYREGION; AWS-IOTCORE) | Architecture board |
| 6 | **Vendor & cost: enterprise spend growth** (GPU training, always-on endpoints, message volume; §4) | 2×2 | Budgets and alerts per resource group; edge aggregation; autoscale schedules; drift-triggered rather than calendar retraining; a quarterly FinOps review | Finance + IT |
| 7 | **Vendor & cost: service availability and residency.** OpenAI and confidential ledger are not in Malaysia West; Planetary Computer Pro is in preview (AZ-AOAI-MODELS; AZ-ACL-RES; AZ-MPCPRO) | 2×2 | Non-personal and hashed data only across the border (§3). Template-text fallback when the LLM is unavailable. Local SHA-256 chain remains verifiable without the ledger. STAC access via the open Planetary Computer API until Pro reaches GA | Architecture board |
| 8 | **Operational: workflow disruption during harvest peaks** | 1×3 | Go-live outside peak months. Allocation suggestions are advisory in phase 1. Rollback via blue/green endpoints (AZ-ENDPOINTS) | Estate manager |
| 9 | **Operational/compliance: PDPA cross-border transfer** | 1×3 | Residency split; TIA and transfer records (MAYER-PDPA2025); Purview classification; DPO sign-off before phase 2 | DPO |
