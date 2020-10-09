import json
import random
from pathlib import Path

import cv2
import numpy as np
import pandas as pd


class ReproCreateInfoCSV:

    """
    Create info.csv in DVC/dataset directory. It contains all infomation about the dataset.
    The following description is column explanation in info.csv

    raw_product_id [int]      : The original product id
    product_id [int]          : Timestamp at camera angle 0
    camera_id [int]           : Camera id
    camera_angle [int]        : Camera angle
    crop_type [str]           : The type of image cropping (uncrop, ziku, tobu)
    color_type                : The type of color (color or gray)
    raw_stem [str]            : Raw filename without its suffix
    stem [str]                : Renamed filename without its suffix. [product_id]_[camera_id]_[camera_angle]_[crop_type]_[color_type]
    product_type [str]        : The type of product (B, C, H, K, RAV4, Y1J, YJA)
    received_date [int]       : The date when we received raw datasets
    timestamp [int]           : The time the image was captured
    is_anomaly_image [int]   : Does the image have kizu? 1 (Yes), 0 (No)
    is_anomaly_product [int] : Does the product have kizu? 1 (Yes), 0 (No)
    has_kizu_dakon [int]     : Does the image have kizu_dakon label? 1 (Yes), 0 (No)
    has_kizu_ware [int]      : Does the image have kizu_ware label? 1 (Yes), 0 (No)
    has_kizu_zairyou [int]   : Does the image have kizu_zairyou label? 1 (Yes), 0 (No)
    has_ignore_shallow [int] : Does the image have ignore_shallow label? 1 (Yes), 0 (No)
    has_ignore_cutting [int] : Does the image have ignore_cutting label? 1 (Yes), 0 (No)
    has_ignore_oil [int]     : Does the image have ignore_oil label? 1 (Yes), 0 (No)
    has_sabi [int]           : Does the image have sabi flag? 1 (Yes), 0 (No)
    has_unuse [int]          : Does the image have unuse flag? 1 (Yes), 0 (No)
    data_block_id [int]       : The raw dataset is split into 10 blocks with ID from 0 to 9
    """

    raw_dataset_dir: Path

    def create_info_csv(self):
        df = self._create_base_dataframe()
        df = self._add_angle_and_product_id(df)
        df = self._add_stem(df)
        df = self._add_has_label(df)
        df = self._add_has_flag(df)
        df = self._add_is_anomaly_image(df)
        df = self._add_is_anomaly_product(df)
        df = self._add_data_block_id(df)

    def _create_base_dataframe(self) -> pd.DataFrame:

        # raw_stem is [raw_product_id]_[timestamp (yyyymmddhhmmssmm)]
        # Example: 301_20200825125742544
        di = {"raw_stem": [p.stem for p in self.raw_dataset_dir.glob("color_images/*.jpg")]}
        df = pd.DataFrame(di)
        df["raw_product_id"] = df["raw_stem"].apply(lambda x: int(x.split("_")[0]))
        df["timestamp"] = df["raw_stem"].apply(lambda x: int(x.split("_")[1]))

        # Folder name of raw_dataset is [received_date]_[product_type]_[camera_id]_[normal or anomaly]
        # Example: 20201005_H_2_anomaly
        received_date, product_type, camera_id, _ = self.raw_dataset_dir.stem.split("_")
        df["received_date"] = int(received_date)
        df["product_type"] = product_type
        df["camera_id"] = int(camera_id)
        df["crop_type"] = "uncrop"

        return df

    def _add_angle_and_product_id(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.sort_values(by=["raw_product_id", "timestamp"], ascending=1)
        df["angle"] = -1
        df["product_id"] = -1
        for raw_product_id in df["raw_product_id"].unique():
            expr = df["raw_product_id"] == raw_product_id

            # The image with youngest timestamp is camera angle 0
            for angle, row in enumerate(df[expr].index):
                df.loc[row, "angle"] = angle

            # product_id is timestamp at camera angle 0
            df.loc[expr, "product_id"] = df.loc[expr & (df["angle"] == 0), "timestamp"].item()

        return df

    def _add_stem(self, df: pd.DataFrame) -> pd.DataFrame:

        # stem is [product_id]_[camera_id]_[camera_angle]_[crop_type]_[color_type]
        df["stem"] = ""
        df["stem"] += df["product_id"].apply(lambda x: str(x))
        df["stem"] += "_"
        df["stem"] += df["camera_id"].apply(lambda x: str(x))
        df["stem"] += "_"
        df["stem"] += df["camera_angle"].apply(lambda x: str(x))
        df["stem"] += "_"
        df["stem"] += df["crop_type"]
        df["stem"] += "_"
        df["stem"] += df["color_type"]

        return df

    def _add_has_label(self, df: pd.DataFrame) -> pd.DataFrame:

        df["has_kizu_dakon"] = 0
        df["has_kizu_ware"] = 0
        df["has_kizu_zairyou"] = 0
        df["has_ignore_shallow"] = 0
        df["has_ignore_cutting"] = 0
        df["has_ignore_oil"] = 0

        for raw_stem in df["raw_stem"]:
            mask = cv2.imread(str(self.raw_dataset_dir / f"masks/{raw_stem}.png"))
            expr = df["raw_stem"] == raw_stem

            if sum(mask == 1) != 0:
                df.loc[expr, "has_kizu_dakon"] = 1
            elif sum(mask == 2) != 0:
                df.loc[expr, "has_kizu_ware"] = 1
            elif sum(mask == 3) != 0:
                df.loc[expr, "has_kizu_zairyou"] = 1
            elif sum(mask == 4) != 0:
                df.loc[expr, "has_ignore_shallow"] = 1
            elif sum(mask == 5) != 0:
                df.loc[expr, "has_ignore_cutting"] = 1
            elif sum(mask == 6) != 0:
                df.loc[expr, "has_ignore_oil"] = 1

        return df

    def _add_has_flag(self, df: pd.DataFrame) -> pd.DataFrame:

        df["has_sabi"] = -1
        df["has_unuse"] = -1
        for raw_stem in df["raw_stem"]:
            with open(self.raw_dataset_dir / f"jsons/{raw_stem}.json") as f:
                flag = json.load(f)["flags"]
                sabi = flag["sabi"]
                unuse = flag["unuse"]

            expr = df["raw_stem"] == raw_stem
            df.loc[expr, "has_sabi"] = sabi
            df.loc[expr, "has_unuse"] = unuse

        return df

    def _add_is_anomaly_image(self, df: pd.DataFrame) -> pd.DataFrame:

        df["is_anomaly_image"] = 0
        df["is_anomaly_image"] += df["has_kizu_dakon"]
        df["is_anomaly_image"] += df["has_kizu_ware"]
        df["is_anomaly_image"] += df["has_kizu_zairyou"]
        df.loc[df["is_anomaly_image"] != 0, "is_anomaly_image"] = 1

        return df

    def _add_is_anomaly_product(self, df: pd.DataFrame) -> pd.DataFrame:

        df["is_anomaly_product"] = -1
        for product in df["product"].unique():
            expr = df["product"] == product
            df.loc[expr, "is_anomaly_product"] = df.loc[expr, "is_anomaly_image"].sum()
        df.loc[df["is_anomaly_product"] != 0, "is_anomaly_product"] = 1

        return df

    def _add_data_block_id(self, df: pd.DataFrame) -> pd.DataFrame:

        # Split the dataset into ten blocks based on product id
        # A seed value is specified to preserve the reproducibility of the split
        product_id_list = df["product_id"].unique()
        random.Random(0).shuffle(product_id_list)
        ten_blocks = np.array_split(product_id_list, 10)

        df["data_block_id"] = -1
        for block_id, block in enumerate(ten_blocks):
            for product_id in block:
                df.loc[df["product_id"] == product_id, "data_block_id"] = block_id

        return df
