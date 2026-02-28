# Drive Skill Sync

## Purpose
Syncs local SKILL.md files to Google Drive nightly so Ramon always has up-to-date copies to review.

## Schedule
- **Cron:** `0 23 * * *` (America/New_York)
- **Frequency:** Daily at 11:00 PM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/drive_skill_sync.py
```

## Behavior
- Compares local SKILL.md modification times against last-sync state
- Uploads only files that changed since last sync
- Creates new Drive folders for any new skills added locally
- State tracked in `memory/drive-sync-state.json`
- Internal (local) files are always the source of truth
- Timeout: 300s

## Error Handling
- If a single file fails to upload, log error and continue with remaining files
- Exit code 1 if any errors occurred (triggers alert)

## Alerts & Delivery
- **Log to:** ClickUp task only (success)
- **Alert to:** #chloebot (C0AD9AZ7R6F) on failure

## Dependencies
- gog CLI (Google Drive access via chloemercer32@gmail.com)
- Drive folder: `1OONVdsIAsCUOy8iKUpj0GFzLzf34KHUY` (skills subfolder)
- Script: `~/amazon-data/collectors/drive_skill_sync.py`
- State: `~/.openclaw/workspace/memory/drive-sync-state.json`
