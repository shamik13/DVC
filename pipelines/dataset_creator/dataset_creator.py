from pathlib import Path
from .extract_zip import DatasetCreatorExtractZIP
from .create_mask import DatasetCreatorCreateMask
from .create_info_csv import DatasetCreatorCreateInfoCSV
from .rename_files import DatasetCreatorRenameFiles


class DatasetCreator(
    DatasetCreatorExtractZIP,
    DatasetCreatorCreateMask,
    DatasetCreatorCreateInfoCSV,
    DatasetCreatorRenameFiles,
):
    def __init__(self, zip_path: Path):

        """[Initialize DatasetCreator]

        Args:
            zip_path (Path): [path to zip file]
        """

        self.zip_path = zip_path
        self.base = self.zip_path.parent / self.zip_path.stem
