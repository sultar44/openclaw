# Platform Health Council

## Purpose
Comprehensive 9-area audit of the entire OpenClaw platform, cron jobs, code quality, and data integrity. Produces a health scorecard.

## Schedule
- **Cron:** `every 14d` (America/New_York)
- **Frequency:** Biweekly Mondays at 11:00 AM EST
- **Cron ID:** b8d400c5-1328-45b4-8632-d6ff696bb626
- **ClickUp Task:** https://app.clickup.com/t/86ewr9297

## Execution
```bash
# AI-driven audit task — no single script
# Systematically evaluate all 9 areas below
```

## Behavior
Audit 9 areas, rating each as **Healthy** / **Watch** / **Risk** with evidence:

1. **Cron Health** — Are all scheduled jobs running on time? Failures in last 2 weeks?
2. **Code Quality** — Any scripts with known issues, TODOs, or tech debt?
3. **Test Coverage** — Do critical scripts have tests? Any untested paths?
4. **Prompt Quality** — Are cron job prompts clear, unambiguous, efficient?
5. **Dependencies** — Any outdated packages, expiring API keys, deprecated APIs?
6. **Storage** — Disk usage, database size, log rotation, old files to clean?
7. **Skill Integrity** — Are all SKILL.md files current and accurate?
8. **Config Consistency** — Do .env files, configs, and cron definitions match reality?
9. **Data Integrity** — Any stale data, missing records, or sync gaps in amazon.db?

- Timeout: 3600s

## Error Handling
- If unable to assess an area, mark as "Unknown" with reason
- Complete all assessable areas even if some fail

## Alerts & Delivery

### Always (every run)
- Post execution comment on ClickUp task (status + summary scorecard)
- On success: mark ClickUp task complete (recurring tasks auto-reopen)

### Report Delivery
- **Send health scorecard to:** #chloebot (C0AD9AZ7R6F)

### On Partial Failure
- ClickUp task comment + alert to #chloe-logs (C0AELHCGW4F)

### On Critical Failure
- ClickUp task comment + alert to #chloebot (C0AD9AZ7R6F)

### ClickUp Logging Command
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/clickup_integration.py --task 86ewr9297 --status <success|partial|critical> --summary "<summary>"
```

## Dependencies
- Access to all cron job logs
- Access to `~/amazon-data/` codebase
- Access to `~/.openclaw/workspace/skills/` for skill audit
- Access to `~/amazon-data/amazon.db` for data checks
- `~/amazon-data/collectors/clickup_integration.py`
- OpenClaw CLI for cron/gateway status
