import os
import yaml

input_folder = "/workspace/mmdetection3d/data/nuscenes/samples/LIDAR_TOP"
base_output_folder = "/workspace/my_workspace/nusecnes_augments"
config_output_dir = "/workspace/my_workspace/configs_augment"

os.makedirs(config_output_dir, exist_ok=True)

def save_yaml(config_data, filename):
    with open(os.path.join(config_output_dir, filename), 'w') as f:
        yaml.dump(config_data, f, sort_keys=False)
    print(f"Created: {filename}")

# Rain configs
for rate in [50.0, 60.0, 70.0, 80.0]:
    config = {
        "input_folder": input_folder,
        "output_folder": f"{base_output_folder}/rain_{int(rate)}",
        "augmentation_type": "rain",
        "rain_rate": rate
    }
    save_yaml(config, f"rain_{int(rate)}.yaml")

# Snow configs
for rate in [2.5, 3.5, 4.5, 5.5]:
    rate_str = str(rate).replace(".", "_")
    config = {
        "input_folder": input_folder,
        "output_folder": f"{base_output_folder}/snow_{rate_str}",
        "augmentation_type": "snow",
        "snow_rate": rate
    }
    save_yaml(config, f"snow_{rate_str}.yaml")

# Fog configs
fog_types = {
    "chu_hogg": "chu_hogg_fog",
    "strong_advection": "strong_advection_fog",
    "moderate_advection": "moderate_advection_fog"
}

for name, fog_type in fog_types.items():
    config = {
        "input_folder": input_folder,
        "output_folder": f"{base_output_folder}/{name}",
        "augmentation_type": fog_type
    }
    save_yaml(config, f"{name}.yaml")
