# contract_test.py results — 2026-11-24 02:44:03 — PASS=156 FAIL=0 OBS=8 BLOCKED=0

| ID | Status | Test | Evidence |
|---|---|---|---|
| BE-01 | PASS | GET /health 200 status ok | 200 {'status': 'ok', 'version': '0.2.6', 'mode': 'local', 'time': '2026-11-23T18:43:56Z', 'ripeness_model': 'm1-effb0-0.1-provisional', 'fertiliser_model': True} |
| BE-02 | PASS | meta thresholds equal §4 (30/80, 4.0/4.2/6.5, margin 0.30) | {"moisture_low": 30.0, "moisture_high": 80.0, "ph_lime": 4.0, "ph_watch_top": 4.2, "ph_high": 6.5, "tds_default_margin": 0.3} |
| BE-03 | PASS | meta action vocabulary == §4 set | ['irrigate', 'drain', 'lime', 'fertilise', 'skip_fertiliser', 'watch', 'ok'] |
| AU-01 | PASS | POST /readings without headers -> 401 | 401 |
| AU-02 | PASS | X-Device-Id without X-Device-Key -> 401 | 401 |
| AU-03 | PASS | wrong X-Device-Key -> 401 | 401 |
| AU-04 | PASS | unknown device id -> 401 | 401 |
| AU-05 | PASS | body device_id != X-Device-Id -> 400 | 400 |
| AU-06 | OBS | camera key accepted on /readings (keys not scoped per endpoint/device type) | 200 |
| VA-01 | PASS | invalid moisture 100.1 -> 422 | 422 |
| VA-02 | PASS | invalid moisture -0.1 -> 422 | 422 |
| VA-03 | PASS | invalid pH 14.01 -> 422 | 422 |
| VA-04 | PASS | invalid tds -1 -> 422 | 422 |
| VA-05 | PASS | invalid moisture as string -> 422 | 422 |
| VA-06 | PASS | invalid seq as string -> 422 | 422 |
| VA-07 | PASS | missing device_id -> 422 | 422 |
| VA-08 | PASS | malformed JSON -> 422 | 422 |
| VA-09 | PASS | v0.2.3 (S-03 retest): garbage / naive / >24 h-future ts treated as null (captured_at=received_at); +08:00 normalised to Z | [] 2026-11-01T02:00:00Z |
| VA-13 | PASS | age_s -1 -> 422 (v0.2.2: int >= 0) | 422 |
| VA-10 | PASS | edge-valid values 0/0/0 accepted (200) | 200 |
| VA-11 | PASS | edge-valid moisture 100, pH 14 accepted (200) | 200 |
| VA-12 | PASS | minimal body (device_id only) accepted, treated as all-null | 200 ['NO DATA', 'check sensors'] |
| TH-01 | PASS | {'soil_moisture_pct': 29.9} -> irrigate/MOIST_LOW/red | 200 ('irrigate', 'MOIST_LOW', 'red', ['IRRIGATE', 'moist 30%<30%']) |
| TH-02 | PASS | {'soil_moisture_pct': 30.0} -> ok/ALL_OK/green | 200 ('ok', 'ALL_OK', 'green', ['OK', 'all in range']) |
| TH-03 | PASS | {'soil_moisture_pct': 80.0} -> ok/ALL_OK/green | 200 ('ok', 'ALL_OK', 'green', ['OK', 'all in range']) |
| TH-04 | PASS | {'soil_moisture_pct': 80.1} -> drain/MOIST_HIGH/amber | 200 ('drain', 'MOIST_HIGH', 'amber', ['DRAIN', 'moist 80%>80%']) |
| TH-05 | PASS | {'soil_ph': 3.99} -> lime/PH_LIME/red | 200 ('lime', 'PH_LIME', 'red', ['LIME', 'pH 3.99<4.0']) |
| TH-06 | PASS | {'soil_ph': 4.0} -> watch/PH_LOW_WATCH/amber | 200 ('watch', 'PH_LOW_WATCH', 'amber', ['WATCH', 'pH 4.00 watch']) |
| TH-07 | PASS | {'soil_ph': 4.19} -> watch/PH_LOW_WATCH/amber | 200 ('watch', 'PH_LOW_WATCH', 'amber', ['WATCH', 'pH 4.19 watch']) |
| TH-08 | PASS | {'soil_ph': 4.2} -> ok/ALL_OK/green | 200 ('ok', 'ALL_OK', 'green', ['OK', 'all in range']) |
| TH-09 | PASS | {'soil_ph': 6.5} -> ok/ALL_OK/green | 200 ('ok', 'ALL_OK', 'green', ['OK', 'all in range']) |
| TH-10 | PASS | {'soil_ph': 6.51} -> watch/PH_HIGH/amber | 200 ('watch', 'PH_HIGH', 'amber', ['WATCH', 'pH 6.51>6.5']) |
| TH-11 | PASS | pH 5.6 -> ok with 'above typical oil-palm band, not harmful' note | All readings within thresholds; pH 5.60 is above the typical oil-palm band (4.2–5.5) but not harmful; TDS baseline not calibrated yet — nutrient rules skipped |
| TH-12 | PASS | TDS rules skipped before calibration (note, no fertilise) | All readings within thresholds; TDS baseline not calibrated yet — nutrient rules skipped |
| TH-13 | PASS | baseline 600 ±30%: TDS 419 -> fertilise/TDS_LOW, simulated=True, led amber/green | fertilise TDS_LOW sim=True ['FERTILISE', 'TDS 419<420'] |
| TH-14 | PASS | baseline 600 ±30%: TDS 420 -> ok/ALL_OK, simulated=False, led amber/green | ok ALL_OK sim=False ['OK', 'all in range'] |
| TH-15 | PASS | baseline 600 ±30%: TDS 780 -> ok/ALL_OK, simulated=False, led amber/green | ok ALL_OK sim=False ['OK', 'all in range'] |
| TH-16 | PASS | baseline 600 ±30%: TDS 781 -> skip_fertiliser/TDS_HIGH, simulated=True, led amber/green | skip_fertiliser TDS_HIGH sim=True ['SKIP FERTILISER', 'TDS 781>780'] |
| TH-17 | PASS | custom margin 0.10 on baseline 1000: 899 fertilise, 900 ok, 1101 skip | fertilise,ok,skip_fertiliser |
| PR-01 | PASS | moist 20 + pH 3.5 + TDS low -> irrigate; actions[] ordered irrigate>lime>fertilise | ['irrigate', 'lime', 'fertilise'] |
| PR-02 | OBS | simulated=true when TDS finding is present even though primary action is irrigate (contract: 'whenever the decision uses simulated agronomy' — acceptable, conservative) | simulated=True |
| PR-03 | PASS | pH 3.5 + TDS high -> lime > skip_fertiliser | ['lime', 'skip_fertiliser'] |
| PR-04 | PASS | pH 4.1 + TDS low -> fertilise > watch, simulated=true | ['fertilise', 'watch'] |
| PR-05 | PASS | moist 85 + pH 3.5 -> drain > lime (led amber per §4 drain row) | drain amber |
| PR-06 | PASS | pH 6.9 + TDS high -> skip_fertiliser > watch(PH_HIGH) | ['TDS_HIGH', 'PH_HIGH'] |
| PR-07 | PASS | non-ok response has counterfactual + confidence in [0,1] | 'Would be OK if moisture ≥ 30%' 0.97 |
| PR-08 | PASS | simulated=false for irrigate without TDS finding | False |
| NU-01 | PASS | pH null -> no pH rule, OLED 'OK (partial)/no pH reading', stored as null (not fabricated) | ['OK (partial)', 'no pH reading'] stored=None |
| NU-02 | PASS | all sensors null -> ok/NO DATA/check sensors, led amber | ['NO DATA', 'check sensors'] amber |
| NU-03 | PASS | moisture null + pH 3.5 -> other rules still fire (lime) | lime |
| NU-04 | OBS | two sensors null: OLED line 2 names only the first missing sensor | ['OK (partial)', 'no moisture'] |
| NU-05 | PASS | null temperature/RH/rssi accepted, decision unaffected | 200 ok |
| EC-01 | PASS | ec null + TDS 620 -> derived EC 1240, flagged ec_derived=true (approximate) | 1240.0 True |
| EC-02 | PASS | ec supplied -> kept, ec_derived=false | 900.0 |
| EC-03 | PASS | S-13 retest: EC tile labelled '≈TDS/0.5' only when ec_derived |  |
| RP-01 | PASS | buffered replay (buffered=true, older seq) accepted 200 | 200 |
| RP-02 | PASS | replayed row stored with buffered=true and its device ts | {'seq': 4990, 'buffered': True, 'ts': '2026-11-20T08:50:00Z'} |
| RP-03 | PASS | /latest (dashboard 'live' panel) still shows the live seq 5000 after an older buffered replay arrives | latest seq=5000 action=ok (live was seq 5000 ok, ev ev_000045) |
| RP-04 | PASS | /readings history (dashboard chart) ordered by captured_at, replay placed at its true time | [(4990, '08:50:00'), (1006, '18:43:57'), (1007, '18:43:57'), (None, '18:43:57'), (1008, '18:43:57'), (1009, '18:43:57'), (1010, '18:43:57'), (1011, '18:43:57'), (1012, '18:43:57'), (1013, '18:43:57'), (1014, '18:43:57'), |
| RP-07 | PASS | v0.2.2: ts null + age_s 120 -> captured_at = received_at - 120 s | 2026-11-23T18:43:57Z - 2026-11-23T18:41:57Z = 120.0 |
| RP-08 | PASS | ts present -> captured_at = ts (age_s ignored) | 2026-11-20T09:00:00Z |
| RP-09 | PASS | v0.2.6 (D-04/D-16): /latest = most recently captured non-buffered row (old-ts row 5002 and replays ignored; robust to seq reset) | seq=3 buffered=False |
| RP-05 | PASS | v0.2.4 (S-06 retest): identical (device_id, seq) re-POST -> original response, duplicate flag, no new evidence | ev_000050 / ev_000050 dup=True evidence +1 |
| RP-10 | PASS | v0.2.4: same seq with different values (seq reset after reboot) -> stored as new reading | ev_000051 irrigate |
| RP-11 | OBS | duplicate test compares only moisture/pH/TDS/soil-temp: same seq with a different air temp / buffered flag is treated as a duplicate (acceptable for retries) | dup=True |
| RP-06 | PASS | ts null -> server stamps received_at in reply | 2026-11-23T18:43:57Z |
| CA-01 | PASS | GET calibration (device) before any set -> baseline null, margin 0.30, updated_at key present | 200 {'tds_baseline_ppm': None, 'tds_margin': 0.3, 'updated_at': None, 'cal_id': None} |
| CA-02 | PASS | POST use_latest for a device with no reading -> 409 | 409 |
| CA-03 | PASS | POST {'tds_baseline_ppm': 0} rejected 422 | 422 |
| CA-04 | PASS | POST {'tds_baseline_ppm': -5} rejected 422 | 422 |
| CA-05 | PASS | POST {'tds_baseline_ppm': 600, 'tds_margin': 0} rejected 422 | 422 |
| CA-06 | PASS | POST {'tds_baseline_ppm': 600, 'tds_margin': 1} rejected 422 | 422 |
| CA-07 | PASS | POST {} rejected 422 | 422 |
| CA-08 | PASS | POST baseline 592 / 0.25 -> echoes v0.2.1 body | 200 {'tds_baseline_ppm': 592.0, 'tds_margin': 0.25, 'updated_at': '2026-11-23T18:43:57Z', 'cal_id': '2026-12-09'} |
| CA-09 | PASS | GET as device returns stored values; firmware parser caches baseline 592, margin 0.25 | {'tds_baseline_ppm': 592.0, 'tds_margin': 0.25, 'updated_at': '2026-11-23T18:43:57Z', 'cal_id': '2026-12-09'} |
| CA-10 | PASS | GET another device's calibration with own creds -> 401 | 401 |
| CA-11 | PASS | GET with wrong key -> 401 | 401 |
| CA-12 | PASS | GET without device headers (dashboard, open/local mode) -> 200 | 200 |
| CA-13 | PASS | POST use_latest takes the last TDS reading (640) | {'tds_baseline_ppm': 640.0, 'tds_margin': 0.3, 'updated_at': '2026-11-23T18:43:57Z', 'cal_id': '2026-11-23'} |
| CA-14 | OBS | baseline cannot be cleared back to null via POST (contract allows number/null) | 422 |
| CA-15 | PASS | each calibration change logged in evidence chain | 5 calibration records |
| CA-16 | PASS | firmware keeps its cached baseline when backend returns null | {'tds_baseline_ppm': None, 'tds_margin': 0.3, 'updated_at': None, 'cal_id': None} |
| CM-01 | PASS | camera poll with empty queue -> 200 {cmd:none}; firmware ignores | {"cmd":"none"} |
| CM-02 | PASS | dashboard POST capture -> queued | {'queued': True, 'id': 1, 'cmd': 'capture'} |
| CM-03 | PASS | poll returns capture once, then none (consumed) | {'cmd': 'capture', 'id': 1} {'cmd': 'none'} |
| CM-04 | PASS | S-07 retest: repeated Capture clicks coalesce into one pending capture | capture,none,none coalesced=True |
| CM-08 | PASS | S-07 retest: a capture older than 60 s expires instead of firing late | none |
| CM-05 | PASS | unknown command 'reboot' -> 422 | 422 |
| CM-06 | PASS | soil node polling camera's queue -> 403 | 403 |
| CM-07 | PASS | poll without device headers -> 401 | 401 |
| RI-01 | PASS | ripeness without device headers -> 401 | 401 |
| RI-02 | PASS | empty body -> 400 | 400 |
| RI-03 | PASS | body > 5 MB -> 413 | 413 |
| RI-04 | PASS | model loaded: SVGA JPEG (177 KB) from D2 test -> 200 (cold 0.13 s incl. model load) | 200 m1-effb0-0.1-provisional |
| RI-05 | PASS | §3 response: all 8 fields, types, 4-class probs sum to 1, label=argmax=confidence, heatmap named by evidence_id | {"label": "ripe", "confidence": 0.999, "probs": {"unripe": 0.0, "underripe": 0.0, "ripe": 0.999, "overripe": 0.0}, "heatmap_url": "/static/heatmaps/ev_000055.png", "model_version": "m1-effb0-0.1-provisional"} |
| RI-06 | PASS | heat-map PNG served (image / overlay side by side, 448x224) + uploaded image served | 200 (448, 224) img 200 |
| RI-07 | PASS | non-image body -> 400 with message | 400 {"detail":"Not a decodable image: cannot identify image file <_io.BytesIO object |
| RI-08 | PASS | cam_node captureAndUpload() parse: label/confidence/harvest_advice/evidence_id typed as the firmware reads them | lastResult='ripe (1.00) Harvest this round ev_000055 [LAN]' |
| RI-09 | PASS | warm CPU latency over 10 SVGA uploads: p95 < 2 s (live demo budget) | p50 0.075 s, p95 0.078 s, max 0.079 s |
| RI-10 | PASS | ripeness evidence on /latest; override to a ripeness class 200, to a soil action 422 (S-04 retest) | 200/422 |
| RI-11 | PASS | /health exposes the model_version (provisional build is labelled '-provisional') | m1-effb0-0.1-provisional |
| RI-12 | OBS | provisional model still outputs an 'underripe' probability although D2 has no underripe images (column untrained; final D1 model fixes this) | p(underripe)=0.0 |
| RI-13 | PASS | soil POST while 3 ripeness inferences run (inference runs inside db._lock) | soil reply 0.17 s (alone ≈0.01 s) |
| RI-14 | PASS | full-size D2 original (8782 KB) -> 200 or 413 | 413 None |
| FW-01 | PASS | soil_node toJson() payload [boot, no NTP (ts null), cal_id 'uncalibrated', ec null] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000072 |
| FW-02 | PASS | soil_node toJson() payload [NTP time, all sensors OK] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000073 |
| FW-03 | PASS | soil_node toJson() payload [DS18B20 + DHT22 failed (NAN -> null)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000074 |
| FW-04 | PASS | soil_node toJson() payload [all soil probes failed (NAN -> null)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'NO DATA' / 'check sensors' led=amber ev_000075 |
| FW-05 | PASS | soil_node toJson() payload [buffered replay, no NTP, age_s 95, rssi unknown (0 -> null)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000076 |
| FW-06 | PASS | soil_node toJson() payload [dry + acidic + TDS low (3 findings)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'IRRIGATE' / 'moist 24%<30%' led=red ev_000077 |
| FW-07 | PASS | v0.2.3 (S-12 retest): LOCAL == CLOUD action, LED and OLED line 1 on 315 raw boundary combos | [] |
| FW-12 | PASS | v0.2.3: all probes failed -> NO DATA / amber in LOCAL and CLOUD | LOCAL NO DATA/amber CLOUD NO DATA/amber |
| FW-08 | OBS | 1-dp pH rounding moves the effective edges by half a step (raw 3.95 -> 4.0 = watch, not lime; raw 6.54 -> 6.5 = ok); within probe accuracy (±0.1 pH), consistent on both sides | LOCAL(3.95)=watch, LOCAL(3.94)=lime |
| FW-10 | PASS | cam_node pollCommands(): idle reply parsed, cmd != 'capture' -> no capture | {"cmd":"none"} |
| FW-11 | PASS | cam_node captureAndUpload(): raw SVGA JPEG + headers -> 200, reply has label/confidence/harvest_advice/evidence_id | 200 ripe |
| OL-01 | PASS | all 50 /readings replies: oled = 2 non-empty strings ≤16 chars | [] |
| OL-02 | PASS | all replies: led ∈ {green, amber, red} | [] |
| OL-03 | PASS | led matches §4 table for the primary action (NO DATA excepted) | [] |
| OL-04 | PASS | action == actions[0].action (highest priority) in every reply | 0 |
| OL-05 | PASS | only §4 action vocabulary used | [] |
| OL-06 | PASS | every reply carries all §2 response fields | [] |
| OL-07 | PASS | OLED line 2 hard-truncated at 16 chars for extreme values (may cut text) | [] |
| OL-08 | PASS | CLOUD line 1 matches firmware LOCAL wording (no underscores, e.g. 'SKIP FERTILISER') | ['DRAIN', 'FERTILISE', 'IRRIGATE', 'LIME', 'NO DATA', 'OK', 'OK (partial)', 'SKIP FERTILISER', 'WATCH'] |
| DB-01 | PASS | GET / 200; no external (CDN/font) src/href in index.html | [] |
| DB-02 | PASS | all referenced local assets served 200 (incl. vendored Chart.js) | {'/static/style.css': 200, '/static/vendor/chart.umd.min.js': 200, '/static/app.js': 200} |
| DB-03 | PASS | app.js / style.css / harvester.html contain no external URLs | [] |
| DB-04 | PASS | panels present: readings, recommendation(+reasoning), camera, calibration, satellite cascade, harvest, evidence, MSPO |  |
| DB-05 | PASS | footer attributions: D1 Kamal, D2 Rosbi, D4 Mimboro, Descals mask, Copernicus, CC BY 4.0; SIMULATED labels | [] |
| DB-06 | PASS | S-11 retest: Copernicus notice has a year and names Earth Engine | Contains modified Copernicus Sentinel data (2024–2026), processed in Google Earth Engine  |
| DB-10 | PASS | S-14 retest: Chart.js MIT notice restored (banner or LICENSE file served) | LICENSE 200; head '/*! Chart.js v4.4.1 / https://www.chartjs.org / (c) 2023 Cha' |
| DB-07 | PASS | every feed the dashboard polls returns 200 | {'/api/v1/latest': 200, '/api/v1/harvest/plan?crew=12': 200, '/api/v1/screening': 200, '/api/v1/satellite': 200, '/api/v1/compliance/coverage': 200, '/api/v1/evidence?limit=25&non_ok=true': 200, '/api/v1/readings?device_ |
| DB-08 | PASS | harvest + satellite feeds self-label SIMULATED | SIMULATED (satellite pre-compute not yet available) |
| EV-01 | PASS | verify chain intact over 401 records | All 401 records intact (SHA-256 chain) |
| EV-02 | PASS | records linked: prev_hash(n) == hash(n-1), SHA-256 hex |  |
| EV-03 | PASS | GET evidence/{id} of a reading -> input, output, calibration, mspo, rules_version | 200 INTERFACES-v0.2.6 mspo=['TRACEABILITY', 'SOIL_FERTILITY', 'WATER_MGMT'] |
| EV-04 | PASS | unknown evidence id -> 404 | 404 |
| EV-05 | PASS | review approve -> new evidence record referencing target | 200 |
| EV-06 | PASS | override without override_action -> 422 | 422 |
| EV-07 | PASS | override_action outside §4 vocabulary rejected (422) | 422 -> logged as None |
| EV-08 | PASS | override flagged retraining_candidate and listed under target's reviews | 2 reviews |
| EV-09 | PASS | review of unknown id -> 404 | 404 |
| EV-10 | PASS | MSPO audit pack: chain VERIFIED, fertiliser rows marked Simulated=yes | Generated 2026-11-23T18:44:00Z · records: 404 · chain: VERIFIED — All 404 records intact ( |
| EV-17 | PASS | S-10 retest: audit pack prints the current chain head hash | 1be9990bfd3e0297 |
| EV-11 | PASS | compliance coverage lists criteria + chain status | 200 |
| EV-12 | PASS | tamper: edit one record's action -> verify fails at that record | Chain broken at ev_000005 — record edited or removed after it was written |
| EV-13 | PASS | tampered chain -> audit pack says BROKEN |  |
| EV-14 | PASS | restoring the original bytes -> chain verifies again | All 404 records intact (SHA-256 chain) |
| EV-15 | PASS | tamper: delete a middle record -> verify fails | Chain broken at ev_000009 — record edited or removed after it was written |
| EV-16 | OBS | S-10: audit pack now prints the chain head for external anchoring (checked in EV-17); tail truncation is detectable only by comparing with a previously quoted head | head id 404 |
| AD-01 | PASS | SAWIT_DEVICE_KEYS override: demo key rejected (401) | 401 |
| AD-02 | PASS | configured key accepted (200) | 200 |
| AD-03 | PASS | admin token set: calibration POST without token -> 403 | 403 |
| AD-04 | PASS | calibration POST with X-Admin-Token -> 200 | 200 |
| AD-05 | PASS | commands POST without token -> 403 | 403 |
| AD-06 | PASS | device GET calibration still works in token mode | 200 |
| AD-07 | PASS | S-01 retest: dashboard GET calibration with X-Admin-Token (app.js get() now sends it) -> 200; no token -> 403 | 200/403 |
| AD-08 | PASS | GET calibration with ?token= query works (fix path for AD-07) | 200 |
| AD-09 | PASS | review POST without token -> 403 | 403 |
| AD-10 | PASS | S-08 retest: cloud mode reads need the token (403 without, 200 with ?token=) | {'/api/v1/latest': 403, '/api/v1/readings': 403, '/api/v1/evidence': 403, '/api/v1/evidence/export': 403, '/api/v1/evidence/verify': 403, '/api/v1/compliance/coverage': 403, '/api/v1/harvest/plan': 403, '/api/v1/screenin |
| AD-14 | PASS | dashboard shell, harvester shell and /health stay public (page loads, then uses ?token=) | {'/': 200, '/harvester': 200, '/api/v1/health': 200, '/static/app.js': 200} |
| AD-11 | PASS | SAWIT_MODE=cloud reported by /health (dashboard CLOUD pill) | cloud |
| AD-12 | PASS | SAWIT_MODE=cloud, no SAWIT_DEVICE_KEYS: demo key rejected (D-12 retest, fail closed) | 401 |
| AD-13 | PASS | SAWIT_MODE=cloud, no SAWIT_ADMIN_TOKEN: writes refused 403 (fail closed) | 403 |
| SV-01 | PASS | test servers stopped (port free) |  |
