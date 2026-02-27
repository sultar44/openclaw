# Listing Monitor (Monday)

## Purpose
Generates a weekly listing health summary with BSR alerts, strikethrough status, and coupon status. Single consolidated message.

## Schedule
- **Cron:** `0 8 * * 1` (America/New_York)
- **Frequency:** Mondays at 8:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/listing_monitor.py --mode monday
```

## Behavior
- Weekly summary (not change-based like weekday mode):
  - BSR alerts: SKUs with BSR >20% worse than 90-day average
  - SKUs without strikethrough price
  - SKUs without active coupon
- Sends a **single consolidated message** to #all7s-alerts
- Timeout: 600s

## Error Handling
- On Keepa token shortage, skip and log
- On failure, log — can run manually

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** #all7s-alerts (CF9T43YMQ) — single weekly summary message

## Dependencies
- `~/amazon-data/collectors/listing_monitor.py`
- Python venv at `~/amazon-data/.venv`
- Keepa API key (`KEEPA_API_KEY` in `~/amazon-data/.env`)
