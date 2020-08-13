import cv2
import json
import labelme
import numpy as np
from pathlib import Path


class DatasetCreatorCreateMask:

    base: Path

    def create_mask(self):

        self.create_anomaly_mask()
        self.create_normal_mask()

    def create_anomaly_mask(self):

        label_name_to_value = {"toubu_kizu": 1, "toubu_kizu_outside_marking": 0}
        for p in self.base.glob("jsons/*.json"):

            with open(p) as f:
                data = json.load(f)

            label = labelme.utils.shapes_to_label(
                img_shape=(int(data["imageHeight"]), int(data["imageWidth"])),
                shapes=data["shapes"],
                label_name_to_value=label_name_to_value,
            )

            labelme.utils.lblsave(self.base / f"masks/{p.stem}.png", label)

    def create_normal_mask(self):

        for p in self.base.glob("images/*.bmp"):

            mask_path = self.base / f"masks/{p.stem}.png"
            if not mask_path.is_file():
                img = cv2.imread(str(p))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                mask = np.zeros(img.shape, dtype=np.uint8)
                cv2.imwrite(str(mask_path), mask)
