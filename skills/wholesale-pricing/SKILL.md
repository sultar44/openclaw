# Wholesale Pricing

## Purpose
Fetches current FBA/FBM inventory and offer prices, updates the wholesale Google Sheet, submits price updates to Amazon Listings API, and runs eBay sync.

## Schedule
- **Cron:** `0 6,18 * * *` (America/New_York)
- **Frequency:** Twice daily at 6:00 AM and 6:00 PM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/update_wholesale_sheet.py
```

## Behavior
- Fetches FBA and FBM inventory levels
- Pulls current offer/competitive prices
- Updates wholesale Google Sheet with current data
- Submits price updates to Amazon Listings API
- Runs eBay listing sync
- Runtime: ~15-20 minutes typical
- Timeout: 1800s

## Error Handling
- On API throttle, implement backoff and retry
- Log partial completions (e.g., "prices updated but eBay sync failed")

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/update_wholesale_sheet.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- Amazon Listings API access
- Google Sheets API
- eBay API credentials
