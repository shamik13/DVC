
BASE=/app/github_actions/DVC

dvc run -n dataset_creator \
        -d ${BASE}/repro/dataset_creator/create_dataset_directory.py \
        -d ${BASE}/repro/dataset_creator/create_info_csv.py \
        -d ${BASE}/repro/dataset_creator/create_mask.py \
        -d ${BASE}/repro/dataset_creator/dataset_creator.py \
        -d ${BASE}/repro/dataset_creator/extract_zip.py \
        -d ${BASE}/repro/dataset_creator/rename_files.py \
        -d ${BASE}/raw_dataset/*.zip \
        -o ${BASE}/dataset/images \
        -o ${BASE}/dataset/masks \
        -o ${BASE}/dataset/info.csv \
        python3 ${BASE}/repro/dataset_creator/dataset_creator.py
