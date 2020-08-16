from pathlib import Path

import pandas as pd


class DatasetCreatorRenameFiles:

    raw_dataset_dir: Path

    def rename_files(self):

        df = pd.read_csv(self.raw_dataset_dir / "info.csv")
        for i in df.index:

            old_stem = df.loc[i, "old_stem"]
            new_stem = df.loc[i, "stem"]

            old_img_path = self.raw_dataset_dir / f"images/{old_stem}.bmp"
            new_img_path = self.raw_dataset_dir / f"images/{new_stem}.bmp"

            old_mask_path = self.raw_dataset_dir / f"masks/{old_stem}.png"
            new_mask_path = self.raw_dataset_dir / f"masks/{new_stem}.png"

            old_json_path = self.raw_dataset_dir / f"jsons/{old_stem}.json"
            new_json_path = self.raw_dataset_dir / f"jsons/{new_stem}.json"

            if old_img_path.is_file():
                old_img_path.rename(new_img_path)

            if old_mask_path.is_file():
                old_mask_path.rename(new_mask_path)

            if old_json_path.is_file():
                old_json_path.rename(new_json_path)

        print("DONE: rename_files")
