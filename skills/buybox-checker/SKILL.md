# Buy Box Checker

## Purpose
Checks Buy Box ownership status for tracked ASINs using Keepa data.

## Schedule
- **Cron:** `0 14 * * *` (America/New_York)
- **Frequency:** Daily at 2:00 PM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/buybox_checker.py
```

## Behavior
- Check `keepa_token_state.json` FIRST — if tokens < 50, wait until tokens replenish
- Fetches Buy Box data from Keepa for tracked ASINs
- Timeout: 600s

## Error Handling
- If insufficient Keepa tokens, delay and retry
- On failure, log error

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/buybox_checker.py`
- Python venv at `~/amazon-data/.venv`
- Keepa API key (`KEEPA_API_KEY` in `~/amazon-data/.env`)
- `keepa_token_state.json` for token availability check
