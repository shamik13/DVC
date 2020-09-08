from pathlib import Path

from convert_bmp_to_jpg import DatasetCreatorConvertBmpToJpg
from create_info_csv import DatasetCreatorCreateInfoCSV
from extract_zip import DatasetCreatorExtractZIP
from rename_files import DatasetCreatorRenameFiles


class DatasetCreator(
    DatasetCreatorExtractZIP,
    DatasetCreatorCreateInfoCSV,
    DatasetCreatorRenameFiles,
    DatasetCreatorConvertBmpToJpg,
):
    def __init__(self, raw_dataset_dir: Path, dataset_dir: Path, zip_path: Path):

        """Initialize DatasetCreator

        Args:
            raw_dataset_dir (Path): path to unzipped directory
            dataset_dir (Path): path to dataset directory for DL models
            zip_path (Path): path to zip file
        """

        self.raw_dataset_dir = raw_dataset_dir
        self.dataset_dir = dataset_dir
        self.zip_path = zip_path


if __name__ == "__main__":

    base = Path(".")

    for zip_path in base.glob("raw_datasets/202006*_H_*_*.zip"):

        raw_dataset_dir = zip_path.parent / zip_path.stem
        dataset_dir = base / "dataset"
        print(f"Working on: {raw_dataset_dir}")

        creator = DatasetCreator(raw_dataset_dir, dataset_dir, zip_path)
        creator.extract_zip()
        creator.create_info_csv()
        creator.rename_files()
        creator.convert_bmp_to_jpg()
