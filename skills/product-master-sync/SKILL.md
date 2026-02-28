# Product Master Sync

## Purpose
One-way pull: downloads the Product Master Google Sheet and imports it into the local SQLite database. The Google Sheet is the source of truth; SQLite is a local read-only copy for other scripts.

## Schedule
- **Cron:** `30 5 * * *` (America/New_York)
- **Frequency:** Daily at 5:30 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python imports/sync_from_sheets.py --url
```

## Behavior
- Downloads product data FROM Google Sheet (`1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs`) as CSV
- Imports INTO local SQLite database (`~/amazon-data/amazon.db`)
- Direction: Sheet → SQLite (never the reverse)
- Timeout: 120s

## Error Handling
- On failure, log error — downstream jobs may use stale data
- Non-critical but should be investigated if failing repeatedly

## Alerts & Delivery
- **Successful completion:** ClickUp task comment only (no Slack alerts)
- **Partial completion:** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/imports/sync_from_sheets.py`
- Python venv at `~/amazon-data/.venv`
- Google Sheets API access
- SQLite database: `~/amazon-data/amazon.db`
