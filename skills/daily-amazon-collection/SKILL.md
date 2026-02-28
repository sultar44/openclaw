# Daily Amazon Data Collection

## Purpose
Single source of truth for FBA inventory and order data. Pulls from Amazon SP-API for US and CA, stores in SQLite. Other jobs (wholesale, restock) read from SQLite instead of hitting SP-API.

## Schedule
- **Cron:** `30 5 * * *` (America/New_York)
- **Frequency:** Daily at 5:30 AM EST (runs before wholesale job at 6:00 AM)

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_collection.py
```

## Behavior
Two isolated tasks (failure in one does not stop the other):

### Task 1: FBA Inventory (overwrite, no history)
- Fetches ALL ASINs via FBA Inventory API (US + CA)
- Deletes existing rows for today's date, then inserts fresh
- Point-in-time data — overwrites daily, no historical accumulation
- Enriches with FC transfer/processing data from Planning report
- Table: `inventory_snapshot` (one row per ASIN per marketplace)
- **This is the single source of truth** — wholesale job reads from here

### Task 2: Orders (60-day lookback, full overwrite)
- Fetches last 60 days of individual orders via SP-API report (US + CA)
- Deletes existing orders in the date range, then inserts fresh
- **Why 60 days:** Captures the full refund window. A sale today gets pulled immediately; if the customer returns within 2 months, the updated order status (refund) gets captured on subsequent runs.
- Captures: order ID, ASIN, SKU, quantity, item price, item/order status, fulfillment channel, shipping state/city, purchase date
- Table: `orders_daily` (keyed on order_id + sku + marketplace)
- Future use: reimbursements, refund rate tracking, A2X replacement

### Important
- Does NOT pull Sales/Traffic (`daily_sales.py` — separate cron)
- Does NOT pull PPC/Ads (`daily_ppc.py` — separate cron)
- These are intentionally separate to isolate API failures

## Data Flow
```
daily_collection (5:30 AM) → inventory_snapshot (SQLite)
                            → orders_daily (SQLite)

wholesale_pricing (6:00 AM) ← reads inventory_snapshot from SQLite (no API call)
restock_calculator          ← reads inventory_snapshot + sales_daily
```

## Alerts & Delivery
- **Success:** ClickUp task comment only (no Slack)
- **Partial failure:** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/daily_collection.py`
- `~/amazon-data/collectors/sp_api_client.py`
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
