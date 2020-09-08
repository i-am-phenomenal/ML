"""FETCH ALL MAILS AND READ THROUGH THE DATSAET TO SEE WHICH MAILS ARE SPAM OR NOT"""
import imaplib, email
import hashlib
import os 
import cryptoUtils as utils
from cryptography.fernet import Fernet
import csv 

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

def connection():
    imapUrl = "imap.gmail.com"
    connection = imaplib.IMAP4_SSL(imapUrl)
    connection.login(EMAIL, PASSWORD)
    connection.select("Inbox")
    type, data = connection.search(None, 'ALL')
    mailIds = data[0]
    idList = mailIds.split()
    firstEmail = int(idList[0])
    lastEmail = int(idList[-1])
    for i in range(latest_email_id,first_email_id, -1):
            typ, data = mail.fetch(i, '(RFC822)' )
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(response_part[1])
                    email_subject = msg['subject']
                    email_from = msg['from']
                    print('From : ' + email_from + '\n')
                    print('Subject : ' + email_subject + '\n')

def readSpamEmails():
    spams = []
    with open(os.getcwd() + "/csv/spam_ham_dataset.csv", "r") as file: 
        records = csv.reader(file)
        for row in records: 
            if row[1] == "spam": 
                spams.append(row)
            else:
                pass
                
    return  spams

def writeSpamsToCsv(spams): 
    filePath = os.getcwd() + "/csv/only_spams.csv" 
    if os.path.exists(filePath): 
        print("File already exists")
        return
    else: 
        with open(filePath, mode="a", encoding="utf-8", newline='') as file: 
            writer  = csv.writer(file, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([
                "Count",
                "Label",
                "Text",
                "Label Num"
            ])
            for spam in spams: 
                writer.writerow(spam)
            print("Done")

        
# readCredentials()
# connection()
spams = readSpamEmails()
writeSpamsToCsv(spams)