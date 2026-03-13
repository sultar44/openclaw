# The Better Hand - Friday Email Playbook

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

### Body (~150 words, scannable in 60 seconds)

1. **Greeting:** "Hey friend," (warm, consistent)
2. **Intro:** "Here's this week's Better Hand. One tip to sharpen your game before the weekend."
3. **The Tip:** 
   - Bold question or scenario as header
   - 2-3 short paragraphs explaining the strategy
   - Written conversationally, not textbook-y
   - Pull from `canasta-rules/strategy.jsonl` (approved entries only)
4. **"Try this weekend" challenge:** One actionable sentence to test the tip
5. **Coupon:** Soft, natural. Use hyperlinked text, NOT bare URLs.
   - **Format:** `Weekend game night? 10% off with code CANASTA10 at checkout: <a href="https://www.amazon.com/stores/page/EA384EB6-4C8B-4632-96EC-6E899F61B850?maas=maas_adg_E0710C1268F76A7D58406646A7111714_afap_abs&ref_=aa_maas&tag=maas">Shop All7s</a>`
   - **Coupon code:** CANASTA10 (not FRIDAY10, Amazon won't allow FRIDAY10)
   - **Store URL (permanent):** `https://www.amazon.com/stores/page/EA384EB6-4C8B-4632-96EC-6E899F61B850?maas=maas_adg_E0710C1268F76A7D58406646A7111714_afap_abs&ref_=aa_maas&tag=maas`
   - Always include "at checkout" after the code
   - Always hyperlink as "Shop All7s" (never show raw URL to readers)
6. **Sign-off:** "Warmly, Ramon"
7. **P.S.:** Rotating (see below)

### P.S. Rotation (3-week cycle, ALL reply-only, no links)
Better Hand emails use their 1 allowed link for the Amazon store CTA. No room for course or social links.
1. **Story:** "P.S. Got a Canasta story that still makes you laugh? Reply and tell us. We collect the best ones."
2. **Strategy:** "P.S. What's your go-to opening strategy? Hit reply and tell us. We read every one."
3. **Feedback:** "P.S. Did last week's tip change anything at your table? Reply and tell us. We love hearing what works."

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
