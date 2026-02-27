# Platform Health Council

## Purpose
Comprehensive 9-area audit of the entire OpenClaw platform, cron jobs, code quality, and data integrity. Produces a health scorecard.

## Schedule
- **Cron:** `0 11 * * 1` (America/New_York) — biweekly (skip alternate weeks)
- **Frequency:** Every other Monday at 11:00 AM EST

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

- High-risk items → alert #chloebot immediately
- Produce summary scorecard
- Timeout: 3600s

## Error Handling
- If unable to assess an area, mark as "Unknown" with reason
- Complete all assessable areas even if some fail

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** #chloebot for any Risk-rated items

## Dependencies
- Access to all cron job logs
- Access to `~/amazon-data/` codebase
- Access to `~/.openclaw/workspace/skills/` for skill audit
- Access to `~/amazon-data/amazon.db` for data checks
- OpenClaw CLI for cron/gateway status
