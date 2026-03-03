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

## Weekly Gmail OAuth Health Check (every Monday)
If it's Monday and you haven't checked today:
1. Run `gog gmail labels list` 
2. If it succeeds → log to memory, move on
3. If it fails (auth error) → immediately alert #chloebot:
   "⚠️ Gmail OAuth token expired. Run `gog auth add` on the Mac mini to re-authenticate."
4. Also trip the circuit breaker preemptively to prevent webhook runaway:
   ```bash
   echo '{"tripped":true,"reason":"preemptive-oauth-expired"}' > ~/.openclaw/hooks/transforms/gmail-circuit-state.json
   ```

**Why:** OAuth tokens expire every 7 days while gog is in Google "Testing" status. This catches it before the webhook storm hits.

## Other periodic checks (rotate through these)
- Nothing else scheduled yet
