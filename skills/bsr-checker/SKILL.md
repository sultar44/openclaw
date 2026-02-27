# BSR Checker

## Purpose
Fetches Best Sellers Rank from Keepa API for Overstock ASINs and updates the wholesale sheet. Alerts when items are ready to ship.

## Schedule
- **Cron:** `15 6,18 * * *` (America/New_York)
- **Frequency:** Twice daily at 6:15 AM and 6:15 PM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/bsr_checker.py
```

## Behavior
- Fetches BSR from Keepa for all Overstock ASINs
- Only writes BSR to column O if BSR < 400,000
- If column P1 = 'Ship', send alert to #chloebot with shipping message
- Keepa token rate: 5 tokens/minute — monitor consumption
- Timeout: 14400s (4 hours — large ASIN lists may take time)

## Error Handling
- Check `keepa_token_state.json` before starting — if tokens < 50, wait
- On Keepa rate limit, pause and retry
- Log ASINs that failed to fetch

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** #chloebot when P1='Ship' (shipping-ready items)

## Dependencies
- `~/amazon-data/collectors/bsr_checker.py`
- Python venv at `~/amazon-data/.venv`
- Keepa API key (`KEEPA_API_KEY` in `~/amazon-data/.env`)
- Google Sheets API
- `keepa_token_state.json` for token tracking
