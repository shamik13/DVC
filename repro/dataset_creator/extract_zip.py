from pathlib import Path
from zipfile import ZipFile


class DatasetCreatorExtractZIP:

    raw_dataset_dir: Path
    zip_path: Path

    def extract_zip(self):

        with ZipFile(self.zip_path, "r") as f:
            f.extractall(self.zip_path.parent)

        Path(self.raw_dataset_dir / "masks").mkdir()
        print("DONE: extract_zip")
