
import os
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = '/Users/ramongonzalez/amazon-data/google_sheets_credentials.json'
SPREADSHEET_ID = '1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc'

def main():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Find the row for Great Day Finds (Carrie)
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Opportunities!A:M').execute()
    values = result.get('values', [])
    
    if not values:
        print("No data found.")
        return

    row_index = -1
    for i, row in enumerate(values):
        # Outlet is index 2, Summary is index 3, Reporter is index 4
        outlet = row[2] if len(row) > 2 else ""
        summary = row[3] if len(row) > 3 else ""
        reporter = row[4] if len(row) > 4 else ""
        
        if ('Great Day Finds' in summary or 'Great Day Finds' in outlet) and 'Carrie' in reporter:
            row_index = i + 1
            break
    
    if row_index == -1:
        print("Row not found.")
        return

    # Update Status (Column I - index 8) and Last Action Date (Column J - index 9)
    # Range is 1-indexed for rows, A-Z for columns
    # Column I is 9th column, Column J is 10th column
    
    body = {
        'values': [['Sent 2', '3/12/2026']]
    }
    
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=f'Opportunities!I{row_index}:J{row_index}',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()
    
    print(f"Updated row {row_index} for Great Day Finds to Sent 2.")

if __name__ == '__main__':
    main()
