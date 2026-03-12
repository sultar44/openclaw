
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pathlib import Path
from datetime import datetime

SHEET_ID = '1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc'
CREDS_PATH = Path('/Users/ramongonzalez/amazon-data/google_sheets_credentials.json')

def get_service():
    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    return build('sheets', 'v4', credentials=creds)

def main():
    service = get_service()
    
    # Update Status to "Sent 1" and Last Action Date to today
    today = datetime.now().strftime('%m/%d/%Y')
    
    body = {
        'values': [['Sent 1', today]]
    }
    
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range='Opportunities!I2:J2',
        valueInputOption='RAW',
        body=body
    ).execute()
    
    print(f"Updated Row 2: Status=Sent 1, Date={today}")

if __name__ == '__main__':
    main()
