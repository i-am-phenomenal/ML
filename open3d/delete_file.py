import os 
import glob

filePath = "C:\Code\Images_DataSet\From_VLC\chair_dataset_2\chairImages/"
matFiles = [file for file in os.listdir(filePath) if file.endswith('.mat')]
if matFiles: 
    for matFile in matFiles: 
        try: 
            os.remove(filePath + matFile)
        except Exception as e:
            print(e)
    print("Deleted all files")

siftFiles = [file for file in os.listdir(filePath) if file.endswith('.sift')]
if siftFiles:
    for siftFile in siftFiles: 
        try: 
            os.remove(filePath + siftFile)
        except Exception as e:
            print(e)
    print("Deleted all files")

allFiles = [file for file in os.listdir(filePath)]
print(len(allFiles))