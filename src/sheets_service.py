import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES, SPREADSHEET_ID, TOKEN_FILE, CREDENTIALS_FILE

def get_sheets_service():
    """Gets an authenticated Sheets API service."""
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # We assume creds are handled/refreshed by the Gmail service call first, 
    # but strictly speaking we should check validity here too.
    if not creds or not creds.valid:
         if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
         else:
             # This path might be redundant if main.py ensures one login flow
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

    service = build('sheets', 'v4', credentials=creds)
    return service

def append_to_sheet(service, data):
    """Appends a list of values to the sheet."""
    # data is expected to be a list: [From, Subject, Date, Content]
    body = {
        'values': [data]
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range="Sheet1!A:D",
        valueInputOption="USER_ENTERED", body=body).execute()
    print(f"{result.get('updates').get('updatedCells')} cells appended.")
