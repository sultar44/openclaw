# Daily Keyword Rank Collection (DataDive Rank Radar)

## Purpose
Collects daily organic keyword rankings for all tracked ASINs from DataDive's Rank Radar API. This is the source of truth for "where do we rank for X keyword?" — used for PPC decisions, listing optimization, and tracking competitive position.

## Schedule
- **Primary:** Daily at 7:00 AM EST (`0 7 * * *`)
- **Retries:** Every 3 hours if any radar's data isn't ready yet

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/daily_ranks.py
```

## Behavior
- **Auto-discovers radars** — calls DataDive API to get ALL Rank Radars, not a hardcoded list. When you add a new ASIN/marketplace on DataDive, it's automatically picked up on the next run.
- Fetches keyword rankings for the target date (today)
- **Per-ASIN retry logic:** DataDive processes ASINs at different speeds. If ASIN 1 has data but ASIN 2 doesn't yet, the script stores ASIN 1's data immediately and marks ASIN 2 for retry. On the next run (3h later), it only retries the missing ones.
- State tracked in `~/amazon-data/rank_state.json`
- Uses `INSERT OR REPLACE` — safe to re-run
- Timeout: 3600s

## Data Stored
- Table: `keyword_ranking` in SQLite
- Fields: asin, marketplace, date, keyword, search_volume, relevancy, organic_rank, impression_rank
- Raw JSON archived in `~/amazon-data/reports/raw/YYYY-MM/`

## Current Coverage
- Auto-discovered from DataDive — currently 15 radars across US + CA
- ~5,800+ keywords tracked daily across all ASINs

## Error Handling
- Each radar runs independently — one failure doesn't stop the others
- Missing data triggers retry state (checked every 3h)
- Email notification on first incomplete collection

## Alerts & Delivery
- **Success:** ClickUp task comment only (no Slack)
- **Partial (retrying):** ClickUp task comment + alert #chloe-logs (C0AELHCGW4F)
- **Critical failure:** ClickUp task comment + alert #chloebot (C0AD9AZ7R6F)

## Dependencies
- `~/amazon-data/collectors/daily_ranks.py`
- Python venv at `~/amazon-data/.venv`
- DataDive API key (`DATADIVE_API_KEY` in `~/amazon-data/.env`)
- SQLite database: `~/amazon-data/amazon.db`
