"""FETCH ALL MAILS AND READ THROUGH THE DATSAET TO SEE WHICH MAILS ARE SPAM OR NOT"""
import imaplib, email
import hashlib
import os 
import cryptoUtils as utils
from cryptography.fernet import Fernet

EMAIL=""
PASSWORD=""

def removeNewLineChars():
    global EMAIL, PASSWORD
    if "\n" in EMAIL: 
        EMAIL = EMAIL.split("\n")[0].strip()
    if "\n" in PASSWORD: 
        PASSWORD = PASSWORD.split("\n")[0].split()
    return [EMAIL, PASSWORD]

def readCredentials():
    global EMAIL, PASSWORD
    with open(os.getcwd() + "/emailCreds.txt", "rb") as file: 
        EMAIL, PASSWORD = file.readlines()
    EMAIL, PASSWORD = utils.decryptMessage(EMAIL, PASSWORD)

readCredentials()