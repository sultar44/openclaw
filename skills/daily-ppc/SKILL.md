# Daily PPC Collection

## Purpose
Collects PPC data from Amazon Ads API for US and CA marketplaces with 3-day lookback for attribution window. Covers both Sponsored Products and Sponsored Display campaigns.

## Schedule
- **Cron:** `30 6 * * *` (America/New_York)
- **Frequency:** Daily at 6:30 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_ppc.py --lookback 3 --max-wait 1800
```

## Behavior
- 3-day lookback with `INSERT OR REPLACE` — overwrites stale data as Amazon finalizes attribution
- Collects US (profile 973179741133617) and CA (profile 4084371223098403)
- **Sponsored Products:** campaigns, keywords/targeting, search terms
- **Sponsored Display:** campaigns, targeting (includes view-through metrics)
- SD reports will return empty data until SD campaigns are launched — no errors, just 0 rows
- Tables: `ppc_campaigns`, `ppc_keywords`, `ppc_search_terms`
- Max wait of 1800s per report for generation
- Timeout: 4200s

## Error Handling
- Each report type runs independently — one failure doesn't stop the others
- If a report isn't ready within max-wait, logs error and continues
- SD report failures are non-fatal (campaigns may not exist yet)

## Alerts & Delivery
- **Success:** ClickUp task comment only (no Slack)
- **Partial failure:** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/daily_ppc.py`
- `~/amazon-data/collectors/ads_api_client.py`
- Python venv at `~/amazon-data/.venv`
- Amazon Ads API credentials (`~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
