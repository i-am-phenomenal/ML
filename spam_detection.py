import os
import csv
import nltk 
from nltk.corpus import stopwords
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

def loadSpamRecords():
    allRecords = []
    with open(os.getcwd() + "/csv/only_spams.csv", "r") as file: 
        records = csv.reader(file)
        for row in records: 
            cleaned = {
                "count": row[0],
                "label": row[1],
                "text": row[2],
                "labelNum": row[3]
            }
            allRecords.append(cleaned)
    allRecords = allRecords[1: len(allRecords)]
    return allRecords

def getFormattedText(text): 
    return text.replace("\n", "")

def removePunctuations(filtered):
    punctuations = string.punctuation
    return [x for x in filtered if x not in punctuations]

def removeStopWords(text):
    stopWords = stopwords.words('english')
    return [x for x in text if x not in stopWords]

def getCleanedText(spams): 
    cleaned = []
    for spam in spams: 
        text = spam["text"]
        text = getFormattedText(text).split(" ")
        filtered = removeStopWords(text) 
        filtered = removePunctuations(filtered)
        spam["text"] = filtered
        cleaned.append(spam)
    return cleaned

def extractFeatures(spams): 
    for spam in spams:
        vect = CountVectorizer()
        X = vect.fit_transform(spam["text"])
        featureNames = vect.get_feature_names()
        xTrain, xTest, yTrain, yTest = train_test_split(X, spam["text"], test_size = 0.20, random_state=0)
        # bow = CountVectorizer(analyzer=process_text).fit_transform(spam["text"])
        # print(bow)


spams = loadSpamRecords()
spams = getCleanedText(spams)
extractFeatures(spams)
