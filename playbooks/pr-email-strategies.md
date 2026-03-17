# PR Email Strategies — Product Placement vs Thought Leadership

Two distinct email strategies for PR outreach. Never mix them.

## How to Determine Lane

- **Product Placement:** Reporter wants product recommendations, gift guides, roundups, "best of" lists. They want THINGS to feature.
- **Thought Leadership:** Reporter wants ideas, expert quotes, insights, trends, advice. They want a SOURCE to interview/cite.

**All Outreach tab emails** = Product Placement (these are cold pitches to existing gift guides).
**Opportunities (HARO/SOS)** = Check the `lane` column. If not set, classify by reading the query:
- Query asks for "products," "recommendations," "gift ideas" → Product Placement
- Query asks for "tips," "advice," "insights," "experts," "quotes," "ideas" → Thought Leadership

---

## Strategy 1: Product Placement (LLM-thin, hardcoded structure)

**Goal:** Get the Canasta Deluxe Game Set featured/listed in the article.
**Tone:** Professional vendor pitch.
**Script:** `pr_email_drafter.py --lane "Product Placement"`

### Structure (hardcoded)
1. `Hi [Name],`
2. **LLM:** Personalized opening (1-2 sentences referencing their specific content)
3. **Hardcoded:** Product intro with full description, price, specs
4. **LLM:** "Why it fits" paragraph connecting product to their audience
5. **Hardcoded:** "What we can offer" bullet list (complimentary set, images, info)
6. **Hardcoded:** Product page + product image links
7. **Hardcoded:** Course link
8. **Hardcoded:** Sign-off

### LLM Provides (3 fields only)
- `personalized_opening` — show you read their content
- `why_it_fits` — connect product to their specific audience/topic  
- `subject_line` — clear, direct (e.g. "For Your Grandmother Gift Guide: Canasta Deluxe Game Set")

### Rules
- Include full product description and price
- Include product page and image links
- Include "What we can offer" section
- OK to sound like a vendor — that's the point

---

## Strategy 2: Thought Leadership (LLM-heavy, expert positioning)

**Goal:** Get Ramon quoted/cited as an expert. Product mention is incidental.
**Tone:** Helpful expert sharing insights. Like replying to a friend's question.
**Script:** `pr_email_drafter.py --lane "Thought Leadership"`

### Structure
1. `Hi [Name],`
2. **LLM:** Hook that addresses the reporter's ACTUAL question/problem (not a product pitch)
3. **Hardcoded:** Brief credibility line ("I run All7s Games and hear about this constantly")
4. **LLM:** 2-3 genuinely useful insights the reporter could quote in their article
5. **Hardcoded:** Soft close ("Happy to share more. Can send a set if you'd like to see it.")
6. **Hardcoded:** Sign-off

### LLM Provides (3 fields, but HEAVIER content)
- `personalized_opening` — address the reporter's actual question. Show you understand their angle. This should sound like a real observation, not a pitch. (2-4 sentences)
- `why_it_fits` — this is the CORE VALUE. 2-3 insight paragraphs or bullet points that the reporter could directly quote. Think "what would make this article better?" not "why should they feature our product." (4-8 sentences)
- `subject_line` — conversational, not salesy. Should read like a reply to a question. (e.g. "Re: 3-gen road trip - the 'end of day' problem")

### Rules
- **NO product descriptions, prices, or spec bullets**
- **NO product page links or image links**
- **NO "What we can offer" section**
- **NO press release language** ("we are pleased to offer," "retails for")
- Mention the product ONCE, casually, as part of a story/insight
- The email should be useful even if the reporter never features the product
- Shorter than Product Placement emails
- Subject line should NOT contain the product name

### Good vs Bad Examples

**BAD (sounds like Product Placement in disguise):**
> I'm the founder of All7s Games, and we make the Canasta Deluxe Game Set - a complete set with premium cards, rotating tray, and point values printed on every card. It retails for $27. When traveling with everyone from teenagers to in-laws, Canasta bridges the generation gap.

**GOOD (sounds like an expert sharing knowledge):**
> Three generations, 5,500 miles, and one question nobody plans for: what do you actually do together at 8 PM in a hotel room in Moab? What we've seen work: bringing a simple card game that grandparents already know. Canasta is the one we hear about most.

### Follow-up Emails (TL)
- Email 2: Add a NEW insight or data point. Stay in expert mode. No product links.
- Email 3: Brief, respectful close. "Loved the concept for this piece. Good luck with it."

---

## Quick Reference

| | Product Placement | Thought Leadership |
|---|---|---|
| Goal | Get product featured | Get Ramon quoted |
| Tone | Professional vendor | Helpful expert |
| Product detail | Full specs + price | One casual mention |
| Links | Product page + image | None |
| "What we can offer" | Yes | No |
| LLM weight | Thin (3 short fields) | Heavy (insight paragraphs) |
| Email length | Longer | Shorter |
| Subject line | Product name OK | Conversational, no product |
