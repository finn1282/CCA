"""Build the Kaggle notebook (sawitsense_m1.ipynb) + kernel-metadata.json from train_m1.py.

Usage:  python training/kaggle/build_notebook.py --user <kaggle-username>
The notebook downloads D1 (Mendeley) and D2 (Zenodo) itself, so nothing needs uploading.
Re-run after editing train_m1.py so the embedded copy stays identical.
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = (HERE.parent / "ripeness" / "train_m1.py").read_text()
PREPROCESS = (HERE.parents[1] / "src" / "app" / "preprocess.py").read_text()

D1_URL = "https://data.mendeley.com/public-files/datasets/424y96m6sw/files/cae49a93-5785-4873-a347-bff2a276f62c/file_downloaded"
D1_SHA = "c3cf88db3194fedd24894a35e27fada3841977e1a09a405a4e064db02ebde0c5"
D2_URL = "https://zenodo.org/api/records/11114885/files/MunirahRosbi/Outdoor-Tenera-Oil-Palm-Fruit-Image-v1.zip/content"


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text}


cells = [
    md("# SawitSense — M1 FFB ripeness training (Kaggle GPU)\n"
       "Trains EfficientNet-B0 on **D1** Kamal et al. (2024, CC BY 4.0, Indonesia) and tests on **D2** Rosbi (2024, CC BY 4.0, Malaysia).\n"
       "Outputs in `/kaggle/working`: `m1_ripeness.onnx`, `m1_ripeness.json`, `m1_metrics.json`.\n\n"
       "**Settings → Accelerator: GPU T4 ×2 or P100. Internet: ON.**"),
    code("!nvidia-smi -L || echo 'No GPU — enable it in Settings > Accelerator'\n"
         "!pip -q install onnx onnxscript onnxruntime"),
    code("import hashlib, os, subprocess, zipfile, pathlib\n"
         "data = pathlib.Path('/kaggle/tmp/data'); data.mkdir(parents=True, exist_ok=True)\n"
         f"D1_URL = '{D1_URL}'\nD1_SHA = '{D1_SHA}'\nD2_URL = '{D2_URL}'\n"
         "def fetch(url, dst):\n"
         "    if not dst.exists():\n"
         "        subprocess.run(['curl', '-sSL', '--retry', '5', '-o', str(dst), url], check=True)\n"
         "    return dst\n"
         "d1 = fetch(D1_URL, data / 'd1.zip')\n"
         "assert hashlib.sha256(d1.read_bytes()).hexdigest() == D1_SHA, 'D1 checksum mismatch'\n"
         "d2 = fetch(D2_URL, data / 'd2.zip')\n"
         "for z, out in ((d1, data / 'd1'), (d2, data / 'd2')):\n"
         "    if not out.exists():\n"
         "        zipfile.ZipFile(z).extractall(out)\n"
         "# D1 may contain nested zips — extract them too\n"
         "for inner in (data / 'd1').rglob('*.zip'):\n"
         "    zipfile.ZipFile(inner).extractall(inner.with_suffix(''))\n"
         "!du -sh /kaggle/tmp/data/*; find /kaggle/tmp/data/d1 -maxdepth 3 -type d | head -30"),
    code("%%writefile /kaggle/working/preprocess.py\n" + PREPROCESS),
    code("%%writefile /kaggle/working/train_m1.py\n" + SCRIPT),
    code("!cd /kaggle/working && python train_m1.py --d1 /kaggle/tmp/data/d1 --d2 /kaggle/tmp/data/d2 "
         "--device cuda --finetune-epochs 8 --workers 4 --out /kaggle/working"),
    code("import json; m = json.load(open('/kaggle/working/m1_metrics.json'))\n"
         "for k, v in m.items():\n"
         "    if isinstance(v, dict) and 'accuracy' in v:\n"
         "        print(f\"{k:40s} acc={v['accuracy']:.3f} macroF1={v['macro_f1_present_classes']:.3f} within1={v['within_one_class_accuracy']:.3f} n={v['n']}\")\n"
         "!rm -rf /kaggle/working/_imgcache; ls -la /kaggle/working"),
]

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}

ap = argparse.ArgumentParser()
ap.add_argument("--user", default="YOUR_KAGGLE_USERNAME")
a = ap.parse_args()
(HERE / "sawitsense_m1.ipynb").write_text(json.dumps(nb, indent=1))
(HERE / "kernel-metadata.json").write_text(json.dumps({
    "id": f"{a.user}/sawitsense-m1-ripeness", "title": "SawitSense M1 ripeness", "code_file": "sawitsense_m1.ipynb",
    "language": "python", "kernel_type": "notebook", "is_private": True, "enable_gpu": True, "enable_tpu": False,
    "enable_internet": True, "dataset_sources": [], "competition_sources": [], "kernel_sources": [], "model_sources": []}, indent=2))
print("wrote sawitsense_m1.ipynb + kernel-metadata.json for user", a.user)
