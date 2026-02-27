# The Better Hand — Friday Email Playbook

## Overview
Weekly Friday email for All7s Games subscribers. Strategy tip + soft coupon + rotating P.S.

## Schedule
- **Drafted:** Wednesday evening (cron job)
- **Sent:** Friday morning via Klaviyo campaign blast
- **Drafted to:** Slack #chloebot for Ramon's approval

## Email Structure

### Subject Line
Always: `The Better Hand: [Topic Hook] 🃏`

### Preview Text
One punchy line that creates curiosity. Never generic.

### Writing Style (Humanizer Rules — apply to ALL written content)
- Use clear, simple language. Short sentences. Active voice.
- **No em dashes.** Use periods or commas instead.
- No metaphors or cliches.
- No hype adjectives or unnecessary adverbs.
- No wrap-up phrases like "in conclusion."
- Banned words: just, really, very, literally, actually, discover, unlock, delve, embark, groundbreaking, harness, illuminate, unveil.
- Write like a real person talking to a friend. Not like AI.
- Vary sentence length. Some short. Some a bit longer to keep rhythm natural.

### Body (~150 words, scannable in 60 seconds)

1. **Greeting:** "Hey friend," (warm, consistent)
2. **Intro:** "Here's this week's Better Hand — one tip to sharpen your game before the weekend."
3. **The Tip:** 
   - Bold question or scenario as header
   - 2-3 short paragraphs explaining the strategy
   - Written conversationally, not textbook-y
   - Pull from `canasta-rules/strategy.jsonl` (approved entries only)
4. **"Try this weekend" challenge:** One actionable sentence to test the tip
5. **Coupon:** Soft, natural — "Weekend game night? 10% off with code CANASTA10 at checkout → [Shop All7s](https://www.amazon.com/stores/page/EA384EB6-4C8B-4632-96EC-6E899F61B850?maas=maas_adg_E0710C1268F76A7D58406646A7111714_afap_abs&ref_=aa_maas&tag=maas)"
   - **Coupon code:** CANASTA10 (not FRIDAY10 — Amazon won't allow FRIDAY10)
   - **Store URL (permanent):** `https://www.amazon.com/stores/page/EA384EB6-4C8B-4632-96EC-6E899F61B850?maas=maas_adg_E0710C1268F76A7D58406646A7111714_afap_abs&ref_=aa_maas&tag=maas`
   - Always include "at checkout" after the code
6. **Sign-off:** "Warmly, Ramon"
7. **P.S.:** Rotating (see below)

### P.S. Rotation (3-week cycle)
1. **Course:** "P.S. Taking our free Canasta course? 500+ players are already in. Start here → [course link]"
2. **Social:** "P.S. We share tips like this every week on Instagram. Come say hi → [IG link]"
3. **Engagement:** "P.S. What's your go-to opening strategy? Hit reply and tell us — we read every one."

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
