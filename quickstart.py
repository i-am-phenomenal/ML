from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import base64
import email
from bs4 import BeautifulSoup
import csv 

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def writeToCsv(formatted):
    with open(os.getcwd() + "/csv/emails.csv", mode="w", encoding="utf-8", newline='') as file:
        writer  = csv.writer(file, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        row = list(formatted.values())
        writer.writerow(row)
        print("Done")

def main():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'S_Email_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    messages = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute()
    messages = messages.get("messages", [])
    counter = 0
    for message in messages:
        counter += 1
        print(counter)
        messageId = message["id"]
        msg = service.users().messages().get(userId='me', id=messageId, format="raw").execute()
        messageString= base64.urlsafe_b64decode(msg["raw"].encode("ASCII"))
        mimeMessage = email.message_from_bytes(messageString)
        formatted = {
            "deliveredTo": mimeMessage["Delivered-To"],
            "date": mimeMessage["Date"],
            "from": mimeMessage["From"],
            "replyTo": mimeMessage["Reply-To"],
            "to": mimeMessage["To"],
            "subject": mimeMessage["Subject"],
            "precedence": mimeMessage["Precedence"],
            "feedbackId": mimeMessage["Feedback-ID"],
            "messageId": mimeMessage["Message-ID"],
            "messageBody": ""
        }
        if mimeMessage.is_multipart(): 
            for payload in mimeMessage.get_payload():
                body = payload.get_payload(decode=True)
                contentType = payload.get_content_type()
                if contentType == "text/html":
                    cleaned = BeautifulSoup(body.decode("utf-8"), "html.parser").get_text()
                    formatted["messageBody"] = cleaned
                elif contentType == "text/plain":
                    formatted["messageBody"] = body
        else: 
            body = mimeMessage.get_payload(decode=True)
            cleaned = BeautifulSoup(body.decode("utf-8"), "html.parser").get_text()
            formatted["messageBody"] = cleaned
        writeToCsv(formatted)

def writeRowsToCSV(): 
    csvFile = os.getcwd() + "/csv/emails.csv"
    if os.path.exists(csvFile): 
       print("File already exists")
       return
    else: 
        try:
            with open(csvFile, mode="w") as file: 
                writer  = csv.writer(file, delimiter=',', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([
                    "Delivered To",
                    "Date",
                    "From",
                    "Reply To",
                    "To",
                    "Subject",
                    "Precedence",
                    "Feedback Id",
                    "Message Id",
                    "Message Body"
                ])
        except Exception as e: 
            print(e)

writeRowsToCSV()
main()