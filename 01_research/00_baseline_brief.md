# 00 — Research Baseline Brief (direction for every team)

> Research wave 1, 23 Nov 2026. One section per team. Keys in brackets → `sources.md`; detail in files 01–05. Items marked **(Lead ruling needed)** are in `PLAN.md` → Proposals.

## Hardware
**What the demo should show (and why):** one ESP32 soil node on a potted plant that turns live readings into an *explained* agronomic action (fertilise / lime / irrigate / skip). This is the IoT input of O3 and the MSPO evidence trail of O4 — fertiliser is ~30 % of estate cost [STAR-FERT2026] and MSPO 2022 requires fertilising/soil-fertility SOPs and records [MPOCC-P21]. ESP32-CAM is a *capture & upload* node for the cloud ripeness model (O1). Keep it small (SPEC §4).

**Must-do wiring facts** [ESPFAQ] [RAW-PH] [DFR-SEN0244] [RNT-CAM]:
- All analog sensors on **ADC1** (GPIO32–39). ADC2 fails while Wi-Fi is on.
- pH board is **5 V** and its output can exceed 3.3 V → **10 kΩ/20 kΩ divider** into ADC1; offset POT1 to 2.50 V at pH 7; slope ≈ 0.18 V/pH; two-point calibration with buffers.
- TDS board is 3.3 V-compatible (0–2.3 V out); temperature-compensate with DS18B20.
- pH and TDS probes are **liquid probes** → measure a soil-water slurry/leachate, not raw soil; read sequentially.
- ESP32-CAM needs solid 5 V supply (brownouts).

**Thresholds to use (labelled "derived from literature")**: pH <4.0 LIME, 4.0–4.2 watch, **4.2–5.5 OK** [KANANG2026] [AAR-SOIL]; relative moisture <30 % IRRIGATE, >80 % drainage warning (demo calibration; justified by −10 % yield per 100 mm water deficit [CARR2011]); TDS low/high points calibrated on the day (simulated agronomy).

**Parts to propose (stakeholder chooses):** pH buffer sachets 4.01/6.86 (essential, ~RM5–10, unverified price), 2-port 5 V/2 A power bank or adaptor, optional 2nd moisture sensor for a "dry block vs wet block" comparison, colour prints of FFB from dataset D2. Details: `05_hardware_notes.md`.

## Software & Cloud AI
**Models & datasets (all licences verified via repository metadata):**
| Model | Data | Approach |
|---|---|---|
| M1 FFB ripeness (live demo) | **D1** Kamal et al. 4,728 imgs, CC BY 4.0 (train) + **D2** Malaysian outdoor FFB 466 imgs, CC BY 4.0 (test/fine-tune) | Transfer learning (EfficientNet-B0/MobileNetV3 or YOLOv8-cls), 4 harmonised classes, Grad-CAM explanation |
| M2 Harvest window | none public → rule (19–24 weeks after anthesis [RAMLI2026]) + M1 output | **SIMULATED/rule-based**, label it |
| M3/M4 Ganoderma & palm detection | **D4** UAV RGB, 9,400 crowns (722 Ganoderma), COCO, CC BY 4.0; keep its geographic split | YOLOv8n/s, class weights; report Ganoderma recall |
| M5 Satellite stress | Sentinel-2 L2A in Earth Engine + global oil-palm mask [GEE-S2] [GEE-OILPALM] | Monthly NDVI composites → anomaly z-score; pre-compute & export |
| M6 Fertiliser/irrigation | **No public data** → SIMULATED dataset from thresholds + live ESP32 readings | Decision tree / gradient boosting + SHAP reasons |

**Platforms:** train on **Kaggle Notebooks** (Colab backup); deploy API + dashboard (+ optional IoT Hub) on **Azure for Students** ($100, no card, Malaysia West region) [AZ-STUDENT]; satellite pre-compute in **Earth Engine** (free noncommercial) [GEE-NONCOM]. Avoid: GCP Free Trial (card; since 16 Nov 2026 credit can't pay for Vertex/"Gemini platform") [GCP-TRIAL]; Azure GPU (students can't get quota) [MSQA-GPU]; SageMaker Studio Lab (closed to new users) [AWS-STUDIOLAB].
**Enterprise architecture to mirror:** Azure ML + Azure IoT Hub/IoT Operations + Malaysia West (see `04_cloud_platforms.md`).

## Report
**Validated problem priority** (`01_problem_evidence.md` §3):
1. **P1 Labour-constrained harvesting → ripe-crop & OER losses** (O1). Strongest stats: ~80 % foreign workforce, RM7.5–20 bn/yr losses claimed [STAR-LAB2026]; 30,000-worker shortage (Oct 2026) [EDGE-LAB2026]; harvesting not mechanisable [EDGE-SDG2025]; shortage drives under-ripe harvesting [MA-POEB]; each 0.5-pt OER ≈ RM2.2 bn *(calc.)*.
2. **P2 Declining stand productivity: Ganoderma (primary) + ageing** (O2). BSR 9.2 % of surveyed smallholdings [IBRAHIM2020], >20 % in some plantings [BORNEO-GANO2025], 43 % loss in 6 months, asymptomatic until 60–70 % infected [KHOO2023]; >25-yr palms ≈8.5 %, replanting 2 % vs 4–5 % target [SARMIDI2025]. **(Lead ruling needed: R-P1)**
3. **P3 MSPO 2.0 / EUDR compliance & fertiliser efficiency** (O3, O4). MSPO mandatory since 2020, 87 % certified, MS 2530:2022 cut-off 31 Dec 2019 + traceability [MSPO-EFI2025]; fertilising SOPs/records + N₂O GHG criterion [MPOCC-P21]; fertiliser ≈30 % of cost [STAR-FERT2026]; EUDR from 30 Dec 2026 [HL-EUDR2026], Malaysia "standard risk" [STAR-EUDR2025].

**Case description facts:** 5.70 M ha, 20.28 Mt CPO (decade high), RM112.4 bn export revenue, estate yield 17.77 t/ha [MPOB2025]; estates 73.6 %, independent smallholders 14.6 %, organised 11.8 % [PARVEEZ2025]; SD Guthrie LMR 13–13.5 ha/worker [EDGE-SDG2025]; IOI estate-wide 4G for IoT [IOI2026].
**Platform comparison:** Azure 83 / AWS 78 / Google 68 / IBM 49 → recommend **Azure**; justify by Malaysia West region + live IoT Hub (Google IoT Core retired 2023 [GCP-IOTCORE], IBM Watson IoT retired 2023 [REG-WIOT]).
**Why cognitive > conventional:** table in `01_problem_evidence.md` §4. **References:** 60+ verified entries in `sources.md` (need ≥10).

## Presentation
- **Hook:** "Malaysia produced a record 20.3 million tonnes of palm oil in 2025 — yet 80 % of the people who harvest it are foreign workers, and the industry is 30,000 short again." [MPOB2025] [STAR-LAB2026] [EDGE-LAB2026]
- **Money line:** half a percentage point of oil extraction lost to under-ripe bunches ≈ **RM2.2 billion** a year *(calc.)*.
- **Invisible enemy:** Ganoderma can cut plantation economics by 43 % in six months and stays invisible until the trunk is 60–70 % rotten [KHOO2023].
- **Compliance clock:** EUDR applies **30 Dec 2026** — weeks after our presentation [HL-EUDR2026].
- **Demo story:** satellite flags a block → drone model finds suspect palms → soil node says "lime, pH 3.8" with a reason → camera grades a bunch "ripe, 0.93". Every decision is explained (Part 3 novelty).

## Verification
Risky things to test:
1. **Dataset licences/attribution:** D1–D6 CC BY 4.0, D10 Apache 2.0, Sentinel "Copernicus Sentinel data [Year]" notice required [COPERNICUS-LEGAL]; check credits appear in report + dashboard. Roboflow datasets unverified → must not be used.
2. **Data leakage:** D4 must keep its geographic split; ripeness test on D2 (different country from D1).
3. **ESP32:** no analog sensor on ADC2; pH divider keeps pin ≤3.1 V; ESP32-CAM brownouts on the actual power source; power bank auto-off.
4. **Credit limits:** Azure for Students sign-up with the university email (unverified acceptance); no GPU; credit expiry; Kaggle phone verification; GCP trial must not be relied upon.
5. **Simulated data labelling:** M2 and M6 outputs must say SIMULATED/rule-based in UI and report.
6. **Claims check:** RM7.5–20 bn is an employer-federation estimate; RM2.2 bn is our calculation — both must be labelled as such.
