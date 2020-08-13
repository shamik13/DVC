from zipfile import ZipFile
from pathlib import Path


class DatasetCreatorExtractZIP:

    zip_path: Path
    base: Path

    def extract_zip(self):

        with ZipFile(self.zip_path, "r") as f:
            f.extractall(self.zip_path.parent)

        Path(self.base / "masks").mkdir()
