# OpenClaw Cron Scheduler Bug Report

**Version:** 2026.2.15 (also present in 2026.2.3-1)
**Platform:** macOS Darwin 25.2.0 (arm64)
**Node:** v22.22.0

## Summary
Cron jobs with `sessionTarget: "isolated"` and `payload.kind: "agentTurn"` are not executing automatically. The scheduler advances `nextRunAtMs` to the next occurrence without spawning the isolated session or running the job.

## Symptoms
1. Jobs show `enabled: true` with correct schedules
2. When due time passes, `nextRunAtMs` advances to next occurrence
3. No `lastRunAtMs` is set (jobs never execute)
4. `cron action=runs` shows empty `entries: []`
5. No isolated sessions are spawned

## Evidence

### Job State Before Due Time (9:50 AM)
```json
{
  "name": "Rank Collection Retry",
  "schedule": {"kind": "cron", "expr": "0 10,13,16,19,22 * * *"},
  "state": {"nextRunAtMs": 1771254000000}  // 10:00 AM
}
```

### Job State After Due Time (10:08 AM)
```json
{
  "state": {"nextRunAtMs": 1771264800000}  // 1:00 PM - SKIPPED 10 AM
}
```

### Run History
```json
{"entries": []}  // Empty - job never executed
```

## What Works
- `openclaw cron run <jobId>` (CLI manual trigger) executes jobs successfully
- Jobs complete and post to Slack when manually triggered
- `cron action=run` via tool also works

## What Doesn't Work
- Automatic scheduled execution at due time
- Jobs are skipped even after gateway restart

## Configuration
```json
{
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "...",
    "timeoutSeconds": 600
  },
  "delivery": {
    "mode": "announce",
    "channel": "slack",
    "to": "C0AELHCGW4F"
  }
}
```

## Timeline
- **Feb 12-14:** Jobs stopped auto-executing (unclear when exactly)
- **Feb 16 8:42 AM:** Updated from 2026.2.3-1 → 2026.2.15
- **Feb 16 9:00 AM:** SQP Retry + GSC Report skipped
- **Feb 16 10:00 AM:** Rank Collection Retry skipped
- All timestamps advanced without execution

## Logs
```
2026-02-16T12:11:45.806Z [diagnostic] lane task error: error="Error: Unknown model: ollama/llama3.1:8b"
```
(Note: This error appeared earlier but jobs still fail even after fixing to valid model)

## Environment
- Heartbeat model: `anthropic/claude-opus-4-5`
- 15 enabled cron jobs
- All jobs have `wakeMode: "now"`
- Gateway mode: local, bind: lan

## Workaround
Using macOS launchd as fallback scheduler to run Python scripts directly.
