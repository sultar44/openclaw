# Daily Strategy Report

## Purpose
Generates a report of pending strategy entries for Ramon to review on the website.

## Schedule
- **Cron:** `0 7 * * *` (America/New_York)
- **Frequency:** Daily at 7:00 AM EST

## Execution
```bash
cd ~/.openclaw/workspace && python canasta-rules/manage_strategy.py report
```

## Behavior
- Generates report of pending/unapproved strategy entries from strategy.jsonl
- No emails — Ramon reviews on website
- Timeout: 300s

## Error Handling
- On failure, log error — non-critical

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/.openclaw/workspace/canasta-rules/manage_strategy.py`
- `~/.openclaw/workspace/canasta-rules/strategy.jsonl`
