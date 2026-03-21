# The Sunday Ritual — Weekly Email + Blog Playbook

## Overview
Weekly Sunday email + blog post for All7s Games. Stories about famous people and their connection to Canasta or card games. Builds brand identity and community feeling.

## Schedule (Automated Pipeline)
- **Ramon selects topic** from dashboard (192.168.68.200:8888/sunday-ritual)
- **Auto-trigger:** Signal watcher cron (every 2 min) detects selection
- **Auto-publish:** LLM writes content → `sunday_ritual_publisher.py` publishes blog + schedules Klaviyo campaign
- **Notification:** Summary posted to #chloebot with blog URL and campaign details
- **No approval needed.** Ramon fixes after the fact if something is off.
- **Email sent:** Sunday 10 AM in recipient's local timezone via Klaviyo campaign
- **Date logic:** Publisher auto-picks the Sunday AFTER the last logged campaign date (never overlaps existing campaigns)

### Klaviyo Campaign Setup (automated, scheduling is manual)
When creating the campaign via API, set:
- `send_strategy.method`: `"static"`
- `send_strategy.options.is_local`: `true` (recipient's local timezone)
- `send_strategy.options.send_past_recipients_immediately`: `true`
- `send_strategy.datetime`: next upcoming Sunday at `10:00:00` (format: `YYYY-MM-DDTHH:MM:SS`)
- After creating the template, assign it via **POST `/api/campaign-message-assign-template`**

**DO NOT auto-schedule.** Do not call `POST /api/campaign-send-jobs`. Ramon reviews the campaign and schedules it himself in Klaviyo. The send time is pre-set so he only needs to click Schedule.

## Writing Style (Humanizer Rules — apply to ALL content)
- Use clear, simple language. Short sentences. Active voice.
- **No em dashes.** Use periods or commas instead.
- No metaphors or cliches.
- No hype adjectives or unnecessary adverbs.
- No wrap-up phrases like "in conclusion."
- Banned words: just, really, very, literally, actually, discover, unlock, delve, embark, groundbreaking, harness, illuminate, unveil.
- Write like a real person talking to a friend. Not like AI.
- Vary sentence length. Some short. Some a bit longer to keep rhythm natural.

---

## Email Structure (plain text, no images)

### Subject Line
Always: `The Sunday Ritual #N: [Person or Hook]`

**N = issue number.** Increment by 1 each week. Check `playbooks/sunday-ritual-log.jsonl` for the last issue number used. If the log is empty, start at 1.

**IMPORTANT:** The `#N` numbering is for the Klaviyo **campaign name only** (internal tracking). The actual **email subject line** that customers see must NOT include the number. Example:
- Campaign name: `The Sunday Ritual #5: Eleanor Roosevelt and the Monday Night Circle`
- Email subject: `The Sunday Ritual: Eleanor Roosevelt and the Monday Night Circle`

Previously sent:
- #1: Julia Child (Mar 2)
- #2: Eva Gabor (Mar 8)
- #3: Betty White (Mar 16)
- #4: Lucille Ball (Mar 23)
- #5: Dolly Parton (Mar 22)

### Preview Text
One curiosity-driven line. Make them want to open it.

### Body — USE TEMPLATE (hardcoded via render_email.py)

**DO NOT manually write the greeting, blog link line, sign-off, or P.S.**
All of those are hardcoded in `templates/sunday-ritual.txt`, `render_email.py`, AND `sunday_ritual_publisher.py`.

**Locked email order (DO NOT rearrange):**
1. `Hey {{ person.first_name|default:'friend' }},`
2. Body text (LLM-written)
3. `Read the full story on our blog →` (linked to blog URL)
4. `Warmly,` / `Ramon`
5. P.S. (engagement question)

**Sign-off is always "Warmly, Ramon".** Not "Happy Sunday," not "Best," not anything else.

**You only supply 2 things:**
1. **body** — The full story (~200-250 words). Opening hook, the story (2-3 paragraphs), and the connection paragraph. Conversational, warm, a little nostalgic.
2. **blog_url** — The published blog post URL on all7s.co

**Preferred method: use `sunday_ritual_publisher.py` directly.** It handles rendering, publishing, and campaign creation in one call.

```bash
python3 ~/amazon-data/collectors/sunday_ritual_publisher.py publish \
  --person "Person Name" \
  --subject-hook "Person Name and the Hook Title" \
  --preview "Preview text" \
  --email-body-file /tmp/sr_email_body.txt \
  --blog-html-file /tmp/sr_blog_body.html \
  --tags "canasta, person name, etc"
```

The publisher handles: Klaviyo personalization tag, blog link line, sign-off ("Warmly, Ramon"), and P.S. rotation. These are locked. Do not regenerate them.

### P.S. Rotation (hardcoded in render_email.py, 5-week cycle)
**Reply-engagement questions ONLY. No links. No socials.**
Business socials (playall7s) are dormant. Do not send anyone there until Ramon says otherwise.
We're trying to land in Gmail Primary, not Promotions. Links in P.S. hurt that goal.

- 0: "What does your Sunday ritual look like?"
- 1: "Do you have a regular game night? Or has it been a while?"
- 2: "Who taught you to play cards?"
- 3: "What's the one game that always comes out when friends visit?"
- 4: "Ever had a game night that turned into something unforgettable?"

All prompt replies to Ramon. Rotate weekly. Never repeat back-to-back.

### What to Skip
- Images in the email
- Product pitches (this is pure brand/story, no coupon)
- Long intros or throat-clearing

---

## Blog Post Structure (published on all7s.co)

### Format
- **Title:** Same as email subject or slightly expanded
- **Image:** One royalty-free or Creative Commons photo at top (of the person or era)
- **Length:** 400-600 words (expanded version of the email story)
- **Sections:**
  1. The hook (same as email)
  2. The deeper story (more detail, quotes if available, historical context)
  3. The Canasta connection (how this ties to the game, the era, the culture)
  4. Closing thought (warm, reflective, ties to community)
- **SEO:** Include "Canasta" + person's name in title and first paragraph
- **CTA at bottom:** "Want to learn Canasta? Start with our free beginner course → [link]"

### Image Sourcing
- Wikimedia Commons (public domain preferred)
- Unsplash / Pexels for era-appropriate lifestyle shots
- Always note the suggested image and source in the draft for Ramon to approve

---

## Topic Selection
1. Check `playbooks/sunday-ritual-log.jsonl` for previously used people
2. Research and pick a new famous person with a Canasta or card game connection
3. Prioritize variety: actors, politicians, musicians, historical figures
4. The connection to Canasta can be direct (they played) or thematic (they embodied the social gathering spirit)

### Starter Ideas (not yet used)
- Eva Gabor (known Canasta player in Hollywood)
- Lucille Ball (card game enthusiast)
- The Rat Pack (card nights in Vegas)
- Queen Elizabeth II (royal card games)
- Frida Kahlo (card games in Mexican culture)

---

## Tracking
All sent emails logged in `playbooks/sunday-ritual-log.jsonl`
Format: `{"issue": N, "date": "YYYY-MM-DD", "person": "Name", "topic": "Brief description", "ps_type": "course|social|engagement", "blog_url": "...", "email_sent": true}`

**Always include `issue` number.** This is the source of truth for the next issue number.
