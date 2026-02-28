# The Sunday Ritual — Weekly Email + Blog

## Purpose
Multi-phase workflow that drafts "The Sunday Ritual" newsletter email AND companion blog post. Stories about famous people or inspirational themes tied to community, structured play, and women 50+ finding connection.

## Schedule
- **Cron ID:** `345e1a54-8086-4715-a3a9-5b628adf56b6`
- **Cron:** `0 21 * * 4` (America/New_York)
- **Frequency:** Thursdays at 9:00 PM EST
- **ClickUp Task:** https://app.clickup.com/t/86ewr9291

## Playbook
Full writing rules and style guide: `~/.openclaw/workspace/playbooks/sunday-ritual-email.md`

---

## Phase 1: Topic Proposals (Thursday 9 PM — automated)

When the cron triggers:

1. Read `playbooks/sunday-ritual-log.jsonl` to see all previously featured topics
2. Check if there's an existing topic queue in `playbooks/sunday-ritual-topic-queue.jsonl`
3. **If fewer than 10 unused topics in the queue**, research and generate new ideas to bring total back to 10
4. Present the 10 topic ideas to Ramon for approval

### Topic Ideas Format
Post to #all7s-marketing (C9T8MAM71) tagging @Ramon:
```
🃏 Sunday Ritual — Topic Proposals

Pick a topic for this week's email + blog:

1. **Elizabeth Montagu** — The 18th-century hostess who invented the dinner party as social activism
2. **Betty White** — Game show queen who proved play keeps you young
3. [etc... 10 total]

Reply with the number or suggest your own.
```

### Topic Research Guidelines
- **Two pillars:** Famous women + Ritual/community themes
- Target audience: Women 50+, empty nesters seeking social connection
- Core message: Friendship requires effort. Gathering creates meaning.
- The connection to Canasta can be direct (they played) or thematic (they embodied social gathering)
- Prioritize variety: different eras, backgrounds, types of connection
- Verify historical claims before proposing
- Previously used topics are tracked in `sunday-ritual-log.jsonl` — never repeat

### Topic Queue Storage
Maintain approved/pending topics in `playbooks/sunday-ritual-topic-queue.jsonl`:
```json
{"topic": "Betty White", "status": "pending", "added": "2026-02-27", "brief": "Game show queen who proved play keeps you young"}
{"topic": "Julia Child", "status": "used", "added": "2026-02-25", "used_date": "2026-02-26"}
```

---

## Phase 2: Email Draft (after topic approval)

Once Ramon approves a topic:

1. Write the email following the playbook style guide exactly
2. **Humanizer rules apply:** No em dashes, no AI tells, natural human voice
3. Email is ~200-250 words, plain text, no images in email
4. PS rotation: course → social → engagement (check log for last type)
5. Present as 3 editable fields:
   - **Subject line**
   - **Preview text**
   - **Email body**

Post to #all7s-marketing (C9T8MAM71) tagging @Ramon for approval.

---

## Phase 3: Image Research (alongside email draft)

Research and present **5 image links** that could work for the email header and blog article:

1. Search Wikimedia Commons, Unsplash, Pexels, and general web for relevant images
2. Prioritize: public domain > Creative Commons > editorial (note licensing)
3. Present as clickable links with brief descriptions
4. Include 2 blank slots for Ramon to add his own image choices
5. Ramon picks 2 images: 1 main (email + blog header) and 1+ blog inline

### Image Format
```
📸 Image Options for "[Topic]"

1. [URL] — Description (Source: Wikimedia, Public Domain)
2. [URL] — Description (Source: Unsplash)
3. [URL] — Description (Source: Pexels)
4. [URL] — Description (Source: Wikimedia)
5. [URL] — Description (Source: web search)

Your picks (paste URLs):
6. ___
7. ___
```

### Image Specs
- Email header: 600px wide, 3:2 ratio, <100KB, JPG, 72 DPI
- Blog header: 1200px wide, 3:2 ratio, <200KB
- Blog inline: 800-1000px wide, <150KB
- Always verify images with vision before uploading

---

## Phase 4: Blog Draft + Shopify Upload (after email + images approved)

1. Write the blog post (400-600 words, expanded version of email story)
2. Follow blog structure from playbook: hook → deeper story → Canasta connection → closing
3. SEO: Include "Canasta" + topic name in title and first paragraph
4. CTA at bottom: Free beginner course link
5. Download and process approved images to spec
6. Upload images to Shopify via Image Host article (ID: 618201022747)
7. Create blog article as draft on all7s.co with images embedded
8. Notify Ramon that blog draft is ready for review

---

## Phase 5: Publish (after all approvals)

1. Publish blog post on all7s.co (change draft → active)
2. Create Klaviyo email template with approved copy
3. Log to `playbooks/sunday-ritual-log.jsonl`
4. Mark ClickUp task complete

---

## Alert Hierarchy
1. **Always:** Comment on ClickUp task (https://app.clickup.com/t/86ewr9291) with execution summary
2. **Success / notifications:** Post to #all7s-marketing (C9T8MAM71) tagging <@U92L1SVD2>
3. **Partial failure:** ClickUp comment + alert to #chloe-logs (C0AELHCGW4F)
4. **Critical failure:** ClickUp comment + alert to #chloebot (C0AD9AZ7R6F)

## ClickUp Logging (REQUIRED)
After execution completes:
```bash
cd ~/amazon-data && source .venv/bin/activate && python3 collectors/clickup_integration.py --cron-id 345e1a54-8086-4715-a3a9-5b628adf56b6 --status <STATUS> --summary "<SUMMARY>"
```
Status options: `success` | `partial_failure` | `critical_failure`

## Dependencies
- `~/.openclaw/workspace/playbooks/sunday-ritual-email.md` (writing style guide)
- `~/.openclaw/workspace/playbooks/sunday-ritual-log.jsonl` (tracking)
- `~/.openclaw/workspace/playbooks/sunday-ritual-topic-queue.jsonl` (topic pipeline)
- `~/amazon-data/collectors/clickup_integration.py`
- Shopify API (blog post publishing)
- Shopify Image Host article (ID: 618201022747)
- Klaviyo (email send — manual by Ramon or API)
