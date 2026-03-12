
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pathlib import Path

SHEET_ID = '1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc'
CREDS_PATH = Path('/Users/ramongonzalez/amazon-data/google_sheets_credentials.json')

def get_service():
    creds = Credentials.from_service_account_file(
        CREDS_PATH,
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    )
    return build('sheets', 'v4', credentials=creds)

def main():
    service = get_service()
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range='Opportunities!A:M'
    ).execute()
    values = result.get('values', [])
    for i, row in enumerate(values):
        print(f"Row {i+1}: {row}")

if __name__ == '__main__':
    main()
