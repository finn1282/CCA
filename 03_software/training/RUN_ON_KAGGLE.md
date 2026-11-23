# Run M1 ripeness training on Kaggle (stakeholder step, D31)

> Internal build doc (D20). Takes about 30–60 minutes, mostly waiting.
>
> **Result:** three files, `m1_ripeness.onnx`, `m1_ripeness.json` and `m1_metrics.json`. They go into `03_software/models/` and the SawitSense API loads them automatically.
>
> The notebook downloads both datasets itself, from Mendeley (D1) and Zenodo (D2). You do not upload any data.

You can use **Option A (website, no command line)** or **Option B (Kaggle CLI with your `KGAT_…` token)**. Both run the same notebook, `training/kaggle/sawitsense_m1.ipynb`.

## Before you start (both options)
1. You need a Kaggle account that is **phone-verified**. GPU and internet access in notebooks require it: kaggle.com → your avatar → **Settings** → **Phone verification**.
2. Make sure the repository is up to date on your laptop:
   ```bash
   cd CCA
   git pull
   ```

---

## Option A — Kaggle website
1. Go to **kaggle.com → Create → New Notebook**.
2. Click **File → Import Notebook**, choose **`03_software/training/kaggle/sawitsense_m1.ipynb`** from your laptop, then click **Import**.
3. Open the right-hand panel (**Settings**, the ⚙ or "▸" icon):
   - **Accelerator** → **GPU T4 ×2** (or **GPU P100**).
   - **Internet** → **On**. This is required, because the notebook downloads the datasets.
   - **Persistence** can stay off.
4. Click **Run All** (▶▶ at the top).
   - Cell 1 should print a GPU name. If it says "No GPU", repeat step 3.
   - Cell 2 downloads about 1.5 GB of data, which takes 2–5 minutes.
   - Cell 4 trains the model. It prints `stage1 val acc …`, then `finetune ep1 … ep8`, then the metrics.
5. When the last cell shows `m1_ripeness.onnx`, open the **Output** panel on the right (or **Data → Output → /kaggle/working**). Download **`m1_ripeness.onnx`**, **`m1_ripeness.json`** and **`m1_metrics.json`**.
6. To keep a permanent copy, click **Save Version → Save & Run All (Commit)**. Outputs of committed versions stay downloadable.

## Option B — Kaggle CLI with the new API token
1. Install the CLI. It needs Python 3.11 or newer.
   ```bash
   python -m pip install --upgrade kaggle
   ```
2. Give the CLI your token through an **environment variable**. Never put it in a file inside the repo.
   - **Linux / macOS:**
     ```bash
     export KAGGLE_API_TOKEN="KGAT_xxxxxxxxxxxxxxxxxxxx"
     ```
   - **Windows PowerShell:**
     ```powershell
     $env:KAGGLE_API_TOKEN="KGAT_xxxxxxxxxxxxxxxxxxxx"
     ```

   Alternatively, save the token to `~/.kaggle/access_token`. That file is in your home folder, outside the repo.

   Check that it works:
   ```bash
   kaggle kernels list --mine
   ```
3. Write your username into the notebook metadata:
   ```bash
   cd 03_software
   python training/kaggle/build_notebook.py --user <your-kaggle-username>
   ```
   This rewrites `training/kaggle/kernel-metadata.json`, which is set to GPU on, internet on and private.
4. Push and start the run:
   ```bash
   kaggle kernels push -p training/kaggle
   ```
5. Check progress until the status is `complete`, waiting a few minutes between checks:
   ```bash
   kaggle kernels status <your-kaggle-username>/sawitsense-m1-ripeness
   ```
   If it ends in `error`, open the notebook on kaggle.com and read the log.
6. Download the outputs straight into the models folder:
   ```bash
   kaggle kernels output <your-kaggle-username>/sawitsense-m1-ripeness -p models
   ```

---

## After either option
1. Make sure these three files are in `03_software/models/`. They are git-ignored, so they will **not** be committed, which is intended.
   - `m1_ripeness.onnx`
   - `m1_ripeness.json`
   - `m1_metrics.json`
2. Copy the metrics file into the repo so that the results are recorded:
   ```bash
   cp models/m1_metrics.json training/ripeness/m1_metrics_kaggle.json
   ```
3. Restart the backend, then check that the model loaded. `ripeness_model` should show `m1-effb0-0.1`:
   ```bash
   cd src && ../.venv/bin/uvicorn app.main:app --port 8000
   curl http://localhost:8000/api/v1/health
   ```
4. Test with a D2 image:
   ```bash
   ../.venv/bin/python simulator.py --count 1 --image ../data/raw/d2/FFBtest/TestRipe/<file>.jpg
   ```
   The simulator downsizes the image to under the API's 5 MB limit. Pick a test image that is not in the duplicate list printed by the training cell (`d2_test_duplicates_removed` in `m1_metrics.json`).
5. Tell the Software member or the Lead. They will record the numbers in `07_actual_build_vs_target.md` §6 (internal; the report describes validation as a planned step, D40).

## Troubleshooting
| Symptom | Fix |
|---|---|
| `No GPU` / very slow | Settings → Accelerator → GPU. If your weekly GPU quota is used up, run `--finetune-epochs 0` (frozen backbone only), which is fine on CPU too |
| Download cell fails / `curl: (6)` | Internet is Off → Settings → Internet → On (needs phone verification) |
| `D1 checksum mismatch` | Partial download; delete `/kaggle/tmp/data/d1.zip` (or restart the session) and re-run |
| `No D1 images found` | Look at the folder listing that cell 2 prints and send it to the Software member. The class-folder names may differ |
| CLI `401 Unauthorized` | The token is wrong or expired. Create a new one under kaggle.com → Settings → **API → Create New Token** and export it again |
| Out of memory | Add `--bs 16` to the training command in cell 4 |
