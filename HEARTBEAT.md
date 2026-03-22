# HEARTBEAT.md

## 🔧 Lightweight Cron Health Check (EVERY heartbeat)
Quick check: run `openclaw cron list --json` (ONE call) and scan for:
- `consecutiveErrors >= 3` → alert #chloebot with job name
- `lastStatus: "error"` on jobs that ran in the last 2 hours → note but don't alert (single errors are normal)
- Any job with `runningAtMs` that's been running > 2x its normal duration → alert #chloebot

**MISSING CRON DETECTION (EVERY heartbeat):**
After the health check above, run this script (ONE call):
```bash
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/cron_missing_checker.py
```
- If output is empty → all good, move on silently
- If output contains alerts → post them to #chloebot immediately
- This compares Cron Registry sheet (Active jobs) against `openclaw cron list` (live jobs)

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
2. If it succeeds → log to memory, move on. **Do NOT trip the circuit breaker.**
3. If it fails (auth error) → immediately alert #chloebot:
   "⚠️ Gmail OAuth token expired. Run `gog auth add` on the Mac mini to re-authenticate."
4. **Only if auth actually fails** (step 3), trip the circuit breaker:
   ```bash
   echo '{"tripped":true,"reason":"oauth-expired-confirmed"}' > ~/.openclaw/hooks/transforms/gmail-circuit-state.json
   ```
5. Also check if the breaker is currently tripped but auth works → reset it:
   ```bash
   echo '{"tripped":false}' > ~/.openclaw/hooks/transforms/gmail-circuit-state.json
   ```

**Note:** gog OAuth moved to Google Production status (permanent tokens, no 7-day expiry). This check is now a safety net, not a weekly expectation.

## Comment Auto-Responder (EVERY heartbeat)
Run the comment auto-responder (no LLM needed, just executes the script):
```bash
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/comment_responder.py
```
- If exit code 0 with no output about replies → move on silently
- If it reports replies sent → post summary to #chloelogs
- If it errors → alert #chloebot

## Other periodic checks (rotate through these)
- Nothing else scheduled yet
