# AWD Inventory

## Purpose
Updates the AWD (Amazon Warehousing & Distribution) inventory sheet with current levels.

## Schedule
- **Cron:** `0 7 * * *` (America/New_York)
- **Frequency:** Daily at 7:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/update_awd_inventory.py
```

## Behavior
- Pulls current AWD inventory levels
- Updates Google Sheet with latest data
- Timeout: 600s

## Error Handling
- On API failure, log and retry once
- Non-critical — stale data acceptable for one day

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/update_awd_inventory.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- Google Sheets API
