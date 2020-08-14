from zipfile import ZipFile
from pathlib import Path


class DatasetCreatorExtractZIP:

    zip_path: Path
    base: Path

    def extract_zip(self):

        with ZipFile(self.DVC / f"zip_dvc/{self.unzip_dir.stem}.zip", "r") as f:
            f.extractall(self.unzip_dir.parent)

        Path(self.unzip_dir / "masks").mkdir()
        print("DONE: extract_zip")
