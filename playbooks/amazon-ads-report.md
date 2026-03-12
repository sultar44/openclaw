# Amazon Ads Console Report Processor

## Trigger
Gmail webhook receives an email from Amazon Ads with a scheduled report download link.
Handles multiple report types: search_terms, campaigns, keywords, targets, ad_groups.

## What You Receive
The message will include the Gmail message ID and email subject.

## Steps

### 1. Extract the download URL
```bash
python3 ~/amazon-data/collectors/ads_report_processor.py extract-url <MESSAGE_ID>
```
This outputs JSON with `download_url`, `report_name`, `report_type`, and `generated_on`.
The report type is auto-detected from the email subject.

### 2. Download the report via cookie-authenticated curl
The download link requires Amazon Ads session cookies. Export cookies from the OpenClaw browser profile and use curl:

```bash
# Export Amazon cookies from the browser
openclaw browser cookies --profile openclaw 2>&1 | python3 -c "
import json, sys
cookies = json.load(sys.stdin)
amazon_cookies = [c for c in cookies if 'amazon' in c.get('domain', '')]
with open('/tmp/amazon_cookies.txt', 'w') as f:
    for c in amazon_cookies:
        domain = c.get('domain', '')
        domain_flag = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = c.get('path', '/')
        secure = 'TRUE' if c.get('secure', False) else 'FALSE'
        expires = str(int(c.get('expires', 0)))
        f.write(f\"{domain}\t{domain_flag}\t{path}\t{secure}\t{expires}\t{c['name']}\t{c['value']}\n\")
"

# Download the report
curl -sL -b /tmp/amazon_cookies.txt -o /tmp/ads_report.xlsx "<DOWNLOAD_URL>"

# Verify it's a real xlsx (not an HTML login page)
file /tmp/ads_report.xlsx
```

If `file` shows "HTML document" instead of "Microsoft OOXML", the Amazon Ads session has expired.
Tell Ramon to log in at advertising.amazon.com in the OpenClaw browser profile.

### 3. Parse and load into BigQuery
```bash
GOOGLE_APPLICATION_CREDENTIALS=~/amazon-data/google_sheets_credentials.json python3 ~/amazon-data/collectors/ads_report_processor.py load /tmp/ads_report.xlsx
```
The script auto-detects the report type from column headers and routes to the correct BQ table.
You can force a type with `--type campaigns` if needed.

### 4. Archive the email
```bash
gog gmail modify <MESSAGE_ID> --remove-labels INBOX --account chloemercer32@gmail.com
```

### 5. Log to #chloelogs (ALWAYS — success or failure)
Post a message to #chloelogs (C0AELHCGW4F) for every report processed:

**Success:**
> ✅ Amazon Ads Report Processed
> • Type: search_terms
> • Rows: 484 | Date range: 2026-03-04 to 2026-03-10
> • BQ table: ads_console_search_terms

**Failure:**
> ❌ Amazon Ads Report Failed
> • Type: search_terms
> • Error: [what went wrong]

### 6. Result handling
- **Success**: Archive email, reply with NO_REPLY (silent)
- **Failure**: Post error to #chloebot (C0AD9AZ7R6F) in addition to #chloelogs

## Common failures
- **"HTML document" from file check**: Amazon Ads session expired. Ramon needs to log in at advertising.amazon.com in the openclaw browser profile.
- **Download URL expired**: Report links expire after ~7 days.
- **Empty body in email**: Amazon Ads emails are HTML-only. The extract-url script handles this by reading the raw HTML from Gmail API.

## BigQuery destinations
| Report Type | BQ Table |
|---|---|
| search_terms | ads_console_search_terms |
| campaigns | ads_console_campaigns |
| keywords | ads_console_keywords |
| targets | ads_console_targets |
| ad_groups | ads_console_ad_groups |

All tables are partitioned by `report_date` with date-based dedup.

## Report Type Detection
1. Email subject (e.g., "campaign report is ready" → campaigns)
2. Column headers (e.g., "Customer Search Term" → search_terms, "Keyword Type" → keywords)
3. Can be forced with `--type` flag

## Key columns (common to all types)
report_date, report_type, campaign_name, portfolio_name, country, impressions, clicks, spend, sales_7d, orders_7d, acos, roas

## Type-specific columns
- **search_terms**: customer_search_term, match_type, ad_group_name, targeting
- **campaigns**: campaign_status, campaign_type, budget, budget_type, bidding_strategy, start_date, end_date
- **keywords**: keyword, keyword_type, ad_group_name, bid, match_type
- **targets**: targeting, targeting_type, ad_group_name, bid
- **ad_groups**: ad_group_name, ad_group_status
