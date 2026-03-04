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
3. **Email 2** = 2 weeks after Email 1
4. **Email 3** = 2 weeks after Email 2

## Status Flow
`Queued` → `Ready to Pitch` → `Email 1 Ready` → `Sent 1` → `Email 2 Ready` → `Sent 2` → `Email 3 Ready` → `Sent 3` → `Placed` / `No Response` / `Declined`

**Rules:**
- Chloe sets: `Email X Ready` (never `Sent X`)
- `Sent X` only when Ramon forwards the email (via BCC learning loop)
- `Placed` when the editor confirms inclusion or we verify our product on the page

## Weekly Cron Behavior
Every Monday at 9 AM EST, the outreach cron checks:

1. **Ready to Pitch rows** — pitch window is open, no Email 1 sent yet → draft Email 1, send to Ramon
2. **Sent 1 rows where Email 2 is due** — 2+ weeks since Email 1, no Email 2 sent → draft Email 2, send to Ramon
3. **Sent 2 rows where Email 3 is due** — 2+ weeks since Email 2, no Email 3 sent → draft Email 3, send to Ramon
4. **Queued rows entering pitch window** — pitch window just opened → update status to "Ready to Pitch"

## Email Drafting Rules

### Email 1 (Initial Cold Pitch)
Keep SHORT (150 words max). Structure:
- Brief compliment about their guide (specific, not generic)
- One sentence about what All7s Canasta Deluxe Set is
- Why it fits their readers (match to their audience)
- Offer to send a free set for review
- Direct product page link: https://www.all7s.co/products/canasta-cards-deluxe-game-set
- Attach product image to the draft email (download from: https://www.all7s.co/cdn/shop/files/CANSET_1280x.png)
- Mention "(Product photo attached.)" in the email body
- Sender: ramon@all7s.co (NOT ramon@goven.com)
- Sign-off: "Warmly, Ramon / Founder, All7s Games / all7s.co"

### Email 2 (Follow-up, +2 weeks)
Even shorter. Structure:
- Quick reference to Email 1
- One new angle or piece of value (e.g., customer testimonial, award, sales milestone)
- Reiterate offer to send a set
- all7s.co link

### Email 3 (Final Follow-up, +2 weeks)
Last touch. Structure:
- Acknowledge they're busy
- One compelling data point or social proof
- "Happy to send a set anytime if you'd like to check it out"
- No pressure, leave the door open

### All Emails
- Run through humanizer before sending to Ramon
- Zero em dashes
- Primary link: all7s.co (NEVER default to Amazon)
- Send draft to ramon@goven.com with same format as HARO/SOS drafts
- Include PR spreadsheet link at bottom

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
