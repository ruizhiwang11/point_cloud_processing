# 实现voxel滤波，并加载数据集中的文件进行验证

import open3d as o3d 
import os
import numpy as np
from pyntcloud import PyntCloud

from os import walk
import random

# 功能：对点云进行voxel滤波
# 输入：
#     point_cloud：输入点云
#     leaf_size: voxel尺寸
def voxel_filter(point_cloud, leaf_size):
    filtered_points = []
    # 作业3
    # 屏蔽开始

    # get min max of x, y ,z
    x_min,x_max = np.min(point_cloud[:,0]),np.max(point_cloud[:,0])
    y_min,y_max = np.min(point_cloud[:,1]),np.max(point_cloud[:,1])
    z_min,z_max = np.min(point_cloud[:,2]),np.max(point_cloud[:,2])
    

    Dx,Dy,Dz = (x_max-x_min)/leaf_size,(y_max-y_min)/leaf_size,(z_max-z_min)/leaf_size

    hx,hy,hz = np.floor(((point_cloud[:,0] - x_min)/leaf_size)),np.floor(((point_cloud[:,1] - y_min)/leaf_size)),np.floor(((point_cloud[:,2] - z_min)/leaf_size))

    h = hx + hy*Dx+hz*Dx*Dy
    for point in np.unique(h):
        point_choosed = point_cloud[h==point]
        filtered_points.append(point_choosed[np.random.choice(a=point_choosed.shape[0])])
 
    # 屏蔽结束

    # 把点云格式改成array，并对外返回
    filtered_points = np.array(filtered_points, dtype=np.float64)
    return filtered_points

def main():
    path = '../modelnet40_normal_resampled'

    data_directory_names = [] 
    with open(os.path.join(path,'modelnet40_shape_names.txt'),'r') as f:
        data_directory_names = f.read().splitlines()

    for data_directory in data_directory_names:
        _, _, data_files = next(walk(os.path.join(path,data_directory)))
        # random select a file to open 
        pc_data_file_name = random.choice(data_files)
        path_to_file = os.path.join(path,data_directory, pc_data_file_name)
        pointcloud = np.loadtxt(path_to_file,delimiter=',')[:,0:3]
        pointcloud_o3d = o3d.geometry.PointCloud(points=o3d.utility.Vector3dVector(pointcloud))
        filtered_cloud = voxel_filter(pointcloud,0.1)+1*np.array([0,1,0])
        filteredcloud_o3d = o3d.geometry.PointCloud(points=o3d.utility.Vector3dVector(filtered_cloud))

        o3d.visualization.draw_geometries([pointcloud_o3d,filteredcloud_o3d])
    

if __name__ == '__main__':
    main()
