import zipfile
from pathlib import Path
import pandas as pd
from tqdm import tqdm
import cv2
import json
import labelme
import numpy as np


base = Path("/dgx/github/DVC/data")
print("Added modification")

for p in base.glob("*.zip"):

    with zipfile.ZipFile(p, "r") as f:
        f.extractall(base / "prepared")

Path(base / "prepared/dataset/masks").mkdir(exist_ok=True)
label_name_to_value = {"toubu_kizu": 1, "toubu_kizu_outside_marking": 0}
for p in tqdm(base.glob("prepared/dataset/jsons/*")):

    with open(p) as f:
        data = json.load(f)

    label = labelme.utils.shapes_to_label(
        img_shape=(int(data["imageHeight"]), int(data["imageWidth"])),
        shapes=data["shapes"],
        label_name_to_value=label_name_to_value,
    )

    labelme.utils.lblsave(base / f"prepared/dataset/masks/{p.stem}.png", label)

# Create masks for images without kizu
for p in tqdm(base.glob("prepared/dataset/images/*.bmp")):

    mask_path = base / f"prepared/dataset/masks/{p.stem}.png"
    if not mask_path.is_file():
        img = cv2.imread(str(p))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask = np.zeros(img.shape, dtype=np.uint8)
        cv2.imwrite(str(mask_path), mask)


df = pd.DataFrame({"old_stem": [p.stem for p in base.glob("prepared/dataset/images/*.bmp")]})
df["product"] = df["old_stem"].apply(lambda x: x.split("_")[0])
df["timestamp"] = df["old_stem"].apply(lambda x: "".join(x.split("_")[1:]))
df = df.sort_values(by=["product", "timestamp"])


df["angle"] = -1
df["new_stem"] = -1
for product in tqdm(df["product"].unique()):
    for angle, row in enumerate(df.query("product==@product").index):
        df.loc[row, "angle"] = angle
        df.loc[row, "new_stem"] = df.query("product==@product & angle==0")["timestamp"].item()
df["new_stem"] = df["new_stem"] + "_" + df["angle"].apply(lambda x: str(x))


df["is_anomaly_image"] = -1
for old_stem in tqdm(df["old_stem"]):
    mask = cv2.imread(str(base / f"prepared/dataset/masks/{old_stem}.png"))
    if mask.sum() == 0:
        df.loc[df["old_stem"] == old_stem, "is_anomaly_image"] = 0
    else:
        df.loc[df["old_stem"] == old_stem, "is_anomaly_image"] = 1


df["is_anomaly_product"] = -1
for product in tqdm(df["product"].unique()):
    expr = df["product"] == product
    df.loc[expr, "is_anomaly_product"] = df.loc[expr, "is_anomaly_image"].sum()
df.loc[df["is_anomaly_product"] != 0, "is_anomaly_product"] = 1

df.to_csv(base / "prepared/info.csv", index=False)
