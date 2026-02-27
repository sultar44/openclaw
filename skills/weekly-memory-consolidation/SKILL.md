# Weekly Memory Consolidation

## Purpose
Reviews the past week's daily memory files, promotes important insights to MEMORY.md, and removes outdated entries.

## Schedule
- **Cron:** `0 10 * * 0` (UTC)
- **Frequency:** Sundays at 10:00 AM UTC (5:00 AM EST)

## Execution
```bash
# AI-driven task — reads memory/YYYY-MM-DD.md files from past 7 days
# Promotes insights to ~/.openclaw/workspace/MEMORY.md
# Removes outdated/superseded entries from MEMORY.md
```

## Behavior
- Read all `memory/YYYY-MM-DD.md` files from the past 7 days
- Identify significant decisions, lessons, insights worth long-term retention
- Add to MEMORY.md under appropriate sections
- Remove entries from MEMORY.md that are outdated or no longer relevant
- Timeout: 180s

## Error Handling
- On failure, log — not critical, can run next week
- Never delete memory files, only consolidate from them

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/.openclaw/workspace/memory/` directory
- `~/.openclaw/workspace/MEMORY.md`
