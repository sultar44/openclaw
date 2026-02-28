# FBA Restock Alert

## Purpose
Runs inventory collection and restock forecasting, then alerts on SKUs that are out of stock, urgent, or running low.

## Schedule
- **Cron:** `0 9 * * 1,4` (America/New_York)
- **Frequency:** Monday and Thursday at 9:00 AM EST
- **Cron ID:** 3f5a7611-06fb-4de1-845f-ad5a98a0ceb8
- **ClickUp Task:** https://app.clickup.com/t/86ewr928d

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_inventory.py && python collectors/restock_alert.py
```

## Behavior
- Runs `daily_inventory.py` first to refresh inventory data
- Then runs `restock_alert.py` to compute restock needs
- Reads `restock_config.json` for alert filtering:
  - Skip disabled SKUs
  - Respect `marketplace_overrides`
- Alert format: group by status (OUT/URGENT first, then LOW)
- Include cartons to ship in alert
- Sheet: `1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs`
- Timeout: 600s

## Error Handling
- If inventory collection fails, do not run restock alert
- On failure, log error with last successful run date

## Alerts & Delivery

### Always (every run)
- Post execution comment on ClickUp task (status + summary)
- On success: mark ClickUp task complete (recurring tasks auto-reopen)

### Report Delivery
- **Send restock report to:** #ops_amazon (CF9T43YMQ)

### On Partial Failure
- ClickUp task comment + alert to #chloe-logs (C0AELHCGW4F)

### On Critical Failure
- ClickUp task comment + alert to #chloebot (C0AD9AZ7R6F)

### ClickUp Logging Command
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/clickup_integration.py --task 86ewr928d --status <success|partial|critical> --summary "<summary>"
```

## Dependencies
- `~/amazon-data/collectors/daily_inventory.py`
- `~/amazon-data/collectors/restock_alert.py`
- `~/amazon-data/restock_config.json`
- `~/amazon-data/collectors/clickup_integration.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- Google Sheets API
- Sheet ID: `1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs`
