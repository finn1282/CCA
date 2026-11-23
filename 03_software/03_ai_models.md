# 03 — AI Models

> Report-facing (Part 2: underlying technologies; Part 1: cognitive capability per problem). The target design trains and serves the models on Azure ML (D20). Explainability follows D32b: the Azure RAI dashboard and monitoring cover only the tabular model, and the image models use Grad-CAM and the open-source RAI Toolbox. Ganoderma output is screening, not diagnosis (D32e). Keys refer to `01_research/sources.md`. Measured metrics are in §9.

## 0. Model map

| ID | Outcome / problem | Type | Data | Status of evidence |
|---|---|---|---|---|
| M1 | O1 / P1 FFB ripeness | Image classification (CNN, transfer learning) | D1 Kamal et al. (D1-KAMAL2024) → D2 Malaysian test (D2-ROSBI2024; OMAR2024) | Real data |
| M2 | O1 / P1 harvest window | Rule-based scheduler over M1 grades | Ripening physiology (RAMLI2026); round intervals (AHMAD2020; MPOB-NEWS2020) | Rule-based; no public timing data |
| M3 | O2 / P2 Ganoderma screening | Object detection (YOLO) on UAV RGB | D4 Mimboro et al., field-confirmed BSR crowns (D4-MIMBORO2026) | Real data, RGB proxy for multispectral |
| M4 | O2 / O4 palm count | Same detector, one class | D4 (+D5-DOMINGUEZ2025) | Real data |
| M5 | O2 / O4 canopy stress | Time-series anomaly (NDVI z-score) | Sentinel-2 L2A (MPC-S2; GEE-S2) + oil-palm mask (GEE-OILPALM) | Real data, unlabelled |
| M6 | O3 / P3 fertiliser, lime, irrigation | Rules + decision tree (tabular) | Thresholds (KANANG2026; AAR-SOIL; CARR2011); **simulated** sensor dataset | Simulated (no public soil-sensor data) |
| M7 | O4 / P3 MSPO compliance | Knowledge base + coverage reasoning | MS 2530:2022 clauses 4.1.3, 4.1.3.4, 4.1.3.5, 4.2.2, 4.5.4, 4.5.5 (MPOCC-P31; MPOCC-P21) | Knowledge-based |
| NLP | All | LLM rewording of structured explanations (multilingual) + audit narrative | Azure OpenAI, non-personal prompts (AZ-AOAI-MODELS) | Target design |

---

## M1 — FFB ripeness classifier (O1)

- **Inputs.** An RGB bunch image from a field camera, phone or drone crop, resized to 224 × 224.
- **Output.** One of `unripe · underripe · ripe · overripe` with class probabilities, a heat-map and a plain-language explanation.
- **Classes.** Harmonised across the datasets:
  - D1 *Immature / Partially ripe / Fully ripe / Overripe + Decayed* map to these four.
  - D2 *Unripe / Ripe / Overripe* map to three of them.
  - D2 *Empty* and *Damaged* bunches are a grading concern, not a ripeness one, and are excluded.
- **Algorithm.** EfficientNet-B0 pre-trained on ImageNet, with transfer learning in two stages: (1) frozen backbone with a class-weighted linear head; (2) fine-tuning of the last blocks.

| Option | For | Against | Decision |
|---|---|---|---|
| **EfficientNet-B0 (chosen)** | Strong accuracy per parameter; global-average-pool → linear head gives an **exact class-activation map** without gradients at inference; small enough for CPU or edge | Classification only (no bunch localisation) | Chosen for explainability + deployability |
| YOLO detector (e.g. YOLO11) | Localises and counts bunches on the tree; 98.3 % mAP on 11,613 drone images (HASSAN2026); YOLOv5m mAP@.5:.95 0.842 (MANSOUR2022) | Needs box labels (D1/D2 are image-level) | Medium-term, for drone bunch counting |
| MobileNetV3 | Fastest on edge | Its two-layer head breaks the exact-CAM property | Edge fallback |
| Azure AutoML for images | Automatic hyper-parameter sweeps, classification and detection (AZ-AUTOML-IMG) | Needs GPU (NC/ND) compute; AutoML models cannot use the RAI dashboard (AZ-RAI) | Enterprise design only (D32d), to benchmark against the custom model |

- **Training data.**
  - D1: 4,728 images, Indonesia, CC BY 4.0, stratified train/val/test.
  - **D2: 466 images from Johor, Negeri Sembilan and Perak**, labelled by an experienced grader (OMAR2024). D2 is the **cross-country test**: train in Indonesia, test in Malaysia (D18).
  - A second variant fine-tunes only the head on D2-train to show the adaptation path for a new estate.
- **Metrics.**
  - Accuracy and macro-F1 on D1-test and on D2.
  - **Within-one-class accuracy**, because ripeness is ordinal: confusing *underripe* with *ripe* costs less than confusing *unripe* with *overripe*.
  - A confusion matrix.
  - Recall on *ripe* and *overripe* matters most for P1, since those are the bunches lost when harvesting is late.
- **Explainability.**
  - CAM heat-map per prediction, mathematically equal to Grad-CAM for this head.
  - An auto-generated sentence ("model attends to the upper bunch surface, dominant colour red/orange").
  - A "low confidence, send to grader" flag below 0.6.
  - Target design: the open-source Responsible AI Toolbox vision explainers. The Azure RAI dashboard is tabular-only (AZ-RAI).
- **MLOps.**
  - Registered in the Azure ML registry and served from a managed online endpoint.
  - New versions roll out blue/green with traffic mirroring (AZ-ENDPOINTS).
  - Grader overrides become labels.
  - A custom monitoring signal (class-distribution shift per estate and month) triggers retraining. The built-in signals are tabular, so this one is custom (AZ-MONITOR).

## M2 — Harvest window (O1)

- **Inputs.** M1 grades per block, the block's last harvest date, and the round interval.
- **Rule.** *unripe* → re-check in about two rounds; *underripe* → next round; *ripe* → harvest this round; *overripe* → harvest immediately and shorten the round for that block.
  - Ripening runs from 19 to 24 weeks after anthesis, and oil content exceeds 40 % at full maturity (RAMLI2026).
  - The recommended round is 7–13 days (AHMAD2020); 10–12 days is optimal, and at least 12–15 days is needed to stop fruit over-ripening (MPOB-NEWS2020).
- **Why rules.** No public bunch-level time series exists. The rule is transparent, and the estate's own logged grades will train a survival or time-to-ripe model in the medium term.
- **Allocation (F2).**
  - Greedy assignment of the available harvesters, ranked by the ripe bunches each harvester can save: block productivity × (1 + 2 × over-ripe share).
  - Productivity falls with palm height: 400–1,000 bunches/day for a 2-person team on palms under 3 m, but 50–90 on palms over 12 m (AHMAD2020).
  - Tall ageing blocks therefore rank low and are flagged, which links P1 to the replanting side of P2.
  - Target design: Azure Maps matrix routing orders crew movement between blocks (AZ-MAPS).

## M3/M4 — Drone Ganoderma screening and palm count (O2)

- **Inputs.** 640 × 640 UAV RGB tiles at about 4 cm GSD.
- **Output.** Crown boxes with P(Ganoderma) per palm, and palm counts per block.
- **Algorithm.** YOLO (nano/small) with class weighting or focal loss for the roughly 1:12 imbalance (722 BSR crowns vs 8,678 negatives).
  - **The dataset's geographically disjoint split is kept** to avoid spatial leakage (`01_research/03_datasets.md`).
  - Alternatives:
    - SVM/ResNet on hyperspectral data: 84 % overall, 74 % early-infection sensitivity (KWANG2025).
    - Multispectral convolutional SVM: 64–68 % early-stage (AHMADI2023).
    - Both need sensors and data that are not publicly available.
  - RGB on field-confirmed labels is the realistic public proxy.
- **Metrics.** Ganoderma-class **recall** first (a missed infected palm keeps spreading), then precision and mAP@0.5. Results are reported on the disjoint test blocks.
- **Positioning (D32e).** BSR stays asymptomatic until 60–70 % of the palm is infected (KHOO2023), and published early-detection accuracy is only 64–84 %. M3 is therefore a **screening and prioritisation** tool: its output is a ranked list for ground or laboratory confirmation, never a diagnosis.
- **Cascade reasoning.**
  - priority = P(Ganoderma) × (1 + 0.5·e^(−d/36 m)), where d is the distance to the nearest confirmed case.
  - Root contact spreads BSR across about 4 planting rows (about 36 m at 9 m spacing) (KHOO2023).
  - The boost is additive, not a filter, because airborne basidiospores also cause scattered new cases (COOPER2011).
- **Explainability.** Boxes, confidence and the rank-reason string ("p = 0.62, 14 m from confirmed case"). Target design: Grad-CAM on the detector backbone via the RAI Toolbox.

## M5 — Satellite canopy-stress anomaly (O2, O4)

- **Inputs.**
  - Sentinel-2 L2A bands B4 and B8 at 10 m, about 5-day revisit (MPC-S2).
  - A cloud mask: Scene Classification layer, or Cloud Score+ in Earth Engine.
  - The oil-palm mask (GEE-OILPALM).
- **Method.**
  - Monthly median NDVI per estate block (median compositing handles Malaysia's persistent cloud).
  - A z-score of the latest month against the block's own history.
  - Blocks with z ≤ −1.5 go to drone survey.
  - Unlabelled, so the method is anomaly detection, not classification.
- **Alternatives.** Isolation forest on multi-index features (NDVI, NDRE, NDMI), or seasonal decomposition. Both come later, once enough history exists.
- **Explainability.** The block's own time series and its z-score; transparent by construction.
- **Pipeline.** Planetary Computer STAC → Azure ML pipeline (monthly schedule) → ADLS gold layer → dashboard and cascade (MPC-S2; AZ-MPCPRO).

## M6 — Fertiliser / lime / irrigation recommender (O3)

- **Inputs.** Soil moisture %, pH, EC/TDS against a per-device baseline, soil temperature, and block. Planned additions: palm age, soil type (mineral or peat), rainfall, leaf-nutrient results.
- **Output.** A primary action and all triggered actions from `ok · irrigate · drain · lime · fertilise · skip_fertiliser · watch`, each with a rule ID, plus a confidence, a counterfactual and the ML agreement.
- **Knowledge.**
  - pH: < 4.0 → lime; 4.0–4.2 → watch; 4.2–5.5 is the typical oil-palm band; > 6.5 → check or stop liming (KANANG2026; AAR-SOIL).
  - Water deficit lowers yield (CARR2011).
  - EC relative to the block baseline is a nutrient proxy. This is simulated agronomy and labelled as such.
- **Algorithm (hybrid).**
  1. The **rule engine is authoritative**, which keeps it safe and auditable.
  2. A **decision tree** (depth 7) is trained on a **simulated dataset**: true soil states are labelled by the rules, then realistic sensor noise is added. The tree therefore learns how measurement uncertainty blurs each threshold.
  3. Its probability tempers the confidence. Disagreement with the rules, or confidence below 0.6, sends the case to agronomist review.
  4. **Alternatives considered.** Gradient boosting is more accurate but less transparent. Pure ML is not acceptable without real labelled data. Satellite nutrient mapping with RF/SVM on Landsat-8 reaches about 80 % for N and 77 % for K (KOK2021) and is a long-term extension.
- **Metrics.**
  - On the simulated test set: per-class precision and recall, especially *lime* and *irrigate* recall.
  - In the pilot: the agronomist agreement rate, and fertiliser saved per hectare.
- **Explainability (D32b).**
  - Rule trace, counterfactual ("would be OK if pH ≥ 4.2"), and per-feature path attributions.
  - In the target design, M6 is an sklearn tabular model registered with MLflow. That makes it **eligible for the Azure Responsible AI dashboard** (global/local importance, DiCE counterfactuals, error analysis, PDF scorecard for MSPO stakeholders) and **built-in drift and data-quality monitoring** (AZ-RAI; AZ-MONITOR).
- **MLOps.** Agronomist overrides plus pilot outcomes, such as leaf-analysis results, replace the simulated labels. Monitoring alerts are sent through Event Grid and trigger retraining (AZ-MONITOR).

## M7 — MSPO compliance reasoner (O4)

- **Knowledge base.** Every evidence record type maps to the MS 2530:2022 clauses it supports (MPOCC-P31; MPOCC-P21):

| Evidence type | Clause |
|---|---|
| Soil reading, fertilise/lime/skip decision | **4.1.3.1** SOP records (fertilising, soil fertility) |
| Irrigation / drainage advice | **4.5.5** water management |
| Fertilise / skip decision → N quantity → N₂O estimate | **4.5.4** GHG |
| Ganoderma screening + follow-up | **4.1.3.5** IPM |
| Ripeness grade at harvest | **4.1.3.1** harvesting SOP records |
| Block ID on every record | **4.1.3.4** block reference system, **4.2.2** traceability |
| Human approve/override | 4.1.3 records of implementation |

- **Reasoning.** It computes coverage per block and period and lists gaps, for example "no IPM evidence for block C2 this quarter".
- **Integrity.** Records are SHA-256 hash-chained, and the digests are anchored in Azure confidential ledger, which is append-only and tamper-evident (AZ-ACL). Only digests leave Malaysia West (D32a).

## NLP — explanations and audit narrative

- The structured explanation (rule ID, reading, threshold, counterfactual) is rewritten into short plain language in BM, English, Bahasa Indonesia or Nepali for a largely foreign field workforce (STAR-LAB2026). Azure OpenAI also drafts the audit-pack narrative.
- **The LLM never decides.** It receives only the structured, non-personal explanation, and runs in Southeast Asia because Malaysia West does not offer it (AZ-AOAI-MODELS; D32a).
- Template text is the fallback when the service is unavailable.

## 9. Measured results (this project)

| Model | Test set | Metric | Result |
|---|---|---|---|
| M1 | D2 Malaysia | accuracy / macro-F1 / within-one-class | *pending: filled from `training/ripeness/m1_metrics.json`* |
| M6 | Simulated hold-out (n = 4,000) | accuracy vs noisy labels | **0.88** (irrigate F1 0.94, lime 0.88, drain 0.92, fertilise 0.82, watch 0.58: the narrow 4.0–4.2 band is where sensor noise matters most) |
| M3 | D4 disjoint test blocks | Ganoderma recall, mAP@0.5 | Roadmap (stretch, SW-P6) |
| M5 | Sentinel-2 over a Malaysian estate AOI | flagged blocks | Pre-computed export (`gee/`) |
