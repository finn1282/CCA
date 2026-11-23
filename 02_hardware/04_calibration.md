# 04 — Calibration Procedures

> Owner: Hardware. Firmware: `firmware/soil_node/soil_node.ino` (Serial 115200, type `help`).
> All captured values are stored in the ESP32's flash (NVS) and survive reboots/reflashing of the same sketch.
> Record every calibration in the log table (§6) and set `cal_id` — it travels in every payload as the audit trail (INTERFACES §2, D18).

## 0. Before you start
- Do the pH divider check **first** (§2.1), before the pH board's PO wire touches the ESP32.
- Room temperature, DS18B20 connected (it gives the buffer/solution temperature).
- Cups: `BUFFER 6.86`, `BUFFER 4.01`, `RINSE` (distilled water), and the three TDS demo cups `REFERENCE`, `PLAIN`, `NUTRIENT` (§3).
- Buffer sachets: dissolve each in the stated volume (usually 250 mL) of distilled water; label with today's date. Use them the same day.

## 1. Capacitive moisture (two-point: dry / wet) [DFR-SEN0193]
The output is inverse: dry = high mV. The firmware maps linearly: `pct = (dry − mV) / (dry − wet) × 100`, clamped 0–100.
1. On the OLED, long-press until the **CALIB** page; it shows live `moist … mV`.
2. **Dry point:** probe clean and dry, held in air. Hold the button **5 s** → OLED shows `dry=XXXX` (or type `cal dry`).
3. **Wet point:** put the probe in a cup of water up to the marked line (never wet the electronics). Hold 5 s → `wet=XXXX` (or `cal wet`).
4. Check: typical clones give dry ≈ 2.6–3.0 V, wet ≈ 1.2–1.6 V (unverified, per unit). Spread < 800 mV → probe faulty or powered from the wrong rail.
5. **ADC range note (Verification D-07):** at 11/12 dB attenuation the ESP32 ADC is accurate only over ≈150–2450 mV [ESP32-DS]; a dry point above 2.45 V is read compressed/non-linear, so resolution near "dry" (0–15 %) is coarse. This is acceptable because the value is relative and the demo threshold (30 %) lies in the linear part. If the bench dry reading exceeds 2.45 V *and* the dry end matters, add a 10 kΩ (top) / 33 kΩ (bottom) divider on AO (×0.77) and recalibrate both points — no firmware change needed.
6. Insert into the pot soil at the same depth every time; dry pot soil should read < 30 % (IRRIGATE), freshly watered > 50 %.
The result is **relative moisture of the calibrated span, not volumetric water content** — say so if asked.

## 2. pH — two-point with 6.86 and 4.01 buffers (D21) [RAW-PH]
### 2.1 Electrical check and offset (once)
1. pH board on 5 V and GND only, PO **not** connected to the ESP32.
2. Short the BNC centre to its shield (or leave the probe in 6.86 buffer). Measure PO with a multimeter; turn the potentiometer next to the BNC (offset) until PO ≈ **2.50 V**.
3. Put the probe in 4.01 buffer: PO should rise (≈ +0.5 V). Note the maximum you see. With the 10 k/20 k divider the pin voltage is PO × 0.667 — it must stay **≤ 3.1 V** (PO ≤ 4.6 V). Only then connect PO through the divider to GPIO35.

### 2.2 Two-point calibration
1. Rinse the probe in `RINSE`, blot (do not wipe) the bulb.
2. Probe + DS18B20 into `BUFFER 6.86`. Wait until the Serial `[read]` PO value is stable to ±0.005 V (30–60 s).
3. Type `cal ph686`.
4. Rinse, blot, probe + DS18B20 into `BUFFER 4.01`, wait, type `cal ph401`.
5. Type `cal show` → check `slope` ≈ **0.16–0.19 V/pH** (ideal 0.18 V/pH at 25 °C [RAW-PH]). Outside 0.14–0.20 → repeat; old/dry electrode or wrong buffer.
6. Verify: back in 6.86 buffer, OLED READINGS page must show 6.86 ± 0.1.
7. Type `cal id 2026-12-DD` (today's date).

Formula used by the firmware:
```
V_PO   = V_pin / 0.667
slope  = (V_4.01 − V_6.86) / (6.86 − 4.01)         [V per pH, at calibration temperature T_cal]
slope_T = slope × (T + 273.15) / (T_cal + 273.15)   [Nernst temperature correction, T from DS18B20]
pH     = 6.86 + (V_6.86 − V_PO) / slope_T
```
Both demo pH bands (4.0, 4.2, 6.5) lie at or near the calibrated range; readings below 4.01 are a short extrapolation — acceptable for a demo, state ±0.1–0.2 pH.

### 2.3 Measuring soil (slurry)
1 part soil : 2.5 parts distilled water by volume, stir 30 s, settle 5 min, dip the probe in the liquid above the sediment [05_hardware_notes §2.2]. Never push the probe into soil; store it in its KCl cap between sessions.
For the "acidic block" cup, a slurry with a few drops of vinegar or a pinch of peat gives pH < 4 (unverified per soil — test at rehearsal).

## 3. TDS (with DS18B20 temperature compensation) [DFR-SEN0244]
Firmware (DFRobot reference formula):
```
V_comp = V / (1 + 0.02 × (T − 25))
TDS    = (133.42·V_comp³ − 255.86·V_comp² + 857.39·V_comp) × 0.5 × K
```
- T comes from the DS18B20 **in the same cup** (move the probe there for TDS/pH steps). If DS18B20 fails, 25 °C is used and `soil_temp_c` is sent as `null`.
- **K (cell constant)**: if you have a known solution or a reference TDS pen, read it and set `cal tdsk <K>` with K = reference ÷ displayed (default 1.0). Otherwise leave 1.0 — the demo rules are **relative to a baseline**, so absolute accuracy is not needed.
- **Baseline for the fertilise rules (INTERFACES §4):** owned by the backend. On the day:
  Three cups (Verification D-01 — a cup used to *set* the baseline can never trigger a rule against it):
  | Cup | Contents | Role | Must read |
  |---|---|---|---|
  | `REFERENCE` | **Pot leachate** (water poured through the pot, collected underneath — not tap water, which can read pH > 6.5) + a **small pinch** of NPK, ~250 mL | Sets the baseline ("adequately fertilised block") | = baseline **and pH 4.2–6.5** (OK) |
  | `PLAIN` | Distilled water | "Nutrient-depleted block" → `fertilise` | **< 0.7 × baseline**, pH **not below 4.0** (else LIME outranks FERTILISE) |
  | `NUTRIENT` | ≈ ½ teaspoon NPK in 250 mL | "Just fertilised block" → `skip_fertiliser` | **> 1.3 × baseline** |
  1. Probes + DS18B20 in `REFERENCE`, wait 30 s → note the dashboard TDS; set it as the device baseline in the dashboard calibration panel (default margin 30 %).
  2. Check REFERENCE shows **OK** (pH 4.2–6.5). Move to `PLAIN`, give the pH electrode **60 s** to settle (distilled water makes glass electrodes drift) → must show FERTILISE, not LIME/WATCH; move to `NUTRIENT` → must show SKIP FERTILISER. If either is inside ±30 %, adjust the pinch in `REFERENCE` (more NPK if PLAIN is not low enough; less if NUTRIENT is not high enough) and re-set the baseline.
  3. Rinse probes in `RINSE` between cups; return them to `REFERENCE` (the demo start state).
  4. The node fetches the baseline (boot + every 5 min) for LOCAL mode; without it, LOCAL mode skips TDS rules.
- pH and TDS are read **sequentially**: the firmware powers the TDS module (GPIO25) only during its own reading, so both probes may sit in one cup.
- Fertiliser decisions are **simulated agronomy** (no published slurry-EC target for oil palm) — the dashboard labels them.

## 4. DS18B20 and DHT22
No calibration. Sanity check: both within ±1 °C of each other in still room air after 5 min. DS18B20 `85.0` or `-127` = wiring fault (firmware sends `null`).

## 5. When to recalibrate
| Item | When |
|---|---|
| Moisture dry/wet | Once per probe; repeat if the probe is moved to another pot/soil |
| pH | On the demo day (morning) and if the 6.86 check drifts > 0.1 |
| TDS baseline | On the demo day, in the room, with the water you will use |
| `cal_id` | Every time pH is recalibrated |
| `cal reset` | Only to return to firmware defaults (keeps `seq`) |

## 6. Calibration log (fill in)
| Date | cal_id | Moist dry / wet (mV) | V6.86 / V4.01 (V) | Slope (V/pH) | T_cal (°C) | TDS K | TDS baseline (ppm) | By |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |

**Build versions (record after the first clean compile):** ESP32 core `____` · ArduinoJson `____` · Adafruit SSD1306 `____` · Adafruit GFX `____` · OneWire `____` · DallasTemperature `____` · DHT sensor library `____` · Adafruit Unified Sensor `____` · soil fw `0.2.6` · cam fw `0.2.6`
