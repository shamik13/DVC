from pathlib import Path
from pipelines.dataset_creator import DatasetCreator


base = Path("./data")

for zip_path in base.glob("*.zip"):

    creator = DatasetCreator(zip_path)
    creator.create_folders()
    creator.extract_zip()
    creator.create_mask()
    creator.create_info_csv()
    creator.rename_files()
    creator.move_files()
