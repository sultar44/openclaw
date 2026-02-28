# Daily Sales & Traffic Collection

## Purpose
Collects per-ASIN daily sales and traffic data (units, revenue, sessions, page views, conversion rate) from Amazon SP-API for US and CA. This is the primary data source for the restock calculator and business performance analysis.

## Schedule
- **Cron:** `0 7 * * *` (America/New_York)
- **Frequency:** Daily at 7:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_sales.py --lookback 3
```

## Behavior
- 3-day lookback with `INSERT OR REPLACE` — Amazon finalizes sales/traffic data over ~48 hours, so each run overwrites the last 3 days with the most current numbers
- Fetches both aggregate daily totals and per-ASIN breakdowns
- Per-ASIN data requires individual day requests (API limitation — byAsin doesn't include date in multi-day ranges)
- Tables: `sales_daily` (per-ASIN), `sales_daily_totals` (aggregate)
- Also supports `--mode backfill` for historical data loading
- Timeout: 900s

## Data Collected
- **Per ASIN:** units ordered (B2C + B2B), revenue, sessions, page views, buy box %, unit session %
- **Daily totals:** aggregate units, revenue, avg selling price, sessions, page views, conversion rates

## Data Flow
```
daily_sales (7:00 AM) → sales_daily + sales_daily_totals (SQLite)
                                    ↓
                        restock calculator reads sales_daily for velocity
```

## Error Handling
- Each marketplace runs independently — US failure doesn't stop CA
- On SP-API throttle, 2s delay between day requests
- Report generation waits up to 600s per report

## Alerts & Delivery
- **Success:** ClickUp task comment only (no Slack)
- **Partial failure:** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/daily_sales.py`
- `~/amazon-data/collectors/sp_api_client.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
