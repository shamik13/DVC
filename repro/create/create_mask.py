import json
from pathlib import Path

import cv2
import labelme
import numpy as np


class DatasetCreatorCreateMask:

    raw_dataset_dir: Path

    def create_mask(self):

        Path(self.raw_dataset_dir / "masks").mkdir(parents=True, exist_ok=True)
        self.create_anomaly_mask()
        self.create_normal_mask()
        print("DONE: create_mask")

    def create_anomaly_mask(self):

        label_name_to_value = {"toubu_kizu": 1, "toubu_kizu_outside_marking": 0}
        for p in self.raw_dataset_dir.glob("jsons/*.json"):

            with open(p) as f:
                data = json.load(f)

            label = labelme.utils.shapes_to_label(
                img_shape=(int(data["imageHeight"]), int(data["imageWidth"])),
                shapes=data["shapes"],
                label_name_to_value=label_name_to_value,
            )

            labelme.utils.lblsave(self.raw_dataset_dir / f"masks/{p.stem}.png", label)

    def create_normal_mask(self):

        for p in self.raw_dataset_dir.glob("images/*.bmp"):

            mask_path = self.raw_dataset_dir / f"masks/{p.stem}.png"
            if not mask_path.is_file():
                img = cv2.imread(str(p))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                mask = np.zeros(img.shape, dtype=np.uint8)
                cv2.imwrite(str(mask_path), mask)
