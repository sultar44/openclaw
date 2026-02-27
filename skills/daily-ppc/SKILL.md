# Daily PPC

## Purpose
Collects Sponsored Products PPC data from Amazon Ads API for US and CA marketplaces with 3-day lookback for attribution.

## Schedule
- **Cron:** `30 6 * * *` (America/New_York)
- **Frequency:** Daily at 6:30 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_ppc.py --lookback 3 --max-wait 1800
```

## Behavior
- 3-day lookback for proper attribution window
- Collects US (profile 973179741133617) and CA (profile 4084371223098403)
- Sponsored Products campaigns only
- Tables: `ppc_campaigns`, `ppc_keywords`, `ppc_search_terms`
- Max wait of 1800s for report generation
- Timeout: 4200s

## Error Handling
- If report not ready within max-wait, mark for retry
- On API errors, log and continue with next profile/report

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/daily_ppc.py`
- Python venv at `~/amazon-data/.venv`
- Amazon Ads API credentials (`~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
