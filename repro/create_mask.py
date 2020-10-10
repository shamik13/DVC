import json
import math
from pathlib import Path

import cv2
import numpy as np
import PIL.Image
import PIL.ImageDraw
from PIL.Image import Image


class ReproCreateMask:

    raw_dataset_dir: Path

    def create_mask(self):

        Path(self.raw_dataset_dir / "masks").mkdir(parents=True, exist_ok=True)
        self._create_anomaly_mask()
        self._create_normal_mask()

        print("DONE: create_mask")

    def _create_anomaly_mask(self):

        label_to_id = {
            "kizu_dakon": 1,
            "kizu_ware": 2,
            "kizu_zairyou": 3,
            "ignore_shallow": 4,
            "ignore_cutting": 5,
            "ignore_oil": 6,
        }
        for p in self.raw_dataset_dir.glob("jsons/*.json"):

            with open(p) as f:
                mask_info = json.load(f)

            mask = self._create_mask_from_json(mask_info, label_to_id)
            mask.save(self.raw_dataset_dir / f"masks/{p.stem}.png")

    def _create_normal_mask(self):

        for p in self.raw_dataset_dir.glob("color_images/*.jpg"):

            mask_path = self.raw_dataset_dir / f"masks/{p.stem}.png"
            if not mask_path.is_file():
                img = cv2.imread(str(p))
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                mask = np.zeros(img.shape, dtype=np.uint8)
                cv2.imwrite(str(mask_path), mask)

    def _create_mask_from_json(self, mask_info: dict, label_to_id: dict) -> Image:

        """
        Create a mask from json file

        Args:
            mask_info (dict): Mask information from the json file
            label_to_id (dict): Dictionary to convert label name to label id

        Rreference:
            - https://github.com/wkentaro/labelme/blob/master/labelme/utils/shape.py
            - https://github.com/wkentaro/labelme/blob/master/labelme/utils/_io.py
        """

        height = int(mask_info["imageHeight"])
        width = int(mask_info["imageWidth"])
        mask = np.zeros((height, width), dtype=np.int32)

        for polygon_info in mask_info["shapes"]:
            points = polygon_info["points"]
            label = polygon_info["label"]
            shape_type = polygon_info.get("shape_type", None)

            bool_array = np.zeros((height, width), dtype=np.int32)
            bool_array = PIL.Image.fromarray(bool_array)
            draw = PIL.ImageDraw.Draw(bool_array)
            xy = [tuple(point) for point in points]

            if shape_type == "circle":
                assert len(xy) == 2, "Shape of shape_type=circle must have 2 points"
                (cx, cy), (px, py) = xy
                d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
                draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)
            elif shape_type == "rectangle":
                assert len(xy) == 2, "Shape of shape_type=rectangle must have 2 points"
                draw.rectangle(xy, outline=1, fill=1)
            elif shape_type == "line":
                assert len(xy) == 2, "Shape of shape_type=line must have 2 points"
                draw.line(xy=xy, fill=1, width=10)
            elif shape_type == "linestrip":
                draw.line(xy=xy, fill=1, width=10)
            elif shape_type == "point":
                assert len(xy) == 1, "Shape of shape_type=point must have 1 points"
                cx, cy = xy[0]
                r = 5
                draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)
            else:
                assert len(xy) > 2, "Polygon must have points more than 2"
                draw.polygon(xy=xy, outline=1, fill=1)

            bool_array = np.array(bool_array, dtype=bool)
            mask[bool_array] = label_to_id[label]

        return PIL.Image.fromarray(mask.astype(np.uint8), mode="P")
