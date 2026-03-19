# The Better Hand - Friday Email Playbook

## Overview
Weekly Friday email for All7s Games subscribers. Strategy tip + soft coupon + rotating P.S.

## Schedule
- **Drafted:** Wednesday evening (cron job)
- **Sent:** Thursday 9 AM in recipient's local timezone via Klaviyo campaign
- **Drafted to:** Slack #chloebot for Ramon's approval

### Klaviyo Campaign Setup (automated, scheduling is manual)
When creating the campaign via API, set:
- `send_strategy.method`: `"static"`
- `send_strategy.options.is_local`: `true` (recipient's local timezone)
- `send_strategy.options.send_past_recipients_immediately`: `true`
- `send_strategy.datetime`: next upcoming Thursday at `09:00:00` (format: `YYYY-MM-DDTHH:MM:SS`)
- Assign template via **POST `/api/campaign-message-assign-template`**

**DO NOT auto-schedule.** Do not call `POST /api/campaign-send-jobs`. Ramon reviews and schedules himself. Time is pre-set.

## Email Structure

### Subject Line
Always: `The Better Hand: [Topic Hook] 🃏`

### Preview Text
One punchy line that creates curiosity. Never generic.

### Format: Plain Text Only (Updated March 4, 2026)
- **No HTML at all.** Plain text emails only.
- Klaviyo template: set `text` field only. Include minimal HTML wrapper for email clients that require it, but content is plain text.
- **Font size: 20px** (Georgia serif, 1.5 line height). Applies to all Better Hand and Sunday Ritual emails.
- No bold, no links with anchor text. Use bare URLs.
- No images, logos, or social icons.

### Writing Style (ALWAYS run through humanizer before presenting to Ramon)
- Use clear, simple language. Short sentences. Active voice.
- **No em dashes.** Use periods, commas, or colons instead.
- No metaphors or cliches.
- No hype adjectives or unnecessary adverbs.
- No wrap-up phrases like "in conclusion."
- Banned words: just, really, very, literally, actually, discover, unlock, delve, embark, groundbreaking, harness, illuminate, unveil.
- Write like a real person talking to a friend. Not like AI.
- Vary sentence length. Some short. Some a bit longer to keep rhythm natural.

### Body — USE TEMPLATE (hardcoded via render_email.py)

**DO NOT manually write the greeting, intro, coupon, sign-off, or P.S.**
All of those are hardcoded in `templates/better-hand.txt` and rendered by `templates/render_email.py`.

**You only supply 3 things:**
1. **title** — Bold question or scenario as header for the strategy tip
2. **body** — 2-3 short paragraphs explaining the strategy (conversational, not textbook-y). Pull from `canasta-rules/strategy.jsonl` (approved entries only)
3. **challenge** — One actionable "try this weekend" sentence

**Rendering:**
```bash
python3 templates/render_email.py better-hand \
  --title "Your Title Here" \
  --body "Your body paragraphs here" \
  --challenge "Your challenge sentence here" \
  --ps-index N  # 0=story, 1=strategy, 2=feedback (rotate weekly)
```

The template handles: Klaviyo personalization tag, intro line, coupon code + Amazon URL, sign-off, and P.S. rotation. These are locked. Do not regenerate them.

### P.S. Rotation (hardcoded in render_email.py, 3-week cycle)
- 0: Story prompt (reply-only)
- 1: Strategy prompt (reply-only)
- 2: Feedback prompt (reply-only)

### Unsubscribe Tag (MANDATORY — added Mar 18, 2026)
Every email MUST end with `{% unsubscribe %}` as the last line after the P.S.
This is Klaviyo's built-in unsubscribe tag. Do NOT rely on Klaviyo to auto-add it (they add it in HTML format which doesn't match our plain text style).

### What to Skip
- Product images
- Multiple CTAs
- Salesy language
- The coupon as the focus

## Strategy Tip Selection
1. Check `playbooks/better-hand-log.jsonl` for previously used strategy IDs
2. Pick an unused approved entry from `canasta-rules/strategy.jsonl`
3. Prefer variety in categories (don't do 3 weeks of "wilds" in a row)
4. Mix Facebook community insights (FB*) with tips doc entries (TT-S*)

## Tracking
All sent emails logged in `playbooks/better-hand-log.jsonl`
