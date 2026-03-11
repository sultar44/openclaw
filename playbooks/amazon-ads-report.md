# Amazon Ads Console Report Processor

## Trigger
Gmail webhook receives an email from Amazon Ads with a scheduled report download link.

## What You Receive
The message will include the Gmail message ID.

## Steps

### 1. Extract the download URL
```bash
python3 ~/amazon-data/collectors/ads_report_processor.py extract-url <MESSAGE_ID>
```
This outputs JSON with `download_url`, `report_name`, and `generated_on`.

### 2. Download the report via browser
Use the **browser tool** (NOT curl/wget — needs authenticated cookies):
```
browser action=navigate profile=openclaw url=<download_url>
```
This will error with "Download is starting" — that's expected and means it worked.

Wait 5 seconds, then find the file:
```bash
ls -lt ~/Downloads/*.xlsx | head -3
```
The newest `.xlsx` file is the report.

### 3. Parse and load into BigQuery
```bash
GOOGLE_APPLICATION_CREDENTIALS=~/amazon-data/google_sheets_credentials.json python3 ~/amazon-data/collectors/ads_report_processor.py load <path_to_xlsx>
```
This parses the XLSX, deduplicates by date, loads into BigQuery, and archives the file.

### 4. Archive the email
```bash
gog gmail thread modify <MESSAGE_ID> --remove INBOX --account chloemercer32@gmail.com
```

### 5. Result handling
- **Success**: Archive email, reply with NO_REPLY (silent)
- **Failure**: Post error to #chloebot (C0AD9AZ7R6F)

## Common failures
- **Browser session expired**: Tell Ramon to log in at advertising.amazon.com in the openclaw browser profile
- **Download URL expired**: Report links expire after ~7 days
- **"Download is starting" error from browser**: This is EXPECTED — it means the download is working

## BigQuery destination
- Table: `lustrous-bounty-460801-b9.amazon_raw.ads_console_search_terms`
- Partitioned by `report_date`
- Deduplicates: deletes existing rows for the same dates before inserting

## Key columns
report_date, campaign_name, ad_group_name, customer_search_term, match_type, impressions, clicks, spend, sales_7d, orders_7d, acos, roas, portfolio_name, country
