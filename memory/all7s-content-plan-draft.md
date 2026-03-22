# All7s Games Brand Page Content Plan — DRAFT

*For Ramon's review. Goal: Make @playall7s FB/IG pages look alive, canasta-focused, drive followers + Klaviyo emails. Low maintenance.*

---

## The Reality Check

The canasta niche on social is tiny. #canasta on Instagram is dominated by Spanish-language posts about gift baskets (canasta = basket in Spanish). The card game content is sparse. That's actually GOOD news — low competition means even basic, consistent posting will make All7s the most active canasta brand page out there.

**Key insight:** You don't need to go viral. You need to look like a real, active brand page that someone landing from a Reel thinks "oh, they post real stuff" and hits Follow.

---

## Posting Cadence: 4x/week (FB + IG simultaneously)

| Day | Post Type | Effort Level | Automatable? |
|-----|-----------|-------------|-------------|
| **Monday** | 🃏 Canasta Tip / Rule Explainer | Low (templated image) | ✅ Fully |
| **Wednesday** | 📸 "Game Night" Lifestyle Post | Low (stock/AI image + caption) | ✅ Fully |
| **Friday** | 📰 Better Hand Preview | Low (templated from email) | ✅ Fully |
| **Sunday** | 📖 Sunday Ritual Blog Teaser | Low (templated from blog) | ✅ Fully |

That's 4 posts/week × 2 platforms = 8 posts, all from templates, zero video editing needed.

---

## Post Type Details

### 1. 🃏 Monday: Canasta Tip / Rule Carousel (Most Valuable)

**Why:** Educational content gets saved + shared. People searching "canasta rules" on IG will find these.

**Format:** 3-5 slide carousel (square images, 1080x1080)
- Slide 1: Hook ("Most people play this wrong 🃏")
- Slides 2-4: The tip/rule explained simply
- Last slide: CTA ("Follow @playall7s for weekly Canasta tips")

**Content bank (50+ topics):**
- Basic rules (drawing, melding, going out)
- Scoring guide (point values, bonus canastas)
- Common mistakes
- Strategy tips ("When to freeze the pile")
- Variations (American Canasta vs Classic vs Hand & Foot)
- Glossary terms ("What is a natural canasta?")
- "Did you know?" history facts

**Automation approach:**
- Pre-write 30 tip scripts (text only, I can draft these)
- Template: consistent brand colors, fonts, layout
- Generate images with a Canva template or simple HTML→image script
- Cron posts every Monday

**Example caption:**
"Most new players don't know this: you need TWO natural cards to pick up the discard pile, not one. ♠️♥️

Save this for your next game night 📌

#canasta #cardgames #gamenighttips #playall7s"

---

### 2. 📸 Wednesday: "Game Night" Lifestyle / Community Post

**Why:** Shows the brand's vibe. Makes people imagine themselves at the table.

**Format:** Single image + short caption

**Content ideas (rotating themes):**
- Flat-lay of cards, snacks, wine glasses on a table
- Quote graphics ("The best conversations happen over a card game")
- "Caption this" engagement posts (photo of a crazy hand)
- Poll: "Red threes — love them or hate them?" 
- Throwback/nostalgia: "Who taught you Canasta?"
- Reposts: Customer photos (if/when they come in via UGC)
- Product shots (the Deluxe set in lifestyle settings)

**Automation approach:**
- Build a library of 20-30 lifestyle images (stock photos, product photos, AI-generated later)
- Pre-write captions with engagement questions
- Cron posts every Wednesday

---

### 3. 📰 Friday: Better Hand Preview

**Why:** Cross-promotes the email, drives Klaviyo signups from social followers.

**Format:** Single branded image + caption teasing the email topic

**Template:**
- Image: Simple text-on-brand-background ("This week's Better Hand: [Topic]")
- Caption: 2-3 sentence teaser + "Get it free every Friday → link in bio" or "Comment START"

**Automation:** 
- Pull from Better Hand email subject/topic (already in Klaviyo)
- Generate templated image automatically
- Post same day as email goes out

---

### 4. 📖 Sunday: Sunday Ritual Blog Teaser

**Why:** Drives traffic to blog + email signups. Extends the Sunday Ritual beyond email.

**Format:** Single image (blog header or quote card) + caption excerpt

**Template:**
- Image: Pull the blog header image or generate a quote card from the story
- Caption: 2-3 best sentences from the blog + "Read the full story → link in bio"
- Include: "Want this in your inbox every Sunday? Comment SUNDAY 💌"

**Automation:**
- Already have blog content from the Sunday Ritual pipeline
- Extract excerpt + image → post
- Can hook into the existing Sunday Ritual publisher

---

## What We DON'T Need

- ❌ Video content (Ramon's Reels handle that on the personal pages)
- ❌ Daily posting (4x/week is plenty for a brand page)
- ❌ Stories (low ROI for brand pages, high effort)
- ❌ Manual posting (everything can be API-driven)
- ❌ Reposting viral canasta content (there's almost none — the niche is too small)

---

## Automation Architecture

```
Content Bank (Google Sheet)
    ↓
Cron Job (weekly batch)
    ↓
Image Generator (HTML template → image, or Canva API)
    ↓
Meta Graph API → FB Page + IG Account
    ↓
Track in Content Tracker sheet
```

**What I'd build:**
1. A "Brand Posts" tab in the existing Idea Bank sheet — pre-loaded with 30 Monday tips + 30 Wednesday lifestyle prompts
2. Image generation script (HTML templates rendered to PNG — no Canva needed)
3. A `brand_social_poster.py` script that reads the sheet, generates the image, and posts to both FB/IG
4. A cron job that fires Mon/Wed/Fri/Sun

**Zero LLM cost** — all content pre-written, images templated, posting is pure script.

---

## Content We Need to Create First

Before any automation:
1. **Brand visual template** — colors, fonts, layout for tip carousels + quote cards
   - Suggestion: Use All7s brand colors from the packaging
   - Clean, simple, readable at phone size
2. **First 12 Monday tips** (3 months of content) — I can draft these
3. **First 12 Wednesday image+caption combos** — need product/lifestyle photos
4. **Friday + Sunday** — auto-generated from existing email/blog content (no pre-work needed)

---

## Open Questions for Ramon

1. **Do you have product lifestyle photos?** (the Deluxe set on a nice table, cards laid out, etc.) These would be huge for Wednesday posts and make the page feel real vs stock-photo-generic.

2. **Brand template style preference?** I can mock up 2-3 options:
   - A) Clean/minimal (white background, bold text, brand accent color)
   - B) Warm/cozy (dark wood table background, card imagery, warm tones)
   - C) Playful (bright colors, card suit emojis, fun fonts)

3. **Link in bio strategy:** Right now @playall7s bio link probably goes to all7s.co. Should we use a Linktree-style page with: Course signup | Shop | Blog | Sunday Ritual?

4. **Should brand posts include the "Comment START" CTA too?** Or keep that for Ramon's personal video content only?

---

## Timeline

- **Week 1:** Finalize template + write first 12 Monday tips
- **Week 2:** Build image generator + posting script
- **Week 3:** First automated brand posts go live
- **Ongoing:** I batch-create content monthly, everything posts automatically

---

## Cost

- API: Free (Meta Graph API)
- LLM: Zero (pre-written content, no AI generation per post)
- Ramon's time: ~1 hour upfront (review templates + approve first batch), then ~0 ongoing
