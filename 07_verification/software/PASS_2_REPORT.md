# SW Verification: Pass 2 Report (milestones M2–M4)

> Date: 23 Nov 2026. Repo HEAD `345ec07` (software at `1ad0560`, firmware at `345ec07`). Contract: INTERFACES **v0.2.6**.
> Environment: the existing `03_software/.venv` (no new venv, no downloads, D43/D44); runtime dirs in scratch; port **8833**, with all servers stopped afterwards (SV-01).
> Model under test: the provisional M1 `m1-effb0-0.1-provisional` (D2-only, `03_software/models/`, git-ignored), with local D2 images in `03_software/data/raw/d2`. Account-bound steps (Kaggle, Azure, Earth Engine) were desk-checked only (D31).

## 1. Summary

**All 15 Pass 1 defects are closed.** Retests pass, S-06 passes under the accepted v0.2.4 deviation, and S-02/S-05 are now documented (D39). The backend, the contract and the firmware integration are clean at v0.2.6. The ripeness endpoint with the provisional model is fully contract-conformant and fast:
- p95 is **0.08 s** on the laptop CPU
- the heat-map is served and focused on the bunch

New findings are in the **model evaluation** and the **Azure deploy guide**:
- **4 majors (S-16…S-19)**
- **6 minors (S-20…S-25)**
- **0 blockers**

| Suite | Result |
|---|---|
| Owner `pytest` (existing `.venv`) | **33 / 33 pass** |
| Owner `smoke_test.sh` (asserted, port 8833) | **pass** |
| `tests/contract_test.py` (164 checks, v0.2.6, incl. ripeness with the model) | **156 pass · 0 fail · 8 pass (obs) · 0 blocked** |
| `tests/eval_m1.py` (independent M1 re-evaluation + leakage) | Mapping ✔; reported 0.9326 is **not** reproduced on the serving path (0.8989): **S-16**. 6/89 D2-test images duplicate D2-train: **S-17** |
| Docs 01–05 vs D20/D23/D32 | D32 residency and RAI scoping ✔ throughout. Build/demo/cost wording leaks into report-facing docs: **S-22**; API spec stale: **S-21** |
| Run guides desk-check | Kaggle ✔ (URLs resolve, CC BY 4.0, notebook = `train_m1.py`); Azure: **S-18, S-19, S-20**; EE ✔ with S-24/S-25; beginner guide ✔ with S-23 |

## 2. Pass 1 defects: retest

| ID | Evidence (Pass 2) | Status |
|---|---|---|
| S-01 dashboard calibration GET without token | AD-07: `app.js get()` sends `X-Admin-Token` → 200; no token → 403 | **closed** |
| S-02 laptop must accept the cloud keys | Documented in DEPLOY_AZURE §7, 06 §4.3, ALTERNATIVES; INTERFACES §2 (D39) | **closed** (doc) |
| S-03 bad `ts` | VA-09: garbage, naive or >24 h-future `ts` becomes null (`captured_at = received_at`); `+08:00` normalised to `Z` (v0.2.3 chose null over 422) | **closed** |
| S-04 override vocabulary | EV-07 → 422; RI-10: ripeness record accepts a class and rejects a soil action | **closed** |
| S-05 one backend at a time | D39 + guides + rehearsal R-07 | **closed** (rule) |
| S-06 seq idempotency | RP-05: identical re-POST returns the same `evidence_id` with `duplicate:true` and no new evidence; RP-10: same seq with new values is stored (v0.2.4). RP-11 (obs): only moisture/pH/TDS/soil-temp are compared | **closed** |
| S-07 command coalesce/expiry | CM-04: two clicks give one capture; CM-08: a capture older than 60 s expires | **closed** |
| S-08 reads public in cloud | AD-10: 10 read endpoints give 403 without the token and 200 with it; AD-14: shell and `/health` stay public. Images and heat-maps are public by design (DEPLOY §8) | **closed** |
| S-09 smoke without assertions | `smoke_e2e.py` asserts; passes | **closed** |
| S-10 head anchor | EV-17: the audit pack prints the chain head | **closed** |
| S-11 Copernicus notice | DB-06: "(2024–2026), processed in Google Earth Engine" | **closed** |
| S-12 LOCAL vs CLOUD | FW-07: 315 raw boundary combinations agree on action, LED and OLED line 1 (firmware v0.2.3 r1 rounding); FW-12: all-null shows NO DATA/amber on both sides | **closed** |
| S-13 cascade retry / harvester / EC label | EC-03 ✔; `app.js` retries the cascade until loaded; `harvester.html` has try/catch with an offline message (static) | **closed** |
| S-14 Chart.js licence | DB-10: `vendor/LICENSE-chartjs.txt` served | **closed** |
| S-15 random cache names | `train_m1.py:99` now uses `hashlib.md5` | **closed** |

## 3. M1 model verification (provisional, D2-only)

**Endpoint (RI-04…14).**
- **Response contract:** all 8 §3 fields are present. `probs` has 4 classes summing to 1, and `label` = argmax = `confidence`. `heatmap_url` = `/static/heatmaps/<evidence_id>.png`, served as a 448×224 PNG (image | overlay). The uploaded image is served too.
- **Error handling:** a non-image gives 400; > 5 MB gives 413.
- **Integration:** the `cam_node` parser accepts the reply. `/health` shows `m1-effb0-0.1-provisional`.
- **Latency:**
  - cold first call: 0.22 s
  - warm SVGA frames: **p50 0.082 s, p95 0.083 s**, far inside the live-demo budget
  - a soil POST during 3 concurrent inferences waits about 0.17 s, because inference runs inside the DB lock (obs)
- **Visual check:** the heat-map concentrates on the fruit bunch. CAM mass in the central 5×5 of the 7×7 map is 0.82 on average.

**Independent re-evaluation (`tests/eval_m1.py` → `tests/pass2_eval_m1.md`).**

| Evaluation path | n | Accuracy | Macro-F1 | Confusion (rows true unripe/ripe/overripe) |
|---|---|---|---|---|
| Reported (`m1_metrics_provisional.json`) | 89 | 0.9326 | 0.9371 | 28·5·1 / 0·41·0 / 0·0·14 |
| Training-time pipeline (288-px JPEG cache → torchvision Resize/Crop), reproduced by me | 89 | **0.9326** (identical CM) | 0.9371 | identical |
| **Serving path** (`inference._preprocess` on the image as uploaded) | 89 | **0.8989** | 0.9162 | 25·9·0 / 0·41·0 / 0·0·14 |
| Serving path, **leaked images removed** (S-17) | 83 | **0.8916** | 0.9112 | 24·9·0 / 0·37·0 / 0·0·13 |

- **Class mapping:** my folder→class mapping and `train_m1.map_class`/`split_of` agree on all 312 local D2 files (0 mismatches). D1 names map correctly (Immature→unripe, Partially Ripe→underripe, Fully Ripe/Mature→ripe, Overripe/Decayed→overripe). Damaged/Empty are excluded.
- **EXIF:** 28 test images carry a rotation tag, and 22 more have malformed EXIF that training also leaves unrotated. Results are identical with or without EXIF transpose, so EXIF is not the cause of the gap.
- **Error direction:** every error is *unripe → ripe*. That is the costly direction, because harvest advice would say "Harvest this round" for an unripe bunch. Ripe precision on the serving path is 0.82. This is not a defect, but the final model's report should name it, and `needs_review` (p < 0.6) is the mitigation.
- **Underripe column:** the provisional model has no underripe training data, so that column is untrained (RI-12). The final D1 model resolves this.

## 4. Defects (new in Pass 2)

| ID | Severity | File:line | Issue | Suggested fix | Owner | Status |
|---|---|---|---|---|---|---|
| S-16 | **major** | `03_software/training/ripeness/train_m1.py:89-124` vs `src/app/inference.py:61-72` | **Mismatch between training and serving preprocessing.** Training and its metrics use a cached 288-px JPEG, then torchvision `Resize(256)`/`CenterCrop(224)`. The API resizes the uploaded image straight to 256 with PIL. The reported D2-test 0.9326 reproduces exactly only on the training path; the deployed path scores **0.8989** (3 more unripe→ripe errors). The same gap will affect the final Kaggle model's reported numbers. | Compute the reported metrics through the **exported ONNX + `inference._preprocess`** (add an eval step after export in `train_m1.py`). Or make serving mirror training (first thumbnail to 288, then 256/224). Report the serving-path numbers in `03_ai_models.md` §9 and the README. | Software | open |
| S-17 | **major** | D2 provided split; `train_m1.py:204-226` | **D2 train/test leakage.** 6 of 89 D2 test images (6.7 %) are the same photographs as D2-train images: `TestRipe(15)`=`TrainRipe(107)` (byte-identical); `TestOverripe(11)`/`TrainOverripe(39)`, `TestUnripe(15)`/`TrainUnripe(101)` (dHash 0); `TestRipe(9)`/`TrainRipe(133)` (1); `TestRipe(39)` and `TestRipe(16)`/`TrainRipe(20)` (3–4). All were checked visually. This inflates the provisional D2 metric and the final `d2_malaysia_test_after_head_finetune`. The local D2 copy is partial, so the full set may hold more duplicates. | In `train_m1.py`, drop D2-test images that have a dHash ≤ 6 twin in D2-train (or drop the twins from train) before any D2 evaluation, and log the excluded list and the n. Run it on the full D2 in the Kaggle notebook. The pair list is in `tests/pass2_eval_m1.md`. | Software | open |
| S-18 | **major** | `03_software/deploy/DEPLOY_AZURE.md:63-67` | The model SAS is generated with `--auth-mode login --as-user` (a user-delegation SAS) and a **60-day** expiry. User-delegation keys are limited to **7 days**, so step 3 fails as written (or the link dies before the presentation if the expiry is clamped). | Expire in at most 6 days and deploy within that window (the model is fetched once and cached in `/home/data`). Or, simpler for a beginner, put the 16 MB model into the zip (`make_package.sh` copies `models/m1_ripeness.*` to `build/models/` and sets `SAWIT_MODEL` accordingly), which removes Blob and SAS from the critical path. | Software | open |
| S-19 | **major** (risk; account-bound, not run) | `03_software/src/app/db.py:48`; `DEPLOY_AZURE.md:76` | SQLite runs in **WAL** mode on `SAWIT_RUNTIME_DIR=/home/data`, which on App Service Linux is an SMB-mounted Azure Files share. SQLite documents that WAL does not work over network filesystems (it needs shared memory), so "database is locked" or disk I/O errors on the live URL are a real risk for the evidence log. | When `SAWIT_MODE=cloud` (or the DB path is under `/home`), use `PRAGMA journal_mode=DELETE`. Keep one worker (already the case). Add R-03b to the rehearsal: 50 readings + Verify chain + app restart. | Software | open |
| S-20 | minor | `DEPLOY_AZURE.md:82`; `deploy/make_package.sh:13-19` | `--startup-file "startup.sh"` relies on App Service resolving a bare file name and on the zip keeping the executable bit. If either fails, the container never starts and the logs only say "startup.sh: not found / permission denied". | Use `--startup-file "bash startup.sh"`, or the inline command `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1`. Add the expected `az webapp log tail` line. | Software | open |
| S-21 | minor | `03_software/05_api_spec.md:128,163-172` | §3 header still says "read: open", but cloud mode now requires the token for every read (S-08). §5 omits `SAWIT_MODEL_URL` / `SAWIT_MODEL_META_URL`, which DEPLOY_AZURE uses. | Change the header to "read: open locally, admin token in cloud mode", and add the two variables. | Software | open |
| S-22 | minor | `03_ai_models.md:152-153`; `02_architecture.md:55,114,138-160` | Report-facing docs carry build/demo/cost wording against D20/D23 (and D40: no prototype results in the report): §9 lists the provisional CPU result and "GPU notebook run (`training/RUN_ON_KAGGLE.md`)"; 02 §4 is a live-presentation sequence; line 114 has "demonstration nodes … stand-in"; line 55 justifies satellite-first by "cheapest". D32 residency and RAI scoping are correct everywhere. | Mark 03 §9 and 02 §4 "internal, not for the report" (or move them to `07_actual_build_vs_target.md`). Replace "cheapest" with a capability reason ("the only source that covers every block every ~5 days"). | Software | open |
| S-23 | minor | `training/RUN_ON_KAGGLE.md:94`; `06_implementation_guide_beginner.md:64,126` | The guides post D2 originals with `simulator.py --image`, but 8 of 89 D2 test files are > 5 MB and get **413**. The "printed D2 photos" item does not say to use test-split images that are not among the leaked ones (S-17). | Make `simulator.py --image` downscale to ≤ 1600 px before upload, or tell the user to pick a file < 5 MB. Print photos only from `FFBtest`, excluding the S-17 list. | Software | open |
| S-24 | minor | `gee/ndvi_estate.py:83`; `src/static/precomputed/estate_blocks.json` | After a real Earth Engine run, the satellite stage names blocks `B01`–`B16`, while the drone stage, harvest plan and demo story use `DEMO-A1, A2…C2` ("NDVI flags block B2 → drone"). The cascade stages would then refer to unrelated blocks, and the real AOI may flag none. | Map the GEE grid onto the estate block IDs (or regenerate `estate_blocks.json`/`screening.json` from the GEE grid). Rehearse the cascade after the stakeholder's run. | Software | open |
| S-25 | minor | `gee/RUN_EARTH_ENGINE.md:22-40` | Commands use `.venv/bin/…` only. Windows users (who get PowerShell lines for `EE_PROJECT`) are not told to use `.venv\Scripts\…`. | Add the same one-line Windows note as 06 §2. | Software | open |

**Observations:**
- **AU-06:** device keys are not scoped per endpoint.
- **PR-02:** the `simulated` flag is conservative.
- **NU-04:** with several sensors null, OLED line 2 names only one.
- **CA-14:** the API cannot clear a baseline to null.
- **FW-08:** 1-dp pH rounding moves the effective edges by 0.05 pH. This is consistent on both sides and within probe accuracy.
- **RP-11:** the duplicate check compares only the 4 soil values.
- **RI-12, RI-13:** the untrained underripe column; soil POSTs wait on the DB lock during inference.
- **Kaggle scratch folder:** the notebook writes data to `/kaggle/tmp`. It should work (the kernel runs as root), but Kaggle's documented scratch folder is `/kaggle/temp`. Worth a glance on the first run.

## 5. Desk-check notes (no account-bound step executed, D31)

- **Kaggle (`RUN_ON_KAGGLE.md`, notebook, metadata): correct for a beginner.**
  - The embedded `train_m1.py` is byte-identical to the repo file.
  - The D1 Mendeley URL redirects to a 272,151,984-byte zip, and the D2 Zenodo URL returns 200 with 1,159,745,282 bytes and CC BY 4.0. Checked by HEAD request only.
  - `kernel-metadata.json` has GPU and internet on and is private.
  - The `KAGGLE_API_TOKEN` env var and `~/.kaggle/access_token` are used, and no token is written into the repo.
  - The download goes to `-p models` from `03_software`, and the post-run health check is clear.
- **Azure (`DEPLOY_AZURE.md`, `make_package.sh`).** The resources, region fallback, app settings (`SAWIT_MODE=cloud`, keys, token, `/home/data`), HTTPS-only, health URL with the expected version (`APP_VERSION` = 0.2.6 ✔), token-in-URL dashboard and clean-up are all complete. Fix S-18, S-19 and S-20 before the stakeholder runs it.
- **Earth Engine (`RUN_EARTH_ENGINE.md`, `ndvi_estate.py`).**
  - `EE_PROJECT` is read from the environment and the script fails clearly without it.
  - The token stays in `~/.config/earthengine`.
  - The outputs are the committed precompute files, and the attribution year is set automatically.
  - Remaining issues: S-24, S-25.
- **06 beginner guide and 07 build-vs-target.** Accurate for v0.2.6 (33 tests, one-backend rule, shared keys, REFERENCE-cup baseline). Remaining issue: S-23.

## 6. What the next pass needs

1. Fixes for S-16…S-19 (S-18/S-19 before the stakeholder deploys), then a re-run of `tests/contract_test.py` and `tests/eval_m1.py`.
2. The stakeholder's Kaggle outputs (`m1_metrics.json` from D1→D2). I will re-run `eval_m1.py`-style checks on the D2 test with the final ONNX, using serving-path and deduped numbers. D1 is not on this machine (D44), so any D1-test check stays with the owner's run log.
3. After the stakeholder's Azure/EE runs, the live URL (rehearsal R-03…R-05, R-03b) and the committed `satellite.json` (S-24).

## 7. How to reproduce

```bash
cd /home/zhen/Documents/taylors/CCA
S=<scratch>
TMPDIR=$S PYTHONDONTWRITEBYTECODE=1 03_software/.venv/bin/python 07_verification/software/tests/contract_test.py --port 8833 --out $S/results.md
03_software/.venv/bin/python 07_verification/software/tests/eval_m1.py --out $S/eval_m1.md   # ~2 min, local D2 only
```
