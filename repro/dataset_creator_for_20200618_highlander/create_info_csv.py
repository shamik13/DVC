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
        df["raw_product_id"] = df["raw_stem"].apply(lambda x: int(x.split("_")[0]))
        df["angle"] = df["raw_stem"].apply(lambda x: int(x.split("_")[1]))

        received_date, product_type, crop_type, _ = self.raw_dataset_dir.stem.split("_")
        df["received_date"] = int(received_date)
        df["product_type"] = product_type
        df["camera"] = 2  # NOTE: 20200618 highlander datasets come from camera 2
        df["crop_type"] = crop_type
        return df

    def _add_timestamp_and_stem_column(self, df: pd.DataFrame) -> pd.DataFrame:

        # Create the surrogate timestamp, because the actual timestamp is not available.
        # Actual timestamp is 16 digits (yyyymmddhhmmssmm).
        df["timestamp"] = (
            df["received_date"].apply(lambda x: str(x))
            + df["product_id"].apply(lambda x: str(x).zfill(4))
            + df["angle"].apply(lambda x: str(x).zfill(4))
        )

        # product_id is a timestamp at camera angle 0
        df["product_id"] = (
            df["received_date"].apply(lambda x: str(x))
            + df["product_id"].apply(lambda x: str(x).zfill(4))
            + "0000"
        )

        # stem is [product_id]_[angle]
        df["stem"] = (
            df["product_id"].apply(lambda x: str(x).zfill(4))
            + "_"
            + df["angle"].apply(lambda x: str(x))
        )

        df["timestamp"] = df["timestamp"].apply(lambda x: int(x))
        df["product_id"] = df["product_id"].apply(lambda x: int(x))
        df["stem"] = df["stem"].apply(lambda x: int(x))
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
        for product_id in df["product_id"].unique():
            expr = df["product_id"] == product_id
            df.loc[expr, "is_anomaly_product"] = df.loc[expr, "is_anomaly_image"].sum()
        df.loc[df["is_anomaly_product"] != 0, "is_anomaly_product"] = 1
        return df

    def _add_supervise_column(self, df: pd.DataFrame) -> pd.DataFrame:

        TRAIN_SIZE = 0.7  # TODO: Inoue: I should move this param into param.yaml

        product_id_list = df["product_id"].unique()
        random.Random(0).shuffle(product_id_list)

        threshold = int(len(product_id_list) * TRAIN_SIZE)
        train_product_id_list = product_id_list[:threshold]
        test_product_id_list = product_id_list[threshold:]

        df["supervise"] = -1
        for train_product_id in train_product_id_list:
            df.loc[df["product_id"] == train_product_id, "supervised"] = "train"
        for test_product_id in test_product_id_list:
            df.loc[df["product_id"] == test_product_id, "supervised"] = "test"
        return df

    def _check_for_default_values(self, df: pd.DataFrame):

        for column in df.columns:
            if sum(df[column] == -1) == 0:
                return df
            else:
                print("Default value -1 is not updated.")
                sys.exit(1)
