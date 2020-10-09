from pathlib import Path

import pandas as pd


class ReproRename:

    raw_dataset_dir: Path

    def rename_to_color_jpg_filename(self) -> None:

        """
        The filename is a little different
        between color_images/*.bmp, color_images/*.jpg, gray_images/*.bmp and gray_images/*.jpg
        This is because the saving is completed at the different time.
        This method is implemented in order to make the filenames same to color_images/*.jpg

        ReproCheckFormat._check_num_images already checks that the number of images is the same.
        """

        di = {}
        di["color_bmp"] = sorted([p for p in self.raw_dataset_dir.glob("color_images/*.bmp")])
        di["color_jpg"] = sorted([p for p in self.raw_dataset_dir.glob("color_images/*.jpg")])
        di["gray_bmp"] = sorted([p for p in self.raw_dataset_dir.glob("gray_images/*.bmp")])
        di["gray_jpg"] = sorted([p for p in self.raw_dataset_dir.glob("gray_images/*.jpg")])
        df = pd.DataFrame(di)

        for row in df.index:
            color_bmp = df.loc[row, "color_bmp"]
            color_jpg = df.loc[row, "color_jpg"]
            gray_bmp = df.loc[row, "gray_bmp"]
            gray_jpg = df.loc[row, "gray_jpg"]

            color_bmp.rename(color_bmp.parent / f"{color_jpg.stem}.bmp")
            gray_bmp.rename(gray_bmp.parent / f"{color_jpg.stem}.bmp")
            gray_jpg.rename(gray_jpg.parent / f"{color_jpg.stem}.jpg")

            # Stems of jsons/*.json is included in stems of gray_images/*.jpg
            json_path = self.raw_dataset_dir / f"jsons/{gray_jpg.stem}.json"
            if json_path.is_file():
                json_path.rename(self.raw_dataset_dir / f"jsons/{color_jpg.stem}.json")

    def rename_raw_stem_to_stem(self) -> None:

        df = pd.read_csv(self.raw_dataset_dir / "info.csv")
        for i in df.index:

            old_stem = df.loc[i, "raw_stem"]
            new_stem = df.loc[i, "stem"]

            old_img_path = self.raw_dataset_dir / f"images/{old_stem}.bmp"
            new_img_path = self.raw_dataset_dir / f"images/{new_stem}.bmp"

            old_mask_path = self.raw_dataset_dir / f"masks/{old_stem}.png"
            new_mask_path = self.raw_dataset_dir / f"masks/{new_stem}.png"

            old_json_path = self.raw_dataset_dir / f"jsons/{old_stem}.json"
            new_json_path = self.raw_dataset_dir / f"jsons/{new_stem}.json"

            if old_img_path.is_file():
                old_img_path.rename(new_img_path)

            if old_mask_path.is_file():
                old_mask_path.rename(new_mask_path)

            if old_json_path.is_file():
                old_json_path.rename(new_json_path)

        print("DONE: rename_files")
