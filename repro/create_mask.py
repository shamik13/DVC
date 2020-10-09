import json
from pathlib import Path

import cv2
import labelme
import numpy as np


class ReproCreateMask:

    raw_dataset_dir: Path

    def create_mask(self):

        Path(self.raw_dataset_dir / "masks").mkdir(parents=True, exist_ok=True)
        self._create_anomaly_mask()
        self._create_normal_mask()
        print("DONE: create_mask")

    def _create_anomaly_mask(self):

        label_name_to_value = {
            "kizu_dakon": 1,
            "kizu_ware": 2,
            "kizu_zairyou": 3,
            "ignore_shallow": 4,
            "ignore_cutting": 5,
            "ignore_oil": 6,
        }
        for p in self.raw_dataset_dir.glob("jsons/*.json"):

            with open(p) as f:
                data = json.load(f)

            # labelme.utils.shapes_to_label returns cls and ins
            # cls is a mask for semantic segmentation
            # ins is a mask for instance segmentation
            # https://github.com/wkentaro/labelme/blob/master/labelme/utils/shape.py
            mask, _ = labelme.utils.shapes_to_label(
                img_shape=(int(data["imageHeight"]), int(data["imageWidth"])),
                shapes=data["shapes"],
                label_name_to_value=label_name_to_value,
            )

            labelme.utils.lblsave(self.raw_dataset_dir / f"masks/{p.stem}.png", mask)

    def _create_normal_mask(self):

        for p in self.raw_dataset_dir.glob("color_images/*.jpg"):

            mask_path = self.raw_dataset_dir / f"masks/{p.stem}.png"
            if not mask_path.is_file():
                img = cv2.imread(str(p))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                mask = np.zeros(img.shape, dtype=np.uint8)
                cv2.imwrite(str(mask_path), mask)
