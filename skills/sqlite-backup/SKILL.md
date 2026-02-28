# SQLite Backup to Google Drive

## Purpose
Auto-discovers SQLite databases, creates encrypted tar backups, uploads to Google Drive with 7-day retention.

## Schedule
- **launchd ID:** com.chloe.sqlite-backup
- **Frequency:** Daily at 2:00 AM EST
- **ClickUp Task:** https://app.clickup.com/t/86ewr929g

## Execution
```bash
/bin/bash /Users/ramongonzalez/.openclaw/workspace/automation/run_sqlite_backup.sh
```

## Behavior
- Wrapper script: `~/.openclaw/workspace/automation/run_sqlite_backup.sh`
- Python script: `~/.openclaw/workspace/automation/sqlite_backup_to_gdrive.py`
- Auto-discovers SQLite databases
- Creates encrypted tar backups
- Uploads to Google Drive
- 7-day retention (old backups pruned)

## Error Handling
- On backup failure, shell script exits with code 1
- Logs to: `~/.openclaw/workspace/backups/logs/sqlite_backup.log`
- launchd stdout/stderr: `~/.openclaw/workspace/backups/logs/sqlite_backup.launchd.{out,err}.log`

## Alerts & Delivery

### Always (every run)
- Post execution comment on ClickUp task (status + summary)
- On success: mark ClickUp task complete (recurring tasks auto-reopen)

### On Partial Failure
- ClickUp task comment + alert to #chloe-logs (C0AELHCGW4F)

### On Critical Failure
- ClickUp task comment + alert to #chloebot (C0AD9AZ7R6F)

### ClickUp Logging Command
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/clickup_integration.py --task 86ewr929g --status <success|partial|critical> --summary "<summary>"
```

## Note
This is a launchd job, not an OpenClaw cron job. Alert hierarchy must be implemented in the shell wrapper script (`run_sqlite_backup.sh`) or monitored externally.

## Dependencies
- `~/.openclaw/workspace/automation/run_sqlite_backup.sh`
- `~/.openclaw/workspace/automation/sqlite_backup_to_gdrive.py`
- `~/.openclaw/workspace/.automation.env`
- Python venv at `~/amazon-data/.venv`
- Google Drive API credentials
- `~/amazon-data/collectors/clickup_integration.py`
- launchd plist: `~/Library/LaunchAgents/com.chloe.sqlite-backup.plist`
