
base=/app/DVC

dvc run -n dataset_creator \
        -d ${base}/repro/dataset_creator/create_info_csv.py \
        -d ${base}/repro/dataset_creator/create_mask.py \
        -d ${base}/repro/dataset_creator/dataset_creator.py \
        -d ${base}/repro/dataset_creator/extract_zip.py \
        -d ${base}/repro/dataset_creator/merge_raw_dataset.py \
        -d ${base}/repro/dataset_creator/rename_files.py \
        -d ${base}/raw_datasets \
        -o ${base}/dataset/info.csv \
        -o ${base}/dataset/images \
        -o ${base}/dataset/masks \
        python3 ${base}/repro/dataset_creator/dataset_creator.py
