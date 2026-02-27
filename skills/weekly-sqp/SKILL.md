# Weekly SQP

## Purpose
Collects Search Query Performance (SQP) data for 14 ASINs across US and CA marketplaces (28 reports total).

## Schedule
- **Cron:** `0 6 * * 1` (America/New_York)
- **Frequency:** Mondays at 6:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/weekly_sqp.py
```

## Behavior
- Pulls SQP data for 14 ASINs in US + CA (28 reports)
- If data not yet available, marks for retry
- Timeout: 1800s

## Error Handling
- Mark unavailable reports for retry rather than failing entire job
- On API throttle, backoff and continue

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/weekly_sqp.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
