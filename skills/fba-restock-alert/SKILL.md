# FBA Restock Alert

## Purpose
Runs inventory collection and restock forecasting, then alerts on SKUs that are out of stock, urgent, or running low.

## Schedule
- **Cron:** `0 9 * * 1,4` (America/New_York)
- **Frequency:** Monday and Thursday at 9:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_inventory.py && python collectors/forecast_restock.py
```

## Behavior
- Runs `daily_inventory.py` first to refresh inventory data
- Then runs `forecast_restock.py` to compute restock needs
- Reads `restock_config.json` for alert filtering:
  - Skip disabled SKUs
  - Respect `marketplace_overrides`
- Alert format: group by status (OUT/URGENT first, then LOW)
- Include cartons to ship in alert
- Sheet: `1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs`
- Timeout: 600s

## Error Handling
- If inventory collection fails, do not run forecast
- On forecast failure, log error with last successful run date

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** #chloebot with restock summary (if any OUT/URGENT/LOW items)

## Dependencies
- `~/amazon-data/collectors/daily_inventory.py`
- `~/amazon-data/collectors/forecast_restock.py`
- `~/amazon-data/restock_config.json`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- Google Sheets API
- Sheet ID: `1MUcmj4mqz-N5QSRFpqrbFUOTX33EKo85CDoaAXuuSGs`
