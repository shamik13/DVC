## 1. Introduction
This repository provides the dataset for SOMIC project. Users mainly work on `DVC/dataset` directory which stores `images/`, `masks/` and `info.csv`.  All the previous images and masks are in the directories. Users can extract the desired data with `info.csv`, and then use them for training and evaluation. If you want to know how to extract in detail, please see `3. Query Recipes`. This repository is available in DGX `/dgx/shared/momo/inoue/DVC`.

<br>


## 2. Label and Flag
This dataset has two type of annotation, `label` and `flag`. `label` is the annotation assigned to each pixel, and `flag` is the annotation assigned to each image.
The following tables are description about `label` and `flag`.

<br>

| Label Name     | Description |
| :-             | :-          |
| kizu_dakon     | カシメ部割れ, 切断面スジ, カシメ段ヒケ |
| kizu_ware      | 打痕, カシメ段差, カス打ち込み, カス打ち残り, 異物打ち込み, カシメ内径キズ, 内径キズ |
| kizu_zairyou   | 材料キズ |
| ignore_shallow | The kizu is shallow and can be ignored |
| ignore_cutting | The kizu will be removed in a later process |
| ignore_oil     | The oil stain failed to be wiped off |

<br>

| Flag Name | Description |
| :-        | :-          |
| sabi      | The image with rust (錆 sabi) |
| unuse     | The deprecated image for train and test |

The image with rust rarely appear in production phase, because the product is created and then take a image imidiately.
However, the products put in a laboratory for a week. That's why the products are getting rust.
The images with rust are deprecated for train and test.

<br>

### ■ Examples

Still working... Please wait for a few days...

| label: kizu_dakon          | label: kizu_ware           | label: kizu_zairyou        |
| --                         | --                         | --                         |
| <img height=300 width=300> | <img height=300 width=300> | <img height=300 width=300> |

| label: ignore_shallow      | label: ignore_cutting      | label: ignore_oil          |
| --                         | --                         | --                         |
| <img height=300 width=300> | <img height=300 width=300> | <img height=300 width=300> |

| flag: sabi                 | flag: unuse                |                            |
| --                         | --                         | --                         |
| <img height=300 width=300> | <img height=300 width=300> | <img height=300 width=300> |


<br>


## 3. info.csv

Still working... Please wait for a few days...

| Variable           | Description                                   | Type | Key |
| :-                 | :-                                            | :-   | :-  |
| product_type       | The type of product                           | str  | B, C, H, K, RAV4, Y1J, YJA |
| camera             | The imaging device                            | int  | 1 (end of body), 2 (whole), 3 (inside of head), 4 (top of head) |
| crop_type          | The type of crop                              | str  | tobu (camera 2), ziku (camera 2), center_of_ziku (camera 2), uncropped |
| received_date      | The date when we received raw datasets        | int  | yyyymmdd |
| timestamp          | The time the image was taken                  | int  | yyyymmddhhmmssmm |
| raw_product_id     | The original product id                       | int  | -   |
| product_id         | Timestamp at camera angle 0                   | int  | yyyymmddhhmmssmm |
| angle              | Camera angle                                  | int  | 0-7 (camera 1), 0-11 (camera 2), 0-4 (camera 3), 0 (camera 4) |
| raw_stem           | Raw filename without its suffix               | str  | -   |
| stem               | Renamed filename without its suffix           | str  | [product_id]_[crop_type]_[angle] |
| is_anomaly_image   | Does the image have kizu?                     | int  | 0 (No), 1 (Yes) |
| is_anomaly_product | Does the product have kizu?                   | int  | 0 (No), 1 (Yes) |
| supervised         | The type of data for supervised learning      | str  | train, test, unuse |

<br>

## 3. Query Recipes
We prepared the query recipes to extract data for supervised or unsupervised learning.
[examples/example.ipynb](https://github.com/TaikiInoue/DVC/blob/master/examples/example.ipynb) is also useful, so check it out.

<br>

### 3.1. for Supervised Learing

`/dgx/shared/momo/inoue/somic/dataset/H_tobu_segmentation`

```
dataset:
  base: <path_to_dataset_dir>
  train:
    query:
      - is_anomaly_image == 1 &
        crop_type == 'tobu' &
        supervised == 'train'
  test:
    query:
      - crop_type == 'tobu' &
        supervised == 'test'
```

<br>

`/dgx/shared/momo/inoue/somic/dataset/H_tobu_segmentation_mix`

```
dataset:
  base: <path_to_dataset_dir>
  train:
    query:
      - is_anomaly_image == 1 &
        crop_type == 'tobu' &
        supervised == 'train'
      - is_anomaly_product == 0 &
        crop_type == 'tobu' &
        supervised == 'train'
  test:
    query:
      - crop_type == 'tobu' &
        supervised == 'test'
```

<br>

### 3.2. for Unsupervised Learing

`/dgx/shared/momo/inoue/somic/dataset/H_tobu_unsupervise` at camera angle 0

```
dataset:
  base: <path_to_dataset_dir>
  train:
    query:
      - is_anomaly_product == 1 &
        is_anomaly_image == 0 &
        angle == 0 &
        crop_type == 'tobu' &
        supervised == 'train'
      - is_anomaly_product == 0 &
        angle == 0 &
        crop_type == 'tobu' &
        supervised == 'train'
  test:
    query:
      - angle == 0 &
        crop_type == 'tobu' &
        supervised == 'test'
```

<br>

## 4. Reproduce a Specific Version Data
To download a specific version data in your local, run the following commands. Please note that you need to contact Inoue to get `azure_storage_connection_string`.


```
git clone git@github.com:TaikiInoue/DVC.git
cd DVC
git checkout <commit_hash>
dvc remote modify --local blob_storage connection_string <azure_storage_connection_string>
dvc pull raw_datasets/*.zip.dvc
dvc repro
```
