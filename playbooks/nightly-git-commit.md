# Nightly Git Commit — amazon-data

## Purpose
Auto-commit any changed code files in ~/amazon-data nightly so we have version history.

## Steps

1. `cd ~/amazon-data`
2. Check `git status --short` — if no changes, log to ClickUp and exit
3. `git add -A`
4. `git commit -m "nightly auto-commit YYYY-MM-DD"` with today's date
5. Log results to ClickUp task via clickup_integration.py

## Rules
- The .gitignore handles exclusions (db, logs, raw reports, cache, state files)
- Only code/config changes will be committed
- No remote push (local-only repo)
- If commit fails for any reason, alert #chloebot
