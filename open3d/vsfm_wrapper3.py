from multiprocessing import Process
import os
import time
import socket
import sys
import _thread
import subprocess

vsfmPath = "C:\Code\VisualSFM_windows_cuda_64bit\VisualSFM.exe"
inputDir = "C:\Code\osm-bundler-pmvs2-cmvs\osm-bundler\examples\Hello"
host = 'localhost'
port = 9999
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

def listenToSocketStreamForDense(_socket):
    while True:
        received = _socket.recv(1048)
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
        if b'*command processed*' in received:
            commandProcessed = True
            print(received)
            # connected = False
            print("COMMAND CONFIRMATION RECEIVED")
            return 0
        else:
            pass

def loadNView(): 
    global connected, host, port, process
    filename = os.getcwd() + "/fileNames.txt"
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

def reconstructDense(_socket):
    outputFilePath = "C:/Colmap_workspace/Output Test/test.nvm"
    if _socket is not None: 
        while True: 
            command = "33471 C:/Colmap_workspace/Output Test/test.nvm"
            sendCommand(_socket, command)
            returnedVal = listenToSocketStreamForDense(_socket)
            if returnedVal == 0: 
                break
        return _socket

# def saveCurrentModel(_socket):
#     if _socket is not None: 
#         while True:
#             command = 


if __name__ == "__main__": 
    openVSFM()
    _socket = loadNView()
    _socket = computeMissingMatches(_socket)
    _socket = reconstructSparse(_socket)
    _socket = reconstructDense(_socket)
    # _socket = saveCurrentModel(_socket)
    print(_socket)