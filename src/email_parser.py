import base64
from bs4 import BeautifulSoup
import datetime

def parse_header(headers, name):
    """Helper to extract header value."""
    for header in headers:
        if header['name'] == name:
            return header['value']
    return ""

def parse_email(msg):
    """Parses the email message object to extract required fields."""
    payload = msg['payload']
    headers = payload.get('headers', [])
    
    sender = parse_header(headers, 'From')
    subject = parse_header(headers, 'Subject')
    date_str = parse_header(headers, 'Date')
    
    # Body extraction
    body = ""
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    body = base64.urlsafe_b64decode(data).decode()
                    break
            elif part['mimeType'] == 'text/html':
                # Fallback or preference? User asked for plain text. 
                # If plain text exists, use it. If only HTML, convert.
                # Complex emails might have nested parts, simplifying for now.
                data = part['body'].get('data')
                if data:
                     html_content = base64.urlsafe_b64decode(data).decode()
                     soup = BeautifulSoup(html_content, 'html.parser')
                     body = soup.get_text()
    else:
        # Single part email
        data = payload['body'].get('data')
        if data:
            if payload['mimeType'] == 'text/html':
                 html_content = base64.urlsafe_b64decode(data).decode()
                 soup = BeautifulSoup(html_content, 'html.parser')
                 body = soup.get_text()
            else:
                 body = base64.urlsafe_b64decode(data).decode()

    return {
        'id': msg['id'],
        'from': sender,
        'subject': subject,
        'date': date_str,
        'content': body.strip()
    }
