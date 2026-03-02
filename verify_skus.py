import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def get_sheet_data():
    creds_path = os.path.expanduser('~/amazon-data/google_sheets_credentials.json')
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
    creds = service_account.Credentials.from_service_account_file(creds_path, scopes=scopes)
    service = build('sheets', 'v4', credentials=creds)
    
    spreadsheet_id = '1HFeDZ0vG3Jb8oi-LY2AsB5JdkogOoq5Qifk-a_03JCM'
    range_name = 'MC!B:C'
    
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])

if __name__ == '__main__':
    data = get_sheet_data()
    search_skus = ["8744T-PLUM-XS", "8744T-REDD-XS", "8744T-TURQ-XS"]
    for sku in search_skus:
        matches = [row[0] for row in data if len(row) > 1 and row[1] == sku]
        print(f"{sku}: {matches}")
