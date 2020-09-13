import open3d as o3d
import numpy as np 
import os
from matplotlib import pyplot as plt
import cv2

def convertPointCloudToMesh():
    inputPath = os.getcwd() + "/input/"
    outputPath = os.getcwd() + "/output/"
    dataName = "sample.xyz"
    pointCloud= np.loadtxt(inputPath + dataName, skiprows=1)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pointCloud[:,:3])
    pcd.colors = o3d.utility.Vector3dVector(pointCloud[:,3:6]/255)
    # pcd.normals = o3d.utility.Vector3dVector(pointCloud[:,6:9])
    # o3d.visualization.draw_geometries([pcd])
    distances = pcd.compute_nearest_neighbor_distance()
    avgDist = np.mean(distances)
    radius = 3 * avgDist
    #Using BPA strategy to create mesh 
    bpaMesh = o3d.geometry.TriangleMesh.create_from_point_cloud_ball_pivoting(pcd,o3d.utility.DoubleVector([radius, radius * 2]))
    decMesh = bpaMesh.simplify_quadric_decimation(100000)
    decMesh.remove_degenerate_triangles()
    decMesh.remove_duplicated_triangles()
    decMesh.remove_duplicated_vertices()
    decMesh.remove_non_manifold_edges()
    o3d.io.write_triangle_mesh(outputPath+"bpa_mesh3.obj", bpaMesh)

def convertImageToPointCloud():
    filePath = os.getcwd() + "/doll/IMG_0975.jpg"
    image = cv2.imread(filePath)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(image)

# convertPointCloudToMesh()
convertImageToPointCloud()