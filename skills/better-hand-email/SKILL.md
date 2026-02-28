# The Better Hand Email

## Purpose
Manages weekly "The Better Hand" newsletter email pipeline: generate draft proposals, review via Mission Control UI, approve to Klaviyo.

## Schedule
- **Cron:** `15 9 * * 3` (America/New_York)
- **Frequency:** Wednesdays at 9:15 AM EST
- **Cron ID:** 339bfde0-3016-4358-a989-4ae7876dbc10
- **ClickUp Task:** 86ewr928u

## Workflow

### Wednesday 9:15 AM — Draft Generation
1. Check `playbooks/better-hand-drafts.jsonl` for current pending count
2. If fewer than 5 pending, generate new drafts to reach 5
3. Pick unused approved strategies from `canasta-rules/strategy.jsonl`
4. Avoid reusing any strategy used in the last 6 months (check `playbooks/better-hand-approved.jsonl`)
5. Write full emails: subject line, preview text, body (~150 words)
6. **Do NOT include P.S.** in draft proposals — P.S. is added automatically on approve
7. Follow humanizer writing rules strictly (no em dashes, no AI tells, natural voice)
8. Notify #mar_marketing (C9T8MAM71) tagging @Ramon with link to review page

### Review — Mission Control UI
- **URL:** http://192.168.68.200:8888/better-hand
- Ramon reviews drafts one at a time, can edit subject/preview/body
- Three actions: Approve, Reject, Skip
- Typically picks 1 per week, remaining carry over to next Wednesday
- Next Wednesday only needs to top up to 5 (replace approved + rejected ones)

### On Approve
1. P.S. is automatically appended based on rotation (not shown in draft)
2. Klaviyo draft campaign is created via API
3. Entry added to `playbooks/better-hand-approved.jsonl` with campaign ID
4. P.S. rotation advances to next type
5. Notify #mar_marketing (C9T8MAM71) that campaign is ready with Klaviyo link

### P.S. Rotation (3-week cycle)
1. **course:** "P.S. Taking our free Canasta course? 500+ players are already in. Start here"
2. **social:** "P.S. We share tips like this every week on Instagram. Come say hi"
3. **engagement:** "P.S. What's your go-to opening strategy? Hit reply and tell us — we read every one."

State tracked in: `playbooks/better-hand-ps-state.json`

### Strategy Reuse Prevention
- All approved emails logged in `playbooks/better-hand-approved.jsonl`
- Do not propose strategies with similar themes to anything approved in the last 6 months
- Vary categories: don't do 3 weeks of the same tag (wilds, discarding, etc.)

## Alert Hierarchy
- **Always:** Comment on ClickUp task (86ewr928u)
- **Partial failures:** ClickUp + #chloe-logs (C0AELHCGW4F)
- **Critical failures:** ClickUp + #chloebot (C0AD9AZ7R6F)
- **Task completion:** #mar_marketing (C9T8MAM71) tagging @Ramon with review link
- **Campaign created:** #mar_marketing (C9T8MAM71) with Klaviyo campaign link

## Email Template Rules
- **Subject:** `The Better Hand: [Topic Hook] 🃏`
- **Preview:** One punchy curiosity line
- **Greeting:** "Hey friend,"
- **Intro:** "Here's this week's Better Hand — one tip to sharpen your game before the weekend."
- **Tip:** Bold question/scenario header + 2-3 short paragraphs
- **Challenge:** "Try this weekend:" one actionable sentence
- **Coupon:** Soft mention of CANASTA10 with Amazon store link
- **Sign-off:** "Warmly, Ramon"
- **P.S.:** Added on approve (not in draft)
- **Humanizer rules:** No em dashes, no AI tells, no hype words, natural voice

## Data Files
- `playbooks/better-hand-drafts.jsonl` — pending/rejected drafts
- `playbooks/better-hand-approved.jsonl` — approved history with Klaviyo campaign IDs
- `playbooks/better-hand-ps-state.json` — P.S. rotation state
- `playbooks/better-hand-email.md` — full playbook/template
- `canasta-rules/strategy.jsonl` — source strategy tips (approved entries only)

## Dependencies
- Mission Control Next.js app (port 8888)
- Klaviyo API (KLAVIYO_API_KEY in ~/amazon-data/.env)
- Humanizer skill rules
