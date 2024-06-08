import os
import base64
import json
import random
import string
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_service():
    """Shows basic usage of the Gmail API."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_verification_email(receiver_email, verification_code):
    """Send a verification code to the specified email."""
    sender_email = "your_email@your_domain.com"
    subject = "Your Verification Code"
    body = f"Your verification code is: {verification_code}"

    message = MIMEMultipart()
    message['to'] = receiver_email
    message['from'] = sender_email
    message['subject'] = subject
    msg = MIMEText(body)
    message.attach(msg)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    try:
        service = get_service()
        message = {'raw': raw}
        message = (service.users().messages().send(userId="me", body=message).execute())
        print(f"Message Id: {message['id']}")
    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == "__main__":
    receiver_email = "receiver_email@gmail.com"
    # send_verification_email(receiver_email, verification_code)
