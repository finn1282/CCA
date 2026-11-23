# Presentation Audit 1 (06_presentation @ 1c62d2a vs REPORT @ 6ac2459) — saved by Lead from the Compliance member's text reply
## Verdict
**Meets:**
- D48 (all changes).
- D51: no figures from our own model.
- D23 and D20, apart from one slip (X-05).
- Timing: 750 s = 12:30, Q&A inside 15 min; all 5 members speak.

**Blocks consistency with the report:**
- IoT Hub/DPS still shown (report rev 2 N-10 removed it).
- Citation keys and table numbers are stale.
- The "Why Azure?" answer uses the old wording and hides 89 vs 85.

**Gaps:**
- No Q&A cross-training drill.
- No working fallback when the laptop is the primary backend.
- No offline camera fallback.

## Timing
Overall ≈116 wpm (realistic). Two risks:
- Demo realistically 3:05–3:30 vs 2:45.
- Novelty scene runs 5–10 s over.

## Q&A gaps
Add answers for:
- Why IoT Hub isn't used (Event Grid MQTT is in Malaysia West).
- An estate without SAP (e.g. FGV): AWS would fit better.
- Our biggest risk.
- SawitSense vs MPOB's SawitSCAN.
- Each member's own contribution.
- Why these three organisations (one line).

## Defects
| ID | Sev | Issue | Fix |
|---|---|---|---|
| X-01 | major | IoT Hub/DPS in scene 6, the pins, the hub, the script, the Q&A and STORYBOARD | Layer 2: "Event Grid MQTT broker (certificate-based registration) · Event Hubs · Data Lake Storage · STAC imagery catalogue". SE Asia pin: "Azure ML, confidential ledger, Azure OpenAI — non-personal or hashed data only". Hub: "LoRaWAN → Event Grid MQTT" |
| X-02 | major | Stale citation keys / table numbers | Microsoft n.d.a/b/c and 2026a/b; MPOCC 2023a/b; "Report Tables 5 and 6"; ledger key in scene 9 |
| X-03 | major | "Why Azure?" answer | Own 89 vs 85 ("within scoring noise"), then the three case-critical requirements (SAP; long outages, 45 days validated; audit counterfactuals). Conditional: AWS for an estate without SAP or with reliable connectivity |
| X-04 | major | Laptop-primary has no fallback; hotspot loss not drilled | Restart-backend row with a copy-ready command; "hotspot lost → F + S" row; config.js comment |
| X-05 | minor (D20) | "our Earth Engine run" | "…until the satellite pipeline runs on real Sentinel-2 imagery" |
| X-06 | minor | No offline camera fallback | `simulator.py --image <prepared image>` row + prepare the image |
| X-07 | minor (PDF p.2) | No cross-training | §6 Q&A drill: each member answers two questions from another member's area + a 15 s contribution statement |
| X-08 | minor | Demo overrun | Swap probes in parallel; merge beats when late; skip harvester (not the camera) at 9:40; trim scene 9 |
| X-09 | minor | 43 % secondary citation; clause stamp | Olaniyi & Szulczyk cited in Khoo & Chong; "4.1.3 SOP records (e.g. fertilising)" |
| X-10 | minor | Roadmap / cloud layer drift | Add Functions/App Service; 7–13 day baselines; Power BI/Teams; long term = continuous learning + governance review |
| X-11 | minor | Uncited pH thresholds on the scene 4 card | Reword to the report's knowledge-base form |
| X-12 | minor | Novelty/extension drift | Chip 5 = learning loop + cross-country validation; add mills + the sector-wide benchmark |
| X-13 | trivial | Wording | "foreign plantation workforce"; "non-personal or hashed" |
