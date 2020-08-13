import pandas as pd
import cv2
import random
from pathlib import Path


class DatasetCreatorCreateInfoCSV:

    base: Path

    def create_info_csv(self):

        df = self.create_base_dataframe()
        df = self.add_angle_and_stem_column(df)
        df = self.add_is_anomaly_image_column(df)
        df = self.add_is_anomaly_product_column(df)
        df = self.add_is_train_and_is_test_column(df)
        df.to_csv(self.base / "info.csv", index=False)

    def create_base_dataframe(self) -> pd.DataFrame:

        df = pd.DataFrame({"old_stem": [p.stem for p in self.base.glob("images/*.bmp")]})
        df["product"] = df["old_stem"].apply(lambda x: x.split("_")[0])
        df["product"] = df["product"].apply(lambda x: int(x))
        df["timestamp"] = df["old_stem"].apply(lambda x: "".join(x.split("_")[1:]))
        df["product_identifier"] = int(self.base.stem.split("_")[0])
        df["product_type"] = self.base.stem.split("_")[1]
        return df

    def add_angle_and_stem_column(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.sort_values(by=["product", "timestamp"])
        df["angle"] = -1
        df["stem"] = -1
        for product in df["product"].unique():
            for angle, row in enumerate(df.query("product==@product").index):
                df.loc[row, "angle"] = angle
                df.loc[row, "stem"] = df.query("product==@product & angle==0")["timestamp"].item()
        df["stem"] = df["stem"] + "_" + df["angle"].apply(lambda x: str(x))
        return df

    def add_is_anomaly_image_column(self, df: pd.DataFrame) -> pd.DataFrame:

        df["is_anomaly_image"] = -1
        for old_stem in df["old_stem"]:
            mask = cv2.imread(str(self.base / f"masks/{old_stem}.png"))
            if mask.sum() == 0:
                df.loc[df["old_stem"] == old_stem, "is_anomaly_image"] = 0
            else:
                df.loc[df["old_stem"] == old_stem, "is_anomaly_image"] = 1
        return df

    def add_is_anomaly_product_column(self, df: pd.DataFrame) -> pd.DataFrame:

        df["is_anomaly_product"] = -1
        for product in df["product"].unique():
            expr = df["product"] == product
            df.loc[expr, "is_anomaly_product"] = df.loc[expr, "is_anomaly_image"].sum()
        df.loc[df["is_anomaly_product"] != 0, "is_anomaly_product"] = 1
        return df

    def add_is_train_and_is_test_column(self, df: pd.DataFrame) -> pd.DataFrame:

        TRAIN_SIZE = 0.7  # TODO: I have to move this param into param.yaml

        product_list = df["product"].unique()
        product_identifier = int(self.base.stem.split("_")[0])
        random.Random(product_identifier).shuffle(product_list)

        threshold = int(len(product_list) * TRAIN_SIZE)
        train_product_list = product_list[:threshold]
        test_product_list = product_list[threshold:]

        df["is_train"] = 0
        for train_product in train_product_list:
            df.loc[df["product"] == train_product, "is_train"] = 1

        df["is_test"] = 0
        for test_product in test_product_list:
            df.loc[df["product"] == test_product, "is_test"] = 1

        return df
