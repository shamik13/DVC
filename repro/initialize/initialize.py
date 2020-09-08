import os
import shutil
from pathlib import Path

base = Path(".")
for p in base.glob("raw_datasets/*"):
    if p.is_dir():
        shutil.rmtree(p)

shutil.rmtree("/mlflow/data/dataset/images", ignore_errors=True)
shutil.rmtree("/mlflow/data/dataset/masks", ignore_errors=True)

if os.path.exists("/mlflow/data/dataset/info.csv"):
    os.remove("/mlflow/data/dataset/info.csv")
