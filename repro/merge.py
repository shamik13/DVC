from pathlib import Path

import pandas as pd


class ReproMerge:

    raw_dataset_dir: Path
    dataset_dir: Path

    def merge(self):

        self._merge_files()
        self._merge_info_csv()
        print("DONE: merge_raw_dataset")

    def _merge_files(self):

        Path(self.dataset_dir / "images").mkdir(parents=True, exist_ok=True)
        Path(self.dataset_dir / "masks").mkdir(parents=True, exist_ok=True)

        for p in self.raw_dataset_dir.glob("images/*.bmp"):
            p.rename(self.dataset_dir / f"images/{p.name}")

        for p in self.raw_dataset_dir.glob("masks/*.png"):
            p.rename(self.dataset_dir / f"masks/{p.name}")

    def _merge_info_csv(self):

        raw_dataset_df = pd.read_csv(self.raw_dataset_dir / "info.csv")

        if Path(self.dataset_dir / "info.csv").is_file():
            dataset_df = pd.read_csv(self.dataset_dir / "info.csv")
            merged_df = pd.concat([raw_dataset_df, dataset_df])
        else:
            merged_df = raw_dataset_df

        merged_df.drop_duplicates(subset="stem", inplace=True)
        merged_df.to_csv(self.dataset_dir / "info.csv", index=False)
