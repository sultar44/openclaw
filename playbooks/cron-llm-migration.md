# Cron LLM Migration Plan

## Problem
Every cron job fires an LLM agent session, even when the job is just "run this Python script."
Most script-only jobs use Claude Opus (~$15/M input, $75/M output) to do what a shell script could do alone.

## Architecture

### Current Pattern (wasteful)
```
Cron fires → LLM agent session (Opus) → reads message → runs script → reads output → posts to Slack/ClickUp
```

### Target Pattern (efficient)
```
Cron fires → LLM agent session (Gemini Flash) → runs script → script handles ALL logging/alerts → done
```
Or ideally (if OpenClaw adds shell exec cron):
```
Cron fires → shell exec → script handles everything → done
```

### Key Tools
- **`cron_runner.sh`** — Generic bash wrapper that runs scripts, captures output, logs to ClickUp, alerts Slack on failure. Already used by 18 jobs.
- **`slack_notify.py`** — Direct Slack Bot API posting (no LLM). Reads token from OpenClaw config.
- **`clickup_integration.py`** — Direct ClickUp API posting.

## Migration Status

### Phase 1: Switch to Gemini Flash ✅ (2026-03-18)
Switched 18 safe script-only jobs from Opus/default to gemini-flash.
These all use `cron_runner.sh` which handles ClickUp + Slack natively.

**Switched:**
- SP Report Poller (Hourly)
- Rank Collection Retry
- BSR Check (Sun/Wed 9PM)
- Nightly Drive Skill Sync
- SP Financial Events (Daily 4AM)
- Daily Product Master Sync
- Wholesale Pricing Report (12h)
- Daily Cron Registry Sync
- AWD Inventory Sheet Update
- SP On-Demand: Inventory Planning (7AM)
- Daily Rank Collection
- SP On-Demand: Merchant Listings (8AM)
- SP On-Demand: Sales & Traffic (9AM)
- Buybox Price Checker
- openclaw-update-check
- Weekly Clickup <> Cron Schedule Checker
- Monday Reimbursement Audit
- Weekly Competitor Price Monitor (Wed 8AM)

### Phase 2: Migrate remaining script-only jobs (TODO)
These 10 jobs run scripts but need review because they either:
- Don't use cron_runner.sh (need to add self-logging)
- Have some LLM interpretation after the script runs
- Use browser automation

**To migrate:**
1. **Gmail Inbox Processor** — Has LLM fallback path for unclassifiable emails. Keep Sonnet but ensure deterministic path runs without LLM.
2. **Facebook Canasta Scraper** — Uses LLM to scrape/parse FB content. Genuinely needs LLM, but could use Flash.
3. **Daily Strategy Report** — Needs audit. Does it use cron_runner.sh?
4. **Listing Monitor (Tue-Fri)** — Needs audit. Script may post its own alerts.
5. **Mon/Thu FBA Restock Alert** — Message says "format results as Slack alert" — move formatting into script.
6. **Weekly Reimbursement Reports** — Needs audit.
7. **Monday IDR Portal Check** — Uses browser. Needs LLM for browser control.
8. **Weekly PO Forecast Alert** — Needs audit.
9. **Monthly PR Discovery** — Uses LLM for search/research. Genuinely needs it.
10. **Monthly PR Archive Closed** — Needs audit. Currently on Sonnet.

### Phase 3: New jobs (POLICY)
**All new cron jobs MUST follow this pattern:**
1. Script handles ALL logic, ClickUp logging, and Slack alerts
2. Use `slack_notify.py` for direct Slack posts (no LLM)
3. Use `cron_runner.sh` wrapper OR self-log via `clickup_integration.py`
4. Cron model: `gemini-flash` (unless job genuinely needs LLM reasoning)
5. Use `--no-deliver` flag (script handles its own delivery)

## Cost Impact Estimate
- 18 jobs switched from Opus ($15/$75 per M tokens) to Flash (~$0.10/$0.40 per M)
- Conservative estimate: ~10K tokens per cron run × 18 jobs × varies per day
- **Estimated savings: 80-95% reduction on these 18 jobs**
