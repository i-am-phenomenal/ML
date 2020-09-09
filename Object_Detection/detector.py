# Activate virtual env -> C:\Code\Object_Detection\venv\Scripts\activate.bat
from imageai.Detection import ObjectDetection
import tensorflow as tf

detector = ObjectDetection()
modelPath = "./models/yolo-tiny.h5"
inputPath = "./input/test1.jpg"
outputPath = "./output/newImageForTest1.jpg"
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath(modelPath)
detector.loadModel()
detection, detectedImagesLocations = detector.detectObjectsFromImage(
    input_image=inputPath, 
    output_image_path=outputPath, 
    extract_detected_objects=True
)
for eachItem in detection: 
    print(eachItem["name"], " : ", eachItem["percentage_probability"])
for location in detectedImagesLocations: 
    print(location)
    