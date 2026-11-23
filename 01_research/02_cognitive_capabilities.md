# 02 — Cognitive Capabilities per Problem (v2, report Part 1 ready)

> Owner: Research. v1 (wave 1) → **v2 (wave 2, 23 Nov 2026)**, organised by the D19 problem order. One primary capability per problem, plus why it beats conventional methods. Keys → `sources.md`. Reported accuracies come from different datasets and metrics and **are not directly comparable**.

## Summary (Report Part 1, "cognitive capability per problem", 4 marks)

| Problem (D19) | Primary cognitive capability | Supporting capabilities | Outcome |
|---|---|---|---|
| **P1** Labour shortage & harvest losses | **Computer vision pattern recognition**: deep-learning detection/classification of FFB ripeness from drone and ground images | Predictive scheduling (harvest windows); optimisation (harvester allocation) | O1 |
| **P2** Declining stand productivity: Ganoderma (primary) + ageing | **Multisource machine learning for anomaly detection**: drone-image detectors fused with satellite NDVI time series, with spatial reasoning over neighbouring palms | Risk ranking; knowledge of disease spread (root contact) | O2 (+O4 replanting priority) |
| **P3** MSPO & fertiliser compliance | **Knowledge representation & reasoning with explainable ML**: agronomic rules and MSPO clauses as a knowledge base, combined with an ML recommender over IoT soil data | NLP for multilingual explanations and audit write-ups (D28) | O3, O4 |

---

## P1: Computer vision for ripeness & harvest planning (O1)

**What it does in SawitSense.** A CNN/YOLO model grades bunches as unripe, underripe, ripe or overripe. The images come from drone passes (estate scale) or a phone/camera (block scale). Per-block counts of ripe bunches then drive a harvest-window schedule and an allocation of the scarce harvesters.

**State of the art (evidence)**
- **Drone, real time:** YOLO11 trained on **11,613** drone images of palms with visible FFB, 6 ripeness classes. Results: **mAP 98.3 %, precision 94.0 %, recall 97.2 %, ~7.7 ms per frame**. The system tracks bunches across video frames and logs per-tree results through QR-coded tree IDs [HASSAN2026] (JOPR/MPOB, Malaysian authors).
- **Ground images:** YOLOv5m reached mAP@0.5:0.95 **0.842** on 4 classes from only 304 images (MMU) [MANSOUR2022]. A Malaysian outdoor dataset with on-tree and ground images in 5 classes is our test set [OMAR2024].
- **Why ripeness matters:** fully mature fruit holds >40 % oil, and under-ripe fruit yields poorer CPO (lower carotene and DOBI, higher chlorophyll and chloride) [RAMLI2026].

**Conventional method and its limits.** Fixed 10–15-day harvesting rounds with human judgement (fruit colour, counting loose fruit). Recommended rounds are 7–13 days, but labour shortages stretch them to 20–25 days [AHMAD2020]; at least 12–15 days is considered necessary to avoid overripe fruit [MPOB-NEWS2020]. Short of workers, estates harvest more under-ripe bunches to avoid collecting loose fruit, losing oil [MA-POEB]. Mill and estate cannot agree on oil content because "no one knows how much oil is in the FFB" [MA-POEB].

**Why cognitive computing beats it.**
1. **It scales without labour.** One drone flight grades every visible bunch; a human census needs exactly the workers who are missing. Conventional harvesters manage about 1 t FFB per day, and only 50–90 bunches per day on palms over 12 m [AHMAD2020].
2. **It is consistent.** A model applies the same grading standard across every block and shift, which reduces estate–mill disputes.
3. **It turns perception into decisions.** Rule-based ERP systems cannot read images. A cognitive system converts unstructured images into a ranked "where and when to harvest" plan.

**Explainability.** Grad-CAM heatmaps show which part of the bunch drove the grade. A confidence score and the class definition are shown beside the result.

**Limits to state.** Accuracy is lower on small or unbalanced datasets and on canopies the drone cannot see (bunches hidden by fronds). Harvest-window prediction has no public time-series data, so in our build it is rule-based (19–24 weeks after anthesis [RAMLI2026]) and labelled as such.

---

## P2: Multisource ML anomaly detection for Ganoderma (O2)

**What it does.** A three-step screening cascade (D18):
1. Sentinel-2 NDVI time series flag blocks whose canopy vigour is falling.
2. A drone-image detector flags individual suspect crowns in those blocks.
3. A spatial rule raises the risk of neighbouring palms.

Ground teams then confirm only the top-ranked palms with lab or GSM tests.

**State of the art (evidence)**

| Approach | Reported performance | Source |
|---|---|---|
| UAV + Pleiades multispectral, convolutional SVM (UPM co-author) | ~64–68 % overall for early-stage infection | [AHMADI2023] |
| UAV hyperspectral + PCA, fine-tuned ResNet50 (MMU) | **84 % overall**, 74 % sensitivity (early infected), 86 % specificity | [KWANG2025] |
| Smartphone images (Malaysia + Thailand), MobileNetV2 in an on-device app | **77 % overall**, early-infected recall 75 %; most errors between early-infected and healthy | [DARANAGAMA2025] |
| UAV RGB with field-confirmed labels, COCO, geographically disjoint split | dataset for our model (722 Ganoderma crowns) | [D4-MIMBORO2026] |

**Disease facts the reasoning uses.** BSR spreads through **root contact with stumps and diseased palms**, and palm roots reach the first four planting rows. Sanitation at replanting cut incidence to **<1 % versus >13 %** without it [KHOO2023]. Airborne basidiospores are also a major input [COOPER2011], so screening must cover all blocks, not only neighbours of known cases.

**Conventional method and its limits.** Visual census by trained workers (the method used in MPOB's national surveillance [IBRAHIM2020]), plus lab confirmation by PCR, ELISA or GSM culture. The lab methods are accurate but costly, slow and labour-intensive. Palms show no symptoms until about 60–70 % infected [KHOO2023]. Visual census therefore finds palms late and depends on the same scarce labour as P1.

**Why cognitive computing beats it.**
1. **It sees earlier and more widely.** Learned spectral and texture patterns can flag stress before obvious symptoms appear, and the system screens **100 % of palms on every satellite revisit** (Sentinel-2 revisits every ~5 days [GEE-S2]).
2. **It reasons over evidence.** It fuses weak signals (satellite trend, drone crown appearance, neighbour status, soil type, palm age) into one risk score. Conventional census only records what a person can see.
3. **It directs scarce experts.** Lab tests go to the highest-risk palms, not to random samples.

**Honest positioning.** Published early-detection accuracy is moderate (64–84 %), so SawitSense is a **screening and prioritisation** tool, not a diagnosis. Human confirmation stays in the loop.

**Ageing trees (secondary).** The same NDVI and yield-trend analytics rank blocks for replanting. Replanting runs at 2 % a year against a 4–5 % target [SARMIDI2025], and tall old palms also cut harvester productivity [AHMAD2020]. The binding constraint on ageing is capital, so cognitive computing contributes prioritisation, not a cure.

---

## P3: Knowledge-based reasoning + explainable ML for fertiliser & MSPO (O3, O4)

**What it does.** Live soil readings (moisture, pH, EC, temperature) and block context (age, soil type) go to an ML recommender that is constrained by an agronomic and MSPO knowledge base. It outputs **fertilise / lime / irrigate / skip** with a reason. Every recommendation and action is written to the explain-to-audit evidence log (D18/D28) against the relevant MSPO clauses.

**State of the art (evidence)**
- **Nutrient sensing:** Landsat-8 + RF/SVM classifiers predict leaf N and K levels in Malaysian variable-rate fertiliser plots, with **N 79.7 ± 4.3 %** and **K 76.6 ± 4.1 %**. P, Mg and Ca were not reliably classified (UPM + Sime Darby Plantation Research) [KOK2021].
- **Agronomic knowledge base:** pH bands for oil palm (4.2–5.5 = high/good) [KANANG2026]; land-suitability criteria (pH >4.0, drainage, water table) [AAR-SOIL]; yield falls about 10 % per 100 mm of soil water deficit [CARR2011].
- **Compliance knowledge (MS 2530:2022):** SOPs and records for fertilising and soil fertility (4.1.3), traceability (4.2.2), GHG including N₂O from fertiliser (4.5.4), water management (4.5.5) [MPOCC-P31] [MPOCC-P21].
- **Explainability tooling:** the Azure ML Responsible AI dashboard provides feature importance, counterfactual "what-if" analysis and a PDF scorecard for **tabular** models [AZ-RAI]. This fits the fertiliser recommender (tabular); image models need separate tools (Grad-CAM).

**Conventional method and its limits.** Blanket fertiliser schedules by palm age and soil type, plus periodic leaf and soil sampling, recorded on paper or spreadsheets for audits. This method is blind between sampling rounds and treats each block the same. Fertiliser is about **30 % of estate production cost**, and a 40 % cut can reduce yields by ≥20 % over 18–24 months [STAR-FERT2026], so both over- and under-application are expensive.

**Why cognitive computing beats it.**
1. **Site-specific and continuous.** Decisions change with live readings per block instead of once a year.
2. **Reasoning, not just display.** A dashboard shows pH 3.8. A cognitive system reasons that pH below 4.0 calls for lime before fertiliser, because nutrient uptake is poor in acid soil [KANANG2026], and gives that reason.
3. **Audit-ready by design.** Each recommendation carries its explanation, data and clause mapping, so MSPO evidence (records, GHG inputs, traceability) is produced as a by-product of normal work. A conventional records system needs separate manual paperwork.
4. **Counterfactual explanations** (for example, "had pH been ≥4.2, the action would be *fertilise*") help agronomists trust and challenge the model [AZ-RAI].

**Limits to state.** No public oil-palm soil-sensor dataset exists, so the build's model is trained on **SIMULATED** data derived from literature thresholds. The pilot phase replaces it with estate-logged data.

---

## Notes for Report / Software
- Report Part 1 can reuse the three "Why cognitive computing beats it" blocks almost directly. Part 3 novelty can reuse the explain-to-audit and counterfactual points.
- All model accuracies in the report should be measured on held-out data: D2 (Malaysian) for ripeness, and D4's geographic test split for Ganoderma.
