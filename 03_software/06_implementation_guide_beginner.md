# 06 — SawitSense Implementation Guide (beginner)

> Internal build doc (D20). It assumes no prior experience: follow the steps in order and copy each command exactly.
> - You need a laptop running Windows, macOS or Linux, with Python 3.11 or newer and git.
> - **Steps that need an account (Kaggle, Earth Engine, Azure) are run by the stakeholder (D31).** They are linked here, not repeated.

## Contents
1. Get the code
2. Install
3. Run backend + dashboard + simulator (no hardware needed)
4. Connect the real devices (soil node + camera)
5. Calibrate on the day
6. Train the ripeness model (Kaggle, or CPU fallback)
7. Satellite panel (Earth Engine)
8. Deploy to the cloud (Azure) and the fallbacks
9. Demo-day checklist
10. Troubleshooting

---

## 1. Get the code
```bash
git clone https://github.com/finn1282/CCA.git
cd CCA/03_software
```

## 2. Install (one time)
**Linux / macOS:**
```bash
python3 -m venv .venv
.venv/bin/pip install -r src/requirements.txt
```
**Windows (PowerShell):**
```powershell
py -m venv .venv
.venv\Scripts\pip install -r src\requirements.txt
```
On Windows, replace `.venv/bin/python` with `.venv\Scripts\python` in every later command.

Check that everything works. You should see `33 passed`, then a list of `PASS …` lines ending in `SMOKE TEST PASSED (all assertions)`:
```bash
cd src
../.venv/bin/python -m pytest -q
PY=../.venv/bin/python ./smoke_test.sh
```
`smoke_test.sh` needs bash. On Windows, run it in Git Bash, or skip it; the pytest suite covers the same ground.

## 3. Run backend + dashboard + simulator (no hardware)
1. **Terminal 1, the backend.** Run from `03_software/src`:
   ```bash
   ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
   Leave it running. `--host 0.0.0.0` lets the devices on the same Wi-Fi reach it.
2. **Browser:** open http://localhost:8000. The dashboard's top bar shows **LOCAL** and **live**.
3. **Terminal 2, the simulator.** It plays the role of the soil node:
   ```bash
   ../.venv/bin/python simulator.py --scenario cycle --interval 2
   ```
   The tiles and chart update. The recommendation card walks through OK → IRRIGATE → LIME → … with reasons and counterfactuals.
4. In the **TDS calibration** card, choose `sim-01` and click **Use current reading**. The fertilise / skip-fertiliser rules (SIMULATED agronomy) now become active.
5. Try **Approve / Override**, **Verify chain** and **MSPO audit pack ↗** in the evidence card.
6. Optional: send a bunch photo, once the model exists (§6):
   ```bash
   ../.venv/bin/python simulator.py --count 1 --image path/to/ffb.jpg
   ```
   The simulator shrinks the photo to ≤ 1600 px before upload, because the API accepts at most 5 MB (S-23). If you upload some other way, use files under 5 MB.
7. Mobile harvester view: http://localhost:8000/harvester. You can open it on a phone using the laptop's IP address.

Stop the servers with **Ctrl+C**. The data is kept in `src/runtime/sawitsense.db`. Delete that file to start fresh before a rehearsal.

## 4. Connect the real devices
Hardware assembly and flashing are in `02_hardware/` (assembly guide + firmware).

1. Find the laptop's IP address on the Wi-Fi:
   - Linux: `ip addr`
   - macOS: `ipconfig getifaddr en0`
   - Windows: `ipconfig`, then look for "IPv4 Address"
2. In each device's `secrets.h`, which is git-ignored (start from `secrets.h.example`):
   - `API_BASE_LOCAL = "http://<laptop-ip>:8000"`
   - `API_BASE = "https://<app>.azurewebsites.net"` (cloud; optional)
   - `DEVICE_ID`: `soilnode-01` for the soil node, `cam-01` for the camera
   - `DEVICE_KEY`: the key for that device
3. **Keys must match on the laptop (S-02).** Each device has **one** key, which it sends to the cloud and to the laptop.
   - If you flashed the demo keys (`demo-soil-key`, `demo-cam-key`), the laptop accepts them with no extra step.
   - If you flashed **real** keys (the same ones set on Azure), start the laptop backend with the same keys:
     ```bash
     export SAWIT_DEVICE_KEYS="soilnode-01:<soil key>,cam-01:<cam key>"     # PowerShell: $env:SAWIT_DEVICE_KEYS="..."
     ../.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
     ```
     Otherwise the laptop answers 401 and the fallback silently fails.
4. Power the soil node. Within about 10 s the dashboard shows `soilnode-01`. The OLED shows the action, tagged **LAN** (laptop) or **CLOUD**.
5. **Camera:** click **Capture** on the dashboard. The camera polls every 2–3 s, takes a photo, and the result plus heat-map appear in the camera card. Repeated clicks are merged, and a capture older than 60 s expires.
6. **One backend at a time (D39).** The laptop and the cloud keep **separate** databases and command queues. Point both devices *and* the dashboard at the same backend, and check that the dashboard's pill (LOCAL/CLOUD) matches the OLED tag.

## 5. Calibrate on the day (5 minutes)
1. **pH:** two-point calibration with the 4.01 and 6.86 buffers, following `02_hardware/` (firmware calibration mode).
2. **TDS baseline (three-cup demo, D33):** put the probe in the **REFERENCE cup**, wait for 2–3 readings, then click **TDS calibration → Use current reading** for `soilnode-01`. Keep the margin at 0.30. Always set the baseline from the reference cup, never from the plain or the nutrient cup.
3. The node fetches its baseline at boot and every 5 minutes (`GET /devices/{id}/calibration`, INTERFACES v0.2.5) for LOCAL mode. To pass it on immediately, press the node's reset button.
4. Demo beats: nutrient cup (extra NPK) → **SKIP FERTILISER**; plain-water cup → **FERTILISE**; dry soil → **IRRIGATE**.

## 6. Train the ripeness model
- **Main path (stakeholder, Kaggle GPU):** follow `training/RUN_ON_KAGGLE.md`. The result is `models/m1_ripeness.onnx` + `.json`.
- **CPU fallback (any laptop, about 15–40 min):**
  ```bash
  .venv/bin/pip install -r training/requirements.txt
  .venv/bin/python training/ripeness/train_m1.py --d1 data/raw/d1 --d2 data/raw/d2 --workers 2
  ```
  Without D1, run with `--d2 data/raw/d2` only. That produces a **PROVISIONAL** model trained on D2 alone; the `-provisional` suffix in the model version shows this.
  - Get D2 images with `python scripts/fetch_d2_github.py data/raw/d2`.
  - Get D1 from https://data.mendeley.com/datasets/424y96m6sw/1 and unzip it into `data/raw/d1`.
- Restart the backend. `curl localhost:8000/api/v1/health` should show the `ripeness_model` version.

## 7. Satellite panel (stakeholder, Earth Engine)
Follow `gee/RUN_EARTH_ENGINE.md`. Afterwards, commit `src/static/precomputed/satellite.json` and `satellite_ndvi.png`; they are small. Until then, the panel shows a labelled SIMULATED placeholder.

## 8. Deploy to the cloud
- Azure App Service + Blob (stakeholder): `deploy/DEPLOY_AZURE.md`.
- If Azure is not available, see `deploy/ALTERNATIVES.md`. The laptop-local setup (§3–4) is the first-class fallback.

## 9. Demo-day checklist
- [ ] `git pull`, then `pytest` and `smoke_test.sh` pass on the presenting laptop.
- [ ] The model files are in `models/` and `/api/v1/health` shows `ripeness_model`.
- [ ] `src/runtime/sawitsense.db` has been deleted for a clean evidence log. Optionally pre-load a short history by running the simulator for 2 minutes.
- [ ] **One backend chosen (D39)**, either the laptop or the cloud. Devices, dashboard and keys all point at it.
- [ ] Phone hotspot ready as Wi-Fi plan B.
- [ ] TDS baseline set and pH calibrated.
- [ ] Printed FFB photos ready for the camera. Use only D2 **FFBtest** images, and **not** the 8 that duplicate training photos (S-17): TestOverripe(11), TestRipe(9), TestRipe(15), TestRipe(16), TestRipe(18), TestRipe(39), TestUnripe(8), TestUnripe(15).
- [ ] For cloud, the dashboard is opened as `https://…/?token=<admin token>`.
- [ ] The simulator is ready in a terminal, in case the soil node fails: `python simulator.py --scenario acidic --interval 3`.

## 10. Troubleshooting
| Symptom | Cause | Fix |
|---|---|---|
| Dashboard pill "offline" | Backend not running / wrong URL, or (cloud) missing `?token=` | Start uvicorn; open with `?token=` |
| Node OLED "LOCAL" only | Laptop unreachable (firewall, different Wi-Fi) | Allow port 8000 in the firewall; put laptop and node on the same hotspot |
| `401` in the backend log | Key mismatch between `secrets.h` and `SAWIT_DEVICE_KEYS` | See §4.3 |
| Ripeness card says model unavailable (503) | No `models/m1_ripeness.onnx` | §6 |
| No fertilise / skip advice | TDS baseline not set | §5.2 |
| Capture does nothing | Camera on a different backend, or offline > 60 s | §4.6; press Capture again |
| `Address already in use` | Another backend is already running | Stop it (one backend at a time) or use `--port 8001` |
