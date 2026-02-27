# Daily Ranks

## Purpose
Collects keyword ranking data from DataDive Rank Radar API for 15 ASIN/marketplace combinations.

## Schedule
- **Cron:** `0 7 * * *` (America/New_York)
- **Frequency:** Daily at 7:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_ranks.py
```

## Behavior
- Pulls rank data for 15 ASIN/marketplace combos (US + CA)
- Table: `keyword_ranking`
- If data not yet available, marks for retry (retries every 3h)
- Timeout: 900s

## Error Handling
- Mark unavailable radars for retry rather than failing
- Retries happen at 3-hour intervals until data available

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/daily_ranks.py`
- Python venv at `~/amazon-data/.venv`
- DataDive API key (`DATADIVE_API_KEY` in `~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
