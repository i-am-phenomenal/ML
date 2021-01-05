import numpy as np
import cv2
import matplotlib.pyplot as plt
import os
from PIL import Image
import imageio
import glob
import sys

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

def findContours(): 
    global inputDirectory
    image = cv2.imread(os.getcwd() + "/testImage.jpg", 3)
    lower = [1, 0, 28]
    upper = [60, 40, 220]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    ret,thresh = cv2.threshold(mask, 40, 255, 0)
    if (int(cv2.__version__[0]) > 3):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)
        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)
        # draw the biggest contour (c) in green
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("RESULT", np.hstack([image, output]))
    cv2.waitKey(0)

# def findLargestContour(): 
    # image= cv2.imread(os.getcwd() + "/testImage.png")
    # original_image= image
    # gray= cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # edged= cv2.Canny(gray, 50,200)
    # contours, hierarchy= cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # cv2.imshow('Original Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # def get_contour_areas(contours):
    #     all_areas= []
    #     for cnt in contours:
    #         area= cv2.contourArea(cnt)
    #         all_areas.append(area)
    #     return all_areas
    # print ("Contour Areas before Sorting", get_contour_areas(contours))
    # sorted_contours= sorted(contours, key=cv2.contourArea, reverse= True)
    # print ("Contour Areas after Sorting", get_contour_areas(sorted_contours))
    # for c in sorted_contours:
    #     cv2.drawContours(original_image, [c], -1, (255,0,0),10)
    #     cv2.waitKey(0)
    #     cv2.imshow('Contours By Area', original_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # largest_area=0;
    # largest_contour_index=0
    # img =cv2.imread(os.getcwd() + "/testImage2.jpg")
    # imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(imgray, 40, 255, 0)
    # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # cnt = contours[0]
    # bounding_rect=0#cv2.boundingRect(0)
    # for i in contours:
    #     area = cv2.contourArea(cnt)
    #     if (area>largest_area):
    #         largest_area=area
    #         largest_contour_index=i
    #         bounding_rect=cv2.boundingRect(contours[i])
    # rect=img(bounding_rect).clone()
    # cv2.imshow('largest contour ',rect)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

def getFileNamesTxt(): 
    global inputDirectory
    outputPath = os.getcwd() + "/imageList.txt"
    for filename in glob.glob(inputDirectory + "/*.jpg"):
        print(filename)

def changeImageBackgroundColor():
    img = cv2.cvtColor(cv2.imread(os.getcwd() + "/testImage2.jpg"), cv2.COLOR_BGR2RGB)
    lower_white = np.array([220, 220, 220], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(img, lower_white, upper_white)  # could also use threshold
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))  # "erase" the small white points in the resulting mask
    mask = cv2.bitwise_not(mask)  # invert mask
    # load background (could be an image too)
    bk = np.full(img.shape, 255, dtype=np.uint8)  # white bk
    # get masked foreground
    fg_masked = cv2.bitwise_and(img, img, mask=mask)
    # get masked background, mask must be inverted 
    mask = cv2.bitwise_not(mask)
    bk_masked = cv2.bitwise_and(bk, bk, mask=mask)
    # combine masked foreground and masked background 
    final = cv2.bitwise_or(fg_masked, bk_masked)
    mask = cv2.bitwise_not(mask)  # revert mask to original
    cv2.imshow('res', final)
    cv2.waitKey()
    # cv2.imshow('res', res) # gives black background
    # cv2.waitKey()


outputDirectory = os.getcwd() + "/resized_images"
inputDirectory="C:\Code\osm-bundler-pmvs2-cmvs\osm-bundler\examples\Hello"
# changeImageBackgroundColor()
# getFileNamesTxt()
# readAllImages("C:\Code\osm-bundler-pmvs2-cmvs\osm-bundler\examples\Hello")
# resize()    
# readHeightAndWidth()
# findContours()
# findLargestContour()