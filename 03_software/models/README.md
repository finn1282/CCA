# models/ (weights are git-ignored)
- `m1_ripeness.onnx` + `m1_ripeness.json`: M1 ripeness model loaded by the API (`SAWIT_MODEL`).
  - Current local file: **provisional** `m1-effb0-0.1-provisional` (CPU, D2-only).
  - Metrics: `training/ripeness/m1_metrics_provisional.json`.
  - Replace it with the Kaggle output (`training/RUN_ON_KAGGLE.md`).
- Rebuild the provisional model locally:
  ```bash
  python training/ripeness/train_m1.py --d2 data/raw/d2 --aug-passes 3 --finetune-epochs 4
  ```
  This takes about 1–2 min on CPU.
