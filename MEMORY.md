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
- **Mexican Train Dominoes** — strongest near-term expansion (same demo, same game night groups, physical differentiation potential)
- Rummikub and Bunco also in the same audience tier

### Market Research (Mar 7, 2026)
- Mahjong is 8-10x more searched than Canasta in the US — long-term expansion target after Canasta dominance
- Hand & Foot is ~half of Canasta search volume (variant, not competitor)
- Mahjong IG content world mirrors Canasta's target audience exactly (women 35-65, social gathering)

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
- **Sent so far:** #1 Julia Child (Mar 2), #2 Eva Gabor (Mar 8)
- **Famous women policy:** Only 5 per month. Must have natural connection to ritual/togetherness. No forced tie-ins.

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

### Klaviyo Deliverability (Mar 7, 2026)
- All emails landing in Gmail Promotions tab (both HTML and plain text)
- Sender reputation issue: all7s.co is new sending domain, ~70 recipients is too small for Gmail to differentiate
- Fix is time + engagement signals (opens, replies, manual moves to Primary). No quick fix.

## Infrastructure & Integrations

### ClickUp
- **Task ID auto-recognition:** Any string matching `86ewr*` or `86ewt*` = ClickUp task ID → look up in `clickup_config.json` → `task_to_cron` to resolve cron job name + UUID. No prefix needed from Ramon.
- All 25+ cron jobs tracked as tasks in ClickUp (list 901816342276)
- Integration script auto-posts comments and marks complete
- ClickUp is Ramon's source of truth for cron job status

### Airbyte Cloud + BigQuery (Deployed Mar 6-8, 2026)
- **Major migration:** Amazon data collection moved from custom SP-API/Ads API scripts → Airbyte Cloud (~$10/month) → BigQuery
- **BigQuery dataset:** `amazon_raw` in project `lustrous-bounty-460801-b9` (39 tables)
- **Airbyte connections:** Amazon Ads (15 streams) + Amazon Seller Partner (13 streams, incl. Sales & Traffic report)
- **Phase 1 + 1.5 complete (Mar 8):** All dual-writes active. Historical SQLite data migrated (159,423 rows across 5 tables). forecast_restock.py reads from BQ.
- **Key gap FIXED:** `sales_daily` (Business Reports) has no Airbyte equivalent. `daily_sales.py` now dual-writes to BQ (cron 93e6e259, daily 7:15 AM).
- **Custom scripts that must keep running (Airbyte gaps):** daily_sales.py, daily_ppc.py, weekly_sqp.py, daily_ranks.py, gsc_report.py — all dual-writing to SQLite + BQ.
- **Settlement Report:** API access confirmed. 90-day retention. Build when QBO comes (~Q2). ClickUp: 86ewvn06j
- **Attribution API:** Access confirmed. Advertiser: Smart Buyers United (580509897613930109). Build when off-Amazon campaigns launch. ClickUp: 86ewvn0mt
- **Airbyte PPC lookback:** 3-day window configured, handles Amazon's attribution lag correctly.
- **Phase 2 (next, ~Mar 14):** Disable SQLite-only crons after dual-write validation. Check SP connection stability Wed Mar 11 (if still 10+ hours, split into 2 connections). Keep sales_daily cron running.
- **Phase 3:** Flip to BQ-only, retire SQLite
- **Crons to disable:** 86ewr926h (Daily Amazon Data), 86ewr926q (Daily PPC) — once Airbyte confirmed stable
- **Future Airbyte sources:** QBO (priority), Klaviyo, Shopify (after DTC volume), Google Ads/Facebook Ads
- Account under Ramon's company domain. Chloe (chloemercer32) has admin access.

### Google Drive Sync
- Skills + scripts synced nightly to Drive for Ramon's review
- Internal files are source of truth; Drive stays current
- Service account: `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`

### Gmail Hook Security
- Tiered routing: `@goven.com`/`@all7s.co` → trusted session; all others → untrusted (restricted)

### Gmail Watcher Resilience (Fixed Mar 7, 2026)
- LaunchAgent `ai.openclaw.tailscale-retry` runs on boot, waits up to 2 min for Tailscale, restarts gateway if gmail watcher failed
- Logs to `~/.openclaw/logs/tailscale-retry.log`
- gog OAuth app moved to Google Production status (permanent tokens, no more 7-day expiry)
- Gmail webhook pipeline stable since Mar 2 (3-day trial passed)

### OpenClaw Configuration
- Model lineup: Claude Opus 4.6 (main), OpenAI Codex 5.2 (fallback), Gemini Flash (heartbeat)
- Slack `textChunkLimit` set to 800 chars (auto-chunks messages)
- `blockStreaming: true` enabled (prevents message overwrites)

### Mac Mini Notes
- SSH (Remote Login) is NOT enabled — enable for future remote troubleshooting
- NoMachine is the current remote access method
- Local IP: `192.168.68.200`

### #thoughts Channel (C08P1NQBXK8)
- Ramon posts → Chloe creates ClickUp task in list 25307274 ("Ramon's Tasks")
- Links get researched/summarized; plain text saved as-is
- Reacts with 👀 to confirm

### Wholesale Pricing Optimization (Mar 5)
- Batch pricing API (`getItemOffersBatch`) implemented: 341 individual calls → 18 batch calls
- Runtime cut from ~11 min to ~3.5 min

### SQP Data Collection
- SQP reports can get stuck IN_QUEUE at Amazon for days (happened week of Feb 22-28)
- Added 2 AM run to schedule, bumped max_wait to 30 min — eventually resolved after retries

### Cron Job Rules
- Runaway/duplicate/wasteful crons: act immediately (disable), report after
- Default `wakeMode: "now"` for scheduled jobs
- Retry wrapper (`retry_wrapper.sh`) for Amazon API jobs
- Empty Gmail webhook notifications: fixed (gmail-security.js returns null for blank emails)

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
- **Ramon's pitch style (locked in after 7+ observations):**
  - ~100-120 words, one-scroll length
  - Opens with specific reference to reporter's article/segment
  - Core message: 4-player game → weekly social commitment → real friendships
  - Offers complimentary set for review
  - Links to all7s.co product page (not Amazon)
  - No product image attachments for cold outreach (text-only)
  - Sign-off varies by warmth: "Warmly, Ramon" (cold) or "Best, Ramon" (established relationship)
  - No em dashes, conversational but professional
- **PR Wins (as of Mar 8):**
  - ConsumerQueen: 2 confirmed placements (Spring guide + Mother's Day guide, syndicated to MSN)
  - MarketingSherpa: positive reply from Daniel Burstein (Senior Director, Content)
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

## SEO Status (Updated Mar 7, 2026)
- **Critical finding (Mar 7):** boardgamefun.com → all7s.co domain migration didn't transfer Google indexing. Most pages not indexed.
- Ramon manually requesting crawling in GSC (daily quota limits)
- Use `www.all7s.co` for all GSC lookups (canonical is www version)
- **68 meta descriptions** written and published across all 20 pages + 48 articles (Mar 7)
- **Hand & Foot article published** — targeting 22,900/mo keyword, ~2,500 words
- **How-to-Play-Canasta hub page rebuilt** — removed custom template, now editable via API, 12 internal links
- **"4 player canasta" rising query** (+3,400%) — added targeting to 6 articles
- **H1 fixes** applied to 10 pages with duplicate H1s
- GSC Weekly Report runs Mondays 9 AM
- DataForSEO set up with $0.50/day budget cap, $10 min balance floor
- Top target keywords: "canasta rules" (12,100/mo), "how to play canasta" (6,600/mo), "hand and foot card game" (22,900/mo)
- Monthly SEO Strategy Review cron: 3rd of every month at 10 AM (`467a1910`, ClickUp `86ewubz7g`)

## Ramon's Socials (Content Strategy)
- **Full working doc:** `memory/ramons-socials.md` (load when Ramon says "Ramon's socials" or discusses video/content strategy)
- 4-pillar video strategy: Isolation/Ritual (10), Famous Women (5), The Table (10), Practical (5)
- Idea Bank in Google Sheet: `1l9VL3DCkz3MNe2kAGy6obqmEulvffmX1UdIGgVIx_YU` (Idea Bank tab + Scripts Archive tab + Content Tracker tab)
- Batch 1 (30 videos) posting daily March 6 – April 4, 2026 (alternating FP/PI pillars, started posting Mar 6)
- Batch 2 scripts: 30 new scripts across 4 pillars in Idea Bank tab, awaiting Ramon review
- Kallaway framework is the strategic foundation
- Email strategy is SEPARATE from video strategy (discussed separately)

### Video Posting System (Active Mar 6, 2026)
- Daily cron: `d991a7a5` delivers posting package to #chloebot at 10 AM EST
- Playbook: `playbooks/daily-video-post.md`
- Drive folders: To Post = `1ogCw4xV7u_PDlT2C9NxZL6xsrYXBaLbf`, Posted = `16X4cz-UYwEKg4uB_pcE26ZUVgpu3_tva`
- Content Tracker: `1l9VL3DCkz3MNe2kAGy6obqmEulvffmX1UdIGgVIx_YU` (Content Tracker tab), 120 rows (4 platforms × 30 videos)
- Platforms: TikTok, IG Reels, YT Shorts, FB Reels
- Pinned comment: "Comment START" (B1), will switch to "SUNDAY" for B2
- TikTok pinned comment uses "DM me START" (ManyChat triggers off DMs on TikTok)
- After Ramon says "done": update spreadsheet + move video from To Post → Posted in Drive

### ManyChat + Klaviyo Integration (Mar 6, 2026)
- Trigger words: "START" and "SUNDAY" on IG/FB comments and TikTok DMs
- Flow: Comment/DM → ManyChat DM → collect email in-app → push to Klaviyo list
- ManyChat has separate Klaviyo API keys (don't share Chloe's keys)
- Will transition to "SUNDAY" keyword only for B2+

## Product Compliance
- **Intertek CPC recertification** — Scavenger Hunt product failed (missing CPSIA Section 103 tracking labels per ASTM F963)
- Required on BOTH product AND packaging: manufacturer name, location, production date, batch number
- Existing FBA inventory: leave as-is. Apply to all future production runs.
- Ramon getting Brother P-Touch PT-D220 (~$30) with TZe-211 tape for on-demand date/batch codes
- Also waiting on details of separate physical/mechanical test failure from Cathy Tang (Intertek)

## Kajabi → Tevello Migration (Planned Dec 2026)
- canastacourse.com on Kajabi (month 3 of 12 prepaid, expires ~Dec 2026)
- Migration target: Tevello (Shopify app) → all7s.co/courses (subfolder, full SEO benefit)
- Don't migrate until December. Redirect active: all7s.co/courses → canastacourse.com
- All new links use all7s.co/courses (not canastacourse.com)

## Slack Bot Capabilities
- `files:read` + `files:write` scopes added (Mar 6, 2026) — Chloe can now see images shared in Slack

## Fridge Moments — Gianna's Business (SEPARATE)
- **Channel:** #fridgemoments (C0AKA6QRCVB)
- **Rule:** When in this channel, ONLY discuss Fridge Moments. No Amazon, no All7s, no main business.
- Custom photo fridge magnets, Shopify/Etsy only
- Domain: fridgemoments.com
- Budget: $1,000 total
- Phase 1: Inkjet → Phase 2: Sublimation (after 25 sales)
- Drive folder: 0ANkC691BDrRwUk9PVA
- Profit sheet: 1fIsb896d2md7EGmS0QXh78fOi7QkyjS81k4JPQzmTs4

## Pending Items
- **all7s.com domain acquisition:** Reached out to owner (disbanded CA heavy metal band) via Facebook as Chloe. Message viewed, awaiting response. Budget: under $1,000. Use Escrow.com if they respond.
- **Postiz self-hosting:** Revisit June 5 for batch video scheduling automation (replace manual posting flow)
- **Airbyte SP connection:** Check Wed Mar 11 for sync stabilization (<2h target)
- **Credential files in Downloads:** Delete `bigquery_service_account_key.json` and `airbyte-seller-central-creds.rtf`

## Working With Ramon

- Filter all advice through: "Does this help All7s, Canasta, community, or email growth?"
- No multi-brand distractions
- No launch-more-products-for-growth mentality
- Structured plans > chaotic tactics
