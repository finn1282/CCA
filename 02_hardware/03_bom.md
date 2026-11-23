# 03 — Bill of Materials

> Owned parts from `components.md`; purchases ruled by the stakeholder (D21, D27). Prices are approximate Malaysian
> marketplace ranges, **unverified** — record the actual price paid in the last column.

## 1. Owned parts (cost RM0 to the project)
| # | Part | Qty used / owned | Used for | Design ref |
|---|---|---|---|---|
| 1 | NodeMCU ESP32 | 1 / 1 | Soil node MCU | `02_system_design.md` §3 |
| 2 | ESP32-CAM + USB base (ESP32-CAM-MB) | 1 / 1 | Capture & upload | §5 |
| 3 | Capacitive soil moisture sensor | 1 / 1 | GPIO34 | |
| 4 | pH electrode E-201-C + signal board | 1 / 1 | GPIO35 via divider, 5 V | |
| 5 | TDS module + probe | 1 / 1 | GPIO32, powered from GPIO25 | |
| 6 | 0.96" OLED (SSD1306, I²C) | 1 / 1 | GPIO21/22 | |
| 7 | DS18B20 probe | 1 / 1 | GPIO4 | |
| 8 | DHT22 | 1 / 1 | GPIO16 | |
| 9 | Resistors: 3 × 10 kΩ, 1 × 4.7 kΩ, 3 × 220 Ω (330 Ω OK) | 7 / kit | Divider (10 k + 2×10 k), 1-Wire pull-up, LEDs | |
| 10 | Breadboards | 1–2 / 2–3 | Node build | |
| 11 | Jumpers M-M, F-M | ~30 / set | | |
| 12 | LEDs green / amber (or yellow) / red | 3 / ~4 | Recommendation | |
| 13 | Push button | 1 / ~2 | Send / page / calibrate | |
| 14 | Power bank | 1 / 1 | Soil node supply | D26 |

## 2. Purchases
| # | Item | Status | Priority | Approx. MYR | Actual MYR |
|---|---|---|---|---|---|
| P1 | pH buffer sachets 4.01 / 6.86 | Approved (D21) | Must | 5–10 | |
| P2 | Distilled (or RO) water, 1 L | Approved (D27) | Must | 3–5 | |
| P3 | Small clear plastic cups ×10 | Approved (D27) | Must | 2–4 | |
| P4 | Water-soluble NPK fertiliser, small pack | Approved (D27) | Must | 5–10 | |
| P5 | Colour A5 prints of FFB (ripe / unripe / overripe) from D1/D2 (CC BY 4.0, attribution on the back) | Approved (D27) | Must | 3–5 | |
| P6 | 2 × micro-USB **data** cables, ≤50 cm | Approved (D27) | Nice | 8–15 | |
| P7 | 2-port power bank ≥2 A/port or 5 V/2 A adaptor | Approved (D27) | Nice | 15–30 | |
| P8 | Spare tactile buttons + LEDs pack | Approved (D27) | Nice | 3–5 | |
| — | Second capacitive moisture sensor | **Not bought** (D27) | — | — | |

**Approved total ≈ RM44–84** (including D21 buffers). Divider and pull-up resistors come from the owned kit.

## 3. Household items for the demo (no purchase expected)
Tray or plate under the pot, paper towels, a spoon for slurry, marker for cup labels ("BUFFER 4.01", "BUFFER 6.86", "RINSE", "REFERENCE", "PLAIN", "NUTRIENT"), tape, a small stand/box to hold the ESP32-CAM ~25–30 cm above the print, USB meter (optional).
