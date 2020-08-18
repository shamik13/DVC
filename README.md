# DVC
Data Version Control

<br>

## Data Structure

```
DVC
├── .dvc
├── .github  
│   └── workflows  
|       └── *.yml
├── zip_dvc  
│   └── *.zip.dvc  
├── dataset  
│   ├── images  
│   │   └── *.bmp
│   ├── masks
│   |   └── *.png
│   └── info.csv
└── repro  
    
```

## info.csv

| Variable | Definition | Key |
| :-       | :-         | :-  |
| old_stem | Old file name without its suffix | - |
| stem | Renamed file name without its suffix | - |
| timestamp | The time the image was taken | - |
| received_date | The date the dataset was completed | - |
| product | product id | - |
| product_type | The type of product | B, C, H, K, RAV4, Y1J, YJA  |
| work_station | The imaging device | 1 (end of body), 2 (whole), 3 (inside of head), 4 (top of head) |
| crop_type | The type of crop | tobu (work station 2), ziku (work station 2), center_of_ziku (work station 2), uncropped |
| angle | Camera angle | 0-7 (work station 1), 0-11 (work station 2), 0-4 (work station 3), 0 (work station 4) |
| is_anomaly_image | Does the image have kizu? | 0 (No), 1 (Yes) |
| is_anomaly_product | Does the product have kizu? | 0 (No), 1 (Yes) |
| data_type | The type of data | train, test |
