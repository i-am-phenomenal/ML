import cv2
import numpy as np 
from matplotlib import pyplot as plt
import os
IMAGEPATH = os.getcwd() + "/input/vase.jpg"

def cropContour(omask, image): 
    img = cv2.imread(IMAGEPATH)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
    kernel = np.ones((9,9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    result = img.copy()
    result = cv2.cvtColor(result, cv2.COLOR_BGR2BGRA)
    result[:, :, 3] = mask
    cv2.imwrite('retina_masked.png', result)

def highlightContours():
    global IMAGEPATH
    image = cv2.imread(IMAGEPATH)
    rgbImage =  cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    red = rgbImage[:,:,0]
    height, width, channels = rgbImage.shape
    mask = np.zeros((height + 2, width + 2), np.uint8)
    flooded = red.copy()
    flags = 4 | cv2.FLOODFILL_MASK_ONLY
    cv2.floodFill(flooded, mask, (8, 8), 1, 2, 2, flags)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    omask = cv2.morphologyEx(1-mask, cv2.MORPH_OPEN, kernel)
    # cropContour(omask, image)
    contours, hierarchy = cv2.findContours(omask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE )
    largestContour = []
    largestArea = 0
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > largestArea:
            largestArea = area
            largestContour = contour
    x,y,w,h = cv2.boundingRect(largestContour)
    # ROI = image[y:y+h,x:x+w]
    # cv2.namedWindow("Largest Contour",cv2.WINDOW_NORMAL)
    # cv2.imshow("Largest Contour",ROI)
    # cv2.waitKey(0)
    cv2.drawContours(rgbImage, [largestContour], -1, (0, 128, 128), 3)
    cv2.rectangle(rgbImage, (x,y), (x+w, y+h), (0, 0, 0), 2)
    return [rgbImage, largestContour]

def plotImage(rgbImage): 
    plt.imshow(rgbImage)
    plt.show()    

def drawAllContours(): 
    global IMAGEPATH
    image = cv2.imread(IMAGEPATH) 
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    edged = cv2.Canny(image, 10, 250) 
    (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    idx = 0 
    largestContour = []
    largestArea = 0
    for c in cnts: 
        area = cv2.contourArea(c)
        if area > largestArea: 
            largestArea = area
            largestContour = c
    x,y,w,h = cv2.boundingRect(largestContour)
    # image = image[y:y+h, x:x+w]
    cv2.drawContours(image, [largestContour], -1, (0, 128, 128), 3)
    cv2.rectangle(image, (x,y), (x+w, y+h), (0, 0, 0), 2)
    plotImage(image)
    #     x,y,w,h = cv2.boundingRect(c) 
    #     if w>50 and h>50: 
    #         idx+=1 
    #         new_img=image[y:y+h,x:x+w] 
    #         cv2.imwrite((os.getcwd() + "/output/" + str(idx) + '.png'), new_img) 
    # cv2.imshow("im",image) 
    # cv2.waitKey(0) 
    # image = cv2.imread(IMAGEPATH) 
    # edged = cv2.Canny(image, 10, 250) 
    # cv2.imshow("Edges", edged) 
    # cv2.waitKey(0) 
    # #applying closing function  
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7)) 
    # closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel) 
    # cv2.imshow("Closed", closed) 
    # cv2.waitKey(0) 
    # #finding_contours  
    # (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    # for c in cnts: 
    #     peri = cv2.arcLength(c, True) 
    #     approx = cv2.approxPolyDP(c, 0.02 * peri, True) 
    #     cv2.drawContours(image, [approx], -1, (0, 255, 0), 2) 
    # cv2.imshow("Output", image) 
    # cv2.waitKey(0) 
    



# rgbImage, largestContour = highlightContours()
# cropContour(rgbImage, la)
# plotImage(rgbImage)
drawAllContours()