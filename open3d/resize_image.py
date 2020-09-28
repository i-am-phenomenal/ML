import numpy
import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image
# import scipy.misc
import imageio
import glob

def resize(image, counter): 
    # image = cv2.imread(os.getcwd() + "/testImage2.jpg", 3)
    global outputDirectory
    b,g,r = cv2.split(image)
    rgbImage = cv2.merge([r,g,b])
    resized = cv2.resize(rgbImage, (640, 480))
    try:
        outputPath = outputDirectory + "\{counter}.jpg"
        outputPath = outputPath.format(counter=counter)
        imageio.imsave(outputPath, resized)
    except Exception as e: 
        print(e)
    # plt.imshow(resized)
    # plt.show()

def readAllImages(folderPath):
    counter = 0
    for filename in glob.glob(folderPath +  "/*.jpg"):
        image = cv2.imread(filename, 3)
        try: 
            resize(image, counter)
        finally: 
            counter += 1

def readHeightAndWidth(): 
    global outputDirectory
    for filename in glob.glob(outputDirectory + "/*.jpg"):
        image = Image.open(filename)
        w, h = image.size
        print(w, h)

outputDirectory = os.getcwd() + "/resized_images"
# readAllImages("C:\Code\osm-bundler-pmvs2-cmvs\osm-bundler\examples\Hello")
# resize()    
readHeightAndWidth()