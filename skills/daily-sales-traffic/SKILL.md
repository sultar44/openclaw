# Daily Sales & Traffic

## Purpose
Collects Sales & Traffic data from Amazon SP-API for US and CA marketplaces.

## Schedule
- **Cron:** `0 7 * * *` (America/New_York)
- **Frequency:** Daily at 7:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_sales.py --mode daily --lookback 3
```

## Behavior
- 3-day lookback for data availability lag
- Collects for US (ATVPDKIKX0DER) and CA (A2EUQ1WTGCTBG2)
- Tables: `sales_daily_totals`, `sales_daily`
- Timeout: 900s

## Error Handling
- On SP-API throttle, retry with backoff
- Log missing dates if data not yet available

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/daily_sales.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
