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

        print("DONE: rename_to_color_jpg_filename")

    def rename_old_stem_to_new_stem(self) -> None:

        df = pd.read_csv(self.raw_dataset_dir / "info.csv")
        for i in df.index:

            old_stem = df.loc[i, "raw_stem"]
            new_stem = df.loc[i, "stem"]

            old_path_list = []
            old_path_list.append(self.raw_dataset_dir / f"color_images/{old_stem}.bmp")
            old_path_list.append(self.raw_dataset_dir / f"color_images/{old_stem}.jpg")
            old_path_list.append(self.raw_dataset_dir / f"gray_images/{old_stem}.bmp")
            old_path_list.append(self.raw_dataset_dir / f"gray_images/{old_stem}.jpg")
            old_path_list.append(self.raw_dataset_dir / f"masks/{old_stem}.png")
            old_path_list.append(self.raw_dataset_dir / f"jsons/{old_stem}.json")

            new_path_list = []
            new_path_list.append(self.raw_dataset_dir / f"color_images/{new_stem}.bmp")
            new_path_list.append(self.raw_dataset_dir / f"color_images/{new_stem}.jpg")
            new_path_list.append(self.raw_dataset_dir / f"gray_images/{new_stem}.bmp")
            new_path_list.append(self.raw_dataset_dir / f"gray_images/{new_stem}.jpg")
            new_path_list.append(self.raw_dataset_dir / f"masks/{new_stem}.png")
            new_path_list.append(self.raw_dataset_dir / f"jsons/{new_stem}.json")

            for old_path, new_path in zip(old_path_list, new_path_list):
                if old_path.is_file():
                    old_path.rename(new_path)

        print("DONE: rename_old_stem_to_new_stem")
