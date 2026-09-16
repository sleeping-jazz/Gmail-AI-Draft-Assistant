import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


def get_gmail_service():
    creds = None

    if os.path.exists("token.json"): #Have we authorized this application before?
        creds = Credentials.from_authorized_user_file("token.json",SCOPES)

    if not creds or not creds.valid: #token.json doesn't exist or Token exists but has expired.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            #Use my application's credentials and start the Google authorization process.
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",SCOPES)
            creds = flow.run_local_server(port=0) #port = 0, Choose an available port automatically.
            #print(creds)

        with open("token.json","w") as token:
            token.write(creds.to_json())

    #Create a Gmail API service object using these credentials.
    service = build("gmail","v1",credentials=creds) #Which Google service? Which API version? Who authorized the application?
    return service


if __name__ == "__main__":

    print("Connecting to Gmail...")

    service = get_gmail_service()

    profile = service.users().getProfile(userId="me").execute()

    print(profile)
    print("Connected Gmail account:", profile["emailAddress"])