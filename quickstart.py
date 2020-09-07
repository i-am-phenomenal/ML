from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
import base64
import email

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

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
    for message in messages:        
        messageId = message["id"]
        msg = service.users().messages().get(userId='me', id=messageId, format="raw").execute()
        messageString= base64.urlsafe_b64decode(msg["raw"].encode("ASCII"))
        mimeMessage = email.message_from_bytes(messageString)
        # msg = mimeMessa
        formatted = [{
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
        }]
        if mimeMessage.is_multipart(): 
            for payload in mimeMessage.get_payload():
                print(payload.get_payload(decode=True))
                print(type(payload.get_payload()))
        else: 
            body = mimeMessage.get_payload(decode=True)
            print(body)
            exit()

main()