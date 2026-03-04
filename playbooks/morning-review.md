# Morning Self-Heal Review

## Trigger
Cron job runs daily at 6:00 AM EST.

## Steps

1. Run the morning review script:
   ```bash
   cd ~/amazon-data && source .venv/bin/activate && python3 collectors/morning_review.py --json
   ```

2. Parse the JSON output. If `clean` is true → log success to ClickUp and stop.

3. If issues found, handle each category:

### Auto-fixable (transient errors)
These are rate limits, timeouts, connection resets. For each:
- Check if the source cron/script has run successfully SINCE the error (look at ClickUp task status or re-run check)
- If it recovered on its own → log as "self-healed" and move on
- If it's still failing → re-run the script once. If it succeeds, log recovery. If not, escalate.

### Needs attention (non-transient)
These require actual investigation:
- **Auth failures** (SMTP, API keys) → Cannot auto-fix. Alert #chloebot immediately.
- **Script errors** (Python exceptions, import errors) → Read the error, check the source file, attempt fix if obvious (missing import, wrong path, etc). If fix applied, re-run to verify.
- **Data issues** (empty results, unexpected formats) → Check if upstream data source changed. Alert #chloebot with details.
- **Unknown errors** → Alert #chloebot with full context for Ramon to review.

4. Post summary to ClickUp task as a comment.

5. If any criticals found, also message #chloebot:
   "🔥 Morning Review found {N} critical issues: [brief list]"

## ClickUp
Task ID: (to be assigned)

## Logging
The morning review itself should log to the event logger:
```python
from event_logger import log_info, log_error
log_info("morning_review", "Review complete: 0 errors, 0 criticals")
```

## Integration Guide
To add logging to any existing script, add to the top:
```python
import sys
sys.path.insert(0, '/Users/ramongonzalez/amazon-data/collectors')
from event_logger import log_info, log_warn, log_error, log_critical
```

Then sprinkle `log_error("script_name", "what happened", {"context": "here"})` at failure points.
Priority scripts to instrument first:
- daily_ppc.py
- daily_ranks.py  
- email_util.py
- bsr_checker.py
- retry_wrapper.sh (log before/after retries)
