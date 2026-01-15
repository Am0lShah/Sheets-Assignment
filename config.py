import os

# Scopes for Gmail and Sheets API
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/spreadsheets'
]

# Spreadsheet ID - User needs to update this
SPREADSHEET_ID = 'ENTER YOUR SPREADSHEET ID HERE'

# Credentials paths
CREDENTIALS_FILE = os.path.join('credentials', 'credentials.json')
TOKEN_FILE = 'token.json'
STATE_FILE = 'processed_emails.json'

# Email filtering
MAX_RESULTS = 10  # Number of emails to fetch per run
