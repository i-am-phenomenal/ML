import requests 
import json
import urllib.parse
import ast
import os 
import time

clientId = ""
clientSecret= ""

AUTHENTICATION_URL = "https://developer.api.autodesk.com/authentication/v1/authenticate"

def getBodyString(): 
    global clientId, clientSecret
    urlEncoded = """client_id={clientId}&client_secret={clientSecret}&grant_type=client_credentials&scope=bucket:create%20bucket:read%20data:write"""
    urlEncoded = urlEncoded.format(
        clientId=clientId,
        clientSecret=clientSecret
    )
    return urlEncoded

def convertBytesToDictionary(content):
    dict_str = content.decode("utf-8")
    records = ast.literal_eval(repr(dict_str))
    converted = json.loads(records)
    return converted

def generateWriteScopeJwt():
    global  AUTHENTICATION_URL
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    body = getBodyString()
    response = requests.post(AUTHENTICATION_URL, data=body, headers=headers)
    response = convertBytesToDictionary(response.content)
    return response["access_token"]

def getHeaders(jwt): 
    headers = {
        "Authorization": "Bearer %s" %jwt,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    headers["Authorization"] = headers["Authorization"].replace('"', "")
    return headers

def createPhotoScene(jwt): 
    headers = getHeaders(jwt)
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/photoscene"
    body = {
        "scenename": "TestScene",
        "format": "obj",
        "scenetype": "object"
    }
    response = requests.post(url, data=body, headers=headers)
    response = convertBytesToDictionary(response.content)
    photoSceneId = response["Photoscene"]["photosceneid"]
    return photoSceneId

def uploadImage(jwt, photoSceneId): 
    headers = getHeaders(jwt)
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/file"
    filePath = os.getcwd() + "/input/vase.jpg"
    body = { 
        "photosceneid": photoSceneId,
        "type": "image",
        "file[0]": open(filePath, "rb")
        # "file[0]": "https://images-na.ssl-images-amazon.com/images/I/51Cr%2Br8NBDL.jpg"
        # "file[1]": "https://static.lladro.com/media/catalog/product/cache/9a0e182083c7c5b80c6d12079a53d350/e/a/eadbbfaa23783b6091e30420fdd5348a5db3b4e7a0931e7ca9c6b7c28938296c992c960304d759ad0280f648842307eacd10c569184b66dda2aefcae483bcdbe.jpg",
        # "file[2]": "https://4.imimg.com/data4/KK/DV/MY-20561285/flower-vase-500x500.jpg"
    }
    response = requests.post(url, data=body, headers=headers)
    print(response.content)

def getAuthenticationTokenForReadScope(): 
    urlEncodedForScope = """client_id={clientId}&client_secret={clientSecret}&grant_type=client_credentials&scope=data:read"""
    urlEncodedForScope = urlEncodedForScope.format(
        clientId=clientId,
        clientSecret=clientSecret
    )
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response =  requests.post(AUTHENTICATION_URL, data=urlEncodedForScope, headers=headers)
    response = convertBytesToDictionary(response.content)
    return response["access_token"]

def getHeadersWithOnlyAuthorization(readScopeToken): 
    headers = { 
        "Authorization": "Bearer %s" %readScopeToken
    }
    headers["Authorization"] = headers["Authorization"].replace('"', "")
    return headers

def checkPhotoSceneProperties( photoSceneId): 
    global clientId, clientSecret
    readScopeToken = getAuthenticationTokenForReadScope()
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/" + photoSceneId + "/properties"
    headers = getHeadersWithOnlyAuthorization(readScopeToken)
    response = requests.get(url, headers=headers)
    response = convertBytesToDictionary(response.content)
    for key, value in response.items():
        print(key, "==>", value )
    # print(response.content)


def trackProgress(photoSceneId): 
    global clientId, clientSecret, AUTHENTICATION_URL
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/" + photoSceneId + "/progress"
    urlEncoded = """client_id={clientId}&client_secret={clientSecret}&grant_type=client_credentials&scope=data:read"""
    urlEncoded = urlEncoded.format(
        clientId=clientId,
        clientSecret=clientSecret
    )
    headersForJwt = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(AUTHENTICATION_URL, data=urlEncoded, headers=headersForJwt)
    response = convertBytesToDictionary(response.content)
    response = response["access_token"]
    actualHeaders = {
        "Authorization": "Bearer %s" %response
    }
    counter = True
    while counter:
        actualResponse = requests.get(url, headers=actualHeaders)
        actualResponse = convertBytesToDictionary(actualResponse.content)
        time.sleep(5)
        if actualResponse["Photoscene"]["progress"] == "100":
            counter = False
            print(actualResponse)
        else: 
            print(actualResponse)
            pass

def startPhotoSceneProcessing(jwt, photoSceneId): 
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/" + photoSceneId
    headers = getHeaders(jwt)
    response = requests.post(url, headers=headers)
    print(response.content)

def downloadProcessedData(photoSceneId): 
    global clientId, clientSecret
    readScopeToken = getAuthenticationTokenForReadScope()
    print(readScopeToken)

def deletePhotoScene(writeScopeJwt, photoSceneId): 
    url = "https://developer.api.autodesk.com/photo-to-3d/v1/photoscene/" + photoSceneId
    headers = getHeaders(writeScopeJwt)
    response = requests.delete(url, headers=headers)
    print(response.content)

writeScopeJwt = generateWriteScopeJwt()
# print(writeScopeJwt)
# photoSceneId =  createPhotoScene(writeScopeJwt)
photoSceneId = ""
# uploadImage(writeScopeJwt, photoSceneId)

# checkPhotoSceneProperties(photoSceneId)
# startPhotoSceneProcessing(writeScopeJwt, photoSceneId)
# trackProgress(photoSceneId)
downloadProcessedData(photoSceneId)

# deletePhotoScene(writeScopeJwt, photoSceneId)