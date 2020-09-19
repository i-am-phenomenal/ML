import os 
import glob
import shutil

def deleteFilesWithGivenExtension(extension):
    filePath = "C:\Code\Images_DataSet\From_VLC\chair_dataset_2\chairImages/"
    matFiles = [file for file in os.listdir(filePath) if file.endswith(extension)]
    if matFiles: 
        for matFile in matFiles: 
            try: 
                os.remove(filePath + matFile)
            except Exception as e:
                print(e)
        print("Deleted all files")

# deleteFilesWithGivenExtension('.sift')
# deleteFilesWithGivenExtension('.mat')

def moveFilesToGivenFolder(source, destination):
    allFiles = os.listdir(source)
    for file in allFiles: 
        shutil.move(source + "/" + file, destination)
    print("Moved all files")

def deleteFolder(dirPath): 
    os.rmdir(dirPath)
    print("Deleted Dir")

source = "C:/Code/Images_DataSet/From_VLC/chair_dataset_2/"
destination = "C:/Code/Images_DataSet/From_VLC/chair_dataset_2/Mug_0"
for iter in range(1, 9):
    completeSource = source + "Mug_" + str(iter)
    # moveFilesToGivenFolder(completeSource, destination)
    deleteFolder(completeSource)



    
