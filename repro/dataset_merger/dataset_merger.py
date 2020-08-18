from pathlib import Path


class DatasetMerger:
    def __init__(self, raw_dataset_dir: Path, dataset_dir: Path):

        self.raw_dataset_dir = raw_dataset_dir
        self.dataset_dir = dataset_dir


if __name__ == "__main__":

    base = Path("/app/github_actions/DVC")  # TODO: Inoue: I should move this param into param.yaml

    raw_dataset_dir_list = [p for p in base.glob("raw_dataset/*") if p.is_dir()]
    for raw_dataset_dir in raw_dataset_dir_list:

        dataset_dir = base / "dataset"
        merger = DatasetMerger(raw_dataset_dir, dataset_dir)
