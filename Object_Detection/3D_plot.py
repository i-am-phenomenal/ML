from tvtk.api import tvtk
import numpy as np
from mayavi import mlab    
import cv2
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
# from matplotlib.pyplot import *
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt

def plotCube():
    X, Y, Z = np.mgrid[-100:10:100j, -10:10:100j, -10:10:100j]
    data = np.sin(X*Y*Z)/(X*Y*Z)
    i = tvtk.ImageData(spacing=(1, 1, 1), origin=(0, 0, 0))
    i.point_data.scalars = data.ravel()
    i.point_data.scalars.name = 'scalars'
    i.dimensions = data.shape
    mlab.pipeline.surface(i)
    mlab.colorbar(orientation='vertical')
    mlab.show()

def plotSphere(xCoord, yCoord, zCoord): 
    mlab.clf()
    phi, theta = np.mgrid[0:np.pi:11j, 0:2*np.pi:11j]
    x = np.sin(phi) * np.cos(theta)
    y = np.sin(phi) * np.sin(theta)
    z = np.cos(phi)
    mlab.mesh(x, y, z)
    mlab.mesh(x, y, z, representation='wireframe', color=(0, 0, 0))
    mlab.show()

def findCoordinatesOfObject():
# Load image
    im = cv2.imread('./input/circles.png')

    # Convert to grayscale and threshold
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,1,255,0)

    # Find contours, draw on image and save
    im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(im, contours, -1, (0,255,0), 3)
    cv2.imwrite('result.png',im)

    # Show user what we found
    for cnt in contours:
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        print('Contour: centre {},{}, radius {}'.format(x,y,radius))

def drawImageUsingPIL():
    image = Image.new("RGB", (640, 480))
    draw = ImageDraw.Draw(image)
    # points = ((1,1), (2,1), (2,2), (1,2), (0.5,1.5))
    points = ((100, 100), (200, 100), (200, 200), (100, 200), (50, 150))
    draw.polygon((points), fill=200)
    image.show()

def drawImageUsingMatPlot():
    x = ([1,2,2,1,0.5,1]) 
    y = ([1,1,2,2,1.5,1])
    z = ([1,1,1,1,1,1])
    plot(x,y, z)
    show()

def f(x, y): 
    return np.sin(np.sqrt(x ** 2 + y ** 2))



def draw3DImage(): 
    x = np.linspace(-6, 6, 30)
    y = np.linspace(-6, 6, 30)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.view_init(60, 35)
#     fig = plt.figure()
#     ax = plt.axes(projection='3d')
# # Data for a three-dimensional line
#     zline = np.linspace(0, 15, 1000)
#     xline = np.sin(zline)
#     yline = np.cos(zline)
#     ax.plot3D(xline, yline, zline, 'gray')
#     # Data for three-dimensional scattered points
#     zdata = 15 * np.random.random(100)
#     xdata = np.sin(zdata) + 0.1 * np.random.randn(100)
#     ydata = np.cos(zdata) + 0.1 * np.random.randn(100)
#     ax.scatter3D(xdata, ydata, zdata, c=zdata, cmap='Greens')


# plotCube()
# plotSphere()
# drawImageUsingPIL()
# drawImageUsingMatPlot()
draw3DImage()
# findCoordinatesOfObject()