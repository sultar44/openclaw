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

Threshold: **>= 70 → draft package.** Below 70 → ignore.

## Email Drafting Rules

### Standard Links (include where appropriate in all drafts)
- Website: https://all7s.co
- Amazon product: https://www.amazon.com/dp/B07KBB1WJS?th=1&psc=1
- Free Canasta course: https://canastacourse.com

### PR Spreadsheet Link (include at bottom of every draft email to Ramon)
- https://docs.google.com/spreadsheets/d/1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc/edit?gid=0#gid=0

### Product Placement Lane
- Lead with the Canasta Deluxe Set ($26 on Amazon)
- Mention: women 50+ audience, brain health + social connection angle
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

Columns (existing): Date, Source, Outlet, Summary, Reporter Name, Reporter Email, AI Score, AI Reasoning, Status, Thread ID, Last Action Date

Additional columns to append if missing: Lane, Follow-up Due

### Status Values
- `Draft 1 Ready` — row added, email package sent to Ramon
- `Sent 1` — Ramon forwarded Email 1 to reporter
- `Sent 2` — Ramon forwarded Email 2 (follow-up 1)
- `Sent 3` — Ramon forwarded Email 3 (follow-up 2)
- `Replied` — Reporter responded (Ramon takes over)
- `Closed` — Rejected by Ramon or abandoned after 3 attempts

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
- **HARO Follow-up Policy**: For HARO specifically, we will ONLY send one follow-up (Sent 2) if no response. Do not send Sent 3 for HARO sources to avoid spam flagging.
- Use OpenClaw's native LLM for scoring/drafting.
