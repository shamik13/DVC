
dvc_run:
		dvc run -n prepare_dataset \
				-d repro/check_format.py \
				-d repro/create_info_csv.py \
				-d repro/create_mask.py \
				-d repro/crop_tobu_and_ziku.py \
				-d repro/merge.py \
				-d repro/rename.py \
				-d repro/repro.py \
				-d repro/unzip.py \
				-d raw_datasets/20201005_H_2_anomaly.zip \
				-d raw_datasets/20201008_H_2_normal.zip \
				-o dataset/info.csv \
				-o dataset/color_images \
				-o dataset/gray_images \
				-o dataset/masks \
				python repro/repro.py

dvc_pull:
		dvc pull raw_datasets/*.zip.dvc

dvc_repro:
		dvc repro
