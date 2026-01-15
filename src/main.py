import os
import json
import sys

# Add parent directory to path to allow importing config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import STATE_FILE
from gmail_service import get_gmail_service, fetch_unread_emails, get_email_content, mark_as_read
from sheets_service import get_sheets_service, append_to_sheet
from email_parser import parse_email

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_state(processed_ids):
    with open(STATE_FILE, 'w') as f:
        json.dump(list(processed_ids), f)

def main():
    print("Starting Gmail to Sheets Automation...")
    
    # 1. Authenticate
    try:
        gmail_service = get_gmail_service()
        sheets_service = get_sheets_service() # Reuses same token if possible
        print("Authentication successful.")
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    # 2. Load State
    processed_ids = load_state()
    print(f"Loaded {len(processed_ids)} processed email IDs.")

    # 3. Fetch Emails
    messages = fetch_unread_emails(gmail_service)
    if not messages:
        print("No unread emails found.")
        return

    print(f"Found {len(messages)} unread emails.")

    # 4. Process Emails
    new_processed_count = 0
    for message in messages:
        msg_id = message['id']
        
        if msg_id in processed_ids:
            print(f"Skipping duplicate email ID: {msg_id}")
            continue
            
        try:
            full_msg = get_email_content(gmail_service, msg_id)
            parsed_data = parse_email(full_msg)
            
            # Data for Sheet: From, Subject, Date, Content
            row_data = [
                parsed_data['from'],
                parsed_data['subject'],
                parsed_data['date'],
                parsed_data['content']
            ]
            
            append_to_sheet(sheets_service, row_data)
            print(f"Appended email from {parsed_data['from']}")
            
            mark_as_read(gmail_service, msg_id)
            
            processed_ids.add(msg_id)
            new_processed_count += 1
            
        except Exception as e:
            print(f"Error processing message {msg_id}: {e}")

    # 5. Save State
    save_state(processed_ids)
    print(f"Finished. Processed {new_processed_count} new emails.")

if __name__ == '__main__':
    main()
