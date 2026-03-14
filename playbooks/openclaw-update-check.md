# OpenClaw Update Check Playbook

**Trigger:** Daily cron at 2:28 PM EST  
**Delivery:** `announce` to #chloebot (C0AD9AZ7R6F)  
**Rule:** Always report — either "update available" or "no update today"

## Steps

### 1. Check versions
```bash
INSTALLED=$(openclaw --version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')
LATEST=$(npm view openclaw version 2>/dev/null)
echo "Installed: $INSTALLED"
echo "Latest: $LATEST"
```

### 2a. No update available
If `INSTALLED == LATEST`:
- Reply: `✅ No new OpenClaw update today (v{INSTALLED} is latest)`
- Log to ClickUp as success

### 2b. Update available
If `INSTALLED != LATEST`:
- Get changelog: `npm view openclaw --json` and extract recent changes if available
- Check cron status: `openclaw cron list --json` — note any jobs with `runningAtMs` set
- Reply:
```
🔄 OpenClaw update available: v{INSTALLED} → v{LATEST}

Changelog:
{changelog summary or "Check npm for details"}

{cron status}

Reply "update" to install now, or I'll check again tomorrow.
```
- Log to ClickUp as success

### 3. If Ramon says "update"
```bash
npm update -g openclaw
openclaw gateway restart
```
Confirm new version in chat.

## Notes
- Never auto-install. Always wait for explicit "update" command.
- This job uses `delivery.mode: announce` — just reply normally, no need to call the message tool.
