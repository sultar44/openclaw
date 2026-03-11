# OpenClaw Update Check Playbook

**Trigger:** Daily cron at 2:28 PM EST
**Channel:** #chloebot (C0AD9AZ7R6F)
**Rule:** Only alert if there IS an update. Silent (NO_REPLY) if already on latest.

## Steps

### 1. Check for updates
```bash
# Get installed version
INSTALLED=$(openclaw --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')

# Get latest published version
LATEST=$(npm view openclaw version 2>/dev/null)

echo "Installed: $INSTALLED"
echo "Latest: $LATEST"
```

If `INSTALLED == LATEST` → no update available → send "No Openclaw Updates" to #chloebot (C0AD9AZ7R6F) using the message tool, then log to ClickUp as success. Done.

If `INSTALLED != LATEST` → proceed.

### 2. Check cron job status
Before alerting, check if any cron is currently running or starting within 5 minutes:

```bash
openclaw cron list --json
```

- Look for any job with `runningAtMs` set (currently executing)
- Look for any job whose next run is within 5 minutes of now
- Report these in the alert so Ramon can decide timing

### 3. Send alert to #chloebot
Format:
```
🔄 OpenClaw update available: v{INSTALLED} → v{LATEST}

{cron status: running jobs or upcoming in <5 min, or "No cron jobs running or starting soon"}

Reply "update" to install now, or I'll check again tomorrow.
```

### 4. Wait for command
If Ramon replies "update" (or similar affirmative):
```bash
npm update -g openclaw
openclaw gateway restart
```

Then confirm the new version in chat.

If Ramon says no/skip/later → acknowledge and move on.

## Notes
- Never auto-install. Always wait for explicit command.
- The update command is `npm update -g openclaw` followed by `openclaw gateway restart`
