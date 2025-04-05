import os
import json
import yaml
import numpy as np
from atmos_models import LISA

def load_config(config_path):
    with open(config_path, 'r') as f:
        if config_path.endswith(".json"):
            return json.load(f)
        elif config_path.endswith(".yaml") or config_path.endswith(".yml"):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported config file format. Use .json or .yaml")


def augment_lidar_file(input_file, output_folder, lisa, augmentation_type, rain_rate=0, snow_rate=0):
    points = np.fromfile(input_file, dtype=np.float32).reshape(-1, 5)
    xyz_reflectivity = points[:, :4]

    if augmentation_type == 'rain':
        augmented_points = lisa.augment_mc(xyz_reflectivity, rain_rate)
    elif augmentation_type == 'snow':
        augmented_points = lisa.augment_mc(xyz_reflectivity, snow_rate)
    elif augmentation_type in ['chu_hogg_fog', 'strong_advection_fog', 'moderate_advection_fog']:
        augmented_points = lisa.augment_avg(xyz_reflectivity)
    else:
        raise ValueError(f"Unsupported augmentation type: {augmentation_type}")

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, os.path.basename(input_file))
    range_channel = points[:, 4].reshape(-1, 1)
    augmented_points_with_range = np.hstack((augmented_points[:, :4], range_channel)).astype(np.float32)
    augmented_points_with_range.tofile(output_file)

    print(f"Processed: {input_file} -> {output_file}")


def process_folder(config_path):
    config = load_config(config_path)

    input_folder = config["input_folder"]
    output_folder = config["output_folder"]
    augmentation_type = config["augmentation_type"]
    rain_rate = config.get("rain_rate")
    snow_rate = config.get("snow_rate")

    lisa = LISA(
        m=1.328,
        lam=905,
        rmax=120,
        rmin=1.0,
        bdiv=3e-3,
        dst=0.05,
        dR=0.02,
        mode='strongest',
        atm_model=augmentation_type
    )

    for filename in os.listdir(input_folder):
        if filename.endswith('.bin'):
            input_file = os.path.join(input_folder, filename)
            augment_lidar_file(input_file, output_folder, lisa, augmentation_type, rain_rate, snow_rate)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Batch LiDAR augmentation using LISA and config file.")
    parser.add_argument("config", help="Path to config file (.yaml or .json)")
    args = parser.parse_args()

    process_folder(args.config)
