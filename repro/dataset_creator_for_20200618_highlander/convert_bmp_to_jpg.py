from pathlib import Path

import cv2


class DatasetCreatorConvertBmpToJpg:

    raw_dataset_dir: Path

    def convert_bmp_to_jpg(self):

        for p in self.raw_dataset_dir.glob("images/*.bmp"):

            img = cv2.imread(str(p))
            cv2.imwrite(str(p.parent / f"{p.stem}.jpg"), img, [cv2.IMWRITE_JPEG_QUALITY, 100])
