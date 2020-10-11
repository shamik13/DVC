from pathlib import Path

from check_format import ReproCheckFormat
from create_info_csv import ReproCreateInfoCSV
from create_mask import ReproCreateMask
from crop_tobu_and_ziku import ReproCropTobuAndZiku
from merge import ReproMerge
from rename import ReproRename
from unzip import ReproUnzip


class Repro(
    ReproCheckFormat,
    ReproCreateInfoCSV,
    ReproCreateMask,
    ReproCropTobuAndZiku,
    ReproMerge,
    ReproRename,
    ReproUnzip,
):
    def __init__(self, raw_dataset_dir: Path, dataset_dir: Path, zip_path: Path):

        """
        Args:
            raw_dataset_dir (Path): path to unzipped directory
            dataset_dir (Path): path to dataset directory
            zip_path (Path): path to zip file
        """

        self.raw_dataset_dir = raw_dataset_dir
        self.dataset_dir = dataset_dir
        self.zip_path = zip_path


if __name__ == "__main__":

    base = Path(".")

    for zip_path in base.glob("raw_datasets/*_anomaly.zip"):

        raw_dataset_dir = zip_path.parent / zip_path.stem
        dataset_dir = base / "dataset"
        print(f"Working on: {raw_dataset_dir}")

        repro = Repro(raw_dataset_dir, dataset_dir, zip_path)
        repro.unzip()
        repro.check_format()
        repro.rename_to_color_jpg_filename()
        repro.create_mask()
        repro.create_info_csv()
        repro.rename_old_stem_to_new_stem()
        repro.crop_tobu_and_ziku()
        repro.merge()
