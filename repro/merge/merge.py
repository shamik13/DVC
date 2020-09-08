from pathlib import Path

import pandas as pd

base = Path(".")

# Create empty folders
Path(base / "dataset/images").mkdir(parents=True, exist_ok=True)
Path(base / "dataset/masks").mkdir(parents=True, exist_ok=True)

# Merge images and masks
for p in base.glob("raw_datasets/*/images/*.jpg"):
    p.rename(base / f"dataset/images/{p.name}")

for p in base.glob("raw_datasets/*/masks/*.png"):
    p.rename(base / f"dataset/masks/{p.name}")

# Merge info.csv
for p in base.glob("raw_datasets/*/info.csv"):
    raw_info = pd.read_csv(p)

    if Path(base / "dataset/info.csv").is_file():
        info = pd.read_csv(base / "dataset/info.csv")
        merged_info = pd.concat([raw_info, info])
    else:
        merged_info = raw_info

    merged_info.drop_duplicates(subset="stem", inplace=True)
    merged_info.to_csv(base / "dataset/info.csv", index=False)
