# 07 — Field Evidence (R1 d–e), LoRaWAN/Cellular Field Nodes (R-HW1), Name Check

> Research wave 2, 23 Nov 2026. Keys → `sources.md`.

## R1(d) — Does Ganoderma BSR spread to neighbouring palms?
**Yes — root contact is a recognised pathway, alongside airborne spores.**
- Spread to healthy palms is linked to **contact between roots and inoculum sources such as stumps, trunks and diseased palms**; root-to-root contact between palms facilitates spread, with palm roots reaching **the first four planting rows**; field patch patterns support roots as a main inoculum source; infected debris keeps spreading the pathogen after replanting [KHOO2023] (citing Ariffin et al. 2000; Soepena et al. 2000; Miller et al. 1999; Turner 1965).
- Sanitation at replanting cut BSR incidence to **<1 % vs >13 %** without sanitation [KHOO2023] (citing Ahmad et al. 2012).
- But genetic studies show a **major input of airborne basidiospores** (entering via wounds/cut fronds), so not every new case is a neighbour of an old one [COOPER2011].
- **Implication for the cascade (D18):** when a palm is flagged, raise the risk of palms within ~4 rows (neighbour-risk weighting) — defensible from [KHOO2023]; keep satellite/drone screening for the spore-driven, non-clustered cases [COOPER2011].

## R1(e) — Harvesting round interval and harvester productivity
| Metric | Value | Source |
|---|---|---|
| Recommended harvesting round | **7–13 days**; labour shortages stretched rounds to **20–25 days**, hurting FFB quality | [AHMAD2020] |
| Industry view | optimum **10–12 days**; at least **12–15 days** needed to stop fruit becoming overripe; some estates went **20 days** without harvesting (2020) | [MPOB-NEWS2020] |
| Conventional harvester output | **≈1 t FFB per worker per day** (sickle/chisel); motorised cutter (Cantas) **doubles** productivity and cut estate workers by 30–40 % | [AHMAD2020] |
| Bunches per day (team of 2) | **400–1,000 bunches/day** for palms <3 m; falls to **50–90 bunches/day** when palms exceed 12 m | [AHMAD2020] |
| Workforce context | 2020: 75 % foreign; MAPA estimated RM16 bn/yr losses; 62,000-worker shortage expected | [MPOB-NEWS2020] |
| Land per worker | industry ~8 ha/worker; SD Guthrie 13–13.5 ha (2025) | [EDGE-LAB2026] [EDGE-SDG2025] |

**Use for harvester allocation (D18):** a simulation can assume 1 t FFB/harvester/day (conventional), round length 10–15 days, and productivity falling with palm height (ageing blocks ⇒ tall palms ⇒ 50–90 bunches/day) — this also links P1 and P2 (old tall palms make the labour problem worse).

## R-HW1 — LoRaWAN / cellular soil-sensor field nodes (demo → real deployment)
| Topic | Evidence | Source |
|---|---|---|
| LoRa in a **Malaysian oil palm plantation** (Selangor, 433 MHz, ~1,500 LoS + 300 NLoS measurements) | LoS path-loss exponent 2.34 (125–250 kHz) / 2.9 (500 kHz); **each palm trunk attenuates 5.0–7.6 dB and each canopy 5.5–9.3 dB** (SF12→SF7); multiwall model RMSE 2.74 dB beats Weissberger/ITU-R | [ANZUM2022] |
| Oil-palm LoRa soil node prototype (Malaysia) | ESP32 + LoRa (TTGO) sender with pH + moisture sensors → LoRa receiver → Wi-Fi → ThingSpeak cloud | [RUSLAN2021] |
| Commercial LoRaWAN soil node (moisture, temperature, **EC**) | Range **up to 15 km rural / 2 km urban**; battery **up to 10 years** at 10-min interval (lab, guideline only), 19,000 mAh Li-SOCl₂; IP67/IP68 probe; **AS923** bands supported (Malaysia's plan) | [MILESIGHT-EM500] |
| Low-power LoRaWAN agri node (research) | Optimised hardware/software gives higher autonomy than commercial motes for soil/climate irrigation monitoring | [BORRERO2020] |
| Gateway → cloud | LoRaWAN network server (The Things Stack) **Azure IoT Hub integration**: uplinks become IoT Hub telemetry, **device twins** updated from decoded payloads, downlinks scheduled from desired properties; deployed via ARM template, serverless | [TTS-AZURE] |
| Cellular alternative (NB-IoT) | Maxis NB-IoT active in Klang Valley, Sarawak, parts of Penang and Johor (not nationwide) — vendor claim | [MAXIS-NBIOT] |
| Estate connectivity | IOI: >100 4G/LTE sites across >100 estates (2026) | [IOI2026] |

**Suggested mapping sentence (Hardware/Presentation):** demo ESP32 + Wi-Fi + HTTPS ⇒ production LoRaWAN (AS923) soil nodes → estate gateway → LoRaWAN network server → Azure IoT Hub (device twins) → Azure ML; plan gateway spacing with plantation-specific foliage loss (5–9 dB per canopy) rather than the vendor's 15 km open-field figure.

## (a) Name check — "SawitSense"
- Web searches for "SawitSense" / "Sawit Sense" (23 Nov 2026) found **no existing product, app or company by that name**. Only unrelated hobby datasets containing "sawit" appeared. **No clash found** (trademark registry MyIPO not searched — unverified).
- Nearby names in the Malaysian palm sector to avoid confusion with: **MySawit** and **Tekno Sawit** (MPOB AI-powered smallholder apps announced Mar 2025) [MPOB-APPS2025]; Sawit360; SmartSawitGrading (seen in search results only).
- **Recommendation:** keep **SawitSense**. Optional fallbacks if the stakeholder wants extra distance: *SawitIQ*, *PalmSight AI*, *KebunMind* (unchecked).
- Bonus for Part 3 (novelty vs off-the-shelf): MPOB's MySawit/Tekno Sawit target plantation management and machinery choice [MPOB-APPS2025]; none of the found tools combines satellite + drone + IoT with an explain-to-audit MSPO log.
