from pathlib import Path


class DatasetCreatorCreateDatasetDirectory:

    raw_dataset_dir: Path
    dataset_dir: Path

    def create_dataset_directory(self):

        Path(self.dataset_dir / "images").mkdir(parents=True, exist_ok=True)
        Path(self.dataset_dir / "masks").mkdir(parents=True, exist_ok=True)
        print("DONE: create_folders")

    def move_files(self):

        for p in self.raw_dataset_dir.glob("images/*.bmp"):
            p.rename(self.dataset_dir / f"images/{p.name}")

        for p in self.raw_dataset_dir.glob("masks/*.png"):
            p.rename(self.dataset_dir / f"masks/{p.name}")

        Path(self.raw_dataset_dir / "info.csv").rename(self.dataset_dir / "info.csv")
        print("DONE: move_files")
