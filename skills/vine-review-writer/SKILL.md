# Vine Review Writer

## Purpose
Processes one qualifying row from the Vine Google Sheet and writes a neutral Amazon product review (title and body).

## Schedule
- **Cron:** `40 23 * * *` (America/New_York)
- **Frequency:** Daily at 11:40 PM EST

## Execution
```bash
# Reads from Google Sheet: 1Q8XCCCmkll6olnxx-aBrtpAZDttu50phWFJO6hrAalk
# Writes review title to column T, review body to column U
# Prefer Google Sheets API (service account) over browser
```

## Behavior
- Process **ONE row** per run
- Qualification: Column F has an ASIN, columns S/T/U are all blank
- Review tone: neutral Amazon reviewer — no hype, no superlatives, no AI tells
- Write review title to column T, review body to column U
- Preferred writer identity: `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`
- Timeout: 1500s

## Error Handling
- Self-heal: retry up to 3x on API failure
- After 3 failures, restart the OpenClaw gateway and retry once more
- If no qualifying rows found, log and exit cleanly

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None

## Dependencies
- Google Sheets API (service account credentials)
- Sheet ID: `1Q8XCCCmkll6olnxx-aBrtpAZDttu50phWFJO6hrAalk`
- Playbook: `~/.openclaw/workspace/playbooks/product-review-writing.md`
