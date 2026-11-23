# SW Verification: Pass 1 Report (milestone M1, backend smoke test)

> Date: 23 Nov 2026. Trigger: M1 (`305bb47`). Re-baselined on the code at test time:
> - software `b3cb4fe` (fixes D-04, D-12; INTERFACES v0.2.2)
> - firmware `54eea6c` (v0.2.2)
> - repo HEAD `4163a6d`
>
> Contract: INTERFACES **v0.2.2**. Environment: fresh Python 3.14 venv in scratch, throw-away `SAWIT_RUNTIME_DIR`, port **8833**. All servers were stopped afterwards (SV-01).
> M1 training is in progress, so the ripeness endpoint returns 503 and the model tests are **blocked**.

## 1. Summary

**Verdict:** the backend conforms to the contract for everything a soil node does. Threshold edges, priority, nulls, OLED/LED, calibration, the command queue, replay and the evidence chain with tamper detection all pass. The exact firmware payloads are accepted, and the firmware's ArduinoJson parsing accepts every reply.

There are **2 majors**, both about deployment and demo-day configuration rather than rule logic:
- **S-01:** in cloud/token mode the dashboard calibration panel is blank.
- **S-02:** the laptop fallback rejects the device key that is used in the cloud.

There are **13 minors** and **0 blockers**.

| Suite | Result |
|---|---|
| Owner `pytest` (fresh venv) | **22 / 22 pass** |
| Owner `smoke_test.sh` (port 8833) | **pass** (but it has no assertions, S-09) |
| `tests/contract_test.py` (154 checks) | **132 pass · 3 fail · 13 pass (obs) · 6 blocked** |
| Review-only checks (TEST_PLAN §C–§G) | FW-13 **fail** (S-02); DB-09, DS-03/04/09 pass (static); DS-05/06/07, MD-*, CL-*, DOC-01 blocked |

**Retests of Hardware verification defects handed to Software:**

| HW defect | What was checked | Result |
|---|---|---|
| D-04 (stale `/latest` after replay) | RP-03 and RP-09: after older buffered replays, `/latest` stays on the highest-seq non-buffered row | **fixed** |
| D-12 (demo keys active in cloud) | AD-12 and AD-13: `SAWIT_MODE=cloud` with no keys or token fails closed (401/403) | **fixed** |
| D-09 (`age_s`) | RP-07 and RP-08: `captured_at` is correct | **fixed** |

## 2. What was run

1. **Owner suite.** `pytest` and `smoke_test.sh` from `03_software/src` with `PYTHONDONTWRITEBYTECODE=1` and runtime dirs in scratch, so nothing was written to other members' folders.
2. **`tests/contract_test.py`.** The script does not import the app. It starts uvicorn on 8833 three times:
   - (a) local/open mode
   - (b) cloud mode with keys and an admin token
   - (c) cloud mode with no secrets

   It sends hand-written requests for every v0.2.2 endpoint and edits the throw-away SQLite DB to test tampering. Full per-check output is in `tests/pass1_results.md`.
3. **Firmware ↔ backend.** I ported `soil_node.ino` `toJson()`, `applyCloudResponse()`, `fetchCalibration()` and `localDecision()`, and `cam_node.ino` `pollCommands()`, to Python. I posted the byte-shaped payloads (key order, `jsonNum` rounding, `age_s`, null for NAN, `rssi` 0 → null) and parsed the replies the way ArduinoJson `|` defaults would. LOCAL and CLOUD were compared on 75 boundary combinations. I did not repeat the firmware internals review, which `07_verification/hardware` covers.
4. **Dashboard.** I checked the served HTML/JS/CSS for any external URL, checked that every asset and feed returns 200, checked panels and attributions, and read the `app.js` error paths.
5. **Datasets.** I read `01_research/03_datasets.md`, `training/ripeness/train_m1.py`, `scripts/fetch_d2_github.py`, `training/fertiliser/*` and the download logs in `03_software/data/raw` (read only).

## 3. Defects

| ID | Severity | File:line | Issue | Suggested fix | Owner | Status |
|---|---|---|---|---|---|---|
| S-01 | **major** | `03_software/src/static/app.js:8-12,118`; `src/app/main.py:44-51` | When `SAWIT_ADMIN_TOKEN` is set (required in cloud mode since D-12), `GET /devices/{id}/calibration` without device headers goes through `admin_auth`. The dashboard's `get()` never sends the token, so it gets **403**, `loadCal()` swallows the error, and the TDS calibration panel stays empty. The operator cannot see or confirm the baseline during the TDS demo beat (AD-07). Save still works, because `post()` sends the token. | In `get()`, add `...(TOKEN ? {"X-Admin-Token": TOKEN} : {})` to the headers (simplest). Or make GET calibration readable without a token, since it is non-secret. Add a pytest case in token mode. | Software | open |
| S-02 | **major** | `03_software/README.md:38`; `src/app/config.py:24-26`; `02_hardware/firmware/*/secrets.h.example:13` | Each node has **one** `DEVICE_KEY` for both `API_BASE` (cloud) and `API_BASE_LOCAL` (laptop). The cloud needs real keys (`SAWIT_DEVICE_KEYS`), but the laptop in local mode only accepts the demo keys unless the same variable is exported. So if the cloud fails on the day, the LAN fallback answers **401**. The v0.2.2 firmware then treats that as a rejection and drops the reading. The fallback the demo relies on would silently fail (FW-13). | Document in the README and the run guide (M4): "start the laptop with `SAWIT_DEVICE_KEYS=<same as App Service>` (and optionally `SAWIT_ADMIN_TOKEN`)". Consider a `run_local.sh` that reads the keys from a git-ignored `.env`. Hardware: note in `secrets.h.example` that the key must be valid on both bases. Rehearsal R-04. | Software (+ Hardware comment) | open |
| S-03 | minor | `src/app/main.py:57,103` | `ts` is a free string and is not validated. `"not-a-timestamp"` is stored as `captured_at`. Because `/readings` sorts by `captured_at` (string order), the bad row then sorts as the **newest chart point forever**, and the evidence log records a bogus capture time (VA-09). | Type `ts` as `AwareDatetime \| None` (pydantic) and normalise it to `YYYY-MM-DDTHH:MM:SSZ`; reject with 422 otherwise. Optionally reject `ts` far in the future (wrong device clock). | Software | open |
| S-04 | minor | `src/app/main.py:88,276-291` | `override_action` accepts any string: `"banana"` was logged as an override and as a retraining candidate (EV-07). That pollutes the audit trail and the retraining queue. | Use `Literal[...]` with the §4 actions for soil records and the M1 class list for ripeness records (validate against the target's `kind`). | Software | open |
| S-05 | minor | Design: `INTERFACES.md` §1 (cloud + LAN fallback), `src/app/db.py` (local SQLite per server) | Cloud and laptop are **separate databases and command queues**. A dashboard on the cloud cannot see readings that went to LAN, and a Capture queued on the cloud never reaches a camera on LAN (FW-14). | Add a "one backend at a time" rule to the demo plan and run guide (rehearsal R-07). Make the dashboard show which base it is on (the `mode` pill exists) next to the OLED tag. | Lead / Software / Hardware | open |
| S-06 | minor | `src/app/main.py:93-121` | No idempotency on `(device_id, seq)`. A POST retried after a lost reply (4 s firmware timeout, cloud then LAN retry) creates a duplicate reading and evidence record (RP-05). | Add a unique index on `(device_id, seq)` when `seq` is not null. On a duplicate, return the stored response (same `evidence_id`). | Software | open |
| S-07 | minor | `src/app/main.py:171-188` | The command queue has no de-duplication or expiry. Repeated Capture clicks queue repeated captures, and a capture queued while the camera is offline fires minutes later (CM-04). | Coalesce pending `capture` commands per device and ignore commands older than about 60 s. | Software | open |
| S-08 | minor | `src/app/main.py:124,227,251-300` | Read endpoints (`/latest`, `/readings`, `/evidence*`, `/compliance`) are unauthenticated even in cloud/token mode. Block IDs, device data and reviewer names are public on the App Service URL (AD-10). | Accept this for the demo, but state it in the deploy guide. Alternatively, require the admin token on reads when `SAWIT_MODE=cloud` (the dashboard already carries `?token=`). | Software | open |
| S-09 | minor | `src/smoke_test.sh:3,27` | `set -e` with `curl -s` (no `-f`) and no assertions: the script prints "SMOKE TEST PASSED" even when steps return 4xx/5xx or the wrong action. | Use `curl -sf`, assert the expected actions, LEDs and `ok:true` in the Python one-liners, and `exit 1` on mismatch. | Software | open |
| S-10 | minor | `src/app/evidence.py:67-77`, audit pack | The hash chain detects edits and middle deletions (EV-12…15). It cannot detect truncation of the newest records or a full recomputation without an external anchor of the head hash (EV-16). | Print the head hash in the audit pack and in the presentation, so it can be quoted as an anchor. Keep Confidential Ledger as the report-facing control (D28). | Software | open |
| S-11 | minor | `src/static/index.html:109` | The Copernicus notice lacks the year, and says "processed via Microsoft Planetary Computer", while the build's satellite pipeline is Earth Engine (D16/D20). Copernicus terms require "Contains modified Copernicus Sentinel data [Year]" (DB-06). | Use "Contains modified Copernicus Sentinel data (2025–2026), processed in Google Earth Engine". Keep Planetary Computer for report-facing docs only. | Software | open |
| S-12 | minor | `02_hardware/firmware/soil_node/soil_node.ino:217-240` | LOCAL vs CLOUD consistency (FW-08/09/12): (a) LOCAL decides on the raw float, while CLOUD receives 1-dp moisture and 2-dp pH, so they disagree within rounding of an edge (raw 29.96 %: LOCAL irrigate, CLOUD ok); (b) with all probes failed, LOCAL shows green "OK / all in range" while CLOUD shows amber "NO DATA"; (c) LOCAL prints pH with 1 dp (`pH 4.0<4.0` at 3.96). | Round to payload precision before the local rules; return "NO DATA"/amber when all three are NAN; use `String(r.ph, 2)`. *Coordination note for `07_verification/hardware`; not re-reviewed here.* | Hardware | open |
| S-13 | minor | `src/static/app.js:218`; `src/static/harvester.html:23-24` | `renderCascade()` runs only on the first tick, so if the backend was down at page load the cascade panel stays empty after recovery. `harvester.html` has no error handling (a blank page when offline). The EC tile is always labelled "≈TDS/0.5", even when EC is measured (EC-03). | Retry the cascade until it succeeds (for example on `n % 15 === 0` while it is empty); add try/catch and an "offline" note to harvester; label the EC tile from `ec_derived`. | Software | open |
| S-14 | minor | `src/static/vendor/chart.umd.min.js:1` | The Chart.js 4.4.1 MIT copyright banner was stripped from the vendored file (DB-10). | Restore the `/*! Chart.js v4.4.1 … MIT */` header or add `vendor/LICENSE-chartjs.txt`. | Software | open |
| S-15 | minor | `03_software/training/ripeness/train_m1.py:98` | Cache filenames use Python's `hash()`, which is randomised per process (`PYTHONHASHSEED`). The 288-px cache is never reused across runs, so every CPU/Kaggle rerun pays the full decode again. | Use `hashlib.md5(str(p).encode()).hexdigest()`. | Software | open |

**Observations, not defects (contract met):**
- AU-06: device keys are not scoped per endpoint.
- PR-02: `simulated` is true whenever a TDS finding is present, even under a higher-priority action (conservative, fine).
- NU-04: with two sensors null, the OLED names only the first.
- OL-07: OLED line 2 is truncated at 16 characters for extreme TDS values.
- CA-14: the API cannot clear a baseline back to null. The v0.2.2 firmware handles null anyway.

## 4. Area notes

- **Thresholds and priority.** Every §4 edge behaves as "strictly less/greater than":
  - moisture 30 and 80 → ok
  - pH 4.0 → watch, pH 4.2 → ok, pH 6.5 → ok
  - TDS at exactly baseline × (1 ± margin) → ok

  Firmware LOCAL uses the same comparisons (FW-07: 75/75 agree on the rounded values).
- **OLED/LED.** About 150 replies were checked. All are 2 strings of 1–16 characters, the LED matches the §4 row, and line 1 now uses "SKIP FERTILISER" (b3cb4fe), the same as LOCAL.
- **Evidence chain.** SHA-256 links are correct. Edits and middle deletions are detected and the audit pack flips to BROKEN. Fertiliser rows are marked Simulated=yes. Overrides are flagged as retraining candidates (D28).
- **Dashboard.** It is offline-safe: no CDN, fonts or external URL, and Chart.js is vendored. All 8 panels are present. The CC BY 4.0 credits for D1/D2/D4/Descals and the SIMULATED badges are visible. If the backend goes down after load, the pill changes to "offline" and the last values stay on screen. A live browser check is deferred to rehearsal R-10/R-12.
- **Datasets.**
  - The class harmonisation and split logic in `train_m1.py` keeps the D2 Malaysian test out of training. The head-only D2 fine-tune uses D2 train and is evaluated on D2 test.
  - A provisional, D2-only model is labelled `-provisional` and lacks underripe training data, which Pass 2 must check.
  - D1 is still downloading (19 MB of 272 MB on disk), and only D2 FFBtest is present locally (23 unripe, 41 ripe, 14 overripe). Leakage (perceptual-hash) and class-balance checks are therefore blocked.
  - D4 (M3) is not built yet.
  - M6 data is clearly SIMULATED in the meta, the dashboard and the audit pack.
- **Docs.** Design docs 01–03 have appeared in `03_software/` and are not reviewed in this pass (M3 trigger). The README is an accurate record of the M1 build, apart from the S-02 note.

## 5. What Pass 2 needs (trigger: M2, model trained)

1. `03_software/models/m1_ripeness.onnx`, `.json` and `m1_metrics.json`, plus the training log. Say whether it is provisional (D2-only) or D1→D2.
2. D1 fully downloaded and extracted, and D2 FFBtrain present, for DS-05 (cross-split near-duplicates) and DS-06 (counts).
3. Fixes for S-01…S-04 at least (S-01 and S-02 before any cloud rehearsal), then a re-run of `contract_test.py`, which should give 0 FAIL.
4. sklearn in the training requirements, for the MD-06 M6 reproducibility check.
5. Pass 3/4 inputs, when ready: design docs 01–05 (DOC-01) and the Kaggle, Azure and GEE run guides (CL-01…03).

## 6. How to reproduce

```bash
S=<scratch>; python3 -m venv $S/venv && $S/venv/bin/pip install -r 03_software/src/requirements.txt
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 $S/venv/bin/python 07_verification/software/tests/contract_test.py --port 8833 --out $S/results.md
```
