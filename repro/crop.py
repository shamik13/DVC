from pathlib import Path

import pandas as pd


class ReproCrop:

    raw_dataset_dir: Path

    def crop(self) -> None:

        df = pd.read_csv(self.raw_dataset_dir / "info.csv")
        df = self._crop_ziku(df)
        df = self._crop_tobu(df)
        df.to_csv(self.raw_dataset_dir / "info.csv", index=False)

    def _crop_ziku(self, df: pd.DataFrame) -> pd.DataFrame:

        """
        At camera id == 2, whole images are captured.
        This method crop the ziku (body) area from the whole image
        """

        return df

    def _crop_tobu(self, df: pd.DataFrame) -> pd.DataFrame:

        """
        At camera id == 2, whole images are captured.
        This method crop the tobu (head) area from the whole image
        """

        return df
