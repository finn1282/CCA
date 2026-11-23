# 07 — Actual Build vs Target Design (internal, D20)

> **Internal only.** Report-facing docs (01–05) describe the target: a fully Azure-native production design, justified by capability (D23). This page records what the demonstration build actually runs, and maps each piece to its production equivalent. Use it to answer Q&A honestly ("the demo is a scaled-down instance of the same API").
> Decisions: D20 (two layers of truth), D29 (build platform), D31 (the stakeholder runs account steps).

## 1. Component mapping

| Function | Actual build (demo) | Production target (report) | Gap / why |
|---|---|---|---|
| Soil sensing | One Wi-Fi ESP32 node posting HTTPS JSON to the API (INTERFACES v0.2.6) | LoRaWAN (AS923) soil nodes → gateway → network server → **IoT Hub Standard** via the TTS integration (TTS-AZURE); **IoT Operations** edge | Demo scale; same payload semantics (seq, buffered, capture time, nulls) |
| Device identity | `X-Device-Id` + `X-Device-Key` from `SAWIT_DEVICE_KEYS` (fail-closed in cloud mode) | **DPS** X.509 provisioning (SEA single-region + private endpoint) + IoT Hub per-device identity | Shared-secret keys are adequate for a demo |
| Command to device | `POST/GET /devices/{id}/commands` (poll every 2–3 s, coalesced, 60 s expiry) | IoT Hub **cloud-to-device** / **device twin** desired properties | Polling avoids broker setup |
| Recommendation back to node | Synchronous in the POST response (`oled`, `led`) | Twin reported/desired properties or C2D | Same content |
| Ingestion / storage | FastAPI + **SQLite** (one file, `/home/data` on App Service) | Event Hubs → **ADLS Gen2** bronze/silver/gold + **Cosmos DB** latest state | Single process; one worker |
| API hosting | **Azure App Service B1 (Linux, Python)** on Azure for Students, Malaysia West if allowed, else Southeast Asia; **laptop fallback** (uvicorn) | **Azure Container Apps** + API Management, Malaysia West | App Service is the simplest student-credit host |
| Model artefact storage | **Azure Blob Storage** container `models`, fetched by SAS URL at start-up | **Azure ML registry** + managed online endpoints (blue/green) | No GPU or endpoint quota on student credit (MSQA-GPU) |
| M1 training | **Kaggle notebook GPU** (stakeholder, `training/RUN_ON_KAGGLE.md`); **CPU script** fallback; provisional D2-only model built locally | **Azure ML** training jobs on NC/ND GPU; AutoML for images as a benchmark (enterprise only, D32d) | No student GPU quota |
| M1 serving | ONNX Runtime CPU inside the API; CAM heat-map computed from the final-layer weights | Azure ML managed online endpoint; Grad-CAM via RAI Toolbox | Same model file format (ONNX) |
| M2 harvest window | Rule in `inference.harvest_advice` (round interval env var, default 10 days) | Same rule, then a learned time-to-ripe model once estate data exists | — |
| Harvester allocation | Greedy allocator over a **SIMULATED** 8-block estate (`estate_blocks.json`) | Same logic on ERP block master + M1/M2 aggregates; **Azure Maps** matrix routing | No public block-level data |
| M3/M4 drone detector | **Not trained** (stretch, SW-P6); cascade stage 2 shows "not yet available" | YOLO on Azure ML GPU; batch scoring of orthomosaics | Time/network budget; D4 is 1.12 GB |
| M5 satellite | **Google Earth Engine** script (stakeholder, `gee/RUN_EARTH_ENGINE.md`) → static `satellite.json` + PNG; SIMULATED placeholder until it runs | **Planetary Computer STAC** → Azure ML monthly pipeline → ADLS gold (MPC-S2) | GEE gives noncommercial access with Cloud Score+ masking |
| M6 fertiliser | Rules + JSON decision tree trained on **SIMULATED** data; pure-Python inference | sklearn/MLflow model in Azure ML → **RAI dashboard** + drift monitoring (tabular only, D32b) | No public soil-sensor data; the rule-based baseline is replaced by estate-trained data in the pilot |
| M7 compliance | Python knowledge base (`compliance.py`) mapping to MS 2530 4.1.3.1/.4/.5, 4.2.2, 4.5.4, 4.5.5 | Same knowledge base + Purview classification; Power BI coverage view | — |
| Evidence integrity | SHA-256 hash chain in SQLite; `/evidence/verify`; head hash printed in the audit pack | **Azure confidential ledger** (Southeast Asia, digests only) anchoring the head hash | Local chain cannot detect truncation of the newest records without an external anchor (S-10) |
| NLP explanations | Template text from rule IDs (English) | **Azure OpenAI** (Southeast Asia, non-personal prompts) for BM/EN/ID/NE rewording + audit narrative | No LLM dependency in the live demo |
| Dashboard | Single static page (vanilla JS, Chart.js stored locally), served by the API; `/harvester` mobile page | Web app + **Power BI** + native harvester app | — |
| Auth for users | Admin token (`?token=` / `X-Admin-Token`); reads protected in cloud mode | **Entra ID** RBAC | Demo scope |
| ERP integration | Not built (documented only) | **Logic Apps SAP connector** (IDoc/BAPI/RFC) + API Management | Out of demo scope |
| Monitoring | `/api/v1/health`; App Service log stream | Azure Monitor + Azure ML model monitoring + Event Grid retrain triggers | — |

## 2. Data actually used

| Data | Build status | Licence / label |
|---|---|---|
| D1 Kamal et al. (2024) | Used in the Kaggle run; local download blocked by very slow Mendeley S3 transfer from this machine | CC BY 4.0 |
| D2 Rosbi (2024) | Downloaded from the GitHub mirror (subset of train + full test) | CC BY 4.0 |
| Sentinel-2 L2A + global oil-palm map | Via Earth Engine (stakeholder) | Copernicus notice + CC BY 4.0 |
| Soil-sensor training data | **SIMULATED** (`train_m6.py`) | Labelled in UI, API (`simulated`) and audit pack |
| Estate blocks / crew | **SIMULATED** (`make_demo_estate.py`), productivity from AHMAD2020 | Labelled |

## 3. Q&A lines (honest, short)
- *"Is this running on Azure ML?"* The API runs on Azure App Service. Training ran on a GPU notebook, and the model is stored in Azure Blob. In production, training and serving move to Azure ML endpoints. The model file (ONNX) is the same.
- *"Is the fertiliser model real?"* The thresholds come from oil-palm literature. The ML layer was trained on simulated sensor data because no public oil-palm soil-sensor dataset exists, and the dashboard labels it as such. The pilot replaces this rule-based baseline with estate-trained data.
- *"Can you detect Ganoderma?"* We screen and prioritise; we do not diagnose. Satellite anomaly → drone scoring → a ranked ground check, consistent with published early-detection accuracy of 64–84 %.
- *"Is the evidence log tamper-proof?"* It is tamper-evident. Any edit breaks the SHA-256 chain, and verification shows where. In production the chain head is anchored in Azure confidential ledger.

## 4. Known deviations from the brief
- Brief item 4 asked for "student implementation within credits; local fallback; cost table" in `04_cloud_design.md`. Under D23 these moved here and to `deploy/` (internal). Doc 04 keeps enterprise cost drivers framed only as a vendor & cost risk.
- M3/M4 (drone YOLO) is not trained: a stretch goal (SW-P6), not reached because of time and network limits.

## 5. Demonstration sequence (live presentation; moved from 02 per S-22)

```mermaid
sequenceDiagram
  autonumber
  participant Node as IoT soil node
  participant Cam as Field camera
  participant API as SawitSense API
  participant ML as Model endpoints
  participant EV as Evidence log
  participant UI as Dashboard
  Note over UI: Pre-computed: Sentinel-2 NDVI anomaly flags block B2 → drone scores → ranked ground list
  Node->>API: POST reading (pH 3.8, moisture 45 %)
  API->>API: Rules → LIME (PH_LIME), counterfactual "OK if pH ≥ 4.2"
  API->>ML: M6 check → agrees, confidence 0.87
  API->>EV: append record (+ MSPO 4.1.3.1), hash-chain
  API-->>Node: action, short text, colour
  UI->>API: Capture request
  Cam->>API: poll → capture → POST image
  API->>ML: M1 → "ripe 0.9" + heat-map
  API->>EV: append record (harvest SOP, traceability)
  UI->>API: Approve / override recommendation
  API->>EV: append review record
  UI->>API: Verify chain → "all N records intact"; export MSPO pack
```

## 6. Measured prototype results (moved from 03 §9 per S-22/D40 — not for the report)

| Model | Test set | Metric | Result |
|---|---|---|---|
| M1 (provisional, CPU) | D2 Malaysia test **after removing 8 train duplicates** (S-17), n = 81 (unripe 32, ripe 36, overripe 13); trained on a 190-image D2-train subset | accuracy / macro-F1, **serving path** (exported ONNX + the API's own preprocessing, S-16) | **0.91 / 0.92**. Recall: unripe 0.78, ripe 1.00, overripe 1.00. Errors: 6 unripe→ripe, 1 unripe→overripe. Same-country test, and no *underripe* class in D2, so this is a sanity check, **not** the cross-country result. Superseded figure (before the fixes): 0.93 on n = 89 including duplicates; 0.90 through the old serving path |
| M1 (final) | D1 test (Indonesia) and D2 (Malaysia, cross-country) | accuracy / macro-F1 / within-one-class | From the GPU notebook run (`training/RUN_ON_KAGGLE.md`). Insert the values from `m1_metrics.json` before the report is frozen |
| M6 | Simulated hold-out (n = 4,000) | accuracy vs noisy labels | **0.88** (irrigate F1 0.94, lime 0.88, drain 0.92, fertilise 0.82, watch 0.58: the narrow 4.0–4.2 band is where sensor noise matters most) |
| M3 | D4 disjoint test blocks | Ganoderma recall, mAP@0.5 | Roadmap (stretch, SW-P6) |
| M5 | Sentinel-2 over a Malaysian estate AOI | flagged blocks | Pre-computed export (`gee/`) |
