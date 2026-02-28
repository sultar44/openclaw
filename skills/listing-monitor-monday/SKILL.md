# Listing Monitor (Monday Weekly)

## Purpose
Generates a weekly listing health report with BSR alerts, strikethrough status, and coupon status. Single consolidated message sent to #ops_amazon.

## Schedule
- **Cron ID:** `47b38a81-6441-4f7e-b93e-ca1dd5d9f5bc`
- **Cron:** `0 8 * * 1` (America/New_York)
- **Frequency:** Mondays at 8:00 AM EST
- **ClickUp Task:** https://app.clickup.com/t/86ewr9288

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python -u collectors/listing_monitor.py --mode monday
```

## Behavior
- Weekly summary (not change-based like weekday mode):
  - BSR alerts: SKUs with BSR >20% worse than 90-day average
  - SKUs without strikethrough price
  - SKUs without active coupon
- Sends a **single consolidated report** to #ops_amazon (CF9T43YMQ)
- Timeout: 600s

## Error Handling
- On Keepa token shortage, skip BSR section and note in report
- On failure, log to ClickUp with error details

## Alert Hierarchy
1. **Always:** Comment on ClickUp task (https://app.clickup.com/t/86ewr9288) with execution summary
2. **Success:** ClickUp comment only. Send report to #ops_amazon (CF9T43YMQ). No Slack logging.
3. **Partial failure:** ClickUp comment + alert to #chloe-logs (C0AELHCGW4F)
4. **Critical failure:** ClickUp comment + alert to #chloebot (C0AD9AZ7R6F)

## ClickUp Logging (REQUIRED)
After execution completes:
```bash
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/clickup_integration.py --cron-id 47b38a81-6441-4f7e-b93e-ca1dd5d9f5bc --status <STATUS> --summary "<SUMMARY>"
```
Status options: `success` | `partial_failure` | `critical_failure`

## Report Delivery
- **Report destination:** #ops_amazon (CF9T43YMQ)
- **Delivery mode:** announce (via cron delivery config)

## Dependencies
- `~/amazon-data/collectors/listing_monitor.py`
- `~/amazon-data/collectors/clickup_integration.py`
- Python venv at `~/amazon-data/.venv`
- Keepa API key (`KEEPA_API_KEY` in `~/amazon-data/.env`)
