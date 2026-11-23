# 03 — Datasets for Each Model

> Owner: Research. Audience: Software & Cloud AI (+ SW tester). All URLs below were opened/queried on **23 Nov 2026**; licence and size come from the repository's own metadata (Mendeley Data public API, Zenodo API, GitHub API, Kaggle API, GEE catalog). Keys refer to `sources.md`.
> Rule: real data first; where none exists the proxy/simulation is stated and must be labelled **SIMULATED** in code, dashboard and report.

## Summary — recommended primary dataset per model

| Model (outcome) | Primary dataset | Secondary / validation | Status |
|---|---|---|---|
| M1 FFB ripeness classifier (O1) — powers ESP32-CAM demo | **D1** Kamal et al. ordinal ripeness, 4,728 imgs, CC BY 4.0 | **D2** Malaysian outdoor FFB (Johor/N.Sembilan/Perak), 466 imgs, CC BY 4.0 → Malaysian test set / fine-tune | Real data ✅ |
| M2 Harvest-window prediction (O1) | No public bunch-level time series. Use M1 class + ripening-age rule (19–24 weeks after anthesis [RAMLI2026]) | Block-level FFB yield trend from MPOB stats [MPOB2025] for context | **Rule + SIMULATED** ⚠️ |
| M3 Ganoderma / palm-health detector from drone (O2) | **D4** UAV RGB Ganoderma crowns, 1,352 tiles, 9,400 crowns, COCO, CC BY 4.0 | **D5** Oil palm anomaly (healthy/anomalous) UAV, CC BY 4.0 | Real data ✅ (RGB only) |
| M4 Palm tree detection / counting (O2/O4 inventory) | **D4** (same crown boxes, collapse to one class "palm") | D5 | Real data ✅ |
| M5 Satellite NDVI stress / anomaly time series (O2/O4) | **D7** Sentinel-2 L2A (GEE `COPERNICUS/S2_SR_HARMONIZED`) masked with **D9** global oil palm map | D8 Landsat 8/9 L2 | Real data ✅ (unlabelled → anomaly detection) |
| M6 Fertiliser / irrigation recommender (O3) | **No public oil-palm soil-sensor dataset exists.** **SIMULATED** dataset generated from literature thresholds (pH bands [KANANG2026], drainage [AAR-SOIL], water deficit [CARR2011]) + live ESP32 readings | D10 Kaggle Crop Recommendation (Apache 2.0, India, no oil palm) only to demo the ML pipeline; D11 SoilGrids for block soil-pH maps | **SIMULATED + rules** ⚠️ |

## Dataset catalogue (ranked within each use)

### A. FFB ripeness (M1)

| # | Name & URL | Licence | Size / format | Classes | Fit | Rank |
|---|---|---|---|---|---|---|
| D1 | **An Ordinal Dataset for Ripeness Level Classification in Oil Palm Fruit Quality Grading** — Kamal, I.M. et al. (2024), Mendeley Data v1, doi:10.17632/424y96m6sw.1 — https://data.mendeley.com/datasets/424y96m6sw/1 | **CC BY 4.0** | 4,728 high-res images, 1 zip, **272 MB**; stratified train/val/test provided | 5 ordinal: Immature, Partially Ripe, Fully Ripe, Overripe, Decayed | Real-world conditions (Central Kalimantan, Indonesia), varied devices/lighting — best size for training; ordinal labels allow an explainable "ripeness score" | **1 (primary)** |
| D2 | **Outdoor Tenera Oil Palm Fruit Image (FFB dataset)** — Rosbi, M. (2024), Zenodo, https://zenodo.org/records/11114885 (GitHub mirror https://github.com/MunirahRosbi/Outdoor-Tenera-Oil-Palm-Fruit-Image). Described in Omar et al. (2024) *Data in Brief* 55, 110667 [OMAR2024] | **CC BY 4.0** | 1 zip, **1.16 GB**; 466 images (train 371 / test 95) | 5: Damaged 15, Empty 12, Unripe 164, Ripe 201, Overripe 74 | **Malaysian** (Johor, N. Sembilan, Perak), on-tree + ground, labelled by experienced grader. Too small/imbalanced alone → use as **Malaysian hold-out test / fine-tune** (strong report point: "validated on Malaysian estates") | 2 |
| D3 | **Palm ripeness dataset** — Nurul, N. (2024), Mendeley Data, doi:10.17632/zrcf6v69y8.1 — https://data.mendeley.com/datasets/zrcf6v69y8/1 | CC BY 4.0 | 254 images, ~1.1 GB | 3: Masak (ripe) 91, Mengkal (half-ripe) 72, Mentah (unripe) 91 | Smallholder plantations (Indonesia); small, extra augmentation | 3 |
| — | Roboflow Universe projects (e.g. "Oil Palm Fruit Ripeness", "Palm oil fruit bunch") | unverified (site blocked automated access) | ~200 imgs | 4–6 | Not verified → do not use unless a member checks licence manually | — |

**Class harmonisation for M1 (recommendation):** map D1/D2/D3 to 4 classes: `unripe` (Immature/Unripe/Mentah), `underripe` (Partially Ripe/Mengkal), `ripe` (Fully Ripe/Ripe/Masak), `overripe` (Overripe + Decayed); optionally `reject` (Empty/Damaged, D2 only). This matches the response JSON in `INTERFACES.md` (`label`, `confidence`, `explanation`).

### B. Ganoderma / palm health from UAV (M3) and palm detection (M4)

| # | Name & URL | Licence | Size / format | Classes | Fit | Rank |
|---|---|---|---|---|---|---|
| D4 | **UAV RGB Image Dataset for Object Detection of Ganoderma-Affected Oil Palm Trees** — Mimboro, P., Soeparno, H., Soewito, B. and Budiharto, W. (2026), Mendeley Data **v2**, doi:10.17632/s23jvbpnr3.2 — https://data.mendeley.com/datasets/s23jvbpnr3 | **CC BY 4.0** | 1,352 tiles 640×640 (train 1,128 / val 106 / test 118, **geographically disjoint blocks**), COCO JSON, 13 files, **1.12 GB**; GSD ≈ 4 cm | 722 Ganoderma-positive crowns, 8,678 "survey-negative-normal" | Only public UAV Ganoderma set found. Labels come from **field survey records** (not visual), so model learns canopy symptoms of confirmed BSR — good realism. Caveat: "negative" ≠ lab-confirmed healthy; heavy class imbalance (≈1:12) → use focal loss / class weights; report recall on Ganoderma class | **1 (primary for M3 and M4)** |
| D5 | **Oil Palm Tree Detection for Anomaly Identification** — Dominguez Meza, A. and Rituay, P. (2025), Mendeley Data, doi:10.17632/nh7d23dgnw.1 — https://data.mendeley.com/datasets/nh7d23dgnw/1 | CC BY 4.0 | 1 file, 68 MB; RGB from DJI Phantom 4 Multispectral | PalmSan (healthy), PalmAnom (anomalous) | Generic stress/anomaly; good extra data for palm detection | 2 |
| D6 | **Image Dataset of Oil Palm Leaf Diseases** — Rahmanto, O., Julianto, V. and Arrahimi, A.R. (2025), Mendeley Data, doi:10.17632/cp65skff89.1 — https://data.mendeley.com/datasets/cp65skff89 | CC BY 4.0 | 1,583 files, 139 MB, cropped leaf images | healthy / diseased | Leaf-level (not Ganoderma-specific); could back an ESP32-CAM "leaf health" demo mode | 3 |
| — | **GanoTrunk v1** (IEEE DataPort) — 64 trunk-base videos, 830 basidiocarp masks, CC BY 4.0, Indonesia | CC BY 4.0 | 700 MB | Ganoderma / normal | **Requires IEEE DataPort subscription** → not usable unless the university provides access | — |
| — | UAV **multispectral/hyperspectral** Ganoderma data (as used in [KHOO2023]-cited studies) | — | — | — | **No public dataset found.** Report must say so; proxy = D4 (RGB) + Sentinel-2 NDVI (D7) | gap |

### C. Satellite (M5)

| # | Source | Licence | Spec | Use |
|---|---|---|---|---|
| D7 | **Sentinel-2 MSI L2A Harmonized** — GEE ID `COPERNICUS/S2_SR_HARMONIZED`, https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED [GEE-S2] | Copernicus: **free, full and open**; attribution "Copernicus Sentinel data [Year]" required [COPERNICUS-LEGAL] | 2017-03 → present; B4 red & B8 NIR at **10 m**; **5-day revisit**; cloud mask via SCL band or `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` | NDVI/NDRE monthly composites per estate block; anomaly (z-score / isolation forest) flags blocks for drone follow-up. Malaysia is very cloudy → use monthly median + Cloud Score+ |
| D8 | **Landsat 9 C2 L2** — `LANDSAT/LC09/C02/T1_L2` (and LC08) [GEE-L9] | US public domain; credit "courtesy of the U.S. Geological Survey" | 30 m, 16-day | Long history (Landsat 8 since 2013) for multi-year trend (ageing blocks) |
| D9 | **Global map of industrial & smallholder oil palm 2019** — Descals et al. (2021), GEE `BIOPAMA/GlobalOilPalm/v1` (superseded by `v1_2`), doi:10.5281/zenodo.4473715 [GEE-OILPALM] | **CC BY 4.0** | 10 m; classes industrial / smallholder / other | Mask to oil-palm pixels; pick a demo AOI in a real Malaysian estate region (e.g. Johor/Perak) |

Access: Earth Engine is free for **noncommercial/research use** with a registered Cloud project (see `04_cloud_platforms.md`); fallback = Copernicus Browser manual download.

### D. Soil / fertiliser (M6)

| # | Source | Licence | Notes | Use |
|---|---|---|---|---|
| D10 | **Crop Recommendation Dataset** — Ingle, A. (2020), Kaggle, https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset | **Apache 2.0** (Kaggle metadata) | 150 KB CSV; columns N, P, K, temperature, humidity, ph, rainfall, label; **built by augmenting Indian rainfall/climate/fertiliser data**; oil palm **not** a crop label | Only for demonstrating the tabular ML pipeline (e.g. AutoML). **Not agronomically valid for oil palm** — do not present predictions as oil-palm advice |
| D11 | **SoilGrids 250 m v2.0** — ISRIC, https://docs.isric.org/globaldata/soilgrids/SoilGrids_faqs.html [ISRIC-SG] | CC BY 4.0 per ISRIC (licence page not opened — **verify**) | 250 m, 6 depths; `phh2o` (÷10), `soc`, `nitrogen`, `cec`; access via WebDAV/WCS/GEE | Background soil-pH / SOC layer per block on the dashboard |
| D12 | **SIMULATED oil-palm soil-sensor dataset** (to be generated by Software) | own | Rows: moisture %, pH, EC/TDS, soil temp, palm age, soil type → label {ok, fertilise, irrigate, lime, skip}; labels from rules in `05_hardware_notes.md` §3 + noise | Train a small explainable model (decision tree / gradient boosting + SHAP) so the recommendation shows "why". **Must be labelled SIMULATED.** |

**Why no real data for M6:** published oil-palm fertiliser ML work uses leaf-nutrient sampling or satellite imagery from private estates (e.g. Landsat-8 + SVM/RF nutrient classification on a Johor plantation; Indonesian 2,000-leaf-sample PreciPalm prototype — see `02_cognitive_capabilities.md`), and none releases soil-sensor time series. State this in the report as a data gap that the pilot phase closes by logging the estate's own IoT data.

## Practical guidance for Software
1. **M1 (demo critical):** train on D1 (+D3), test on D2 → report both in-distribution and Malaysian accuracy. Transfer learning (MobileNetV3/EfficientNet-B0 or YOLOv8-cls) fits in Colab/Kaggle or Vertex free credit. Add printed D2 test images for the live ESP32-CAM demo.
2. **M3/M4:** YOLOv8n/s on D4 COCO tiles; keep the provided geographic split (no re-shuffling — the dataset authors warn about spatial leakage).
3. **M5:** pre-compute in GEE, export PNG/GeoJSON for the dashboard (no live GEE dependency during the presentation).
4. **Attribution:** every CC BY dataset must be credited in the report reference list and on the dashboard "Data sources" panel.
