import json
import re
import sys
from pathlib import Path

import numpy as np


class ReproCheckFormat:

    """
    Check the format of a raw dataset
    """

    raw_dataset_dir: Path

    def check_format(self) -> None:
        self._check_naming_convention()
        self._check_num_images()
        self._check_label_and_flag()
        self._check_camera_angle()

        print("DONE: check_format")

    def _check_naming_convention(self) -> None:

        """
        Predefined naming convention without suffix is [product_id]_[timestamp (yyyymmddhhmmssmmm)]
        Pattern: [0-9]+_[0-9]{16}
        Example: 301_20200825125742544
        """

        for color_type in ["color", "gray"]:
            for suffix in ["bmp", "jpg"]:

                pattern = re.compile(r"\d+_\d{17}." + f"{suffix}")
                for p in self.raw_dataset_dir.glob(f"{color_type}_images/*.{suffix}"):
                    if not pattern.match(p.name):
                        sys.exit(1)

    def _check_num_images(self) -> None:

        """
        Check that the number of images is same
        between color_images/*.bmp, color_images/*.jpg, gray_images/*.bmp and gray_images/*.jpg

        ├── color_images
        |   ├── *.bmp
        |   └── *.jpg
        └── gray_images
            ├── *.bmp
            └── *.jpg
        """

        num_images_list = []
        num_images_list.append(len([p for p in self.raw_dataset_dir.glob("color_images/*.bmp")]))
        num_images_list.append(len([p for p in self.raw_dataset_dir.glob("color_images/*.jpg")]))
        num_images_list.append(len([p for p in self.raw_dataset_dir.glob("gray_images/*.bmp")]))
        num_images_list.append(len([p for p in self.raw_dataset_dir.glob("gray_images/*.jpg")]))

        if len(set(num_images_list)) != 1:
            print("Error: _check_num_images")
            sys.exit(1)

    def _check_label_and_flag(self) -> None:

        """
        Check that labels and flags are in the predefined names
        """

        predefined_labels = [
            "kizu_dakon",
            "kizu_ware",
            "kizu_zairyou",
            "ignore_shallow",
            "ignore_cutting",
            "ignore_oil",
        ]
        predefined_flags = ["sabi", "unuse"]

        # Normal dataset doesn't have jsons/ folder, so the following for loop is skipped.
        for p in self.raw_dataset_dir.glob("jsons/*.json"):
            with open(p) as f:
                annotaiton = json.load(f)
                label_list = annotaiton["shapes"]
                flag_dict = annotaiton["flags"]

            for label in label_list:
                label_name = label["label"]
                if label_name not in predefined_labels:
                    sys.exit(1)

            for flag_name in flag_dict.keys():
                if flag_name not in predefined_flags:
                    sys.exit(1)

    def _check_camera_angle(self) -> None:

        """
        Check that the camera angle is not too many or too few
        """

        for color_type in ["color", "gray"]:
            for suffix in ["bmp", "jpg"]:

                # p.stem is [raw_product_id]_[timestamp (yyyymmddhhmmssmmm)]
                product_id_list = []
                for p in self.raw_dataset_dir.glob(f"{color_type}_images/*.{suffix}"):
                    product_id_list.append(p.stem.split("_")[0])

                _, counts = np.unique(product_id_list, return_counts=True)
                if len(set(counts)) != 1:
                    sys.exit(1)
