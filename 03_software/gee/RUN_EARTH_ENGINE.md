# Run the satellite NDVI pre-compute in Google Earth Engine (stakeholder step, D31)

> Internal build doc (D20). Takes about 15 minutes.
>
> **Result:** two files, `src/static/precomputed/satellite.json` and `satellite_ndvi.png`. The dashboard's "1 · Satellite" panel and the screening cascade then show **real Sentinel-2 data** instead of the SIMULATED placeholder.
>
> **What it computes:** for a 4 km × 4 km oil-palm area in Johor, divided into 16 blocks of 1 km²:
> - monthly NDVI over the last 24 months, using only oil-palm pixels (mask from Descals et al. 2021) and clear-sky pixels (Cloud Score+);
> - a z-score of the latest month against each block's own history.
>
> Blocks with z ≤ −1.5 are flagged for drone survey.

## 0. What you need
- Your Earth Engine **Cloud project ID**, for example `sawitsense-ee`. You already have one.
- Python 3.10 or newer on your laptop.
- **Credentials never go in the repo.** The project ID is passed as the environment variable `EE_PROJECT`. The login token lives in your home folder.

## Option A — Python script (writes the dashboard files directly; recommended)
1. Install the Earth Engine library, inside the project's virtual environment:
   ```bash
   cd CCA/03_software
   .venv/bin/pip install earthengine-api
   ```
2. Log in once. A browser window opens; sign in with the Google account that owns the EE project, then allow access.
   ```bash
   .venv/bin/earthengine authenticate
   ```
   The token is saved under `~/.config/earthengine/`, which is outside the repo.
3. Set your project ID for this terminal session:
   - **Linux / macOS:**
     ```bash
     export EE_PROJECT="your-project-id"
     ```
   - **Windows PowerShell:**
     ```powershell
     $env:EE_PROJECT="your-project-id"
     ```
4. Run the script:
   ```bash
   .venv/bin/python gee/ndvi_estate.py
   ```
   It prints one line per month (`2025-01 estate NDVI 0.78`, …). At the end it prints `wrote …satellite.json and satellite_ndvi.png` and the list of flagged blocks. This takes 3–8 minutes.

   Optional flags:
   - `--lon 101.45 --lat 3.05` picks another estate area (for example Selangor). Choose a spot that is mostly oil palm on Google Maps satellite view.
   - `--months 36` uses a longer history.
   - `--drive` also exports a 10 m GeoTIFF to Google Drive in the folder `sawitsense/`.
5. Restart the backend (or just reload the dashboard). Panel "1 · Satellite" now shows the map, the estate NDVI chart, and the flagged blocks.
6. Commit the two small output files so that the presentation laptop has them offline:
   ```bash
   git add src/static/precomputed/satellite.json src/static/precomputed/satellite_ndvi.png
   git commit -m "03_software: real Sentinel-2 NDVI pre-compute"
   git push
   ```

## Option B — Code Editor (visual check, no install)
1. Open https://code.earthengine.google.com and select your project (top right).
2. Click **New → File**, paste in the contents of **`gee/ndvi_estate_codeeditor.js`**, then click **Run**.
3. You will see two layers, "NDVI latest month" and "NDVI z-score" (red = below normal), plus an NDVI chart in the Console.
4. To get the GeoTIFF, open the **Tasks** tab, click **Run** next to `sawitsense_ndvi_latest`, and confirm. The file appears in Google Drive under `sawitsense/`.
5. Option B does **not** write `satellite.json`. Use Option A for the dashboard panel.

## Troubleshooting
| Symptom | Fix |
|---|---|
| `Set EE_PROJECT …` | Step 3 was skipped, or this is a new terminal. Export the variable again |
| `ee.Initialize … not registered / permission denied` | The project is not registered for Earth Engine. Go to https://code.earthengine.google.com/register and register it for **noncommercial** use, then retry |
| `Too few cloud-free months` | Malaysia is cloudy. Run with `--months 36` or `--cs 0.5` |
| Many `None` values in the series | The AOI has little oil palm. Move `--lon/--lat` to a plantation area |
| Thumbnail download fails | Re-run. The PNG URL expires after a few minutes |

**Licence note:** the dashboard footer already includes "Contains modified Copernicus Sentinel data" and the Descals et al. (2021) CC BY 4.0 credit. Keep them in any screenshots used in the report or slides (COPERNICUS-LEGAL; GEE-OILPALM).
