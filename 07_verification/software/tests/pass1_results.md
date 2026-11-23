# contract_test.py results — 2026-11-23 14:17:10 — PASS=132 FAIL=3 OBS=13 BLOCKED=6

| ID | Status | Test | Evidence |
|---|---|---|---|
| BE-01 | PASS | GET /health 200 status ok | 200 {'status': 'ok', 'version': '0.2.2', 'mode': 'local', 'time': '2026-11-23T06:17:06Z', 'ripeness_model': None, 'fertiliser_model': True} |
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
| VA-09 | FAIL | ts 'not-a-timestamp' rejected 422 (contract: ISO-8601 or null) | 200; accepted row then sorts as newest on the chart: newest captured_at='not-a-timestamp' |
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
| EC-03 | OBS | dashboard tile label 'EC (≈TDS/0.5)' shown for all EC values, incl. measured ones |  |
| RP-01 | PASS | buffered replay (buffered=true, older seq) accepted 200 | 200 |
| RP-02 | PASS | replayed row stored with buffered=true and its device ts | {'seq': 4990, 'buffered': True, 'ts': '2026-12-10T08:50:00Z'} |
| RP-03 | PASS | /latest (dashboard 'live' panel) still shows the live seq 5000 after an older buffered replay arrives | latest seq=5000 action=ok (live was seq 5000 ok, ev ev_000043) |
| RP-04 | PASS | /readings history (dashboard chart) ordered by captured_at, replay placed at its true time | [(1036, '06:17:06'), (1037, '06:17:06'), (1038, '06:17:06'), (5000, '06:17:06'), (4990, '08:50:00')] |
| RP-07 | PASS | v0.2.2: ts null + age_s 120 -> captured_at = received_at - 120 s | 2026-11-23T06:17:06Z - 2026-11-23T06:15:06Z = 120.0 |
| RP-08 | PASS | ts present -> captured_at = ts (age_s ignored) | 2026-12-10T09:00:00Z |
| RP-09 | PASS | /latest still = highest-seq non-buffered row after more replays (D-04 retest) | seq=5002 buffered=False |
| RP-05 | OBS | same seq posted twice -> both accepted, 2 evidence records (no idempotency on device_id+seq; a retried POST after a lost reply duplicates evidence) | 200 ev_000047 / 200 ev_000048 |
| RP-06 | PASS | ts null -> server stamps received_at in reply | 2026-11-23T06:17:06Z |
| CA-01 | PASS | GET calibration (device) before any set -> baseline null, margin 0.30, updated_at key present | 200 {'tds_baseline_ppm': None, 'tds_margin': 0.3, 'updated_at': None, 'cal_id': None} |
| CA-02 | PASS | POST use_latest for a device with no reading -> 409 | 409 |
| CA-03 | PASS | POST {'tds_baseline_ppm': 0} rejected 422 | 422 |
| CA-04 | PASS | POST {'tds_baseline_ppm': -5} rejected 422 | 422 |
| CA-05 | PASS | POST {'tds_baseline_ppm': 600, 'tds_margin': 0} rejected 422 | 422 |
| CA-06 | PASS | POST {'tds_baseline_ppm': 600, 'tds_margin': 1} rejected 422 | 422 |
| CA-07 | PASS | POST {} rejected 422 | 422 |
| CA-08 | PASS | POST baseline 592 / 0.25 -> echoes v0.2.1 body | 200 {'tds_baseline_ppm': 592.0, 'tds_margin': 0.25, 'updated_at': '2026-11-23T06:17:06Z', 'cal_id': '2026-12-09'} |
| CA-09 | PASS | GET as device returns stored values; firmware parser caches baseline 592, margin 0.25 | {'tds_baseline_ppm': 592.0, 'tds_margin': 0.25, 'updated_at': '2026-11-23T06:17:06Z', 'cal_id': '2026-12-09'} |
| CA-10 | PASS | GET another device's calibration with own creds -> 401 | 401 |
| CA-11 | PASS | GET with wrong key -> 401 | 401 |
| CA-12 | PASS | GET without device headers (dashboard, open/local mode) -> 200 | 200 |
| CA-13 | PASS | POST use_latest takes the last TDS reading (640) | {'tds_baseline_ppm': 640.0, 'tds_margin': 0.3, 'updated_at': '2026-11-23T06:17:06Z', 'cal_id': '2026-11-23'} |
| CA-14 | OBS | baseline cannot be cleared back to null via POST (contract allows number/null) | 422 |
| CA-15 | PASS | each calibration change logged in evidence chain | 5 calibration records |
| CA-16 | PASS | firmware keeps its cached baseline when backend returns null | {'tds_baseline_ppm': None, 'tds_margin': 0.3, 'updated_at': None, 'cal_id': None} |
| CM-01 | PASS | camera poll with empty queue -> 200 {cmd:none}; firmware ignores | {"cmd":"none"} |
| CM-02 | PASS | dashboard POST capture -> queued | {'queued': True, 'id': 1, 'cmd': 'capture'} |
| CM-03 | PASS | poll returns capture once, then none (consumed) | {'cmd': 'capture', 'id': 1} {'cmd': 'none'} |
| CM-04 | OBS | repeated Capture clicks queue N captures (no de-dup/expiry; stale commands fire when camera reconnects) | capture,capture,none |
| CM-05 | PASS | unknown command 'reboot' -> 422 | 422 |
| CM-06 | PASS | soil node polling camera's queue -> 403 | 403 |
| CM-07 | PASS | poll without device headers -> 401 | 401 |
| RI-01 | PASS | ripeness without device headers -> 401 | 401 |
| RI-02 | PASS | empty body -> 400 | 400 |
| RI-03 | PASS | body > 5 MB -> 413 | 413 |
| RI-04 | PASS | model absent -> 503 with clear message (expected while M1 trains) | {"detail":"Ripeness model not found at /home/zhen/Documents/taylors/CCA/03_software/models/m1_ripeness.onnx — train it w |
| RI-05 | BLOCKED | label/confidence/probs(4 classes)/harvest_advice/explanation/heatmap_url/model_version/evidence_id | M1 model not yet exported (503) |
| RI-06 | BLOCKED | heatmap PNG produced and served at heatmap_url | M1 model not yet exported (503) |
| RI-07 | BLOCKED | non-image body -> 400 | M1 model not yet exported (503) |
| RI-08 | BLOCKED | cam_node parser accepts reply (label, confidence, harvest_advice, evidence_id) | M1 model not yet exported (503) |
| RI-09 | BLOCKED | inference latency on laptop CPU < 2 s | M1 model not yet exported (503) |
| FW-01 | PASS | soil_node toJson() payload [boot, no NTP (ts null), cal_id 'uncalibrated', ec null] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000053 |
| FW-02 | PASS | soil_node toJson() payload [NTP time, all sensors OK] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000054 |
| FW-03 | PASS | soil_node toJson() payload [DS18B20 + DHT22 failed (NAN -> null)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000055 |
| FW-04 | PASS | soil_node toJson() payload [all soil probes failed (NAN -> null)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'NO DATA' / 'check sensors' led=amber ev_000056 |
| FW-05 | PASS | soil_node toJson() payload [buffered replay, no NTP, age_s 95, rssi unknown (0 -> null)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'OK' / 'all in range' led=green ev_000057 |
| FW-06 | PASS | soil_node toJson() payload [dry + acidic + TDS low (3 findings)] -> 200 and applyCloudResponse() accepts | 200 CLOUD 'IRRIGATE' / 'moist 24%<30%' led=red ev_000058 |
| FW-07 | PASS | LOCAL fallback rules == CLOUD action+LED on 75 boundary combos | [] |
| FW-08 | OBS | LOCAL (raw float) vs CLOUD (rounded payload) can disagree within rounding of an edge | raw m=29.96 pH=5.0: LOCAL irrigate vs CLOUD ok; raw m=50 pH=3.996: LOCAL lime vs CLOUD watch; raw m=80.04 pH=5.0: LOCAL drain vs CLOUD ok; raw m=50 pH=4.196: LOCAL watch vs CLOUD ok |
| FW-12 | OBS | all probes failed: LOCAL shows green 'OK / all in range' while CLOUD shows amber 'NO DATA' | LOCAL OK/all in range/green vs CLOUD ['NO DATA', 'check sensors']/amber |
| FW-09 | OBS | LOCAL OLED uses 1-dp pH: raw pH 3.96 shows 'pH 4.0<4.0' (CLOUD shows 2-dp) | LOCAL 'pH 4.0<4.0' vs CLOUD 'pH 3.96<4.0' |
| FW-10 | PASS | cam_node pollCommands(): idle reply parsed, cmd != 'capture' -> no capture | {"cmd":"none"} |
| FW-11 | BLOCKED | cam_node captureAndUpload(): raw JPEG + headers accepted and reply parsed | HTTP 503: node would show 'upload failed (HTTP 503)' until M1 is exported |
| OL-01 | PASS | all 46 /readings replies: oled = 2 non-empty strings ≤16 chars | [] |
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
| DB-06 | OBS | Copernicus notice lacks the year ('Contains modified Copernicus Sentinel data [2025/2026]') and names Planetary Computer while D16/D29 build uses Earth Engine |  |
| DB-07 | PASS | every feed the dashboard polls returns 200 | {'/api/v1/latest': 200, '/api/v1/harvest/plan?crew=12': 200, '/api/v1/screening': 200, '/api/v1/satellite': 200, '/api/v1/compliance/coverage': 200, '/api/v1/evidence?limit=25&non_ok=true': 200, '/api/v1/readings?device_ |
| DB-08 | PASS | harvest + satellite feeds self-label SIMULATED | SIMULATED (satellite pre-compute not yet available) |
| EV-01 | PASS | verify chain intact over 146 records | All 146 records intact (SHA-256 chain) |
| EV-02 | PASS | records linked: prev_hash(n) == hash(n-1), SHA-256 hex |  |
| EV-03 | PASS | GET evidence/{id} of a reading -> input, output, calibration, mspo, rules_version | 200 INTERFACES-v0.2.2 mspo=['TRACEABILITY', 'SOIL_FERTILITY', 'WATER_MGMT'] |
| EV-04 | PASS | unknown evidence id -> 404 | 404 |
| EV-05 | PASS | review approve -> new evidence record referencing target | 200 |
| EV-06 | PASS | override without override_action -> 422 | 422 |
| EV-07 | FAIL | override_action outside §4 vocabulary rejected (422) | 200 -> logged as ev_000149 |
| EV-08 | PASS | override flagged retraining_candidate and listed under target's reviews | 3 reviews |
| EV-09 | PASS | review of unknown id -> 404 | 404 |
| EV-10 | PASS | MSPO audit pack: chain VERIFIED, fertiliser rows marked Simulated=yes | Generated 2026-11-23T06:17:07Z · records: 150 · chain: VERIFIED — All 150 records intact ( |
| EV-11 | PASS | compliance coverage lists criteria + chain status | 200 |
| EV-12 | PASS | tamper: edit one record's action -> verify fails at that record | Chain broken at ev_000005 — record edited or removed after it was written |
| EV-13 | PASS | tampered chain -> audit pack says BROKEN |  |
| EV-14 | PASS | restoring the original bytes -> chain verifies again | All 150 records intact (SHA-256 chain) |
| EV-15 | PASS | tamper: delete a middle record -> verify fails | Chain broken at ev_000009 — record edited or removed after it was written |
| EV-16 | OBS | truncating the newest records or recomputing the whole chain is not detectable without an external anchor of the head hash (demo limitation; report target = Confidential Ledger) | head id 150 |
| AD-01 | PASS | SAWIT_DEVICE_KEYS override: demo key rejected (401) | 401 |
| AD-02 | PASS | configured key accepted (200) | 200 |
| AD-03 | PASS | admin token set: calibration POST without token -> 403 | 403 |
| AD-04 | PASS | calibration POST with X-Admin-Token -> 200 | 200 |
| AD-05 | PASS | commands POST without token -> 403 | 403 |
| AD-06 | PASS | device GET calibration still works in token mode | 200 |
| AD-07 | FAIL | dashboard GET calibration (app.js get() sends no token) works in token mode | 403 -> calibration panel blank with ?token= in cloud mode |
| AD-08 | PASS | GET calibration with ?token= query works (fix path for AD-07) | 200 |
| AD-09 | PASS | review POST without token -> 403 | 403 |
| AD-10 | OBS | read endpoints (latest, readings, evidence, export) are unauthenticated even in token mode (block/device data public on a cloud URL) | export 200 |
| AD-11 | PASS | SAWIT_MODE=cloud reported by /health (dashboard CLOUD pill) | cloud |
| AD-12 | PASS | SAWIT_MODE=cloud, no SAWIT_DEVICE_KEYS: demo key rejected (D-12 retest, fail closed) | 401 |
| AD-13 | PASS | SAWIT_MODE=cloud, no SAWIT_ADMIN_TOKEN: writes refused 403 (fail closed) | 403 |
| SV-01 | PASS | test servers stopped (port free) |  |
