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
| 0:00 | Start state (D-10): pot dry, moisture probe in soil; pH + TDS + DS18B20 in **REFERENCE** cup. Point at pot + node | Dashboard live panel; OLED "SawitSense CLOUD" | "This pot stands in for one management block. The node measures moisture, pH, nutrients and temperature, and sends them to SawitSense every ten seconds." |
| 0:15 | Pot is dry (not watered since rehearsal) | Red LED, OLED **IRRIGATE** "moist 24%<30%" (only rule firing: pH OK, TDS = baseline); dashboard reason + counterfactual | "It isn't just a number — it gives an action and the reason: moisture 24 %, below 30 %. It would be OK at 30 %." |
| 0:35 | Pour ~100 mL water; press button (send now) | Moisture rises → **OK, green** (probes still in REFERENCE); new evidence-log row | "Every decision is logged with its reading number and calibration date — the audit trail MSPO needs for fertiliser and soil records." |
| 1:00 | Rinse; probes into **PLAIN** (distilled water) cup, wait ~60 s for pH to settle, press button | TDS < 0.7 × baseline → amber **FERTILISE (simulated)** | "This cup is a nutrient-depleted block. Nutrients are low against this block's baseline, so it recommends fertilising — labelled simulated agronomy." |
| 1:25 | Rinse; probes to **NUTRIENT** cup, press button | TDS > 1.3 × baseline → **SKIP FERTILISER** | "After fertiliser, it says skip the next round — saving cost and runoff. Fertiliser is about 30 % of estate cost." |
| 1:50 | Hold A5 FFB print under the ESP32-CAM; operator clicks **Capture** | Dashboard: label + confidence + heatmap | "At harvest time the same platform grades bunches: ripe, 0.87 — and the heatmap shows what the model looked at." |
| 2:20 | Wrap | Dashboard overview | "Field sensors, camera and satellite all flow into one explained, auditable decision." |
Optional (if time): **acidic** cup → red **LIME** "pH 3.8<4.0".

## 3. One backend at a time (D39)
- **At the rehearsal, pick the primary:** cloud (Azure) if it is deployed and stable on the presentation hotspot, otherwise the laptop.
- Set `API_BASE` on both boards to the primary; `API_BASE_LOCAL` = laptop (only used if the primary fails). If the laptop is the primary, see the tag note below.
- Open the dashboard **on the primary** only. Both backends use the same `SAWIT_DEVICE_KEYS`.
- OLED tags follow the URL scheme (v0.2.6): an `https://` base shows **CLOUD**, an `http://` (laptop) base shows **LAN** — so if the laptop is the primary, the OLED honestly says LAN. When the laptop is primary, set `API_BASE_LOCAL ""` (or the same URL; the node does not retry an identical URL).
- If the primary fails on stage, the nodes switch to LAN by themselves; the operator then opens the laptop dashboard (`http://localhost:8000`).

## 4. Setup timeline (venue)
| T− | Task |
|---|---|
| Day before | Full rehearsal on the **same phone hotspot** and power; calibrate moisture; charge power bank + phone; record the fallback video |
| Morning | pH two-point calibration (`04_calibration.md` §2), set `cal_id`; prepare cups (fresh buffers) |
| 30 min | Check the **primary** backend `GET /api/v1/health`; start the laptop server as standby with the same `SAWIT_DEVICE_KEYS` |
| 15 min | Table layout (`02_system_design.md` §7); power bank → soil node; laptop USB → CAM |
| 10 min | Hotspot on; both nodes join (OLED network page shows IP, CAM Serial shows IP) |
| 8 min | Probes in **REFERENCE** cup → set TDS baseline in dashboard; dip-check PLAIN (FERTILISE) and NUTRIENT (SKIP); probes back to REFERENCE; check node shows CLOUD; one test capture |
| 5 min | Dry soil check (IRRIGATE showing); dashboard on projector; probes rinsed, pH probe in water cup |

## 5. Fallbacks (decide fast — operator calls it)
| Failure | Symptom | Fallback | Time |
|---|---|---|---|
| Venue WiFi blocked/captive | Nodes don't connect | Phone hotspot is **primary** already; WIFI_SSID_2 = venue as spare | 0 s |
| Cloud API down / slow | OLED tag changes CLOUD → **LAN** | Laptop runs the same API (`API_BASE_LOCAL`); nodes fall back automatically and retry the cloud every 5 min; operator switches dashboard URL to localhost | 10 s |
| TLS certificate error (HTTP −1 on cloud only) | LAN tag, local base works | Continue on local base; do **not** reflash on stage | 0 s |
| No network at all | OLED **LOCAL** + "NO NET", buffer count rising | Demo runs on OLED/LEDs (LOCAL decisions); explain buffering; buffered readings replay first with `buffered:true` and `age_s` when the link returns | 0 s |
| Dashboard Capture does nothing | No new result after 5 s | Open `http://<cam-ip>/capture` on laptop; else press RST on CAM (capture on boot) | 10 s |
| CAM brownout loop | CAM Serial "Brownout detector was triggered" | Move CAM to the 2-port power bank / shorter cable | 30 s |
| Sensor reads `--` | OLED shows `--`, payload `null`; all soil sensors null → amber **NO DATA** | Say "failed sensors are sent as null, never faked" — reseat the wire, continue | 0 s |
| Everything fails | — | Play recorded video (laptop desktop, 2:30) | 5 s |

## 6. Pre-show checklist
- [ ] `secrets.h` filled on both boards (hotspot SSID, `API_BASE` = primary chosen at rehearsal, `API_BASE_LOCAL` = laptop IP on hotspot, device keys)
- [ ] Laptop server started with the same `SAWIT_DEVICE_KEYS` as the cloud; dashboard opened on the primary only
- [ ] Laptop IP on hotspot noted and matches `API_BASE_LOCAL` (set a fixed IP if the phone allows)
- [ ] Power bank stays on ≥15 min at node load (auto-off test)
- [ ] Laptop power saving / sleep off; USB ports stay powered
- [ ] pH calibrated today, `cal show` slope 0.16–0.19 V/pH, `cal_id` = today
- [ ] REFERENCE cup made from **pot leachate** (not tap water); TDS baseline set from it
- [ ] pH check 1: REFERENCE reads **4.2–6.5** (OK, green — else WATCH spoils the 0:35 beat)
- [ ] pH check 2: PLAIN reads **not below 4.0** after 60 s (else LIME outranks FERTILISE)
- [ ] PLAIN reads < baseline × 0.7, NUTRIENT > baseline × 1.3
- [ ] Start state: pot dry, probes in REFERENCE, OLED shows IRRIGATE only
- [ ] Pot soil dry enough for IRRIGATE (< 30 %)
- [ ] Cups labelled and filled; rinse water; paper towels; tray
- [ ] FFB prints (ripe + one other class) and attribution on the back
- [ ] CAM framing checked with `/preview` at 25–30 cm
- [ ] Fallback video on desktop; local server command ready
- [ ] No analog wire on an ADC2 pin; pH pin ≤ 3.1 V (Verification checks [ESPFAQ] [RAW-PH])
