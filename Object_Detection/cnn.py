import pandas as pd
import numpy as np
from tqdm import tqdm
import os
from skimage.io import imread
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.utils.data
from torch.optim import *
import h5py
from plot3D import *


class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        self.conv_layer1 = self.convLayerSet(3, 32)
        self.conv_layer2 = self.convLayerSet(32, 64)
        self.fc1 = nn.Linear(2**3*64, 128)
        self.fc2 = nn.Linear(128, numClasses)
        self.relu = nn.LeakyReLU()
        self.batch = nn.BatchNorm1d(128)
        self.drop = nn.Dropout(p=0.15)
    
    def convLayerSet(self, in_c, out_c): 
        conv_layer = nn.Sequential(
            nn.Conv3d(in_c, out_c, kernel_size=(3,3,3), padding=0),
            nn.LeakyReLU(),
            nn.MaxPool3d((2,2,2)),
        )
        return conv_layer

    def forward(self, x): 
        out = self.conv_layer1(x)
        out = self.conv_layer2(out)
        out = out.view(out.size(0), -1)
        out = self.fc1(out)
        out = self.relu(out)
        out = self.batch(out)
        out = self.drop(out)
        out = self.fc2(out)
        return out

def arrayToColor(array, cmap="Oranges"): 
    scalarMappable = plt.cm.ScalarMappable(cmap=cmap)
    return scalarMappable.to_rgba(array)[:, :-1]

# Reshape the data into 3D format
def rgbDataTransform(data): 
    dataT = []
    for i in range(data.shape[0]):
        dataT.append(arrayToColor(data[i]).reshape(16, 16, 16, 3))
    return np.asarray(dataT, dtype=np.float32)

def readDataset(): 
    with h5py.File("./full_dataset_vectors.h5", "r") as file: 
        XTrain = file["X_train"][:]
        targetsTrain = file["y_train"][:]
        XTest = file["X_test"][:]
        targetsTest = file["y_test"][:]
        sampleShape = (16, 16, 16, 3)
        XTrain = rgbDataTransform(XTrain)
        XTest = rgbDataTransform(XTest)
    Xtrain = XTrain.reshape(10000, 3, 16,16, 16)
    Xtest = XTest.reshape(2000, 3, 16, 16, 16)
    trainX = torch.from_numpy(XTrain).float()
    trainY = torch.from_numpy(targetsTrain).long()
    testx = torch.from_numpy(XTest).float()
    testy = torch.from_numpy(targetsTest).long()
    batchSize = 100 
    train = torch.utils.data.TensorDataset(trainX, trainY) 
    test = torch.utils.data.TensorDataset(testx, testy)
    trainLoader = torch.utils.data.DataLoader(train, batch_size=batchSize, shuffle=False)
    testLoader = torch.utils.data.DataLoader(test, batch_size = batchSize, shuffle=False)
    # Definition of hyperparameters
    nIters = 4500
    numEpochs = nIters / (len(trainX)/ batchSize)
    numEpochs = int(numEpochs)
    model = CNNModel()
    error = nn.CrossEntropyLoss()
    learningRate = 0.001
    optimizer = torch.optim.SGD(model.parameters(), lr=learningRate)
    # CNN model training
    count = 0
    lossList = []
    iterationList = []
    accuracyList = []
    for epoch in range(numEpochs): 
        for i, (images, labels) in enumerate(trainLoader):
            train = Variable(images.view(100, 3, 16, 16, 16))
            labels = Variable(labels)
            optimizer.zero_grad()
            outputs = model(train)
            loss = error(outputs, labels)
            loss.backward()
            optimizer.step()
            count += 1
            if count % 50 == 0:
                correct = 0
                total = 0
                for images, labels in testLoader: 
                    test = Variable(images.view(100, 3, 16, 16, 16))
                    outputs = model(test)
                    predicted = torch.max(outputs.data, 1)[1]
                    total += len(labels)
                    correct += (predicted == labels).sum()
                accuracy = 100 * correct / float(total)
                lossList.append(loss.data)
                iterationList.append(count)
                accuracyList.append(accuracy)
            if count % 500 == 0: 
                print("Iteration: {} Loss: {} Accuracy: {} %".format(count, loss.data, accuracy))
                    

    

        




        

numClasses = 10
readDataset()