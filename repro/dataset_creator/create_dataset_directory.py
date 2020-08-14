from pathlib import Path


class DatasetCreatorCreateDatasetDirectory:

    base: Path
    zip_path: Path

    def create_dataset_directory(self):

        Path(self.DVC / "dataset/images").mkdir(parents=True, exist_ok=True)
        Path(self.DVC / "dataset/masks").mkdir(parents=True, exist_ok=True)
        print("DONE: create_folders")

    def move_files(self):

        for p in self.unzip_dir.glob("images/*.bmp"):
            p.rename(self.DVC / f"dataset/images/{p.name}")

        for p in self.unzip_dir.glob(f"masks/*.png"):
            p.rename(self.DVC / f"dataset/masks/{p.name}")

        Path(self.unzip_dir / "info.csv").rename(self.DVC / "dataset/info.csv")
        print("DONE: move_files")
