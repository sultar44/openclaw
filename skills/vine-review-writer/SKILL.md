# Nightly Vine Review Writer

## Purpose
Processes ALL qualifying rows in the Vine Google Sheet nightly. Reads Amazon product pages and writes review titles + bodies.

## Schedule
- **Cron ID:** `6bcec19f-c884-4638-9934-4933a6462840`
- **Cron:** `40 23 * * *` (America/New_York)
- **Frequency:** Daily at 11:40 PM EST
- **ClickUp Task:** https://app.clickup.com/t/86ewr925x

## Sheet
https://docs.google.com/spreadsheets/d/1Q8XCCCmkll6olnxx-aBrtpAZDttu50phWFJO6hrAalk/edit?gid=0#gid=0

## Qualification Rule
Row qualifies when ALL are true:
- Column F (ASIN) is not blank
- Column S is blank
- Column T is blank
- Column U is blank

## Execution
1. Preflight: Read columns F,S,T,U via Sheets API to find ALL qualifying rows
2. If none qualify, exit with "No qualifying rows"
3. For each qualifying row:
   a. Open Amazon product page: https://www.amazon.com/dp/{ASIN}
   b. Collect product info (title, features, rating)
   c. Write review per playbook rules (one title + one paragraph)
   d. Write Column T (title) and Column U (body) via Sheets API
   e. Verify write succeeded before moving to next row
4. Leave Column S untouched (review date added manually)

## Writing Rules
Follow: `~/.openclaw/workspace/playbooks/product-review-writing.md`

## Self-Heal
- Retry failed browser actions up to 3x
- If still failing, restart gateway once and retry
- If still failing, mark row as failed and continue to next row

## Alert Hierarchy
1. **Always:** Comment on ClickUp task + mark task complete
2. **Partial failure** (some rows failed): ClickUp + #chloe-logs (C0AELHCGW4F)
3. **Critical failure** (no rows processed): ClickUp + #chloebot (C0AD9AZ7R6F)
4. **Success:** ClickUp only, no Slack

## ClickUp Logging
```bash
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/clickup_integration.py --cron-id 6bcec19f-c884-4638-9934-4933a6462840 --status <STATUS> --summary "<SUMMARY>"
```
