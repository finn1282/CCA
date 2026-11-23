# 05 — Hardware Notes for the IoT Soil-Sensor Demo

> Owner: Research. Audience: Hardware member (+ HW tester). Source keys refer to `sources.md`.
> Scope reminder (SPEC §4): the hardware is a **small demo of the IoT soil-sensor layer only**.

## 1. Critical ESP32 facts (affect pin map)

| # | Fact | Consequence for the build | Source |
|---|---|---|---|
| H1 | **ADC2 cannot be used while Wi-Fi is active**; the Wi-Fi driver has priority and `adc2_get_raw()` fails. | Put **all analog sensors (moisture, pH, TDS) on ADC1 pins** of the NodeMCU ESP32 (GPIO32, 33, 34, 35, 36/VP, 39/VN). GPIO34–39 are input-only, which is fine for sensors. Do **not** use GPIO0/2/4/12–15/25–27 for analog. | [ESPFAQ] |
| H2 | ESP32 ADC input must stay within 0–3.3 V (effective top lower on some chips); internal reference ≈1.1 V; default inter-chip error up to **±6 %**; two-point calibration recommended. | Use 11/12 dB attenuation, average ≥10 samples, apply `analogReadMilliVolts()` (uses eFuse calibration) rather than raw counts; keep sensor signals ≤ ~3.1 V. | [ESPFAQ] |
| H3 | Strapping pins: GPIO0, 2, 5, 12 (MTDI), 15 (MTDO) — their level at boot matters. | Avoid wiring pull-ups/sensors to GPIO12 (wrong level can set flash voltage and stop boot). Buttons on GPIO0 only if intended. | [ESPFAQ] |
| H4 | Datasheet: two 12-bit SAR ADCs, 18 channels; **GPIO34–39 input-only, no internal pull-up/down**; five strapping pins (GPIO0, 2 boot mode; others). ADC accuracy at 11 dB attenuation (atten = 3) is specified for **150–2450 mV (±60 mV)**; above ~2450 mV (raw >3000) accuracy is worse [ESP32-DS]. | Keep analog signals ≤ ~2.45 V where accuracy matters: pH via 10k/20k divider stays ≤2.5 V even at pH 0 (fine for pH 3–9); TDS 0–2.3 V fine; **capacitive moisture dry-air reading may sit above 2.45 V** → treat the very dry end as less accurate, or add a divider. | [ESP32-DS] |
| H5 | Azure TLS endpoints chain to **DigiCert Global Root G2** (among other roots listed by Microsoft); Baltimore CyberTrust Root was removed from Azure's CA list on 8 Oct 2024 [AZ-CA]. | Firmware doing HTTPS to Azure should pin/embed **DigiCert Global Root G2** (and ideally a second listed root, e.g. Microsoft RSA Root CA 2017) — not Baltimore. | [AZ-CA] |

## 2. Sensor-by-sensor notes

### 2.1 Capacitive soil moisture sensor (v1.2-style)
- DFRobot's reference capacitive sensor (SEN0193) runs on **3.3–5.5 V** and outputs **0–3.0 V** analog; calibration is two-point: record the reading **in air (dry boundary)** and **in water (wet boundary)**, then map linearly to 0–100 % [DFR-SEN0193]. Generic v1.2 clones behave similarly but their exact span differs per unit → **calibrate the actual probe** (unverified per-clone values).
- Output is *inverse*: drier soil = higher voltage.
- Power it from **3.3 V** so the output can never exceed the ADC range. Do not submerge the electronics above the marked line; coat the PCB edge with nail polish/epoxy if the demo runs long (common practice, unverified).
- Result is *relative* moisture (% of calibrated span), **not** volumetric water content — say so on the dashboard.

### 2.2 pH electrode E-201-C + signal board (typically the "PH-4502C" board)
- Board needs **5 V supply** (~0.5 W); pins PO (analog pH), TO (temperature-related), DO (comparator) [RAW-PH]. Offset calibration: short the BNC centre to shield and set POT1 so **PO ≈ 2.500 V (= pH 7)**, then fine-tune in pH 7.00 buffer; pH = 7 + (V_offset − V_meas)/slope, slope ≈ **0.18 V/pH** at room temperature; accuracy ≈ ±0.1 pH, response up to ~60 s, drifts → recalibrate [RAW-PH]. Some listings state a 0–3 V output span [CIRKIT-PH], but with a 2.5 V offset and 0.18 V/pH, PO reaches ≈3.76 V at pH 0, so assume it **can exceed 3.3 V**.
- **Level handling is mandatory** for the ESP32: PO → resistor divider → ADC1 pin. [RAW-PH] suggests a 2:1 divider (10 k/10 k). Recommended: **10 kΩ top / 20 kΩ bottom (×0.667)** → pH 0 ≈ 2.5 V at the pin, better resolution than ×0.5 while staying safe. **Measure the real PO extremes with a multimeter first**, then recompute the formula with the divider ratio (V_PO = V_pin / 0.667).
- E-201-C is a **glass liquid electrode** — never push it into soil (breakage, clogged junction). The agronomically correct method is a **soil:water slurry (e.g. 1:2.5) measured after settling**; for the demo, pour water through the pot and measure the leachate, or use small cups of "healthy" vs "acidic" soil slurry. Store the probe wet in its KCl cap.
- Readings drift with temperature; the DS18B20 value can be used for software temperature compensation.

### 2.3 TDS module (EC proxy for nutrient level)
- DFRobot Gravity TDS reference design: **3.3–5.5 V supply, 0–2.3 V analog output**, 0–1000 ppm, ±10 % FS at 25 °C, **no built-in temperature sensor** — compensation needs an external temperature value [DFR-SEN0244]. → **Fully 3.3 V-compatible; no divider needed.** Generic clones usually copy this board (verify output with a multimeter).
- TDS probe is designed for liquids → measure the **same soil slurry / leachate** as pH. Use the DS18B20 temperature for compensation. EC (µS/cm) ≈ TDS(ppm) / 0.5 (the factor used by the DFRobot sample code; label as approximation).
- Do **not** run the TDS and pH probes in the same cup simultaneously — the TDS excitation signal interferes with the pH electrode (widely reported by makers; unverified formally). Read them sequentially or in separate cups.

### 2.4 DS18B20 / DHT22 / OLED (quick facts)
- DS18B20 (1-Wire) needs a **4.7 kΩ pull-up** from data to 3.3 V (resistor kit has it). Any free GPIO (e.g. GPIO4).
- DHT22: 3.3 V OK, one digital GPIO, min 2 s between reads.
- 0.96" OLED (SSD1306, I²C): SDA GPIO21, SCL GPIO22 default.

### 2.5 ESP32-CAM (AI-Thinker)
- Needs a **stable 5 V supply**; weak USB/cables cause the "Brownout detector was triggered" reset loop [RNT-CAM]. Power from the USB base on a short data cable or a 5 V/2 A source.
- Flashing: GPIO0 → GND (the USB base handles this) [RNT-CAM].
- With PSRAM use up to UXGA (1600×1200); without PSRAM fall back to SVGA [RNT-CAM]. For the demo, **capture VGA/SVGA JPEG and POST to the cloud model** — do not attempt on-device inference of a ripeness CNN (no meaningful TinyML headroom alongside the camera driver; on-device inference is out of scope).
- Few free GPIOs (SD card + camera use most); keep the CAM as a pure "capture & upload" node.
- Many boards ship with the external-antenna resistor selected → weak Wi-Fi; place it close to the hotspot [RNT-CAM].

### 2.6 Power
- Power bank → NodeMCU via USB (5 V) is fine for the soil node. If one bank powers both boards, use a **2-port bank ≥2 A**; the CAM's Wi-Fi bursts cause brownouts on weak ports (see 2.5). Many power banks auto-shut-off at low current draw — test for ≥15 min idle before the presentation.

## 3. Agronomic thresholds for the demo (oil palm)

| Parameter | Evidence | Demo rule (labelled as "demo thresholds derived from literature") |
|---|---|---|
| Soil pH | Soil-nutrient status classification for oil palm: pH **<3.5 very low, 3.5–4.0 low, 4.0–4.2 moderate, 4.2–5.5 high (good), >5.5 very high** [KANANG2026]. Malaysian land-suitability criteria: pH **>4.0 desirable**, 3.5–4.0 minor limitation, <3.5 serious [AAR-SOIL]. Liming is the standard correction for acid soils [KANANG2026]. | **pH < 4.0 → "LIME"** (red); **4.0–4.2 → watch** (amber); **4.2–5.5 → OK** (green); **> 6.5 → "check / stop liming"** (amber; >5.5 is outside the typical oil-palm band but not harmful per se). |
| Soil water | Oil palm yield falls **~10 % for every 100 mm increase in soil water deficit** (≈20–25 kg FFB/ha per mm) [CARR2011]; irrigated palms in a dry Malaysian site yielded **56 % more** over 23 years [AFANDI2023]. | Relative moisture from the calibrated capacitive probe: **< 30 % → "IRRIGATE"**; 30–80 % OK; **> 80 % → "waterlogged / check drainage"** (oil palm prefers moderately well to well drained soil [AAR-SOIL]). The % cut-offs are **demo calibration assumptions**, not published values — say so. |
| Nutrient level (EC proxy) | No published oil-palm EC target found for slurry TDS (gap). Fertiliser is ~30 % of estate production cost and a 40 % cut can reduce yields ≥20 % over 18–24 months [STAR-FERT2026] → both under- and over-application matter. | Calibrate on the day: tap water vs. water + a pinch of NPK fertiliser. Rule: **TDS below "low" calibration point → "FERTILISE"**, above "high" point → "over-fertilised: skip round (saves cost, reduces runoff)". Label as **simulated agronomy**. |
| Temperature/RH | Context only (oil palm: hot, humid tropics). | Display; use soil temp for pH/TDS compensation. |

## 4. Proposed optional purchases (stakeholder chooses; prices are approximate, **unverified** Shopee/Lazada Malaysia ranges at time of writing — confirm before buying)

| Item | Why | Approx. MYR |
|---|---|---|
| pH buffer powder sachets (pH 4.01 / 6.86 / 9.18) | Required for two-point pH calibration — without it the pH reading is not credible. **Strongly recommended.** | 5–10 per set (unverified) |
| Logic-level/divider: none needed (resistor kit covers it) | — | 0 |
| Small plastic cups + distilled water | Soil slurry method for pH/TDS | 5 (unverified) |
| Second capacitive moisture sensor | Compare "dry block" vs "wet block" pots side-by-side (more convincing demo of block-level recommendations) | 5–10 generic clone (unverified); branded DFRobot SEN0193 from Digi-Key MY RM24.08 (qty 1, ex-tax, checked 23 Nov 2026) [DIGIKEY-SEN0193] |
| 5 V / 2 A USB wall adaptor or 2-port power bank | Prevents ESP32-CAM brownouts | 15–30 (unverified) |
| FTDI USB-TTL adapter | Only if the ESP32-CAM USB base fails | 8–15 (unverified) |
| Printed FFB photos (ripe/unripe/overripe) in colour, A5 | Camera target for the ripeness demo | ~5 printing |

## 5. Things to tell the HW tester
1. Verify no analog sensor is on an ADC2 pin while Wi-Fi runs (H1).
2. Measure pH board max output before connecting to ESP32; confirm divider keeps it ≤3.1 V.
3. Test ESP32-CAM upload with Wi-Fi on the actual presentation hotspot and power source (brownouts).
4. Check power bank doesn't auto-off.
