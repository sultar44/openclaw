# Cron Registry Sync Playbook

## Overview
Daily sync of the Cron Registry spreadsheet with live OpenClaw cron state.
Source of truth: Google Sheet `1aPek6nXAht0BYkO5fR-ildJ4u7gnOFSsXMyqjDXMPDQ` (tab: Cron Registry)

## Sheet Columns
A: Job Name | B: Cron ID | C: ClickUp Task ID | D: ClickUp Task URL
E: Schedule (Human) | F: Schedule (Raw) | G: Timezone | H: Status
I: Last Run | J: Last Result | K: Consecutive Errors | L: Retirement Status
M: Objective | N: Outcome | O: Skill.md (Drive Link) | P: Skill.md Proposal
Q: Dependencies | R: Last Synced

## Daily Sync Steps

### 1. Read current state
- Run `openclaw cron list --json` to get all live cron jobs
- Read the Cron Registry sheet (all rows)
- Read `~/amazon-data/collectors/clickup_config.json`

### 2. Update existing rows
For each row in the sheet:
- Match by Cron ID (column B)
- Update: Status (H), Last Run (I), Last Result (J), Consecutive Errors (K), Last Synced (R)
- If cron ID not found in OpenClaw: set Status = "MISSING" 
- Do NOT overwrite: Objective (M), Outcome (N), Skill.md links (O), Dependencies (Q), Retirement Status (L)
  - These are human-managed columns

### 3. Detect new cron jobs
For each cron job in OpenClaw not in the sheet:
- Add a new row with all auto-fillable columns
- Set ClickUp Task URL = "NEEDS TASK"
- Set Retirement Status = "Active"

### 4. Sync clickup_config.json
- Ensure every sheet row with a ClickUp Task ID has a matching entry in clickup_config.json
- If sheet has a newer cron ID (job was recreated), update the JSON

### 5. Self-heal disabled jobs
Before flagging a job as MISSING, check if it exists but is disabled:
```bash
openclaw cron list --json  # only returns enabled jobs
```
Then read `~/.openclaw/cron/jobs.json` directly to find disabled jobs.

For each sheet row where the cron ID is NOT in `cron list` output:
1. Check `~/.openclaw/cron/jobs.json` — is the job there with `enabled: false`?
2. **If disabled (not deleted):**
   - Check the "Retirement Status" column (L). If it says "Retired" or "Intentionally Disabled", skip it.
   - Otherwise, auto-re-enable: `openclaw cron enable <cronId>`
   - Set Status = "ok" in the sheet
   - Add to alert list: "🔄 Re-enabled {job name} — was disabled (likely from gateway recovery)"
3. **If truly deleted (not in jobs.json at all):**
   - Set Status = "MISSING"
   - Add to alert list: "❌ {job name} is deleted. ClickUp task {id} still exists. Needs manual recreation."

### 6. ClickUp overdue detection
For each sheet row with a ClickUp Task ID:
- Check if the ClickUp task has been overdue for 2+ days with no execution comments in that period
- If so, add to alert list: "⏰ {job name} (ClickUp {id}) overdue 2+ days with no recent execution"

### 7. Alert conditions (send to #chloebot C0AD9AZ7R6F)
- Any self-healed (re-enabled) job
- Any truly MISSING/deleted job
- Any job with Consecutive Errors >= 3
- Any ClickUp task overdue 2+ days without execution
- Any new untracked cron job added to sheet (needs ClickUp task)
- If alerts: send ONE consolidated message, not per-job

### 8. Weekly: ClickUp description sync (Thursdays only)
On Thursdays, also update each ClickUp task description with this format:
```
{Objective from column M}

Schedule: {Schedule Human from column E}
Cron ID: {Cron ID from column B}

Skill: {Skill.md link from column O}

Outcome: {Outcome from column N}
```

### 9. ClickUp logging
After sync completes:
```
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/clickup_integration.py \
  --cron-id <THIS_JOB_CRON_ID> --status <STATUS> --summary "<SUMMARY>"
```

## Alert Rules
- Self-healed (re-enabled) job: always alert (informational, confirms auto-fix)
- Truly MISSING/deleted job: always alert (needs manual recreation)
- ClickUp task overdue 2+ days: alert (something stopped running)
- 3+ consecutive errors: alert (include job name and error count)
- New untracked job: alert with "NEEDS TASK" flag
- All clear: silent (ClickUp comment only)

## Intentionally Disabled Jobs (DO NOT re-enable)
- `6ac25d5e` — Nightly OpenClaw Auto-Update (replaced by external LaunchAgent `ai.openclaw.auto-update`)
- Any job with Retirement Status = "Retired" or "Intentionally Disabled" in the sheet

## Notes
- Human-managed columns (M, N, O, P, Q, L) are NEVER overwritten by sync
- The sheet is the source of truth for mappings; clickup_config.json is a local cache
- If a cron ID changes (job recreated), update both sheet and JSON
