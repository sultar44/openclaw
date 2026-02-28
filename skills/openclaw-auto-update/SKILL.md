# OpenClaw Auto Update

## Purpose
Checks for and installs OpenClaw updates. If updates are found, reads the changelog and proposes business uses for Ramon.

## Schedule
- **Cron:** `15 3 * * *` (America/New_York)
- **Frequency:** Daily at 3:15 AM EST

## Execution
```bash
openclaw gateway update
```

## Behavior
- Runs `openclaw gateway update` to check for and install updates
- If updates installed: read changelog, summarize new features, propose business applications for Ramon considering our current implementation
- If no updates: log clean status and exit
- Timeout: 900s

## Error Handling
- On failure, alert #chloebot immediately
- Log full error output for debugging

## Alerts & Delivery
- **ClickUp task comment:** Status only — "✅ Updated to vX.Y.Z" or "ℹ️ No new update tonight" or "❌ Install failure: [reason]"
- **#chloe-logs (C0AELHCGW4F):** Recommendations only — when there's a new version, post a summary of new features and how they could benefit our business
- **#chloebot (C0AD9AZ7R6F):** Only on critical failure

## Dependencies
- OpenClaw CLI (`openclaw` command)
- Network access for update check
