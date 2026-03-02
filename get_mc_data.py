import os
import json
import gspread
from google.oauth2.service_account import Credentials

def get_caja_info():
    scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds_path = os.path.expanduser('~/amazon-data/google_sheets_credentials.json')
    creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
    gc = gspread.authorize(creds)
    
    sh = gc.open_by_key('1HFeDZ0vG3Jb8oi-LY2AsB5JdkogOoq5Qifk-a_03JCM')
    worksheet = sh.worksheet('MC')
    
    # Read columns B and C
    values = worksheet.get('B:C')
    return values

if __name__ == '__main__':
    data = get_caja_info()
    print(json.dumps(data))
