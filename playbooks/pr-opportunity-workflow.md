# PR Opportunity Workflow (HARO + Source of Sources)

## Goal
Triage PR leads from HARO and Source of Sources emails. Score for All7s Games fit, draft outreach emails, and send packages to Ramon for manual forwarding.

## Intake Sources
- `haro@helpareporter.com` (Help A Reporter Out)
- `peter@sourceofsources.com` (Source of Sources)
- `peter@shankman.com` (Source of Sources, same person)

## Trigger
Gmail Pub/Sub webhook intercepts emails from the above senders in `gmail-security.js` transform. Routed to session `hook:gmail:haro-sos:<messageId>` with this playbook.

## Parsing
Each HARO/SOS email contains multiple query blocks. Parse each one individually:
- Query/topic summary
- Reporter name
- Reporter email
- Outlet name
- Deadline (if given)
- Category

## Blacklist Filters (from Sheet → Blacklist tab)
Skip queries matching:
- **Keywords:** crypto, blockchain, sexually, cbd
- **Outlets:** Famadillo
- **Categories:** Biotech and Healthcare, Business and Finance, Technology, Beauty and Wellness, Health and Pharma

## Classification Lanes
Each parsed query is classified into one of three lanes:

1. **Product Placement**
   - Gift guides, product roundups, products for seniors/women 50+, family activities, board games, brain games, game nights
2. **Thought Leadership / Story**
   - Isolation after 50, loneliness, friendship, social connection, community building, routines/rituals, aging well, empty nesting, cognitive activity, women's social lives
3. **Ignore**
   - Everything else (irrelevant categories, no audience fit)

## Scoring Rubric (0-100)
- Audience fit (women 50+, seniors, empty nesters): 0-30
- Topic fit (games/community/friendship/isolation/ritual): 0-30
- Outlet relevance/quality: 0-20
- Actionability (clear ask + deadline + contact): 0-20

Threshold: **>= 70 → proceed to domain quality check.** Below 70 → ignore.

## Domain Quality Gate (ETV Check)

After a query scores >= 70, check the outlet's domain quality BEFORE drafting:

1. Extract the outlet domain from the query
2. Run: `cd ~/amazon-data/collectors && python3 pr_domain_checker.py <domain>`
3. This calls DataForSEO Labs (~$0.01/lookup) and returns Estimated Monthly Traffic (ETV)

**Rules:**
- **ETV >= 1,000** → Qualifies. Proceed to draft email.
- **ETV < 1,000** → Skip. Do NOT create a row. Do NOT draft an email. Silent skip.
- If the domain can't be resolved or has no data → skip (assume too small)
- **Exception:** If the outlet syndicates to a major platform (MSN, Yahoo, etc.), it qualifies regardless of its own domain ETV. Check the syndication target's ETV instead.

Log the ETV value in the sheet's "ETV" column for qualifying opportunities.

## Placement Cooldown Check

After ETV passes, check the Placements tab for cooldown conflicts BEFORE drafting:

1. Run: `cd ~/amazon-data/collectors && python3 pr_placement_checker.py <domain> "<guide type>"`
2. This checks the Placements tab for same outlet + same seasonal guide group within the last 12 months.

**Seasonal groups** (queries in the same group are considered duplicates):
- **spring:** spring, easter, mother's day
- **summer:** summer, father's day, graduation
- **fall:** fall, back to school, halloween, thanksgiving
- **holiday:** holiday, christmas, winter, black friday
- **general:** reviews, roundups, features (non-seasonal)

**Rules:**
- **BLOCKED** → Same outlet + same seasonal group within 12 months = skip silently. No row, no draft.
- **CLEAR** → Proceed to draft email.
- Same outlet + DIFFERENT seasonal group = fine (e.g. ConsumerQueen Spring 2026 → ConsumerQueen Holiday 2026 is OK)

**When a row status changes to "Replied":**
1. Add entry to the Placements tab: Date, Outlet, Domain, Reporter, Guide Type, Notes
2. This ensures future queries against the same outlet+season are caught

Script: `~/amazon-data/collectors/pr_placement_checker.py`

## Email Drafting Rules

### Link Strategy (IMPORTANT - backlink priority)
The #1 goal of every PR email is to earn backlinks to **all7s.co**, not Amazon.

**Link hierarchy:**
1. **Primary (always include):** https://all7s.co — this is our website, our Shopify store, and where we want backlinks pointed
2. **Secondary (mention only):** Amazon — only include if the reporter explicitly asks for an Amazon/marketplace link, or if the guide format requires a marketplace buy link. Use: https://www.amazon.com/dp/B07KBB1WJS?th=1&psc=1
3. **Course link:** https://canastacourse.com — include when relevant (note: this builds Kajabi's domain, not ours)

**"Where can I buy it?"** → all7s.co (it IS a store, they can buy there)
**Reporter says "Amazon link only"** → provide Amazon link
**Gift guide with buy links** → all7s.co product page as primary, "also available on Amazon" as secondary
**Default in all drafts** → all7s.co featured prominently, Amazon mentioned casually if at all

**Why:** all7s.co has zero domain authority. Every quality backlink from an editorial site builds the foundation for organic traffic. Amazon.com (DA ~96) doesn't need our backlinks. We're building all7s.co's authority now so that when the $60 premium set launches and we turn on Meta ads, the site already has SEO traction.

**In practice:** When drafting emails, weave in "learn more at all7s.co" or "visit us at all7s.co" naturally. If including a product link, use the all7s.co product page URL rather than the Amazon listing URL.

### Sender Email
- **Always send from:** ramon@all7s.co (brand recognition, credibility)
- **NOT from:** ramon@goven.com (editors don't know Goven, weakens brand connection)
- Include "SEND FROM: ramon@all7s.co" in every draft package to Ramon

### PR Spreadsheet Link (include at bottom of every draft email to Ramon)
- https://docs.google.com/spreadsheets/d/1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc/edit?gid=0#gid=0

### Product Image (ALWAYS include in email body)
- Include this URL in the draft body so Ramon can easily add the image:
  https://cdn.shopify.com/s/files/1/0828/1692/5979/files/canasta_ffbb7786-59c7-451b-81f2-f03824363710.png?v=1772579041
- Format in draft as: "Product image: [URL]" so Ramon can set it as an inline image when forwarding
- This saves Ramon from searching for the image every time

### Product Placement Lane
- Lead with the Canasta Deluxe Set ($26 at all7s.co)
- Mention: women 50+ audience, brain health + social connection angle
- Link to all7s.co product page, NOT Amazon
- Offer to send a complimentary set for review
- Include product images/links if requested
- Keep concise, professional, warm

### Thought Leadership Lane
- Lead with Ramon's expertise: founder of All7s Games, focused on social connection for women 50+.
- **Core Narrative**: Friendship requires effort, and gathering creates meaning. The physical product is a "gateway" to a shared ritual.
- **Key Insight**: Canasta is a strict 4-player game. Once a "table tribe" forms and sets a weekly date, not showing up isn't an option because the group can't play without you. This creates forced consistency and deep friendship.
- Mention the "Before and After" stories of customers finding community.
- Mention the free Canasta course (canastacourse.com) as the tool that removes the "objection to sitting down" (the learning curve).
- Position Ramon as a source/expert, NOT as a product pitch.
- Offer availability for interview/quotes.

### Follow-up Emails (all lanes)
- Reference the original email specifically
- Shorter than Email 1
- Add one new angle or piece of value
- Professional but not pushy

## Output: Email Package to Ramon
For each qualifying opportunity, send an email to `ramon@goven.com` with:

```
Subject: PR Opportunity: [Outlet] - [Brief Topic]

REPORTER: [Name]
EMAIL: [reporter@email.com] (Email to use when forwarding)
OUTLET: [Outlet Name]
DEADLINE: [date or "none specified"]
LANE: [Product Placement / Thought Leadership]
SCORE: [X/100]

WHY THIS FITS:
[2-3 sentence rationale]

SUGGESTED SUBJECT LINE:
[subject line to use when forwarding]

--- EMAIL BODY (copy and forward) ---

[Full draft email ready to forward]

--- ORIGINAL REQUEST ---

[Full original query text from the HARO/SOS email]

--- END ---
```

## Sheet Logging
Sheet ID: `1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc`
Tab: `Opportunities`
Service account: `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`

**Row insertion order: NEWEST ON TOP.** Always insert new rows at row 2 (right under the header). Push existing rows down. This keeps the most recent opportunities visible at the top.

Columns: Date, Source, Outlet, Summary, Reporter Name, Reporter Email, AI Score, AI Reasoning, Status, Last Action Date, Lane, Follow-up Due, ETV

### Status Values
- `Draft 1 Ready` — Chloe drafted Email 1, sent package to Ramon
- `Sent 1` — Ramon forwarded Email 1 to reporter (set via BCC learning loop)
- `Draft 2 Ready` — Chloe drafted follow-up Email 2, sent package to Ramon
- `Sent 2` — Ramon forwarded Email 2 to reporter (set via BCC learning loop)
- `Draft 3 Ready` — Chloe drafted follow-up Email 3, sent package to Ramon (SOS only)
- `Sent 3` — Ramon forwarded Email 3 to reporter (set via BCC learning loop)
- `Replied` — Reporter responded (Ramon takes over)
- `Closed` — Rejected by Ramon or abandoned after 3 attempts

**RULE:** Chloe ONLY sets "Draft X Ready" statuses. "Sent X" is ONLY set via the BCC learning loop when Ramon actually forwards the email.

## Slack Notification
Post in `#mar_marketing` (C9T8MAM71) when a package is sent:
"📰 PR opportunity sent to your inbox: [Outlet] — [brief summary of why it fits]"

## Silent Mode
If an edition has **zero qualifying opportunities** → no email, no Slack, no notification of any kind.

## Follow-up Cron (Monday-Friday)
A cron job checks the Opportunities sheet (Mon-Fri at 10 AM EST):
- Rows with `Sent 1` and Last Action Date > 7 days ago → draft Email 2, send package to Ramon, post in #mar_marketing
- Rows with `Sent 2` and Last Action Date > 7 days ago → draft Email 3 (SOS only), send package to Ramon, post in #mar_marketing
- Rows with `Sent 3` (SOS) or `Sent 2` (HARO) and Last Action Date > 7 days ago → mark `Closed` (abandoned)

## BCC Learning Loop
Ramon will BCC chloemercer32@gmail.com when he sends a pitch to a reporter. When I receive a BCC'd pitch email:
1. **Study the email** — analyze Ramon's tone, structure, talking points, and what he changed from my draft
2. **Update the pitch database** — note patterns, preferred language, successful angles in memory
3. **Update the sheet** — find the matching row by reporter email/outlet and advance the status:
   - If currently `Draft 1 Ready` → set to `Sent 1`
   - If currently `Sent 1` → set to `Sent 2`
   - If currently `Sent 2` → set to `Sent 3`
   - Update `Last Action Date` to today

## Learning from Rejections
When Ramon marks a row `Closed` without ever sending, I should note the pattern in memory. Over time this refines scoring accuracy.

## Post-Processing: Archive Email
After fully processing a HARO/SOS email (or BCC learning loop email), **archive it** from Chloe's inbox:
```
gog gmail modify <messageId> --remove-labels INBOX
```
This keeps the inbox clean so Ramon can spot unprocessed emails (failure detection).

## Safety + HARO Caution (IMPORTANT)
- **Never email reporters directly** — all drafts go to ramon@goven.com
- **No hardcoded API keys**
- **Tread Lightly with HARO**: HARO (Help A Reporter Out) is aggressively banning/shadowbanning accounts suspected of using AI for pitches. They use AI detection tools like Pangram.
- **Humanization Requirement**: Before sending any draft package to Ramon, the draft MUST be run through the `humanizer-pro` skill to remove AI patterns and sound authentic.
- **Em Dash Ban (CRITICAL)**: ALL text must have ZERO em dashes (—). This includes the email body, subject lines, suggested subject lines, wrapper text, and the email package subject sent to Ramon. Check EVERYTHING, not just the body. Use hyphens (-) or rewrite.
- **HARO Follow-up Policy**: For HARO specifically, we will ONLY send one follow-up (Sent 2) if no response. Do not send Sent 3 for HARO sources to avoid spam flagging.
- Use OpenClaw's native LLM for scoring/drafting.
