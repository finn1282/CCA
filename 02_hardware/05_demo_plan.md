# 05 — Live Demo Plan (2–3 min)

> Owner: Hardware, for Presentation. The demo is one short segment of the 15-minute talk (SPEC §4): it shows the
> IoT soil-sensing layer and the camera path feeding SawitSense's explained decisions. Contract: INTERFACES v0.2.

## 1. Roles
| Role | Who | Does |
|---|---|---|
| Presenter | `[Member X]` | Speaks, pours water/nutrient, holds the FFB print |
| Operator | `[Member Y]` | Laptop: dashboard on projector, Capture button, fallback switching |

## 2. Script (target 2:30)
| Time | Action (on the table) | What the audience sees | Line (say) |
|---|---|---|---|
| 0:00 | Point at pot + node | Dashboard live panel; OLED "SawitSense CLOUD" | "This pot stands in for one management block. The node measures moisture, pH, nutrients and temperature, and sends them to SawitSense every ten seconds." |
| 0:15 | Pot is dry (not watered since rehearsal) | Red LED, OLED **IRRIGATE** "moist 24%<30%"; dashboard reason + counterfactual | "It isn't just a number — it gives an action and the reason: moisture 24 %, below 30 %. It would be OK at 30 %." |
| 0:35 | Pour ~100 mL water; press button (send now) | Moisture rises → OLED/LED change (green or next action); new evidence-log row | "Every decision is logged with its reading number and calibration date — the audit trail MSPO needs for fertiliser and soil records." |
| 1:00 | Probes (pH + TDS + DS18B20) into **PLAIN** leachate cup, press button | pH OK, TDS low → amber **FERTILISE (simulated)** | "pH 5.1 is in the oil-palm band. Nutrients are low against this block's baseline, so it recommends fertilising — labelled simulated agronomy." |
| 1:25 | Move probes to **NUTRIENT** cup, press button | TDS jumps → **SKIP FERTILISER** | "After fertiliser, it says skip the next round — saving cost and runoff. Fertiliser is about 30 % of estate cost." |
| 1:50 | Hold A5 FFB print under the ESP32-CAM; operator clicks **Capture** | Dashboard: label + confidence + heatmap | "At harvest time the same platform grades bunches: ripe, 0.87 — and the heatmap shows what the model looked at." |
| 2:20 | Wrap | Dashboard overview | "Field sensors, camera and satellite all flow into one explained, auditable decision." |
Optional (if time): **acidic** cup → red **LIME** "pH 3.8<4.0".

## 3. Setup timeline (venue)
| T− | Task |
|---|---|
| Day before | Full rehearsal on the **same phone hotspot** and power; calibrate moisture; charge power bank + phone; record the fallback video |
| Morning | pH two-point calibration (`04_calibration.md` §2), set `cal_id`; prepare cups (fresh buffers) |
| 30 min | Start backend (cloud) + local fallback server on laptop; check `GET /api/v1/health` |
| 15 min | Table layout (`02_system_design.md` §7); power bank → soil node; laptop USB → CAM |
| 10 min | Hotspot on; both nodes join (OLED network page shows IP, CAM Serial shows IP) |
| 8 min | Set TDS baseline in dashboard from PLAIN cup; check node shows CLOUD; one test capture |
| 5 min | Dry soil check (IRRIGATE showing); dashboard on projector; probes rinsed, pH probe in water cup |

## 4. Fallbacks (decide fast — operator calls it)
| Failure | Symptom | Fallback | Time |
|---|---|---|---|
| Venue WiFi blocked/captive | Nodes don't connect | Phone hotspot is **primary** already; WIFI_SSID_2 = venue as spare | 0 s |
| Cloud API down / slow | OLED shows **LOCAL**, HTTP code ≠ 200 | Laptop runs the same API (`API_BASE_LOCAL`); nodes fall back automatically; operator switches dashboard URL to localhost | 10 s |
| TLS certificate error (HTTP −1 on cloud only) | LOCAL tag, local base works | Continue on local base; do **not** reflash on stage | 0 s |
| No network at all | OLED "NO NET", buffer count rising | Demo runs on OLED/LEDs (LOCAL decisions); explain buffering; buffered readings replay with `buffered:true` later | 0 s |
| Dashboard Capture does nothing | No new result after 5 s | Open `http://<cam-ip>/capture` on laptop; else press RST on CAM (capture on boot) | 10 s |
| CAM brownout loop | CAM Serial "Brownout detector was triggered" | Move CAM to the 2-port power bank / shorter cable | 30 s |
| Sensor reads `--` | OLED shows `--`, payload `null` | Say "failed sensors are sent as null, never faked" — continue | 0 s |
| Everything fails | — | Play recorded video (laptop desktop, 2:30) | 5 s |

## 5. Pre-show checklist
- [ ] `secrets.h` filled on both boards (hotspot SSID, `API_BASE`, `API_BASE_LOCAL` = laptop IP on hotspot, device keys)
- [ ] Laptop IP on hotspot noted and matches `API_BASE_LOCAL` (set a fixed IP if the phone allows)
- [ ] Power bank stays on ≥15 min at node load (auto-off test)
- [ ] Laptop power saving / sleep off; USB ports stay powered
- [ ] pH calibrated today, `cal show` slope 0.16–0.19 V/pH, `cal_id` = today
- [ ] TDS baseline set in dashboard; NUTRIENT cup reads > baseline × 1.3
- [ ] Pot soil dry enough for IRRIGATE (< 30 %)
- [ ] Cups labelled and filled; rinse water; paper towels; tray
- [ ] FFB prints (ripe + one other class) and attribution on the back
- [ ] CAM framing checked with `/preview` at 25–30 cm
- [ ] Fallback video on desktop; local server command ready
- [ ] No analog wire on an ADC2 pin; pH pin ≤ 3.1 V (Verification checks [ESPFAQ] [RAW-PH])
