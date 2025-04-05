#!/bin/bash

python batch_augment_lidar.py configs_augment/rain_60.yaml

python batch_augment_lidar.py configs_augment/rain_70.yaml

python batch_augment_lidar.py configs_augment/rain_80.yaml

python batch_augment_lidar.py configs_augment/snow_2_5.yaml

python batch_augment_lidar.py configs_augment/snow_3_5.yaml

python batch_augment_lidar.py configs_augment/snow_4_5.yaml

python batch_augment_lidar.py configs_augment/snow_5_5.yaml

python batch_augment_lidar.py configs_augment/chu_hogg.yaml

python batch_augment_lidar.py configs_augment/moderate_advection.yaml

python batch_augment_lidar.py configs_augment/strong_advection.yaml

echo "All scripts executed!"
