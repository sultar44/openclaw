# Buy Box Price Checker

## Purpose
Fetches current Buy Box *prices* for tracked ASINs using Keepa data and updates the "Por Vender" sheet.

## Schedule
- **Cron:** `0 14 * * *` (America/New_York)
- **Frequency:** Daily at 2:00 PM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/buybox_checker.py
```

## Behavior
- Check `keepa_token_state.json` FIRST — if tokens < 50, wait until tokens replenish
- Fetches current Buy Box *price* (not ownership) from Keepa for tracked ASINs
- Updates "Por Vender" tab, column D ("Hoy") in sheet `1Q8XCCCmkll6olnxx-aBrtpAZDttu50phWFJO6hrAalk`
- Timeout: 600s

## Error Handling
- If insufficient Keepa tokens, delay and retry
- On failure, log error

## Alerts & Delivery
- **Successful completion:** ClickUp task comment only (no Slack alerts)
- **Partial completion:** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/buybox_checker.py`
- Python venv at `~/amazon-data/.venv`
- Keepa API key (`KEEPA_API_KEY` in `~/amazon-data/.env`)
- `keepa_token_state.json` for token availability check
