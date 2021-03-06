# 实现PCA分析和法向量计算，并加载数据集中的文件进行验证

import open3d as o3d 
import numpy as np
from pyntcloud import PyntCloud

import os
from os import walk
import random

# 功能：计算PCA的函数
# 输入：
#     data：点云，NX3的矩阵
#     correlation：区分np的cov和corrcoef，不输入时默认为False
#     sort: 特征值排序，排序是为了其他功能方便使用，不输入时默认为True
# 输出：
#     eigenvalues：特征值
#     eigenvectors：特征向量
def PCA(data, correlation=False, sort=True):
    # 作业1
    # 屏蔽开始
    # calculate the mean x = (1/m)*sum(xi)
    point_cloud_data_mean = np.mean(data,axis=0)
    # normalized the value for all point cloud data
    normalized_point_cloud_data = data - point_cloud_data_mean
    # compute SVD H = X'*X
    H = np.dot(normalized_point_cloud_data.T , normalized_point_cloud_data)

    # get the eigen vectors https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html#numpy.linalg.svd
    u,s, unitary_array = np.linalg.svd(H)
    print(u, s , unitary_array)


    return u, s, unitary_array

    # 屏蔽结束

    if sort:
        sort = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[sort]
        eigenvectors = eigenvectors[:, sort]

    return eigenvalues, eigenvectors


def main():
    dataset_path = "../modelnet40_normal_resampled"

    data_directory_names = [] 
    with open(os.path.join(dataset_path,'modelnet40_shape_names.txt'),'r') as f:
        data_directory_names = f.read().splitlines()

    for data_directory in data_directory_names:
        _, _, data_files = next(walk(os.path.join(dataset_path,data_directory)))
        
        # random select a file to open 
        pc_data_file_name = random.choice(data_files)
        path_to_file = os.path.join(dataset_path,data_directory, pc_data_file_name)

        point_cloud_data = np.loadtxt(path_to_file,delimiter=',')
        # get the only x, y ,z values
        point_cloud_data = point_cloud_data[:,0:3]


        u, s, unitary_array = PCA(point_cloud_data)

        # get the main direction
        point_cloud_vector = u[:,0]
        print(f"the First principle vector:\t{point_cloud_vector}")
        # convert to open 3d format
        open_3d_point_cloud = o3d.geometry.PointCloud(points=o3d.utility.Vector3dVector(point_cloud_data))
        o3d.visualization.draw_geometries([open_3d_point_cloud], point_show_normal=True)

        # project to 2D
        point_cloud_2D = point_cloud_data - np.dot(point_cloud_data,u[:,2][:,np.newaxis])*u[:,2]
        open_3d_point_cloud_2D = o3d.geometry.PointCloud(points=o3d.utility.Vector3dVector(point_cloud_2D))
        o3d.visualization.draw_geometries([open_3d_point_cloud_2D])


if __name__ == '__main__':
    main()
