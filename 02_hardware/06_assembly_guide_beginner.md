# 06 — Beginner Assembly & Flashing Guide

> For any team member, no prior electronics needed. Build **one sensor at a time**, check the expected Serial
> output, then add the next. Pin numbers: `02_system_design.md` §3. Calibration: `04_calibration.md`.

## 1. Tools & software
- Laptop (Windows/macOS/Linux), the 2 micro-USB **data** cables (D27) — a charge-only cable shows no serial port.
- Multimeter (borrow one for the pH check), small screwdriver (pH potentiometer), tweezers/pliers optional.
- **Arduino IDE 2.x** (arduino.cc) — or `arduino-cli`.
- ESP32 board support: *File → Preferences → Additional boards manager URLs* →
  `https://espressif.github.io/arduino-esp32/package_esp32_index.json`, then *Boards Manager* → install **esp32 by Espressif Systems** (3.x).
- USB driver if no port appears: CP210x (Silicon Labs) or CH340 (WCH), depending on the chip near the USB socket.
- Libraries (*Library Manager*), exact names:
  | Library | Author | Used by |
  |---|---|---|
  | ArduinoJson (7.x) | Benoit Blanchon | both |
  | Adafruit SSD1306 | Adafruit | soil |
  | Adafruit GFX Library | Adafruit | soil |
  | OneWire | Paul Stoffregen et al. | soil |
  | DallasTemperature | Miles Burton | soil |
  | DHT sensor library | Adafruit | soil |
  | Adafruit Unified Sensor | Adafruit | soil |
  WiFi, HTTPClient, WebServer, Preferences and esp_camera come with the ESP32 board package.

## 2. Breadboard basics (2 minutes)
- The long red/blue rails run along the edges: use one red rail = **3V3**, the other red rail = **5V**, both blue rails = **GND** (link the two GND rails).
- In the middle, each column of 5 holes is connected; the centre gap separates the two sides.
- The NodeMCU ESP32 is wide: straddle it across the centre gap (or across two boards) so one row of holes stays free on each side.
- **Always unplug USB before changing wires.** Red = power, black = GND, other colours = signals.

## 3. Flash a test first
1. Plug in the NodeMCU, select *Board* **ESP32 Dev Module**, choose the new *Port*.
2. *File → Examples → 01.Basics → Blink*, change `LED_BUILTIN` to `2`, Upload. The blue LED blinks → toolchain works.
   If upload stalls at "Connecting…", hold the **BOOT** button until it starts writing.

## 4. Wire and test one sensor at a time
Open *Tools → Serial Monitor* at **115200** baud. For each step, flash `firmware/soil_node/soil_node.ino` (after §5 step 1 creates `secrets.h`; WiFi can stay unconfigured for now) and watch the `[read]` line every 10 s. Missing sensors print `nan` and are sent as `null` — that is expected until they are wired.

| Step | Wire | Expected Serial | If wrong |
|---|---|---|---|
| 1 LEDs + button | GPIO18/19/23 → 220 Ω → LED long leg; short leg → GND. Button: GPIO27 ↔ GND | At boot G, A, R flash once; short press triggers an extra `[read]` line | LED reversed → flip it |
| 2 OLED | VCC→3V3, GND, SDA→21, SCL→22 | No `[oled] not found`; screen shows "SawitSense" | Swap SDA/SCL; some boards are 0x3D |
| 3 Moisture | VCC→**3V3**, GND, AOUT→GPIO34 | `moist=..% (2800mV)` in air, ~1300 mV in water (above ~2450 mV the ADC is less accurate — see `04_calibration.md` §1 step 5) | 0 mV → AOUT wire; 3300 mV → powered from 5 V or wrong pin |
| 4 DS18B20 | Red→3V3, black→GND, yellow→GPIO4, **4.7 kΩ between yellow and 3V3** | `T=24.5` (room) | `nan` → pull-up missing; 85.0 → power glitch |
| 5 DHT22 | + →3V3, − →GND, out→GPIO16 (bare sensor: add 10 kΩ out→3V3) | `air=27.3C/65%` | `nan` → wrong pin order, wait 2 s after boot |
| 6 TDS | + → **GPIO25** (not 3V3), − →GND, A→GPIO32; probe in a cup of tap water | `tds=150ppm (0.3V)` tap water, higher in NUTRIENT | 0 ppm always → probe not in water / + wire not on GPIO25 or loose / A wire not on GPIO32 |
| 7 pH (careful) | First do `04_calibration.md` §2.1 with a multimeter. Board V+ → **5V rail (VIN)**, G → GND, PO → 10 kΩ → GPIO35, and GPIO35 → 20 kΩ (two 10 kΩ in series) → GND | `pH≈7.0 (PO 2.50V)` in 6.86 buffer before calibration (rough; defaults assume 2.50 V @ pH 7) | `nan` → board unpowered / PO > 4.9 V; never connect PO directly to GPIO35 |

Type `raw` in the Serial Monitor to print raw millivolts any time.

## 5. Integrate and flash for the demo
1. In `firmware/soil_node/`, copy `secrets.h.example` → `secrets.h` and fill in hotspot SSID/password, `API_BASE`, `API_BASE_LOCAL` (laptop IP on the hotspot, port 8000), `DEVICE_KEY` (from Software) and the root CA (instructions inside the file). **Never commit `secrets.h`** (it is git-ignored).
2. Upload; Serial must show `[wifi] connected …` and, once the backend is up, `[cloud] action=… ev=…`.
3. Calibrate (`04_calibration.md`).
4. **Camera:** in `firmware/cam_node/`, create `secrets.h` the same way (`DEVICE_ID "cam-01"`). Seat the ESP32-CAM on its USB base (camera facing away from the USB socket), *Board* **AI Thinker ESP32-CAM**, Upload (the base handles boot mode; if it fails, hold IO0 on the base, tap RST, release IO0). After upload press **RST**. Serial shows `[cam] ok`, `[wifi] … local page http://<ip>/` and a boot capture `[infer] ripe (0.87) …`.
5. Open `http://<cam-ip>/preview` to aim the camera, then use the dashboard **Capture** button.

CLI equivalent (as used for the compile check):
```
arduino-cli compile --fqbn esp32:esp32:esp32 02_hardware/firmware/soil_node
arduino-cli compile --fqbn esp32:esp32:esp32cam 02_hardware/firmware/cam_node
arduino-cli upload  -p /dev/ttyUSB0 --fqbn esp32:esp32:esp32 02_hardware/firmware/soil_node
```

## 6. Troubleshooting
| Problem | Likely cause | Fix |
|---|---|---|
| No serial port | Charge-only cable / missing driver | Use a D27 data cable; install CP210x/CH340 driver |
| `Failed to connect to ESP32` | Not in boot mode | Hold BOOT (NodeMCU) or IO0 (CAM base) while uploading |
| `secrets.h: No such file` | Not created | Copy `secrets.h.example` → `secrets.h` |
| Board resets when WiFi starts / CAM "Brownout detector was triggered" | Weak USB supply or long cable | Short cable, different port, 2-port ≥2 A bank (D27) [RNT-CAM] |
| Analog values jump wildly or read 4095/0 while WiFi on | Sensor on an ADC2 pin | Only GPIO32–39 for analog [ESPFAQ] |
| Board won't boot with wires attached | Something on GPIO0/2/5/12/15 | Move it; see pin map |
| OLED blank | Wrong address / SDA-SCL swapped | Check wiring; try 0x3D |
| pH stuck at one value / `nan` | Board not on 5 V, probe cap still on, divider wrong | Check VIN 5 V, remove cap, measure PO |
| pH drifts | Probe not settled / TDS interference | Wait 30–60 s; firmware already turns TDS off for pH |
| HTTP −1 on cloud, local works | TLS root CA wrong/rotated | Re-export root CA; emergency `ALLOW_INSECURE_TLS 1` (log it) |
| HTTP 401/403 | Wrong `DEVICE_KEY` / `DEVICE_ID` | Ask Software for the key |
| OLED stays on LOCAL (or LAN when the cloud should work) | Backend unreachable (LAN: cloud down/TLS; node retries cloud every 5 min) | Check laptop IP matches `API_BASE_LOCAL`, firewall allows port 8000 |
| CAM poll never captures | Dashboard command not issued / wrong device id | Check `cam-01`; use local `/capture` page |
| Power bank switches off | Load too low for auto-off detection | Use the 2-port bank or keep laptop/USB meter in line |
