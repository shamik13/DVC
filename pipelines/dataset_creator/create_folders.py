from pathlib import Path


class DatasetCreatorCreateFolders:

    zip_path: Path

    def create_folders(self):

        Path(self.zip_path.parent / "dataset/images").mkdir(parents=True, exist_ok=True)
        Path(self.zip_path.parent / "dataset/masks").mkdir(parents=True, exist_ok=True)

    def move_files(self):

        for p in self.base.glob("images/*.bmp"):
            p.rename(self.base.parent / f"dataset/images/{p.stem}.bmp")

        for p in self.base.glob("masks/*.png"):
            p.rename(self.base.parent / f"dataset/masks/{p.stem}.png")

        Path(self.base / "info.csv").rename(self.base.parent / "dataset/info.csv")
