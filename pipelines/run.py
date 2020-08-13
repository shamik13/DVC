import shutil
from pathlib import Path
from pipelines.dataset_creator import DatasetCreator


base = Path("/dgx/github/DVC/data")

for zip_path in base.glob("*.zip"):

    creator = DatasetCreator(zip_path)
    creator.extract_zip()
    creator.create_mask()
    creator.create_info_csv()
    creator.rename_files()

    base = zip_path.parent
    shutil.move(str(base / f"{zip_path.stem}/images"), str(base / "dataset/images"))
    shutil.move(str(base / f"{zip_path.stem}/masks"), str(base / "dataset/masks"))
    shutil.move(str(base / f"{zip_path.stem}/info.csv"), str(base / "dataset/info.csv"))
