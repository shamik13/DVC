from pathlib import Path

from .check_format import ReproCheckFormat
from .create_info_csv import ReproCreateInfoCSV
from .create_mask import ReproCreateMask
from .merge import ReproMerge
from .rename import ReproRename
from .unzip import ReproUnzip


class Repro(
    ReproCheckFormat, ReproCreateInfoCSV, ReproCreateMask, ReproMerge, ReproRename, ReproUnzip
):
    def __init__(self, raw_dataset_dir: Path, dataset_dir: Path, zip_path: Path):

        """
        Args:
            raw_dataset_dir (Path): path to unzipped directory
            dataset_dir (Path): path to dataset directory for DL models
            zip_path (Path): path to zip file
        """

        self.raw_dataset_dir = raw_dataset_dir
        self.dataset_dir = dataset_dir
        self.zip_path = zip_path


if __name__ == "__main__":

    base = Path("/dgx/shared/nas/inoue/DVC")

    for zip_path in base.glob("raw_datasets/*.zip"):

        raw_dataset_dir = zip_path.parent / zip_path.stem
        dataset_dir = base / "dataset"
        print(f"Working on: {raw_dataset_dir}")

        repro = Repro(raw_dataset_dir, dataset_dir, zip_path)
        repro.unzip()
        repro.check_format()
        repro.create_mask()
        repro.create_info_csv()
        repro.rename()
        repro.merge()
