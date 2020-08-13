import pandas as pd
from pathlib import Path


class DatasetCreatorRenameFiles:

    base: Path

    def rename_files(self):

        df = pd.read_csv(self.base / "info.csv")
        for i in df.index:

            old_stem = df.loc[i, "old_stem"]
            new_stem = df.loc[i, "stem"]

            old_img_path = self.base / f"images/{old_stem}.bmp"
            new_img_path = self.base / f"images/{new_stem}.bmp"

            old_mask_path = self.base / f"masks/{old_stem}.png"
            new_mask_path = self.base / f"masks/{new_stem}.png"

            old_json_path = self.base / f"jsons/{old_stem}.json"
            new_json_path = self.base / f"jsons/{new_stem}.json"

            if old_img_path.is_file():
                old_img_path.rename(new_img_path)

            if old_mask_path.is_file():
                old_mask_path.rename(new_mask_path)

            if old_json_path.is_file():
                old_json_path.rename(new_json_path)
