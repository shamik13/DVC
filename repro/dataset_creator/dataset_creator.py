from pathlib import Path

from create_dataset_directory import DatasetCreatorCreateDatasetDirectory
from create_info_csv import DatasetCreatorCreateInfoCSV
from create_mask import DatasetCreatorCreateMask
from extract_zip import DatasetCreatorExtractZIP
from rename_files import DatasetCreatorRenameFiles


class DatasetCreator(
    DatasetCreatorExtractZIP,
    DatasetCreatorCreateMask,
    DatasetCreatorCreateInfoCSV,
    DatasetCreatorRenameFiles,
    DatasetCreatorCreateDatasetDirectory,
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

    base = Path("/app/github_actions/DVC")  # TODO: Inoue: I should move this param into param.yaml

    for zip_path in base.glob("raw_dataset/*.zip"):

        raw_dataset_dir = zip_path.parent / zip_path.stem
        dataset_dir = base / "dataset"

        creator = DatasetCreator(raw_dataset_dir, dataset_dir, zip_path)
        creator.create_dataset_directory()
        creator.extract_zip()
        creator.create_mask()
        creator.create_info_csv()
        creator.rename_files()
        creator.move_files()
