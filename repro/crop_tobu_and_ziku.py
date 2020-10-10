from pathlib import Path

import cv2
import numpy as np
import pandas as pd


class ReproCropTobuAndZiku:

    raw_dataset_dir: Path

    def crop_tobu_and_ziku(self) -> None:

        df = pd.read_csv(self.raw_dataset_dir / "info.csv")
        df = self._add_tobu_row_and_ziku_row(df)
        self._crop_img(df)
        self._crop_mask(df)
        df = self._update_has_label(df)
        df = self._update_has_flag(df)
        df = self._update_is_anomaly_image(df)
        df = self._update_is_anomaly_product(df)
        df.to_csv(self.raw_dataset_dir / "info.csv", index=False)

        print("DONE: crop_tobu_and_ziku")

    def _add_tobu_row_and_ziku_row(self, df: pd.DataFrame) -> pd.DataFrame:

        out_df = df.copy()

        for row in df.loc[df["camera_id"] == 2].index:

            # stem is [product_id]_[camera_id]_[camera_angle]_[crop_type]
            # Example: 20200914175813908_2_10_uncrop
            stem = df.loc[row, "stem"]
            product_id, camera_id, camera_angle, crop_type = stem.split("_")
            tobu_stem = f"{product_id}_{camera_id}_{camera_angle}_tobu"
            ziku_stem = f"{product_id}_{camera_id}_{camera_angle}_ziku"

            tobu_row = df.iloc[row].copy()
            tobu_row["stem"] = tobu_stem
            tobu_row["crop_type"] = "tobu"

            ziku_row = df.iloc[row].copy()
            ziku_row["stem"] = ziku_stem
            ziku_row["crop_type"] = "ziku"

            out_df = out_df.append(tobu_row, ignore_index=True)
            out_df = out_df.append(ziku_row, ignore_index=True)

        return out_df

    def _crop_img(self, df: pd.DataFrame, boundary: int = 980) -> None:

        for row in df.loc[df["crop_type"] == "uncrop"].index:

            stem = df.loc[row, "stem"]
            product_id, camera_id, camera_angle, _ = stem.split("_")
            tobu_stem = f"{product_id}_{camera_id}_{camera_angle}_tobu"
            ziku_stem = f"{product_id}_{camera_id}_{camera_angle}_ziku"

            for color_type in ["color", "gray"]:
                for suffix in ["bmp", "jpg"]:

                    parent_dir = self.raw_dataset_dir / f"{color_type}_images"
                    img = cv2.imread(str(parent_dir / f"{stem}.{suffix}"))
                    tobu_img = img[:, :boundary, :]
                    ziku_img = img[:, boundary:, :]

                    cv2.imwrite(str(parent_dir / f"{tobu_stem}.{suffix}"), tobu_img)
                    cv2.imwrite(str(parent_dir / f"{ziku_stem}.{suffix}"), ziku_img)

    def _crop_mask(self, df: pd.DataFrame, boundary: int = 980) -> None:

        for row in df.loc[df["crop_type"] == "uncrop"].index:

            stem = df.loc[row, "stem"]
            product_id, camera_id, camera_angle, _ = stem.split("_")
            tobu_stem = f"{product_id}_{camera_id}_{camera_angle}_tobu"
            ziku_stem = f"{product_id}_{camera_id}_{camera_angle}_ziku"

            mask_path = self.raw_dataset_dir / f"masks/{stem}.png"
            mask = cv2.imread(str(mask_path))
            tobu_mask = mask[:, :boundary, :]
            ziku_mask = mask[:, boundary:, :]

            cv2.imwrite(str(self.raw_dataset_dir / f"masks/{tobu_stem}.png"), tobu_mask)
            cv2.imwrite(str(self.raw_dataset_dir / f"masks/{ziku_stem}.png"), ziku_mask)

    def _update_has_label(self, df: pd.DataFrame) -> pd.DataFrame:

        # Initialize has_label column
        expr = df["crop_type"] != "uncrop"
        df.loc[expr, "has_kizu_dakon"] = 0
        df.loc[expr, "has_kizu_ware"] = 0
        df.loc[expr, "has_kizu_zairyou"] = 0
        df.loc[expr, "has_ignore_shallow"] = 0
        df.loc[expr, "has_ignore_cutting"] = 0
        df.loc[expr, "has_ignore_oil"] = 0

        for stem in df.loc[expr, "stem"]:

            mask = cv2.imread(str(self.raw_dataset_dir / f"masks/{stem}.png"))
            expr = df["stem"] == stem

            if np.sum(mask == 1) != 0:
                df.loc[expr, "has_kizu_dakon"] = 1
            if np.sum(mask == 2) != 0:
                df.loc[expr, "has_kizu_ware"] = 1
            if np.sum(mask == 3) != 0:
                df.loc[expr, "has_kizu_zairyou"] = 1
            if np.sum(mask == 4) != 0:
                df.loc[expr, "has_ignore_shallow"] = 1
            if np.sum(mask == 5) != 0:
                df.loc[expr, "has_ignore_cutting"] = 1
            if np.sum(mask == 6) != 0:
                df.loc[expr, "has_ignore_oil"] = 1

        return df

    def _update_has_flag(self, df: pd.DataFrame) -> pd.DataFrame:

        """
        At camera id == 2, the flag is annotated to the uncrop image.
        Therefore, what the flag indicates is not necessarily contained in ziku or head image.
        However, has_sabi and has_unuse in info.csv are the same between uncrop, tobu and ziku.
        """

        return df

    def _update_is_anomaly_image(self, df: pd.DataFrame) -> pd.DataFrame:

        # Initialize is_anomaly_image column
        expr = df["crop_type"] != "uncrop"
        df.loc[expr, "is_anomaly_image"] = 0

        df.loc[expr, "is_anomaly_image"] += df["has_kizu_dakon"]
        df.loc[expr, "is_anomaly_image"] += df["has_kizu_ware"]
        df.loc[expr, "is_anomaly_image"] += df["has_kizu_zairyou"]
        df.loc[expr & (df["is_anomaly_image"] != 0), "is_anomaly_image"] = 1

        return df

    def _update_is_anomaly_product(self, df: pd.DataFrame) -> pd.DataFrame:

        # Initialize is_anomaly_product column
        uncrop_expr = df["crop_type"] != "uncrop"
        df.loc[uncrop_expr, "is_anomaly_product"] = -1

        for product_id in df["product_id"].unique():

            tobu_expr = (df["product_id"] == product_id) & (df["crop_type"] == "tobu")
            df.loc[tobu_expr, "is_anomaly_product"] = df.loc[tobu_expr, "is_anomaly_image"].sum()

            ziku_expr = (df["product_id"] == product_id) & (df["crop_type"] == "ziku")
            df.loc[ziku_expr, "is_anomaly_product"] = df.loc[ziku_expr, "is_anomaly_image"].sum()

        df.loc[uncrop_expr & (df["is_anomaly_product"] != 0), "is_anomaly_product"] = 1

        return df
