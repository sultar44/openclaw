# PR Follow-up Check (Daily Cron)

You are running as a cron job (Mon-Fri) to check for PR opportunities that need follow-up emails.

## Steps

1. Read the PR Opportunities sheet (ID: `1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc`, tab: `Opportunities`)
   - Use service account via: `cd ~/amazon-data && source .venv/bin/activate && python3 -c "..."`
   - Credentials: `~/amazon-data/google_sheets_credentials.json`

2. Check each row for follow-up eligibility:
   - **`Sent 1`** + Last Action Date > 7 days ago → Draft Email 2 (first follow-up), mark as `Draft 2 Ready`
   - **`Sent 2`** + Last Action Date > 7 days ago:
     - If **Source is `SOS`** → Draft Email 3 (final follow-up), mark as `Draft 3 Ready`
     - If **Source is `HARO`** → Auto-close (mark `Closed`, update Last Action Date) - *Safety: Avoid over-pitching HARO*
   - **`Sent 3`** + Last Action Date > 7 days ago → Auto-close (mark `Closed`, update Last Action Date)
   
   **IMPORTANT:** Never mark a row as "Sent X" — only Ramon does that by forwarding the email. Cron jobs set "Draft X Ready" status only.

3. For each follow-up needed:
   a. Read the original row (Outlet, Summary, Reporter Name, Reporter Email, AI Reasoning, Lane)
   b. Draft a follow-up email aligned to the original lane.
   c. **Humanize (MANDATORY)**: Save the draft to a temp file and run through the `humanizer-pro` skill:
      - `node ~/.openclaw/workspace/skills/operator-humanizer/scripts/humanize.js analyze -f /tmp/pr-draft.txt`
      - Fix ALL flagged issues (em dashes, AI vocabulary, patterns)
      - **Specifically check for and remove ALL em dashes (—)** — Ramon's #1 rule
      - Re-run humanizer until clean
   d. Email `ramon@goven.com` with the follow-up package (same format as Email 1).
   e. Post in `#mar_marketing` (C9T8MAM71): "📰 Follow-up [2/3] ready for: [Outlet] - [topic]"
   f. Update Status to `Draft [2/3] Ready` and `Last Action Date` to today.

4. For auto-closed rows:
   - Update Status to `Closed`.
   - Update Last Action Date to today.
   - No notifications needed.

5. If nothing needs follow-up → reply with ONLY: NO_REPLY

## Email Package Format (same as initial)
```
Subject: PR Follow-up [2/3]: [Outlet] - [Brief Topic]

REPORTER: [Name]
EMAIL: [reporter@email.com] (Email to use when forwarding)
OUTLET: [Outlet Name]
FOLLOW-UP: Email [2/3]
ORIGINAL SENT: [date of last action]

--- EMAIL BODY (copy and forward) ---

[Full humanized follow-up draft ready to forward]

--- ORIGINAL REQUEST ---

[Full original query text from the HARO/SOS email]

--- END ---
```

## ClickUp Logging
After completion, log to ClickUp using the integration script:
```bash
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/clickup_integration.py --cron-id pr-followup-check --status success --summary \"Checked X rows, Y follow-ups sent, Z auto-closed\"
```

## Safety
- Never email reporters directly
- Only email ramon@goven.com
- Only update Status and Last Action Date columns
