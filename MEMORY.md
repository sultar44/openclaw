# MEMORY.md — Long-Term Memory

*Curated insights, not raw logs. Updated periodically.*

---

## Ramon — The Essentials

- Analytical, systems-oriented, values clarity over speed
- Running All7s Games mostly solo (one employee handles Amazon PPC)
- Main bottleneck: time and bandwidth
- Before any resource commitment → needs clear reason, small test, measurable result

## Family Dates to Remember

| Date | Event |
|------|-------|
| Jan 16 | Gianna's birthday |
| Feb 17 | Yamaris's birthday |
| Aug 1 | Ramon's birthday |
| Aug 21 | Julian's birthday |
| Nov 7 | Wedding anniversary |

**Critical:** Julian (son) is allergic to eggs, milk, and nuts.

## All7s Games — Strategic Focus

- **Only brand being actively grown** — all others are restock-only
- **Audience:** Women 50+, empty nesters, seeking social connection
- **Core message:** Friendship requires effort. Gathering creates meaning.
- **Funnel:** Social content → Free Canasta course (Kajabi) → Email list (Klaviyo) → Products

### 2026 Priorities
1. Grow email list via free Canasta course
2. Build consistent social presence
3. Launch $60 premium Canasta set (Q4)
4. Start building player community

### Future Product Ideas (not yet built)
- AI scoring app (photo → score)
- Local game table finder/community

## Content Rules

- **No em dashes anywhere** — Ramon is firm on this
- **All blog/script content must run through humanizer skill before Ramon reviews**
- Humanizer tool: `node skills/operator-humanizer/scripts/humanize.js analyze -f <file>`
- **Message chunking**: Split responses over 800 characters into multiple messages (Slack crops)

## Email Strategy

### Better Hand (Friday, strategy email)
- Coupon code: CANASTA10 (permanent)
- Store URL: Amazon storefront with attribution tag
- Sign-off: "Warmly, Ramon"
- **Better Hand #1 performance: 48.68% open rate, 6.58% CTR** — excellent baseline
- **PS rotation: reply-only prompts** (story/strategy/feedback). No links. Amazon CTA uses the 1 allowed link.
- Brand socials are "playall7s" (FB/IG/TT/YT) but dormant. Video content going to "Ramon Gonzalez" personal pages per agency advice.

### Sunday Ritual (Sunday, community/story email)
- Stories about women who built connection on purpose
- Two pillars: Famous women (15 figures) + Ritual themes (15 topics)
- **No selling** — this is the community email
- Plain text HTML only (Georgia 20px, 1.5 line height, no images/logos)
- PS rotation: 3/5 reply prompts, 2/5 with one link (builds Gmail reputation)
- Sender: "Ramon from All7s" <hello@all7s.co>
- Multi-phase workflow: Thu draft → Ramon review → revisions → publish blog + Klaviyo
- Evergreen flow (not campaigns) — each subscriber gets #1 first, then weekly

### Course Link (Updated Mar 7, 2026)
- **Use all7s.co/courses** (NOT canastacourse.com) for all blog CTAs and links going forward

### Deliverability Rules (all relationship emails)
- **Plain text only. No HTML at all.** (Updated March 4, 2026)
- **Font size: 20px** (Georgia serif, 1.5 line height) for all emails
- No Klaviyo templates, no images/logos/social icons
- No bold, no anchor-text links. Bare URLs only.
- Minimize links (1 content link + unsubscribe)
- Klaviyo personalization: `{{ person.first_name|default:'friend' }}`

## Klaviyo API Notes
- Can't create flows via API (UI-only)
- Can't PATCH campaign-owned templates (create standalone + assign)
- Can't schedule campaigns via API (UI-only)

## Infrastructure & Integrations

### ClickUp
- **Task ID auto-recognition:** Any string matching `86ewr*` or `86ewt*` = ClickUp task ID → look up in `clickup_config.json` → `task_to_cron` to resolve cron job name + UUID. No prefix needed from Ramon.
- All 25+ cron jobs tracked as tasks in ClickUp (list 901816342276)
- Integration script auto-posts comments and marks complete
- ClickUp is Ramon's source of truth for cron job status

### Google Drive Sync
- Skills + scripts synced nightly to Drive for Ramon's review
- Internal files are source of truth; Drive stays current
- Service account: `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`

### Gmail Hook Security
- Tiered routing: `@goven.com`/`@all7s.co` → trusted session; all others → untrusted (restricted)

### #thoughts Channel (C08P1NQBXK8)
- Ramon posts → Chloe creates ClickUp task in list 25307274 ("Ramon's Tasks")
- Links get researched/summarized; plain text saved as-is
- Reacts with 👀 to confirm

### Cron Job Rules
- Runaway/duplicate/wasteful crons: act immediately (disable), report after
- Default `wakeMode: "now"` for scheduled jobs
- Retry wrapper (`retry_wrapper.sh`) for Amazon API jobs

## PR Opportunity Workflow (HARO/SOS) — Built Mar 2, 2026
### Domain Quality Gate (Added Mar 3, 2026)
- Uses DataForSEO Labs ETV (Estimated Traffic Value) to filter outlets
- **ETV < 1,000 = skip** (no row, no draft, silent)
- **ETV >= 1,000 = proceed** normally
- Exception: syndicated outlets (MSN, Yahoo) qualify regardless of own domain ETV
- Script: `~/amazon-data/collectors/pr_domain_checker.py`
- Cost: ~$0.01 per lookup
- ETV column added to sheet (column M)

### Placement Cooldown System (Added Mar 3, 2026)
- Placements tab tracks successful placements (outlet + guide type + date)
- Before drafting, check if same outlet + same seasonal group was placed in last 12 months
- Seasonal groups: spring (spring/easter/mother's day), summer, fall, holiday, general
- Same outlet + different season = OK (e.g. ConsumerQueen Spring → ConsumerQueen Holiday)
- Script: `~/amazon-data/collectors/pr_placement_checker.py`
- When row hits "Replied" → auto-log to Placements tab

- Gmail webhook intercepts HARO/SOS emails via `gmail-security.js` transform
- Senders: `haro@helpareporter.com`, `peter@shankman.com`, `peter@sourceofsources.com`
- Two lanes: Product Placement + Thought Leadership
- Scoring threshold: >= 70 out of 100
- Draft packages emailed to `ramon@goven.com` (never contact reporters directly)
- Notifications in `#mar_marketing` (C9T8MAM71)
- Silent when no qualifying hits
- **Backlink priority:** all7s.co ALWAYS primary link, Amazon only when reporter explicitly asks
- Rationale: all7s.co has zero DA, every editorial backlink builds foundation for organic traffic. Amazon doesn't need our backlinks.
- Vision: end Amazon dependency, build DTC, expand to Walmart/Target/B2B. Can't do Meta ads profitably at $26 AOV, but building SEO now for when $60 premium set launches.
- Sheet: `1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc` (Opportunities tab)
- Columns: Date, Source, Outlet, Summary, Reporter Name, Reporter Email, AI Score, AI Reasoning, Status, Thread ID, Last Action Date, Lane, Follow-up Due
- Statuses: Draft 1 Ready → Sent 1 → Sent 2 → Sent 3 → Closed/Replied
- BCC learning loop: Ramon BCCs chloemercer32@gmail.com when he sends a pitch → I study his edits, update pitch database, advance row status
- Daily cron at 10 AM EST checks for 7-day follow-ups (job: `pr-followup-check`)
- Playbooks: `playbooks/pr-opportunity-workflow.md` + `playbooks/pr-followup-check.md` + `playbooks/pr-outreach-workflow.md`

### Phase 2: Proactive Outreach (Built Mar 3, 2026)
- Outreach tab in PR sheet: proactive cold pitching to existing gift guide editors
- 26 guides tracked (NYT, Forbes, AARP, Good Housekeeping, CNET, WIRED, etc.)
- Pitch timing: 8 weeks before expected page update, 3 emails spaced 2 weeks
- Weekly cron: Mondays 9 AM EST, checks pitch windows and drafts emails
- Same rules: ETV >= 1,000, Placements cooldown, Blacklist, all7s.co primary link
- Old sheet (1kMvnhHTTzRIz4rbw3A8iiKd81Cqrp9kQXDj7D1kUAvI) retired

### Phase 3: Monthly Discovery (Built Mar 3, 2026)
- Monthly cron (1st Monday 10 AM): searches DataForSEO SERP for new opportunities
- Rotates through 22 search queries, 5 per run, with seasonal awareness
- Qualification: ETV >= 1k, list format, updated within 2yr, contact findable
- No forced minimums. Alerts #chloebot only for high-value finds (ETV > 100k)

### Sender Email Rule (Mar 3, 2026)
- ALL PR emails sent from ramon@all7s.co (brand recognition)
- Never from ramon@goven.com (editors don't know Goven)
- Learn from Ramon's rejections (Closed without sending)

## Centralized Logging (Built Mar 3, 2026)
- `~/amazon-data/collectors/event_logger.py` - central JSONL logger
- `~/amazon-data/logs/events.jsonl` - auto-rotates daily, 30-day retention
- `~/amazon-data/collectors/morning_review.py` - categorizes errors as transient vs needs-attention
- Morning Self-Heal cron: daily 6 AM EST, reads logs, auto-fixes transient issues, escalates criticals
- CLI: `event_logger.py summary`, `event_logger.py show --level error --hours 12`
- Instrumented scripts: email_util, dataforseo_api, clickup_integration (more to add over time)

## SEO Baseline (Feb 2025)
- all7s.co ranks for ZERO keywords in top 100 (starting from scratch)
- Google has 78 pages indexed
- GSC Weekly Report runs Mondays 9 AM
- DataForSEO set up with $0.50/day budget cap, $10 min balance floor
- Top target keywords: "canasta rules" (12,100/mo), "how to play canasta" (6,600/mo)

## Ramon's Socials (Content Strategy)
- **Full working doc:** `memory/ramons-socials.md` (load when Ramon says "Ramon's socials" or discusses video/content strategy)
- 4-pillar video strategy: Isolation/Ritual (10), Famous Women (5), The Table (10), Practical (5)
- Idea Bank in Google Sheet: `1l9VL3DCkz3MNe2kAGy6obqmEulvffmX1UdIGgVIx_YU` (Idea Bank tab + Scripts Archive tab + Content Tracker tab)
- Batch 1 (30 videos) already shot, posting starts March 6, 2026
- Batch 2 scripts in review with new 4-pillar approach
- Kallaway framework is the strategic foundation
- Email strategy is SEPARATE from video strategy (discussed separately)

## Working With Ramon

- Filter all advice through: "Does this help All7s, Canasta, community, or email growth?"
- No multi-brand distractions
- No launch-more-products-for-growth mentality
- Structured plans > chaotic tactics
