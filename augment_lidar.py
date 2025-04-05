import os
import numpy as np
from atmos_models import LISA

def augment_lidar_data(input_file, output_folder, augmentation_type, rain_rate=0, snow_rate=0):
    """
    Augments a single LiDAR point cloud file using the LISA class.

    Parameters:
    - input_file: Path to the input LiDAR point cloud file (.bin format).
    - output_folder: Path to the folder where the augmented file will be saved.
    - augmentation_type: Type of augmentation ('rain', 'snow', 'fog').
    - rain_rate: Rain rate in mm/hr (used for rain augmentation).
    - snow_rate: Snow rate in mm/hr (used for snow augmentation).

    Returns:
    - None
    """
    # Load the LiDAR point cloud
    points = np.fromfile(input_file, dtype=np.float32).reshape(-1, 5)  # [N, 5]
    xyz_reflectivity = points[:, :4]  # x, y, z, reflectivity

    # Initialize the LISA class
    lisa = LISA(    m=1.328,            # refractive index of water
                    lam=905,            # wavelength in nm (Velodyne HDL-32E)
                    rmax=120,           # maximum range ~120 m
                    rmin=1.0,           # minimum range ~1 m
                    bdiv=3e-3,          # beam divergence ~3 mrad
                    dst=0.05,           # droplet diameter (you can tweak this based on condition)
                    dR=0.02,            # range accuracy ~2 cm
                    mode='strongest',    # Velodyne generally uses strongest return
                    atm_model=augmentation_type)

    # Perform augmentation based on the selected type
    if augmentation_type == 'rain':
        augmented_points = lisa.augment_mc(xyz_reflectivity, rain_rate)
    elif augmentation_type == 'snow':
        augmented_points = lisa.augment_mc(xyz_reflectivity, snow_rate)
    elif augmentation_type in ['chu_hogg_fog', 'strong_advection_fog', 'moderate_advection_fog']:
        augmented_points = lisa.augment_avg(xyz_reflectivity)
    else:
        raise ValueError(f"Unsupported augmentation type: {augmentation_type}")

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the augmented point cloud
    output_file = os.path.join(output_folder, os.path.basename(input_file))
    
    # Keep original 5th channel (range or ring index)
    range_channel = points[:, 4].reshape(-1, 1)

    # Combine augmented data with original 5th channel
    augmented_points_with_range = np.hstack((augmented_points[:, :4], range_channel)).astype(np.float32)

    # Save
    augmented_points_with_range.tofile(output_file)


    print(f"Augmented point cloud saved to: {output_file}")


if __name__ == "__main__":
    # Example usage
    input_file = '/workspace/mmdetection3d/demo/data/nuscenes/n015-2018-07-24-11-22-45+0800__LIDAR_TOP__1532402927647951.pcd.bin'
    output_folder = '/workspace/my_workspace/augmented_lidar_data'
    
    print("Select augmentation type:")
    print("1. Rain")
    print("2. Snow")
    print("3. Chu-Hogg Fog")
    print("4. Strong Advection Fog")
    print("5. Moderate Advection Fog")
    choice = int(input("Enter your choice (1-5): "))

    if choice == 1:
        augmentation_type = 'rain'
        rain_rate = float(input("Enter rain rate (mm/hr): "))
        augment_lidar_data(input_file, output_folder, augmentation_type, rain_rate=rain_rate)
    elif choice == 2:
        augmentation_type = 'snow'
        snow_rate = float(input("Enter snow rate (mm/hr): "))
        augment_lidar_data(input_file, output_folder, augmentation_type, snow_rate=snow_rate)
    elif choice == 3:
        augmentation_type = 'chu_hogg_fog'
        augment_lidar_data(input_file, output_folder, augmentation_type)
    elif choice == 4:
        augmentation_type = 'strong_advection_fog'
        augment_lidar_data(input_file, output_folder, augmentation_type)
    elif choice == 5:
        augmentation_type = 'moderate_advection_fog'
        augment_lidar_data(input_file, output_folder, augmentation_type)
    else:
        print("Invalid choice. Exiting.")