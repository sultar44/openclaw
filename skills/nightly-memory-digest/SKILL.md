# Nightly Memory Digest

## Purpose
Extracts important information from daily conversations and writes a structured summary to the daily memory file.

## Schedule
- **Cron:** `0 23 * * *` (America/New_York)
- **Frequency:** Daily at 11:00 PM EST

## Execution
```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/nightly_memory.py
```

## Behavior
- Reads today's conversation history
- Extracts decisions, action items, insights, and important context
- Writes to `~/.openclaw/workspace/memory/YYYY-MM-DD.md`
- **Skip** routine cron outputs, heartbeat responses, and status checks
- Focus on: decisions made, new information learned, tasks completed, pending items
- Timeout: 120s

## Error Handling
- If no meaningful conversations occurred, write minimal entry noting quiet day
- On failure, log error — non-critical job

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- `~/amazon-data/collectors/nightly_memory.py`
- Python venv at `~/amazon-data/.venv`
- Access to conversation history
