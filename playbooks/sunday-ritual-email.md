# The Sunday Ritual — Weekly Email + Blog Playbook

## Overview
Weekly Sunday email + blog post for All7s Games. Stories about famous people and their connection to Canasta or card games. Builds brand identity and community feeling.

## Schedule
- **Drafted:** Thursday evening (cron job)
- **Ramon reviews:** Friday/Saturday
- **Blog published:** Saturday or Sunday morning on all7s.co
- **Email sent:** Sunday 10 AM via Klaviyo campaign blast

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
Always: `The Sunday Ritual: [Person or Hook]`

### Preview Text
One curiosity-driven line. Make them want to open it.

### Body (~200-250 words)

1. **Opening hook:** Start with the person or a surprising fact. No preamble.
2. **The story:** 2-3 short paragraphs about the famous person and their connection to Canasta or card games. Keep it conversational, warm, a little nostalgic.
3. **The connection:** One paragraph tying it back to the reader. "Next time you sit down to play, remember..." or "That same feeling of gathering around a table? That's what we're keeping alive."
4. **Blog link:** "Want the full story? We wrote it up on the blog → [link]"
5. **Sign-off:** "Happy Sunday, —The All7s Team"
6. **P.S.:** Rotating (same 3-week cycle as Better Hand):
   - Week 1: Free course link
   - Week 2: Instagram/social link
   - Week 3: "Reply and tell us..." engagement

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
Format: `{"date": "YYYY-MM-DD", "person": "Name", "topic": "Brief description", "ps_type": "course|social|engagement", "blog_url": "...", "email_sent": true}`
