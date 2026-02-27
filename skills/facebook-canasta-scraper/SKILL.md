# Facebook Canasta Scraper

## Purpose
Scrapes Canasta Facebook groups for strategy content, rotating through one group per run. Saves approved tips to strategy.jsonl for use in email newsletters.

## Schedule
- **Cron:** `30 22 * * *` (America/New_York)
- **Frequency:** Daily at 10:30 PM EST

## Execution
```bash
# Browser-based scraping via OpenClaw browser profile
# Config: ~/.openclaw/workspace/canasta-rules/groups_config.json
# Output: ~/.openclaw/workspace/canasta-rules/strategy.jsonl
```

## Behavior
- Scrapes **ONE group per run**, rotating through groups in order
- Source prefixes: FB (Modern American Canasta), CCG (Canasta Card Game), CL (Canasta Lovers), NYMC (Not Your Mother's Canasta)
- Stop after ~50 posts OR 25 minutes, whichever comes first
- No emails sent — content saved to strategy.jsonl only
- Each entry tagged with source prefix, date, and approval status
- Timeout: 1800s

## Error Handling
- If Facebook login fails, log error and skip run
- If group is inaccessible, rotate to next group
- On timeout, save whatever was collected

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None (passive collection)

## Dependencies
- OpenClaw browser profile (logged into Facebook as Chloe Mercer)
- Config: `~/.openclaw/workspace/canasta-rules/groups_config.json`
- Output: `~/.openclaw/workspace/canasta-rules/strategy.jsonl`
