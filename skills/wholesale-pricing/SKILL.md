# Wholesale Pricing & eBay Sync

## Purpose
Updates the wholesale Google Sheet with inventory/pricing data, applies price/inventory changes, and syncs quantities to eBay. Reads FBA inventory from SQLite (populated by daily_collection at 5:30 AM) instead of hitting SP-API directly.

## Schedule
- **Cron:** `0 6 * * *` (America/New_York)
- **Frequency:** Daily at 6:00 AM EST (runs after daily_collection at 5:30 AM)

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/update_wholesale_sheet.py
```

## Behavior (in order)
1. Load wholesale product list from base CSV
2. **Read FBA inventory from SQLite** (`inventory_snapshot` table — populated by `daily_collection.py` at 5:30 AM). Falls back to SP-API if SQLite data unavailable. FBM inventory still fetched from listings API.
3. **eBay quantity sync** (runs immediately after inventory fetch — highest priority step)
   - Updates existing eBay listing quantities
   - Creates new eBay listings for FBM SKUs not yet on eBay
4. Fetch offer prices from SP-API → `MY_PRICE`, `BUYBOX_PRICE`, `LOWEST_FBA`, `LOWEST_FBM`
5. Update wholesale Google Sheet (`1Hc6PBFrSBbAYmtbN_xo0r-DZ6wiDS19bsAKmva_7Q1s`, "Overstock" tab)
6. Read column M (`New Price`) → submit price changes to Amazon Listings API
7. Read column N (`New Inventory`) → submit inventory adjustments to Amazon

- Runtime: ~15-20 minutes typical
- Timeout: 1800s

## Data Flow
```
daily_collection (5:30 AM) → inventory_snapshot (SQLite)
                                    ↓
wholesale_pricing (6:00 AM) ← reads inventory from SQLite (no SP-API call for FBA)
                            ← reads FBM inventory from listings API
                            → eBay sync
                            → Google Sheet update
                            → Price/inventory changes to Amazon
```

## Error Handling
- eBay sync runs before pricing steps so partial failures don't block it
- On API throttle, implement backoff and retry
- Log partial completions (e.g., "prices updated but eBay sync failed")

## Alerts & Delivery
- **Success:** ClickUp task comment only (no Slack)
- **Partial failure:** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/update_wholesale_sheet.py`
- `~/amazon-data/collectors/ebay_sync.py`
- `~/amazon-data/collectors/ebay_client.py`
- `~/amazon-data/collectors/daily_collection.py` (must run first — 5:30 AM)
- Python venv at `~/amazon-data/.venv`
- Amazon SP-API credentials (`~/amazon-data/.env`)
- eBay API credentials (`EBAY_CLIENT_ID`, `EBAY_CLIENT_SECRET`, `EBAY_REFRESH_TOKEN` in `~/amazon-data/.env`)
- Google Sheets API (service account)
- SQLite database: `~/amazon-data/amazon.db` (inventory_snapshot table)
