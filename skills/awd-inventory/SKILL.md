# AWD Inventory Sheet Update

## Purpose
Updates AWD (Amazon Warehousing & Distribution) carton counts in the Inventory_Counts Google Sheet. Pulls current AWD inventory via SP-API and writes to the Product_List tab, Column E for matching ASINs. Appends new rows for ASINs not already in the sheet.

## Schedule
- **Cron:** `0 7 * * *` (America/New_York)
- **Frequency:** Daily at 7:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/update_awd_inventory.py
```

## Behavior
- Pulls current AWD inventory levels via SP-API
- Updates Google Sheet `1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs` (Product_List tab, Column E)
- Matches by ASIN; appends new rows for unrecognized ASINs
- Timeout: 600s

## Outcome
- **Sheet:** https://docs.google.com/spreadsheets/d/1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs

## Error Handling
- On API failure, log and retry once
- Non-critical — stale data acceptable for one day

## Alerts & Delivery
- **Success:** ClickUp task comment only (no Slack)
- **Partial failure:** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/update_awd_inventory.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- Google Sheets API (service account)
