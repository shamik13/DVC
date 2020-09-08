from pathlib import Path

import pandas as pd


class DatasetCreatorMergeRawDataset:

    raw_dataset_dir: Path
    dataset_dir: Path

    def merge_raw_dataset(self):

        self._merge_files()
        self._merge_info_csv()
        print("DONE: merge_raw_dataset")

    def _merge_files(self):

        Path(self.dataset_dir / "images").mkdir(parents=True, exist_ok=True)
        Path(self.dataset_dir / "masks").mkdir(parents=True, exist_ok=True)

        for p in self.raw_dataset_dir.glob("images/*.jpg"):
            p.rename(self.dataset_dir / f"images/{p.name}")

        for p in self.raw_dataset_dir.glob("masks/*.png"):
            p.rename(self.dataset_dir / f"masks/{p.name}")

    def _merge_info_csv(self):

        raw_info = pd.read_csv(self.raw_dataset_dir / "info.csv")

        if Path(self.dataset_dir / "info.csv").is_file():
            info = pd.read_csv(self.dataset_dir / "info.csv")
            merged_info = pd.concat([raw_info, info])
        else:
            merged_info = raw_info

        merged_info.drop_duplicates(subset="stem", inplace=True)
        merged_info.to_csv(self.dataset_dir / "info.csv", index=False)
