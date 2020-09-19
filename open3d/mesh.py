import open3d as o3d
import numpy as np 
from numpy import int32, array, uint8
import os
from matplotlib import pyplot as plt
import cv2
from PIL import Image
from imageio import imread, imsave
import skimage.color
from skimage import io
from itertools import product
import glob
import os
import csv
import imutils
from imutils import paths


def convertPointCloudToMesh():
    inputPath = os.getcwd() + "/input/"
    outputPath = os.getcwd() + "/output/"
    dataName = "sample.xyz"
    dataname = "bundle.out"
    # pointCloud= np.loadtxt(inputPath + dataName, skiprows=1)
    pointCloud = np.loadtxt(inputPath + dataname, skiprows = 2)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pointCloud[:,:3])
    # pcd.colors = o3d.utility.Vector3dVector(pointCloud[:,3:6]/255)
    # pcd.normals = o3d.utility.Vector3dVector(pointCloud[:,6:9])
    o3d.visualization.draw_geometries([pcd])
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

def distanceFromCamera(): 
    filePath = os.getcwd() + "/doll/IMG_0975.jpg"
    image = cv2.imread(filePath)
    def findMarker(image): 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5,5), 0)
        edged  = cv2.Canny(gray, 35, 125)
        contours = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        c = max(contours, key=cv2.contourArea)
        return cv2.minAreaRect(c)
    def distanceToCamera(knownWidth, focalLength, perWidth): 
        return (knownWidth * focalLength) / perWidth
    marker = findMarker(image)
    knownDistance = 24.0
    knownWidth = 11.0
    focalLength = (marker[0][1] * knownDistance) / knownWidth
    print(focalLength)

def computeSift(): 
    filePath1 = os.getcwd() + "/doll/IMG_0975.jpg"
    filePath2 = os.getcwd() + "/doll/IMG_0979.jpg"
    image1 = cv2.imread(filePath1)
    image2 = cv2.imread(filePath2)
    image1= cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    image2= cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    sift = cv2.xfeatures2d.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)
    bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
    matches = bf.match(descriptors1, descriptors2)
    matches = sorted(matches, key=lambda x: x.distance)
    img3 = cv2.drawMatches(image1, keypoints1, image2, keypoints2, matches[:50], image2, flags=2)
    plt.imshow(img3),plt.show()

def plot(): 
    filePath = os.getcwd() + "/doll/*.jpg"
    imCollection = io.imread_collection(filePath)
    im3d = imCollection.concatenate()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(im3d[:,0], im3d[:, 1], im3d[:, 2])
    plt.show()

convertPointCloudToMesh()
# convertImageToPointCloud()
# convertImagesToRGB()
# convertPointCloudToMesh()
# loadImageAndGetDepth()
# distanceFromCamera()
# computeSift()
# plot()