dvc run -n dataset_creator \
        -d pipelines/run.py \
        -d pipelines/dataset_creator/__init__.py \
        -d pipelines/dataset_creator/create_info_csv.py \
        -d pipelines/dataset_creator/create_mask.py \
        -d pipelines/dataset_creator/dataset_creator.py \
        -d pipelines/dataset_creator/extract_zip.py \
        -d pipelines/dataset_creator/rename_files.py \
        -d data/*.zip \
        -o data/dataset/images \
        -o data/dataset/masks \
        -o data/dataset/info.csv \
        python pipelines/run.py
