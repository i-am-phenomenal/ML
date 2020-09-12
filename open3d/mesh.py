import open3d as o3d
import numpy as np 
import os
from matplotlib import pyplot as plt
# Figure out a way to save the output to a rcm or obj file

inputPath = os.getcwd() + "/input/"
outputPath = os.getcwd() + "/output/"
dataName = "sample.xyz"
pointCloud= np.loadtxt(inputPath + dataName, skiprows=1)
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(pointCloud[:,:3])
pcd.colors = o3d.utility.Vector3dVector(pointCloud[:,3:6]/255)
# pcd.normals = o3d.utility.Vector3dVector(pointCloud[:,6:9])
o3d.visualization.draw_geometries([pcd])

