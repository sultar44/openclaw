import sys
from pathlib import Path
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

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
    # Get metadata to find the sheet name
    spreadsheet = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
    sheet_name = spreadsheet['sheets'][0]['properties']['title']
    print(f"Sheet name: {sheet_name}")

    # Read data
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=f"'{sheet_name}'!A1:Z500"
    ).execute()
    values = result.get('values', [])
    if not values:
        print("No data found.")
        return

    header = values[0]
    status_idx = -1
    for i, col in enumerate(header):
        if 'status' in col.lower():
            status_idx = i
            break
    
    if status_idx == -1:
        print("Status column not found in header.")
        return

    row_num = -1
    row_data = None
    for i, row in enumerate(values[1:], 2): # Start from row 2
        # Check if "Ginger Casa" is in this row
        if any("Ginger Casa" in str(cell) for cell in row):
             row_num = i
             row_data = row
             break
    
    if row_num == -1:
        print("Could not find 'Ginger Casa' in the sheet.")
        return

    print(f"Found 'Ginger Casa' at row {row_num}: {row_data}")
    
    # Update status
    col_letter = chr(ord('A') + status_idx)
    cell_range = f"'{sheet_name}'!{col_letter}{row_num}"
    print(f"Updating status at {cell_range} to 'Closed (Not interested)'")
    service.spreadsheets().values().update(
        spreadsheetId=SHEET_ID,
        range=cell_range,
        valueInputOption='RAW',
        body={'values': [['Closed (Not interested)']]}
    ).execute()
    print("Successfully updated status.")

if __name__ == "__main__":
    main()
