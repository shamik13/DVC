
base=/app/github_actions/DVC

for zip_path in ${base}/raw_datasets/*.zip
do
        dvc run -n dataset_creator_$(basename "${zip_path}" .zip) \
                -d ${base}/repro/dataset_creator/create_info_csv.py \
                -d ${base}/repro/dataset_creator/create_mask.py \
                -d ${base}/repro/dataset_creator/dataset_creator.py \
                -d ${base}/repro/dataset_creator/extract_zip.py \
                -d ${zip_path} \
                -o ${zip_path%.zip} \
                python3 ${base}/repro/dataset_creator/dataset_creator.py ${zip_path}
done
