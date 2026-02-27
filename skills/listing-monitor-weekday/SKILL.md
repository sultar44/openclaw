# Listing Monitor (Weekday)

## Purpose
Monitors Amazon listings for critical changes using Keepa data. Alerts only on meaningful changes, not static state.

## Schedule
- **Cron:** `0 8 * * 2-5` (America/New_York)
- **Frequency:** Tuesday through Friday at 8:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/listing_monitor.py --mode weekday
```

## Behavior
- Uses Keepa data to detect listing changes
- **Alert ONLY on changes**, not static conditions:
  - Category changed
  - Strikethrough price disappeared
  - Coupon disappeared
- Timeout: 600s

## Error Handling
- On Keepa token shortage, skip and log
- On failure, log — next run will catch changes

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** #all7s-alerts (CF9T43YMQ) — only when changes detected

## Dependencies
- `~/amazon-data/collectors/listing_monitor.py`
- Python venv at `~/amazon-data/.venv`
- Keepa API key (`KEEPA_API_KEY` in `~/amazon-data/.env`)
