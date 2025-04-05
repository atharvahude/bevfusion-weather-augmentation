# minimal_visualize_nuscenes.py

import numpy as np
import open3d as o3d
import argparse

def main(path):
    # Load .pcd.bin file manually (nuScenes format is 5 floats: x, y, z, intensity, ring index)
    points = np.fromfile(path, dtype=np.float32).reshape(-1, 5)  # [N, 5]
    xyz = points[:, :3]  # x, y, z

    # --- Option 1: Use Open3D (3D view)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(xyz)
    o3d.visualization.draw_geometries([pcd], window_name="nuScenes LiDAR")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize nuScenes LiDAR point cloud from .pcd.bin file")
    parser.add_argument("path", type=str, help="Path to the .pcd.bin file")
    args = parser.parse_args()

    main(args.path)
