from multiprocessing import Process
import os
import time
import socket
import glob 
import sys
import _thread
import subprocess

vsfmPath = "C:\Code\VisualSFM_windows_cuda_64bit\VisualSFM.exe"
# inputDir = "C:\Code\osm-bundler-pmvs2-cmvs\osm-bundler\examples\Hello"
host = 'localhost'
port = 2048
connected = False 
locked = False
commandProcessed = False
process = None

def startProgram():
    global port
    global process
    args = ' listen[+log] %s'%(port)
    args = [vsfmPath,'listen[+log]','%d'%port ]
    print(args)
    process = subprocess.Popen(args)

def openVSFM():
    Process(target=startProgram).start()

def sendCommand(sock, command): 
    global commandProcessed
    command = command + "\n"
    command = bytes(command, "utf-8")
    sock.sendall(command)
    commandProcessed = False

def loadNViewMatch(sock, filename): 
    command = "33045 %s"%filename
    sendCommand(sock, command)

def listenToSocketStreamForFindMorePoints(_socket):
    while True:
        received = _socket.recv(1048)
        print(received)
        if b"*command processed*" in received: 
            commandProcessed = True
            print(received)
            print("CONFIRMATION RECEIVED FOR FIND MORE POINTS")
            return 0
        else:
            pass



def listenToSocketStreamForDense(_socket):
    while True:
        received = _socket.recv(1048)
        print(received)
        if b"*command processed*" in received: 
            commandProcessed = True
            print(received)
            print("CONFIRMATION RECEIVED FOR DENSE RECONSTRUCTION")
            return 0
        else:
            pass

def listenToSocketStreamForSparse(_socket):
    while True: 
        received = _socket.recv(1048)
        print(received)
        if b"*command processed*" in received: 
            commandProcessed = True
            print(received)
            print("CONFIRMATION RECEIVED FOR SPARSE RECONSTRUCTION")
            return 0
        else:
            pass

def listenToSocketStreamForMissingMatches(_socket):
    while True: 
        received = _socket.recv(1048)
        print(received)
        if b"*command processed*" in received: 
            commandProcessed = True
            print(received)
            print("CONFIRMATION RECEIVED FOR MISSING MATCHES")
            return 0
        else:
            pass
    

def listenToSocketStreamForNView(sock): 
    global connected, commandProcessed
    while True:
        received = sock.recv(1048)
        print(received)
        if b'*command processed*' in received:
            commandProcessed = True
            print(received)
            print("COMMAND CONFIRMATION RECEIVED")
            return 0
        else:
            pass

def loadNView(filename): 
    global connected, host, port, process
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    connected = True
    while connected: 
        loadNViewMatch(sock, filename)
        returnedVal = listenToSocketStreamForNView(sock)
        if returnedVal == 0:
            print(returnedVal)
            break
    return sock

def computeMissingMatches(_socket):
    if _socket is not None: 
        connected = True
        while connected:
            command ="33033"
            sendCommand(_socket, command)
            returnedVal = listenToSocketStreamForMissingMatches(_socket)
            if returnedVal == 0:
                break
        return _socket

def reconstructSparse(_socket): 
    if _socket is not None: 
        connected = True
        while connected:
            command = "33041"
            sendCommand(_socket, command)
            returnedVal = listenToSocketStreamForSparse(_socket)
            if returnedVal == 0: 
                break
        return _socket

def reconstructDense(_socket, ouputFilePath):
    if _socket is not None: 
        while True: 
            command = "33471 " + outputFilePath
            sendCommand(_socket, command)
            returnedVal = listenToSocketStreamForDense(_socket)
            if returnedVal == 0: 
                break
        return _socket

def getFileCountInGivenDirectory(path): 
    count = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    return count

def findMorePoints(_socket):
    if _socket is not None: 
        while True: 
            command = "33066"
            sendCommand(_socket, command)
            returnedVal = listenToSocketStreamForFindMorePoints(_socket)
            if returnedVal == 0:
                break
        return _socket

def getFileNamesForGivenPath(filePath, extension): 
    fileOutputPath = os.getcwd() + "/fileWithImagePaths/"
    fileCount = getFileCountInGivenDirectory(fileOutputPath)
    txtFileName = fileOutputPath + str(fileCount) + ".txt"
    with open(txtFileName, "w") as file: 
        for filename in glob.glob(filePath + "/*." + extension):
            writableContent = filename + "\n"
            file.write(writableContent)
    return txtFileName

def directoryExists(outputMainFolder, dirName):
    path = outputMainFolder + dirName
    return os.path.isdir(path)

def createDirectoryIfDoesntExists(outputMainFolder, dirName):
    if directoryExists(outputMainFolder, dirName):
        return
    else: 
        os.mkdir(outputMainFolder + dirName)
        print("CREATED DIRECTORY")

def checkIfPortIsInUse(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as _socket: 
        print(_socket.connect_ex(('localhost', port)) == 0)

if __name__ == "__main__": 
    checkIfPortIsInUse(2048)
    openVSFM()
    filename = getFileNamesForGivenPath(
        "C:\Code\Images_DataSet\Buddha", 
        "jpg"
    )
    _socket = loadNView(filename)
    _socket = computeMissingMatches(_socket)
    _socket = reconstructSparse(_socket)
    # _socket = findMorePoints(_socket)
    # _socket = resumeConstruction()
    outputMainFolder = "C:/Colmap_workspace"
    outputDirectory = "/Output_Test4/"
    createDirectoryIfDoesntExists(outputMainFolder, outputDirectory)
    outputFilePath = outputMainFolder + outputDirectory +  "test4.nvm"
    _socket = reconstructDense(_socket, outputFilePath)
    print(_socket)
    _socket.close()