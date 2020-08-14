from pathlib import Path
from extract_zip import DatasetCreatorExtractZIP
from create_mask import DatasetCreatorCreateMask
from create_info_csv import DatasetCreatorCreateInfoCSV
from rename_files import DatasetCreatorRenameFiles
from create_dataset_directory import DatasetCreatorCreateDatasetDirectory


class DatasetCreator(
    DatasetCreatorExtractZIP,
    DatasetCreatorCreateMask,
    DatasetCreatorCreateInfoCSV,
    DatasetCreatorRenameFiles,
    DatasetCreatorCreateDatasetDirectory,
):
    def __init__(self, DVC: Path, unzip_dir: Path):

        self.DVC = DVC
        self.unzip_dir = unzip_dir


if __name__ == "__main__":

    DVC = Path("/app/github_actions/DVC")

    for p in DVC.glob("zip_dvc/*.zip"):

        unzip_dir = p.parent / p.stem
        creator = DatasetCreator(DVC, unzip_dir)
        creator.create_dataset_directory()
        creator.extract_zip()
        creator.create_mask()
        creator.create_info_csv()
        creator.rename_files()
        creator.move_files()
