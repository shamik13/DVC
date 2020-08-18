import random
import sys
from pathlib import Path

import cv2
import pandas as pd


class DatasetCreatorCreateInfoCSV:

    raw_dataset_dir: Path

    def create_info_csv(self):

        df = self._create_base_dataframe()
        df = self._add_angle_and_stem_column(df)
        df = self._add_is_anomaly_image_column(df)
        df = self._add_is_anomaly_product_column(df)
        df = self._add_supervise_column(df)
        df = self._check_for_default_values(df)
        df.to_csv(self.raw_dataset_dir / "info.csv", index=False)
        print("DONE: create_info_csv")

    def _create_base_dataframe(self) -> pd.DataFrame:

        di = {"raw_stem": [p.stem for p in self.raw_dataset_dir.glob("images/*.bmp")]}
        df = pd.DataFrame(di)
        df["product"] = df["raw_stem"].apply(lambda x: x.split("_")[0])
        df["product"] = df["product"].apply(lambda x: int(x))
        df["timestamp"] = df["raw_stem"].apply(lambda x: "".join(x.split("_")[1:]))

        received_date, product_type, work_station, _ = self.raw_dataset_dir.stem.split("_")
        df["received_date"] = int(received_date)
        df["product_type"] = product_type
        df["work_station"] = int(work_station)
        df["crop_type"] = "tobu"
        return df

    def _add_angle_and_stem_column(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.sort_values(by=["product", "timestamp"])
        df["angle"] = -1
        df["stem"] = -1
        for product in df["product"].unique():
            for angle, row in enumerate(df.query("product==@product").index):
                df.loc[row, "angle"] = angle
                df.loc[row, "stem"] = df.query("product==@product & angle==0")["timestamp"].item()

        # TODO: Inoue: Fix here when we receive new datasets
        df["stem"] = (
            df["stem"]
            + df["product"].apply(lambda x: str(x).zfill(3))
            + "_"
            + df["crop_type"]
            + "_"
            + df["angle"].apply(lambda x: str(x))
        )
        return df

    def _add_is_anomaly_image_column(self, df: pd.DataFrame) -> pd.DataFrame:

        df["is_anomaly_image"] = -1
        for raw_stem in df["raw_stem"]:
            mask = cv2.imread(str(self.raw_dataset_dir / f"masks/{raw_stem}.png"))
            if mask.sum() == 0:
                df.loc[df["raw_stem"] == raw_stem, "is_anomaly_image"] = 0
            else:
                df.loc[df["raw_stem"] == raw_stem, "is_anomaly_image"] = 1
        return df

    def _add_is_anomaly_product_column(self, df: pd.DataFrame) -> pd.DataFrame:

        df["is_anomaly_product"] = -1
        for product in df["product"].unique():
            expr = df["product"] == product
            df.loc[expr, "is_anomaly_product"] = df.loc[expr, "is_anomaly_image"].sum()
        df.loc[df["is_anomaly_product"] != 0, "is_anomaly_product"] = 1
        return df

    def _add_supervise_column(self, df: pd.DataFrame) -> pd.DataFrame:

        TRAIN_SIZE = 0.7  # TODO: Inoue: I should move this param into param.yaml

        product_list = df["product"].unique()
        random.Random(0).shuffle(product_list)

        threshold = int(len(product_list) * TRAIN_SIZE)
        train_product_list = product_list[:threshold]
        test_product_list = product_list[threshold:]

        df["supervise"] = -1
        for train_product in train_product_list:
            df.loc[df["product"] == train_product, "supervise"] = "train"
        for test_product in test_product_list:
            df.loc[df["product"] == test_product, "supervise"] = "test"
        return df

    def _check_for_default_values(self, df: pd.DataFrame):

        for column in df.columns:
            if sum(df[column] == -1) == 0:
                return df
            else:
                print("Default value -1 is not updated.")
                sys.exit(1)
