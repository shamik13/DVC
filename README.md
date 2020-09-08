# DVC
Data Version Control

<br>

## Clone Dataset in Your PC

```
cd docker
make build
make run
```

<br>

## info.csv

| Variable           | Definition                                    | Type | Key |
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
| unsupervised       | The type of data for unsupervised learning    | str  | train, test, unuse |
| semi_supervised    | The type of data for semi-supervised learning | str  | train, test, unuse |


I created info.csv with the following points in my mind:

- Split data into train and test based on product id to avoid data leakage
- Share test product id during supervise, unsupervise, semi-supervise in order to compare quantitatively.

<br>

## How to Use the dataset


