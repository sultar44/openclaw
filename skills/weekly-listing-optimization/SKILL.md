# Weekly Listing Optimization

## Purpose
Pulls 90 days of order data via SP-API for CA marketplace, computes ideal restock window and average orders per day, and updates the optimization sheet.

## Schedule
- **Cron:** `0 22 * * 0` (America/New_York)
- **Frequency:** Sundays at 10:00 PM EST

## Execution
```bash
# AI-driven task using SP-API
# Pull 90 days orders in 3x 30-day windows
# CA marketplace: A2EUQ1WTGCTBG2
# Update Sheet: 1z7WGoXHJ-k2K72wUmp5VU81h37wKaKyqcf9F5cwy_2s
```

## Behavior
- Pull orders from SP-API in three 30-day windows (90 days total)
- Marketplace: CA (A2EUQ1WTGCTBG2)
- Compute `ideal_window` and `avg_order_per_day` for each SKU
- **IMPORTANT:** Find columns by header NAME, not column index — headers may shift
- Update Google Sheet: `1z7WGoXHJ-k2K72wUmp5VU81h37wKaKyqcf9F5cwy_2s`
- Timeout: 360s

## Error Handling
- On SP-API throttle, retry with backoff
- If sheet structure changed, log warning and skip rather than writing to wrong columns

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- Amazon SP-API credentials (`~/amazon-data/.env`)
- Google Sheets API (service account)
- Sheet ID: `1z7WGoXHJ-k2K72wUmp5VU81h37wKaKyqcf9F5cwy_2s`
