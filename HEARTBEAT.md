# HEARTBEAT.md

## 🔧 Lightweight Cron Health Check (EVERY heartbeat)
Quick check: run `openclaw cron list --json` (ONE call) and scan for:
- `consecutiveErrors >= 3` → alert #chloebot with job name
- `lastStatus: "error"` on jobs that ran in the last 2 hours → note but don't alert (single errors are normal)
- Any job with `runningAtMs` that's been running > 2x its normal duration → alert #chloebot

**DO NOT** run the full `cron_watchdog.py` script. That's been retired.
**DO NOT** call `openclaw cron runs` for individual jobs. One `list` call is enough.

If nothing looks wrong, move on silently.

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
