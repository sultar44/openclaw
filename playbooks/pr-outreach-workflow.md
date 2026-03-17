# PR Outreach Workflow (Proactive Gift Guide Pitching)

## Goal
Proactively pitch All7s Canasta Deluxe Set to editors of existing gift guides, product roundups, and "best of" articles. Get included when they refresh their pages.

## How It Differs From HARO/SOS
- **HARO/SOS (Opportunities tab):** Reactive. Editors ask for products, we respond.
- **Outreach tab:** Proactive. We find existing pages and pitch to get added.

The tone is different. These are COLD pitches to editors who didn't ask for us. Keep emails shorter, more value-focused, and lead with why their readers would benefit.

## Sheet
Spreadsheet: `1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc`
Tab: **Outreach**

Columns: Publication, Article Title, Guide URL, Guide Type, Author/Editor, Email, ETV, Last Updated, Expected Update, Pitch Window, Email 1 Date, Email 2 Date, Email 3 Date, Status, Notes

## Shared Resources (same as HARO/SOS)
- **Placements tab** — check before pitching (cooldown: same outlet + same seasonal group within 12 months)
- **Blacklist tab** — skip blocked outlets/keywords
- **ETV threshold** — >= 1,000 to qualify (already filtered during migration)
- **Link strategy** — all7s.co is ALWAYS the primary link. Amazon only when explicitly requested.

## Guide Types
- **seasonal** (spring/summer/fall/holiday) — pages refresh at predictable times each year
- **evergreen** — "Best Card Games", "Best Games for Seniors" — can update any time, estimate same month next year

## Timing Logic
1. **Expected Update** = same month as "Last Updated", next year (or year after if already past)
2. **Pitch Window** = 8 weeks before Expected Update (when Email 1 goes out)
3. **Email 2** = 14 days after Email 1
4. **Email 3** = 14 days after Email 2

**Follow-ups are handled by the daily `pr-followup-check` cron (Mon-Fri 10 AM), NOT the weekly outreach cron.**

## Status Flow
`Queued` → `Ready to Pitch` → `Email 1 Ready` → `Sent 1` → `Email 2 Ready` → `Sent 2` → `Email 3 Ready` → `Sent 3` → `Placed` / `No Response` / `Declined`

**Rules:**
- Chloe sets: `Email X Ready` (never `Sent X`)
- `Sent X` only when Ramon forwards the email (via BCC learning loop)
- `Placed` when the editor confirms inclusion or we verify our product on the page

## Weekly Cron Behavior (Mondays 9 AM)
The weekly outreach cron handles DISCOVERY ONLY:
- **Queued rows entering pitch window** — pitch window just opened → update status to "Ready to Pitch"
- Scan for new guides to add (see pr-discovery.md)

**Follow-ups (Email 1/2/3 drafting) are handled by the daily `pr-followup-check` cron**, which checks both Opportunities AND Outreach tabs Mon-Fri at 10 AM.

## Email Drafting

**ALL PR emails MUST be assembled via `pr_email_drafter.py`.** Same script used for HARO/SOS opportunities.

```bash
cd ~/amazon-data && source .venv/bin/activate
# Email 1 (cold pitch):
python3 collectors/pr_email_drafter.py --type outreach --email-num 1 \
    --outlet "The Strategist (NYMag)" --reporter-name "Arielle" \
    --reporter-email "arielle.avila@nymag.com" \
    --article-title "Best Gifts for Grandmothers" \
    --article-url "https://nymag.com/..." \
    --personalized-opening "..." --why-it-fits "..." --subject-line "..." --send
# Follow-ups:
python3 collectors/pr_email_drafter.py --type outreach --email-num 2 \
    --outlet "..." --reporter-name "..." --reporter-email "..." \
    --personalized-opening "..." --new-angle "..." --subject-line "..." --send
```

**ALWAYS use `--send` flag** to send email directly from the script with perfect formatting.

The LLM generates ONLY: `--personalized-opening`, `--why-it-fits` (Email 1), `--new-angle` (Email 2/3), `--subject-line`.
Everything else (product facts, links, image, sign-off, wrapper) is hardcoded.

**DO NOT compose PR emails in free-form LLM text. Always use pr_email_drafter.py.**

### Email Guidelines (for LLM-generated parts only)
- **Email 1:** Brief compliment about their guide + why our product fits their readers. Keep the personalized parts SHORT.
- **Email 2:** Quick reference to Email 1 + one new angle (testimonial, milestone, data point).
- **Email 3:** Acknowledge they're busy + one compelling social proof. No pressure.
- **Zero em dashes** (the script auto-validates and fixes)
- **Humanizer runs automatically** (the script calls it)

## Pre-Pitch Checks (before drafting any email)
1. Verify the guide URL is still live (quick HEAD request)
2. Check Placements tab for cooldown conflicts
3. Check Blacklist tab
4. Verify email address hasn't bounced (check Notes column)

## Adding New Guides
To add a new guide to the Outreach tab:
1. Find the guide URL
2. Run ETV check: `python3 collectors/pr_domain_checker.py <domain>`
3. If ETV >= 1,000, add the row with all fields populated
4. Research the editor/author contact info
5. Set Guide Type, Last Updated, Expected Update, Pitch Window
6. Status: Queued (or Ready to Pitch if window is already open)

## Discovery
See `playbooks/pr-discovery.md` for the monthly discovery cron (1st Monday, 10 AM EST).

## Article Lifecycle & Re-Pitch Rules

### Status Flow
```
Queued → Ready to Pitch → Email 1 Ready → Sent 1 → Email 2 Ready → Sent 2 → Email 3 Ready → Sent 3 → [outcome]
```

### After 3 Emails with No Response
- Status: "No Response"
- The article goes **dormant**, NOT dead
- Do NOT keep emailing about the same article in the same refresh cycle
- The row stays in the sheet

### Re-Pitch Trigger
When the article gets refreshed/updated (new year's edition, seasonal update):
1. Update the URL, Last Updated, Expected Update, and Pitch Window
2. Reset status to "Ready to Pitch"
3. Draft a NEW 3-email sequence with a fresh angle and subject line
4. This counts as a new cycle

### Exhausted (truly dead)
An article is marked "Exhausted" and permanently retired when:
- 3 emails with no response across **TWO separate refresh cycles** (6 total emails, ~2 years)
- The page returns 404 or is taken down
- The publication shuts down
- The editor explicitly says "not interested, don't contact again"
- The page pivots to an unrelated topic

### Statuses Reference
| Status | Meaning |
|--------|---------|
| Queued | Identified, not yet in pitch window |
| Ready to Pitch | Pitch window is open, draft Email 1 |
| Email 1 Ready | Draft sent to Ramon for review |
| Sent 1 | Ramon sent Email 1 (via BCC loop) |
| Email 2 Ready | Follow-up draft sent to Ramon |
| Sent 2 | Ramon sent Email 2 |
| Email 3 Ready | Final follow-up draft sent to Ramon |
| Sent 3 | Ramon sent Email 3 |
| Replied | Editor responded (Ramon takes over) |
| No Response | 3 emails, no reply. Dormant until next refresh. |
| Closed | Ramon decided not to pursue |
| Exhausted | 2 full cycles with no response. Permanently retired. |
