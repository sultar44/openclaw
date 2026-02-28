# Git Auto-Sync

## Purpose
Auto-commits and pushes workspace changes to git daily.

## Schedule
- **launchd ID:** com.chloe.git-autosync
- **Frequency:** Daily at 11:10 PM EST
- **ClickUp Task:** https://app.clickup.com/t/86ewr929p

## Execution
```bash
/bin/bash /Users/ramongonzalez/.openclaw/workspace/automation/run_git_autosync.sh
```

## Behavior
- Wrapper: `~/.openclaw/workspace/automation/run_git_autosync.sh`
- Core script: `~/.openclaw/workspace/automation/git_autosync.sh`
- Auto-commits any uncommitted workspace changes
- Pushes to remote

## Error Handling
- On git failure, shell script exits with code 1
- Logs to: `~/.openclaw/workspace/backups/logs/git_autosync.log`
- launchd stdout/stderr: `~/.openclaw/workspace/backups/logs/git_autosync.launchd.{out,err}.log`

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
cd ~/amazon-data && source .venv/bin/activate && python collectors/clickup_integration.py --task 86ewr929p --status <success|partial|critical> --summary "<summary>"
```

## Dependencies
- `~/.openclaw/workspace/automation/run_git_autosync.sh`
- `~/.openclaw/workspace/automation/git_autosync.sh`
- `~/.openclaw/workspace/.automation.env`
- `~/amazon-data/collectors/clickup_integration.py`
- Git configured with remote access
- launchd plist: `~/Library/LaunchAgents/com.chloe.git-autosync.plist`
