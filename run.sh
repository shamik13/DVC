dvc run -n initialize \
        -d repro/initialize/initialize.py \
        python repro/initialize/initialize.py

dvc run -n create_for_202006_highlander \
        -d repro/create_202006_highlander/convert_bmp_to_jpg.py \
        -d repro/create_202006_highlander/create_info_csv.py \
        -d repro/create_202006_highlander/dataset_creator.py \
        -d repro/create_202006_highlander/extract_zip.py \
        -d repro/create_202006_highlander/rename_files.py \
        -d raw_datasets/20200611_H_tobu_normal.zip \
        -d raw_datasets/20200611_H_ziku_normal.zip \
        -d raw_datasets/20200618_H_tobu_anomaly.zip \
        -d raw_datasets/20200618_H_ziku_anomaly.zip \
        -o raw_datasets/20200611_H_tobu_normal \
        -o raw_datasets/20200611_H_ziku_normal \
        -o raw_datasets/20200618_H_tobu_anomaly \
        -o raw_datasets/20200618_H_ziku_anomaly \
        python repro/create_202006_highlander/dataset_creator.py

dvc run -n merge \
        -d raw_datasets/20200611_H_tobu_normal \
        -d raw_datasets/20200611_H_ziku_normal \
        -d raw_datasets/20200618_H_tobu_anomaly \
        -d raw_datasets/20200618_H_ziku_anomaly \
        -o dataset/images \
        -o dataset/masks \
        -o dataset/info.csv \
        python repro/merge/merge.py
