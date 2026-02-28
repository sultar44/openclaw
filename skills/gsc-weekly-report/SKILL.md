# GSC Weekly Report

## Purpose
Generates a Google Search Console report for all7s.co covering key SEO metrics and opportunities.

## Schedule
- **Cron:** `0 9 * * 1` (America/New_York)
- **Frequency:** Mondays at 9:00 AM EST
- **Cron ID:** ae40885b-880e-47f4-aa4c-f6c743dd6fbe
- **ClickUp Task:** https://app.clickup.com/t/86ewr928h

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/gsc_report.py
```

## Behavior
- Site: all7s.co
- Report sections: overview, quick wins (positions 8-20), winners/losers, CTR opportunities, top pages
- Timeout: 120s

## Error Handling
- On GSC API failure, log error
- Non-critical — weekly data is not time-sensitive

## Alerts & Delivery

### Always (every run)
- Post execution comment on ClickUp task (status + summary)
- On success: mark ClickUp task complete (recurring tasks auto-reopen)

### Report Delivery
- **Send GSC report to:** #mar_marketing (C9T8MAM71)

### On Partial Failure
- ClickUp task comment + alert to #chloe-logs (C0AELHCGW4F)

### On Critical Failure
- ClickUp task comment + alert to #chloebot (C0AD9AZ7R6F)

### ClickUp Logging Command
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/clickup_integration.py --task 86ewr928h --status <success|partial|critical> --summary "<summary>"
```

## Dependencies
- `~/amazon-data/collectors/gsc_report.py`
- `~/amazon-data/collectors/clickup_integration.py`
- Python venv at `~/amazon-data/.venv`
- Google Search Console API credentials
- Site: all7s.co
