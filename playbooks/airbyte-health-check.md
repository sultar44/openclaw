# Airbyte Health Check Playbook

## Purpose
Daily check of Airbyte Cloud sync health. Runs at 8 AM EST after overnight syncs complete.

## Connections
- **Amazon Ads → BigQuery** (`ads`): PPC entity tables + daily report streams
- **Amazon Seller Partner → BigQuery** (`sp`): Orders, inventory, financials, returns, settlements, listings, feedback

## Procedure

1. Run `python3 ~/amazon-data/collectors/airbyte_api.py check` to get latest job status for both connections

2. For each connection:
   - **succeeded** → log silently to ClickUp task, done
   - **running** → note it, no action needed (still in progress)
   - **failed** → investigate:
     a. Run `python3 ~/amazon-data/collectors/airbyte_api.py jobs <ads|sp> --limit 3` to see recent history
     b. If this is a first-time failure (previous jobs succeeded), trigger a retry: `python3 ~/amazon-data/collectors/airbyte_api.py sync <ads|sp>`
     c. If this is a consecutive failure (2+ in a row), alert #chloebot with the connection name and error pattern
     d. Do NOT auto-retry more than once per day per connection

3. Log results to ClickUp task (see task ID in clickup_config.json)

## Alert Rules
- **Single failure + auto-retry** → silent (just log to ClickUp)
- **Consecutive failures (2+)** → alert #chloebot: "⚠️ Airbyte {connection} has failed {N} consecutive syncs. Last error: {summary}. May need manual investigation."
- **Both connections failed** → alert #chloebot with higher urgency

## ClickUp Task
- Task ID will be added to clickup_config.json after cron creation

## Delivery
- On failure alerts: send to #chloebot (C0AD9AZ7R6F)
- On success: silent (ClickUp only)
