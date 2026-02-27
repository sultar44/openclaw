# GSC Weekly Report

## Purpose
Generates a Google Search Console report for all7s.co covering key SEO metrics and opportunities.

## Schedule
- **Cron:** `0 9 * * 1` (America/New_York)
- **Frequency:** Mondays at 9:00 AM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/gsc_report.py
```

## Behavior
- Site: all7s.co
- Report sections: overview, quick wins (positions 8-20), winners/losers, CTR opportunities, top pages
- Passive — no alerts, just generates report for review
- Timeout: 120s

## Error Handling
- On GSC API failure, log error
- Non-critical — weekly data is not time-sensitive

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None (passive report)

## Dependencies
- `~/amazon-data/collectors/gsc_report.py`
- Python venv at `~/amazon-data/.venv`
- Google Search Console API credentials
- Site: all7s.co
