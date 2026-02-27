# Product Master Sync

## Purpose
Syncs the product master Google Sheet to the local SQLite database.

## Schedule
- **Cron:** `30 5 * * *` (America/New_York)
- **Frequency:** Daily at 5:30 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python imports/sync_from_sheets.py --url
```

## Behavior
- Pulls current product data from Google Sheet
- Updates local SQLite database (`~/amazon-data/amazon.db`)
- Timeout: 120s

## Error Handling
- On failure, log error — downstream jobs may use stale data
- Non-critical but should be investigated if failing repeatedly

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/imports/sync_from_sheets.py`
- Python venv at `~/amazon-data/.venv`
- Google Sheets API access
- SQLite database: `~/amazon-data/amazon.db`
