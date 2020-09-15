import open3d as o3d
import numpy as np 
from numpy import int32, array, uint8
import os
from matplotlib import pyplot as plt
import cv2
from PIL import Image
from imageio import imread, imsave
import skimage.color
from itertools import product
import glob
import os
import csv


def convertPointCloudToMesh():
    inputPath = os.getcwd() + "/input/"
    outputPath = os.getcwd() + "/output/"
    dataName = "sample.xyz"
    pointCloud= np.loadtxt(inputPath + dataName, skiprows=1)
    pcd = o3d.geometry.PointCloud()
    print(type(pointCloud))
    exit()
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

def checkIfGrayScale(filePath): 
    image = Image.open(filePath).convert("RGB")
    width, height = image.size
    for i in range(width):
        for j in range(height):
            r,g,b = image.getpixel((i,j))
            if r != g != b:
                 return False
    return True

def checkIfGrayScaleV2(filePath): 
    image = imread(filePath)
    shape = image.shape
    if len(shape) == 3: 
        print("Color RGB")
    elif len(shape) < 3: 
        print("Gray")
    else: 
        print("Others")

def readPointCloud(filePath):
    path = os.getcwd() + "/input/sample.xyz"
    pcd = o3d.io.read_point_cloud(path)
    print(pcd)

def convertImageToPointCloud():
    filePath = os.getcwd() + "/doll/IMG_0975.jpg"
    # image = cv2.imread(filePath)
    # rgb = array([array(image)])
    # converted = skimage.color.rgb2xyz((rgb / 255 * (2**31 - 1)).astype(int32))
    readPointCloud(filePath)
    # filePathR = os.getcwd() + "/doll/IMG_0992.jpg"
    # filePathL = os.getcwd() + "/doll/IMG_0980.jpg"
    # imageL = cv2.imread(filePathL, 0)
    # imageR = cv2.imread(filePathR, 0)
    # stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
    # disparity = stereo.compute(imageL, imageR)
    
    
    # plt.imshow(disparity, 'gray')
    # plt.show()
    # val = checkIfGrayScale(filePath)
    # checkIfGrayScaleV2(filePath)
    # print(val)
    # image = cv2.imread(filePath)
    # grayScale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # depthImage = OpenEXR.InputFile(filePath)
    # print(depthImage)
    # depth = o3d.geometry.Image(np.asarray(image[:, :, 2]*1000).astype('uint16'))
    # print(depth)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def convertImagesToRGB(): 
    with open('rgb.csv', "a", newline='') as file: 
        csvOutput = csv.writer(file)
        csvOutput.writerow(["Image Name", "R", "G", "B"])
        for filename in glob.glob(os.getcwd() + "/doll/*.jpg"):
            image = Image.open(filename)
            imageName = os.path.basename(filename)
            pix = image.load()
            width, height = image.size
            row = [[imageName, *pix[x, y]] for x, y in product(range(width), range(height))] 
            # print(row)
            # exit()
            # file.writerows([imageName, *pix[x,y]] for x, y in product(range(width), range(height)))
            csvOutput.writerow(row)            
            print("Done")

def loadImageAndGetDepth(): 
    filePath = os.getcwd() + "/doll/IMG_0975.jpg"
    image = Image.open(filePath)
    modeToBpp =  {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
    # print(len(set(image.getdata())))
    # print(image.mode)
    bpp = modeToBpp[image.mode]
    print(bpp)

# convertPointCloudToMesh()
# convertImageToPointCloud()
# convertImagesToRGB()
# convertPointCloudToMesh()
loadImageAndGetDepth()