# Weekly SQP

## Purpose
Collects Search Query Performance (SQP) data for all ASINs on the product master sheet, per country (US/CA). As ASINs are added to the sheet, they're automatically included.

## Schedule
- **Cron:** `0 6 * * 1` (America/New_York)
- **Frequency:** Mondays at 6:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/weekly_sqp.py
```

## Behavior
- Reads ASIN + Country dynamically from the product master Google Sheet (`1z7WGoXHJ-k2K72wUmp5VU81h37wKaKyqcf9F5cwy_2s`)
- Only runs US ASINs against the US marketplace, CA ASINs against CA (no duplication)
- If data not yet available, marks for retry
- Timeout: 1800s

## Error Handling
- Mark unavailable reports for retry rather than failing entire job
- On API throttle, backoff and continue

## Alerts & Delivery
- **Standard hierarchy:** Success → ClickUp only, Partial failure → ClickUp + #chloe-logs (C0AELHCGW4F), Critical failure → ClickUp + #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/weekly_sqp.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- Google Sheets service account: `~/amazon-data/google_sheets_credentials.json`
- Product master sheet: `1z7WGoXHJ-k2K72wUmp5VU81h37wKaKyqcf9F5cwy_2s`
- SQLite database: `~/amazon-data/amazon.db`
