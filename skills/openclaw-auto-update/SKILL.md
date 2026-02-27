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
- Runs `gateway.update.run` to check for and install updates
- If updates installed: read changelog, summarize new features, propose business applications for Ramon
- If no updates: log clean status and exit
- Timeout: 900s

## Error Handling
- On failure, alert #chloebot immediately
- Log full error output for debugging

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** #chloebot on failure

## Dependencies
- OpenClaw CLI (`openclaw` command)
- Network access for update check
