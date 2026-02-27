# Daily Amazon Collection

## Purpose
Collects FBA Inventory and Orders data from Amazon SP-API for US and CA marketplaces.

## Schedule
- **Cron:** `0 6 * * *` (America/New_York)
- **Frequency:** Daily at 6:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_collection.py
```

## Behavior
- Collects FBA Inventory for US (ATVPDKIKX0DER) and CA (A2EUQ1WTGCTBG2)
- Collects Orders for both marketplaces
- Stores in SQLite: `~/amazon-data/amazon.db`
- Timeout: 900s

## Error Handling
- On SP-API throttle, retry with backoff
- Log which marketplace/report failed if partial

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/daily_collection.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
