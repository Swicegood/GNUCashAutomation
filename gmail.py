import threading
import webbrowser
import os
from http.server import HTTPServer
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import socket

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def run_flow_with_timeout(flow, timeout=60):
    """Run the flow's local server with a timeout."""
    def run_server():
        flow.run_local_server(port=0)

    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # Allow thread to be interrupted
    server_thread.start()
    server_thread.join(timeout=timeout)

    if not server_thread.is_alive():
        # Server thread completed within timeout
        if flow.credentials and flow.credentials.valid:
            return flow.credentials
        else:
            raise ValueError("Failed to obtain valid credentials.")
    else:
        # Timeout reached, server thread still alive (user did not authenticate)
        raise TimeoutError("Authentication process did not complete within the allotted time.")

def grab_emails(search_str):
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            try:
                creds = run_flow_with_timeout(flow, timeout=30)  # 60 seconds timeout
            except (TimeoutError, ValueError) as e:
                print(e)
                return []  # or handle the exception as needed

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', q=search_str, maxResults=10).execute()
    messages = results.get('messages', [])
    emailmatches = []    

    if not messages:
        print('No messages found.')
    else:
        print('Messages:')
        for message in messages:
            emailmatches.append(service.users().messages().get(userId='me', id=message['id']).execute())
            emailmatches[-1]['confidence'] = 7
            print(emailmatches[-1]['snippet'])

    return emailmatches


if __name__ == "__main__":
    grab_emails("419.25")