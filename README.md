# Gmail to Google Sheets Automation

This project automates the process of fetching unread emails from your Gmail inbox and logging them into a Google Sheet. It uses the official Google Gmail and Sheets APIs with OAuth 2.0 authentication.

## Features
- Authenticates securely via OAuth 2.0.
- Fetches unread emails from the Inbox.
- Parses Email Sender, Subject, Date, and Body (converting HTML to plain text).
- Appends data to a specified Google Sheet.
- Prevents duplicates using a local state file and checks against existing message IDs.
- Marks processed emails as Read.

## Prerequisites
1. **Python 3.x** installed.
2. A **Google Cloud Project** with Gmail API and Google Sheets API enabled.
3. **OAuth 2.0 Credentials** (`credentials.json`) downloaded from the Google structure.

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd gmail-to-sheets
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Credentials
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project and enable **Gmail API** and **Google Sheets API**.
3. Create OAuth 2.0 Client IDs (Desktop App).
4. Download the JSON file, rename it to `credentials.json`, and place it in the `credentials/` folder.

### 4. Configure Spreadsheet
1. Create a new Google Sheet.
2. Copy the Spreadsheet ID from the URL: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit...`
3. Open `config.py` and replace `YOUR_SPREADSHEET_ID_HERE` with your actual ID.
4. Add headers to your sheet: `From`, `Subject`, `Date`, `Content`.

## Usage
Run the main script:
```bash
python src/main.py
```
On the first run, a browser window will open asking you to log in and authorize the application. A `token.json` file will be created for subsequent runs.

## Architecture
```mermaid
graph TD
    A[User Run Script] --> B{Auth Valid?}
    B -- No --> C[OAuth Login Flow]
    B -- Yes --> D[Load State (processed_ids)]
    C --> D
    D --> E[Fetch Unread Emails (Gmail API)]
    E --> F{Emails Found?}
    F -- No --> G[End]
    F -- Yes --> H[Loop through Emails]
    H --> I{ID in State?}
    I -- Yes --> H
    I -- No --> J[Parse Email (Body/Subject/Date)]
    J --> K[Append to Google Sheet (Sheets API)]
    K --> L[Mark as Read (Gmail API)]
    L --> M[Update Local State]
    M --> H
    H --> N[Save State to JSON]
```

## Design Decisions & Explanations

### OAuth Flow
We use the **device-based OAuth 2.0 flow** for installed applications.
1.  The script initiates a flow requesting `gmail.readonly`, `gmail.modify`, and `spreadsheets` scopes.
2.  The user authorizes in the browser.
3.  A `token.json` is saved locally.
4.  Subsequent runs use this token to refresh credentials automatically, avoiding manual login.

### Duplicate Prevention & State Persistence
**Strategy**: We maintain a local JSON file `processed_emails.json` that acts as a database of processed Message IDs.
**Why this approach?**
RELIABILITY. Relying solely on the "UNREAD" label is risky. If the script crashes after writing to Sheets but before marking as read, the next run would duplicate the entry. By checking against a permanent set of IDs, we ensure **idempotency**—no matter how many times you run the script on the same emails, they will only be logged once.

## Challenges & Solutions
**Challenge**: Handling various email formats (HTML vs Plain Text).
**Solution**: Emails come as multipart payloads. We implemented a parser in `email_parser.py` that iterates through parts. It prioritizes `text/plain` but falls back to `text/html`. We used `BeautifulSoup` to strip HTML tags and ensure clean text in the spreadsheet.

**Challenge**: Virtual Environment Issues during setup.
**Solution**: The system had issues creating a standard venv. We adapted by installing dependencies to the user path (`--user`) to ensure the script could run immediately without complex environment troubleshooting.

## Limitations
1.  **Local State**: If `processed_emails.json` is deleted, already-read emails won't be duplicated (since we fetch UNREAD), but if an email is manually marked unread again, it would be duplicated.
2.  **Attachment Handling**: The current script ignores attachments and only captures text content.
3.  **Rate Limiting**: We fetch a maximum of 10 emails per run (`MAX_RESULTS`), which is a respectful limit for the API but might check fewer emails for high-volume inboxes.

## Author
Amol Shah
