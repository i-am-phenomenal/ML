from multiprocessing import Process
import os
import time
import socket
import sys
import _thread
import subprocess

# vsfmPath = 'C:\Users\BOIRUM\Documents\Curt\CMU\Fall 2013\Computer Vision\VisualSFM_windows_cuda_64bit\VisualSFM_windows_cuda_64bit\VisualSFM.exe'
vsfmPath = "C:\Code\VisualSFM_windows_cuda_64bit\VisualSFM.exe"
# inputDir = r'C:\Users\BOIRUM\Desktop\VsfmInput'
inputDir = "C:\Code\osm-bundler-pmvs2-cmvs\osm-bundler\examples\Hello"
host = 'localhost'
port = 2048
connected = False
locked = False
cmdProcessed = False
process = None
#print 'Using for VisualSFM path: %s'% vsfmPath

"""
Documentation from the VSFM executable help text:

VisualSFM listen[+log] port
    Start the GUI and listen to a socket port for UI commands,
    which simulate menu clicks. Each command should in the for
    of "id[c][s] [argument]\n". The [id] is an integer that
    corresponds to a menu item, for which the complete list
    can be found in the sample ui.ini file. The optional flag
    [c][s] corresponds CTRL and SHIFT press; The [argument] is
    for the input string like filepath.
    Log messages will be send to client if +log is specified
"""

def startProgram(port):
    global process
    args = ' listen[+log] %s'%(port)
    #os.execlp(vsfmPath,args)#' listen',' 2000')#args)
    args = [vsfmPath,'listen[+log]','%d'%port ]
    
    print(args)
    process = subprocess.Popen(args)

def startVSFM(port):
    
    #print 'Command Line Arguments: %s'%args
    Process(target=startProgram,args=(port,)).start()
    
def listen2socket(sock,empty):
    print("0000000000000000000000")
    """
    Prints all data received from the socket in a while loop
    and closes on socket disconnect
    call from thread.start_new_thread
    """
    global connected
    global cmdProcessed
    try:

        #sock.sendall(data + '\n')
        while True:
            received = sock.recv(1048)
            # print(received, "22222222")
            #print received
            if '*command processed*' in received:
                cmdProcessed = True
                print("Confirmation received")
            #print "Received: {}".format(received)
    except:
        print('VisualSFM disconnected')
        sock.close()
        connected = False
        
#menu_file    _File
    #menu_33166    Open+ Multi Images
    #menu_33028    Open+ Image &  SIFT
    #menu_33186    Open Current Path
    #menu_32928    Detect Features
    #menu_33167    Load Feature File
    #menu_32841    New  _Window
    #menu_105    _Close Window
    #menu_32842    _Exit Program
    
#menu_view    _View
    #menu_32777    Single Image
    #menu_33019    Feature Matches
    #menu_33007    Inlier Matches
    #menu_33005    2-View 3D Points
    #menu_33037    N-View 3D Points
    #menu_33467    Dense 3D Points
    #menu_33190    Image Thumbnails
    #menu_33530    Perspective View
    #menu_33451    Dark Background
    #menu_33218    Show Single Model
    #menu_33034    Show 2View Tracks

def loadImage(sock,fileName):
    cmd = '33028 %s'%fileName    #Open+ Image &  SIFT
    #cmd = '33166 %s'%fileName
    #cmd = '33166 %s'%fileName #Open+ Multi Images
    #cmd = '33186 %s'%'C:\Users\BOIRUM\Documents\Curt\Research Ideas\SFM Models\Kristi Doug Kadyn Couch Home'    #Open Current Path
    #sock.sendall(cmd + '\n')
    #cmd = '33119'
    sendCommand(sock,cmd)
    
def setCal(sock):
    cal = '265.6548 324.6482 265.7165 232.9243 0'
    cmd = '3299 [%s]'%cal
    print('sent calibration:')
    print(cal)
    sendCommand(sock,cmd)

def reconstructDense(sock): 
    command = "33471"
    sendCommand(sock, command)
    pass

def reconstructSparse(sock): 
    command = "33041"
    sendCommand(sock, command)
    pass

def computeMissingMatch(sock): 
    command = '33033'
    sendCommand(sock, command)
    pass

def matchSequence(sock,spread):
    #spread = matching range of each image in sequence
    spread = 2
    cmd = '33498 %d'%spread
    sendCommand(sock,cmd)

def resumeConstruction(sock):
    cmd = '33065'    #Reconstruct Resume
    sendCommand(sock,cmd)
    pass

def findMatches(sock,file1,file2):
    pass

def loadNViewMatch(sock,fileName):
    cmd = '33045 %s'%fileName
    sendCommand(sock,cmd)
    
def sendCommand(sock,cmd):
    global cmdProcessed
    cmd = cmd + '\n'
    cmd = bytes(cmd, "utf-8")
    # print(cmd)
    # print(type(cmd))
    # exit()
    sock.sendall(cmd)
    cmdProcessed = False

def getImList(path):
    """
    gets list of images in the specified path
    """
    included_extentions = ['jpg','bmp','png','gif' ]
    contents = os.listdir(path)
    imList = []
    for fn in contents:
        for ext in included_extentions:
            if fn.lower().endswith(ext):
                imList.append(os.path.join(path,fn))
                break
    return imList
    
def getNewImage(oldList,inputDir):
    newList = getImList(inputDir)
    if newList:
        if oldList:
            newList = set(newList)
            oldList = set(oldList)
            newList = list(newList.difference(oldList))
    
    if len(newList)>0:
        return newList
    else:
        return False

def wait4finish(task):
    global cmdProcessed
    global process
    dt = .5
    et = 0
    while not cmdProcessed:
        print("Waiting for %s..."%task)
        et +=dt
        time.sleep(dt)
    print("Processing Next Command")

def controlVSFM(port, command):
    """
    Start a client to sent commands to VSFM
    """
    global connected
    global cmdProcessed
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    connected = True
    _thread.start_new_thread(listen2socket,(sock,True))
    # print("111111111111111")
    i = 0
    oldImList = []
    #print'set calibration to: 265.6548 324.6482 265.7165 232.9243 0'
    #jack =raw_input('press enter when ready')
    #setCal(sock)
    #quit()
    # print(sock)
    # exit()
    while connected:
        if command == "33045":
            filename = os.getcwd() + "/fileNames.txt"
            loadNViewMatch(sock, filename)
            received = sock.recv(2048)
            received == received.decode("utf-8")
            print(received)
            wait4finish('Loading NView Images')
        elif command == "33033":
            computeMissingMatch(sock)
        # if b"----------------------------------------------------------------\r\nLoad existing NView match, finished" in received: 
        # if b"*command processed*" in received:
        #     print(received)
        #     print("111111111111111111111111111")
        #     sock.close()
        #     exit()
        #     # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     # sock = sock.connect((host,port))
        #     # exit()
        #     computeMissingMatch(sock)
        #     if b"----------------------------------------------------------------\r\nCompute Missing Pairwise Matching, finished\r\n" in received:
        #         # print(received)
        #         # sock.close()
        #         # exit()
        #         reconstructSparse(sock)
        #         # if b"----------------------------------------------------------------\r\nRun full 3D reconstruction, finished" in received:
        #         if b"########-------timing------#########" in received:
        #             time.sleep(5)
        #             print(received)
        #             reconstructDense(sock)
        #             # exit()
            




        # print(received)
        # if received == "Load existing NView match, finished": 
            # print(received)
        # wait4finish('Loading NView Images')
        # time.sleep(20)
        # matchSequence(sock,4)
        # computeMissingMatch(sock)
        # wait4finish('COMPUTING MISSING MATCH')
        # reconstructSparse(sock)
        # wait4finish("RECONSTRUCTING SPARSE")
        # reconstructDense(sock)
        # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        # connected= False
        # resumeConstruction(sock)
        # newImList = getNewImage(oldImList,inputDir)
        # if newImList:
        #     for path in newImList:
        #         loadImage(sock,path)
        #         wait4finish('Image loading')
            # oldImList.extend(newImList)
            # matchSequence(sock,4)
            # wait4finish('Sequence Matching')
            # resumeConstruction(sock)
            # wait4finish('Sparse Reconstruction')
        time.sleep(1)


if __name__ == '__main__':
    
    startVSFM(port)
    controlVSFM(port, "33045")
    controlVSFM(port, "33033")


    print('Main program exiting')