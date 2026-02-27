# HEARTBEAT.md

## 🔧 Cron Watchdog (EVERY heartbeat)
Run the watchdog script to detect and recover missed cron jobs:

```bash
cd ~/amazon-data && source .venv/bin/activate && python collectors/cron_watchdog.py --run
```

This script:
- Gets all cron jobs from OpenClaw
- Calculates when each should have last run
- Compares to actual `nextRunAtMs` 
- If a job was skipped (nextRunAtMs too far ahead), runs it with `--force`

If any jobs are recovered, alert #chloebot and post ClickUp comments:
"🔄 Cron Watchdog recovered X missed job(s): [names]"

**Skip if:** Last watchdog ran < 30 minutes ago (check `memory/heartbeat-state.json`)

## Daily Cron Audit (once per day, early morning)
If it's between 5:00-6:00 AM EST and you haven't audited today:
1. Run `cron action=list` to get all jobs
2. For each enabled job, run `cron action=runs jobId=X` 
3. Count runs in the last 2 hours
4. If any job has >10 runs in 2 hours → it's runaway:
   - Alert Ramon in #chloebot with job name and run count
   - Disable the job: `cron action=update jobId=X patch={"enabled": false}`
5. Log audit completion to memory/YYYY-MM-DD.md

## Other periodic checks (rotate through these)
- Nothing else scheduled yet
