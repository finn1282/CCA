# 06 — Azure Services, MSPO Clause Numbers, PDPA Cross-Border (answers R1 a–c)

> Research wave 2, 23 Nov 2026. Requested by Software (R1). Official Microsoft Learn / MPOCC / law-firm pages opened today. Keys → `sources.md`. Per D23, capabilities only — no pricing arguments.

## (a) Azure services in the target design — verified capabilities and caveats

| Service | Verified capability (cite in report) | Caveat that affects our design | Key |
|---|---|---|---|
| **Azure ML managed online endpoints** | Real-time HTTPS inference; key, AML-token or Entra auth; **blue/green traffic split and traffic mirroring** (safe rollout); Azure Monitor autoscale (metric/schedule); managed network isolation (private endpoints); model data collection + monitoring built in | Instance count ≥3 recommended for HA; 20 % quota reserve on some SKUs | [AZ-ENDPOINTS] |
| **Responsible AI dashboard** | Error analysis, fairness, interpretability (global/local feature importance), **counterfactual what-if (DiCE)**, causal analysis (EconML), data analysis; exportable **PDF scorecard** for compliance stakeholders | **Tabular only** (regression/classification), **sklearn MLflow models**, ≤5,000 points in UI, **not AutoML models**. Image explanations need the open-source Responsible AI Toolbox | [AZ-RAI] |
| **Model monitoring** | Signals: data drift, prediction drift, data quality, feature-attribution drift (preview), model performance (preview); alerts via **Event Grid** can trigger retraining | Built-in signals are **tabular** → fits fertiliser model (M6); image models need custom signals | [AZ-MONITOR] |
| **AutoML for images** | Image classification (multi-class/multi-label), **object detection**, instance segmentation; data as JSONL→MLTable (COCO/VOC converters provided); automatic hyper-parameter sweeps | **Requires GPU SKUs (NC/ND families)**; authored via Python SDK/CLI | [AZ-AUTOML-IMG] |
| **IoT Hub (tiers)** | Basic: device-to-cloud telemetry, per-device identity, routing, DPS. **Standard adds cloud-to-device, device twins, IoT Edge**. Free tier = Standard features with small allowance. Size 1 unit = 400,000 msgs/day; size 2 = 6 M; size 3 = 300 M. MQTT v5 profile (preview, S1 only) up to 250,000 concurrent devices | Use **Standard** (twins/C2D needed for pushing recommendations back to nodes); free tier can't be upgraded | [AZ-IOTHUB-SCALE] |
| **Device Provisioning Service** | Zero-touch, just-in-time provisioning; X.509/TPM attestation; allocation policies (lowest latency, weighted, static, custom); multi-hub, cross-region | **Data residency:** only Southeast Asia and Brazil South can disable DR replication; authentication secrets may transit other regions unless a private endpoint is used | [AZ-DPS] |
| **Azure IoT Operations** | Unified edge data plane on Azure Arc-enabled Kubernetes; edge **MQTT broker**; data flows to Event Hubs, ADLS, Fabric, Data Explorer; **local processing during outages, recovery validated after up to 45 days offline**; Essentials (single-node) and Standard SKUs from v1.5 (2610) | Essentials lacks OPC UA connector (irrelevant for soil sensors) | [AZ-IOTOPS] |
| **Event Hubs** | Fully managed streaming, millions of events/s, **Kafka-compatible** | — | [AZ-EVENTHUBS] |
| **ADLS Gen2** | Data-lake capabilities on Blob Storage: hierarchical file system semantics, file-level security, tiered storage | — | [AZ-ADLS] |
| **Planetary Computer (open data)** | STAC collection `sentinel-2-l2a`: global archive (2015-06 →), 13 bands, 10–60 m, ~5-day revisit, Sen2Cor L2A | Licence field "proprietary" in STAC metadata → follow Copernicus terms [COPERNICUS-LEGAL] | [MPC-S2] |
| **Planetary Computer Pro** | GeoCatalog Azure resource to ingest/manage/search/distribute geospatial data using the **STAC** standard | Announced as public preview (May 2025); GA status not confirmed | [AZ-MPCPRO] |
| **Azure OpenAI** (for multilingual explanations, D28) | Model/region availability table lists **Southeast Asia (Singapore)**; **Malaysia West is not listed** | Report: host Azure OpenAI in Southeast Asia and send only non-personal text (block IDs, readings) → avoids PDPA s129 transfer of personal data | [AZ-AOAI-MODELS] |
| **Azure confidential ledger** (evidence log, D28) | Append-only, tamper-evident, immutable ledger for audit trails | **Always replicates to the Azure paired region; cannot be restricted to one region.** Malaysia West has **no paired region** in the region list [AZ-REGIONS] → Malaysia West availability unverified; plan for Southeast Asia and store **hashes only** (no personal data) | [AZ-ACL] [AZ-ACL-RES] |
| **Azure Maps** | Map rendering incl. satellite imagery, search, routing incl. **multipoint optimisation and matrix routing**, geofencing, spatial analytics | Matrix routing supports the harvester-allocation idea (D18) | [AZ-MAPS] |
| **Microsoft Purview** | Unified data governance, sensitive-data protection, risk & regulatory compliance | — | [AZ-PURVIEW] |
| **Logic Apps SAP connector** | Connects to S/4HANA and classic R/3/ECC; **IDoc, BAPI, RFC/tRFC** | Supports "integration with existing estate ERP" (Part 2, 3 marks) | [AZ-SAP] |

**Not verified:** a Microsoft "products by region" check for Azure ML, IoT Hub and Event Hubs in **Malaysia West** (page is script-rendered). Report should say "deployed in Malaysia West where the service is offered, otherwise Southeast Asia (Singapore) with PDPA s129 safeguards".

## (b) MS 2530:2022 criterion numbers (from MPOCC official guidance documents)

Part 3-1 = plantations 40.46–500 ha [MPOCC-P31]; Part 2-1 = independent smallholders [MPOCC-P21]. Numbering is the same in both for these items.

| Requirement | Clause | What it requires (guidance) | SawitSense evidence |
|---|---|---|---|
| Site-management SOPs incl. **fertilising, soil-fertility management, safe agrochemical use, water management, FFB harvesting** | **4.1.3 Criterion 3, Indicator 1 (4.1.3.1)** — SOP list in Part 2-1; Part 3-1: "Records related to its implementation should be maintained" | Recommendation + action log per block |
| Block visual reference system (block number, area, planting date, clone) | **4.1.3.4** (Part 3-1) | Block IDs in payloads/dashboard |
| Integrated Pest Management | **4.1.3.5** (Part 3-1) | Ganoderma screening as IPM evidence |
| **Traceability** (FFB traceable to plantation/smallholding; one level up/down) | **4.2.2 Criterion 2** (4.2.2.1–4.2.2.3) | Geolocated harvest/ripeness records |
| **GHG emissions** (stepwise; report via MSPO GHG Calculator, Jan–Dec period, submit by 31 Mar) — N₂O from fertiliser named as a source | **4.5.4 Criterion 4** (4.5.4.1–4.5.4.3) | Fertiliser quantities → N₂O estimate |
| Water resources management plan | **4.5.5 Criterion 5** | Irrigation advice log |

## (c) PDPA 2010 — cross-border transfer (only where it constrains integration)
- **Section 129 was replaced by the Personal Data Protection (Amendment) Act 2024**; the old Minister "whitelist" regime ended. Transfer is allowed where the destination has a **substantially similar law or ensures adequate protection (s129(2))**, or under listed exceptions (explicit consent, contract necessity, legal proceedings, vital interests, controller's reasonable precautions/due diligence) [MAYER-PDPA2025].
- Amendments phased in Jan–Jun 2025; **Cross Border Personal Data Transfer Guidelines issued 29 Apr 2025**; a **Transfer Impact Assessment** is valid up to 3 years; controllers must **record each transfer** (recipient, country, data type, purpose, evidence); **DPO appointment and breach notification** effective June 2025 [MAYER-PDPA2025].
- **Design implication:** keep personal data (worker/smallholder names, IC numbers, individually linked plot geolocation) in **Malaysia West**; services outside Malaysia (Azure OpenAI, confidential ledger in Southeast Asia) receive only non-personal or hashed data. Primary Act text not opened — Report may cite via [MAYER-PDPA2025].
