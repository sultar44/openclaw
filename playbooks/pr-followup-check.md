# PR Follow-up Check (Daily Cron)

You are running as a cron job (Mon-Fri) to check for PR follow-ups across BOTH tabs.

## Steps

### Part 1: Opportunities Tab (HARO/SOS — 7-day follow-up)

1. Read the PR Opportunities sheet (ID: `1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc`, tab: `Opportunities`)
   - Use service account via: `cd ~/amazon-data && source .venv/bin/activate && python3 -c "..."`
   - Credentials: `~/amazon-data/google_sheets_credentials.json`
   
   **⚠️ ROW TARGETING — MANDATORY VERIFICATION:**
   Row 1 = header. Before writing ANY update to a row, READ BACK that exact row range (e.g. `Opportunities!A40:M40`) and confirm the outlet/reporter name matches the one you intend to update. Do not rely on index math alone — always verify.

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
      - **Link strategy by email number:**
        - Email 1: all7s.co ONLY (SEO backlink is the primary PR benefit)
        - Email 2+: Introduce Amazon link + social proof (1,600+ reviews, 4.7 stars). The drafter handles this automatically.
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

---

### Part 2: Outreach Tab (Cold Pitches — 14-day follow-up)

5. Read the same sheet, tab: `Outreach`
   - Columns: Publication(A), Article Title(B), Guide URL(C), Guide Type(D), Author/Editor(E), Email(F), ETV(G), Last Updated(H), Expected Update(I), Pitch Window(J), Email 1 Date(K), Email 2 Date(L), Email 3 Date(M), Status(N), Notes(O), Cycle(P)

6. Check each row for follow-up eligibility:
   - **`Sent 1`** + Email 1 Date > 14 days ago + Email 2 Date is empty → Draft Email 2, mark as `Email 2 Ready`
   - **`Sent 2`** + Email 2 Date > 14 days ago + Email 3 Date is empty → Draft Email 3, mark as `Email 3 Ready`
   - **`Sent 3`** + Email 3 Date > 14 days ago → Auto-close (mark `No Response`, no notification needed)

   **IMPORTANT:** Never mark a row as "Sent X" — only Ramon does that by forwarding the email.

7. For each Outreach follow-up needed:
   a. Read the row: Publication, Article Title, Guide URL, Author/Editor, Email, Guide Type, Notes
   b. Draft a follow-up email per the outreach playbook rules:
      - **Email 2:** Short. Reference Email 1. One new angle or value-add (customer testimonial, sales milestone, social proof). Reiterate offer to send a set. Amazon link + social proof (1,600+ reviews, 4.7 stars) is included automatically by the drafter.
      - **Email 3:** Final touch. Acknowledge they're busy. One compelling data point. Leave the door open. No pressure.
   c. **Humanize (MANDATORY)**: Same process as Opportunities — run through humanizer, fix ALL issues, zero em dashes.
   d. Email `ramon@goven.com` with the follow-up package:
   ```
   Subject: PR Outreach Follow-up [2/3]: [Publication] - [Article Title]

   EDITOR: [Name]
   EMAIL: [editor@email.com] (Email to use when forwarding)
   PUBLICATION: [Publication Name]
   ARTICLE: [Article Title]
   GUIDE URL: [URL]
   FOLLOW-UP: Email [2/3]
   LAST EMAIL SENT: [Email 1 or 2 date]
   SEND FROM: ramon@all7s.co

   --- EMAIL BODY (copy and forward) ---

   [Full humanized follow-up draft ready to forward]

   --- END ---
   ```
   e. Post in `#mar_marketing` (C9T8MAM71): "📰 Outreach follow-up [2/3] ready for: [Publication] - [Article Title]"
   f. Update Status to `Email [2/3] Ready` (do NOT fill in the Email 2/3 Date — that happens when Ramon sends it via BCC loop)

8. For auto-closed Outreach rows:
   - Update Status to `No Response`
   - No notifications needed

---

### Part 3: New Outreach Emails Due (Pitch Window Check)

9. Also check for Outreach rows where:
   - Status is `Queued` or `Ready to Pitch`
   - Pitch Window date has arrived or passed (today >= Pitch Window)
   - Email 1 Date is empty
   → Draft Email 1 per the outreach playbook, send package to Ramon, mark as `Email 1 Ready`
   → Post in `#mar_marketing`: "📰 New outreach pitch ready for: [Publication] - [Article Title]"

---

## Final Step

10. If nothing needs action across both tabs → reply with ONLY: NO_REPLY

## ClickUp Logging
After completion, log to ClickUp using the integration script:
```bash
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/clickup_integration.py --cron-id pr-followup-check --status success --summary "Opportunities: X follow-ups, Y auto-closed. Outreach: X follow-ups, Y new pitches, Z auto-closed"
```

## Safety
- Never email reporters/editors directly
- Only email ramon@goven.com
- Only update Status columns (never fill in "Sent X" or Email dates — that's Ramon's action via BCC loop)
- All emails must use SEND FROM: ramon@all7s.co
