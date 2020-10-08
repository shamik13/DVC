from pathlib import Path
from zipfile import ZipFile


class ReproUnzip:

    zip_path: Path

    def extract_zip(self):

        with ZipFile(self.zip_path, "r") as f:
            f.extractall(self.zip_path.parent)
