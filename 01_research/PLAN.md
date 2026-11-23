# Research — PLAN

## Approach
**Wave 1 (done 23 Nov 2026):** baseline evidence that unblocks every team, in dependency order: hardware notes → datasets → cloud platforms → problem evidence → short capabilities → baseline brief. Every fact opened and cited; dataset licences/sizes taken from repository APIs (Mendeley, Zenodo, GitHub, Kaggle, GEE catalog); each file committed and pushed as soon as finished.

**Later waves (on demand):** members append rows to `REQUESTS.md`; the Lead dispatches a wave; Research answers in a new file (`06_…`, `07_…`) or extends an existing one, adds sources to `sources.md` with a stable key, updates the row's Status/Answer file, and commits. Expected candidates: deeper Ganoderma-satellite literature, yield forecasting, MSPO standard clause text, PDPA 2010 constraints, Part 3 novelty precedents.

## Ideas (beyond the brief)
1. **"Explain-to-audit" loop (Part 3 novelty):** every AI recommendation (fertilise/lime/irrigate, Ganoderma screening, ripeness grade) is stored with its explanation and geolocation as an **MSPO/EUDR evidence log** — turns compliance from paperwork into a by-product of operations. Grounded in MSPO 2022 records/traceability/GHG criteria [MPOCC-P21] and EUDR geolocation gaps [MSPO-EFI2025].
2. **Satellite → drone → ground "cascade":** cheap Sentinel-2 anomaly screening of all blocks triggers targeted drone flights, which trigger ground GSM tests only for top-ranked palms — saves scarce labour (links P1 and P2).
3. **Harvester-allocation optimiser:** use ripeness predictions to route the limited harvest crew to the blocks with most ripe bunches — directly attacks P1 rather than just reporting ripeness.
4. **Malaysian-validation claim:** train on Indonesian D1, test on Malaysian D2 — report cross-country generalisation (credible, uncommon in student projects).
5. **Extension to other sectors (Part 3, 2 marks):** same stack for rubber (also EUDR-regulated) and cocoa; smallholder mobile app via cooperatives/MPOB.

## Conflicts (evidence vs SPEC / brief)
1. **Ganoderma framing:** SPEC places BSR "under P1/P2". Evidence shows it is a stronger cognitive-computing problem than ageing trees (ageing is capital/policy-bound). → R-P1.
2. **Labour shortage is cyclical**, eased in 2024–25 (yields up on better labour availability) and re-emerging in late 2026 — the brief implies a steady worsening.
3. **EUDR volume exposure is small** (EU = 6.8 % of 2025 exports) — MSPO, not EUDR, is the universal driver.
4. **No public data** for harvest-window prediction (M2), soil-sensor fertiliser model (M6), or UAV multispectral/hyperspectral Ganoderma → simulated/proxy data needed (SPEC §4 anticipates this).
5. **Cloud training on credits is not viable for GPUs**: Azure for Students can't get GPU quota; GCP trial credit excludes Vertex ("Gemini platform") for sign-ups since 16 Nov 2026 and needs a card; SageMaker Studio Lab closed. D4 says "train on cloud if credits allow" — they don't for GPU; train on Kaggle/Colab, deploy on Azure.
6. **"Vertex AI" naming:** Google now calls it "Gemini platform (formerly Vertex AI)" — Report should use both names.

## Proposals
| ID | Proposal | Why (evidence) | Impact on other teams | Lead ruling |
|---|---|---|---|---|
| R-P1 | Re-frame P2 as "Declining stand productivity: **Ganoderma BSR (primary)** + ageing trees" and rank problems P1 (labour/harvest) > P2 (Ganoderma+ageing) > P3 (MSPO/fertiliser) | BSR 9.2 % → >20 %, 43 % loss in 6 months, asymptomatic until 60–70 % infected [IBRAHIM2020] [BORNEO-GANO2025] [KHOO2023]; ageing is capital-bound [SARMIDI2025] | Report Part 1 structure; Presentation story order || ESCALATED to stakeholder (changes problem list); Lead recommends accept, keeping "ageing trees" named in P2 |
| R-P2 | Training platform = **Kaggle (Colab backup)**; deployment = **Azure for Students** (Malaysia West); satellite pre-compute = **Earth Engine** | Credit terms in `04_cloud_platforms.md` | Software: notebooks on Kaggle, API on Azure; Verification: test Azure sign-up early || ESCALATED to stakeholder (changes D4); Lead recommends accept |
| R-P3 | Enterprise recommendation in report = **Microsoft Azure** (83/100), AWS runner-up | Only option with live Malaysian region + live first-party IoT/edge; Google IoT Core & IBM Watson IoT retired | Report Part 2; Software architecture diagram should mirror Azure services || ACCEPTED (D15) |
| R-P4 | Primary datasets: **D1 + D2** (ripeness), **D4** (Ganoderma/palm detection), **Sentinel-2 + oil-palm mask** (satellite), **SIMULATED** (fertiliser) | Verified CC BY 4.0 / open licences; no public soil-sensor data | Software dataset prep; Verification licence checks || ACCEPTED (D16) |
| R-P5 | Demo thresholds: pH 4.2–5.5 OK, <4.0 lime; moisture <30 % irrigate / >80 % drainage; TDS calibrated on the day | [KANANG2026] [AAR-SOIL] [CARR2011] | Hardware firmware + Software rules must use the same numbers (add to INTERFACES) || ACCEPTED (D17) — moisture thresholds labelled demo calibration values; added to INTERFACES v0.1 |
| R-P6 | Buy pH buffer sachets (4.01/6.86) — essential; other parts optional | pH calibration requires buffers [RAW-PH] | Stakeholder purchase; Hardware calibration || ESCALATED to stakeholder (purchase) |
| R-P7 | Ask the lecturer whether Taylor's can issue **Google Cloud education credits** or is in **IBM SkillsBuild** | Both require faculty/university enrolment [GCP-EDU] | Optional; not blocking || ESCALATED to stakeholder (optional) |
| R-P8 | Add the "explain-to-audit" MSPO evidence log as the Part 3 novelty anchor | Idea 1 above | Software (log + dashboard view), Report Part 3, Presentation || ACCEPTED (D18) |
