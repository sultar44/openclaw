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
- PS rotation: ALL reply-engagement questions, no links (socials are dormant, links hurt Primary inbox placement)
- Sender: "Ramon from All7s" <hello@all7s.co>
- Multi-phase workflow: Thu draft → Ramon review → revisions → publish blog + Klaviyo
- Evergreen flow (not campaigns) — each subscriber gets #1 first, then weekly
- **Sent so far:** #1 Julia Child (Mar 2), #2 Eva Gabor (Mar 8), #3 Betty White (Mar 16), #4 Lucille Ball (Mar 23)
- **Publisher script:** `~/amazon-data/collectors/sunday_ritual_publisher.py` (handles Shopify + Klaviyo + logging, no LLM needed)
- **Auto-trigger:** Signal watcher cron checks every 2 min for dashboard selection, runs full pipeline
- **No approval gate for content.** Ramon selects topic from dashboard, blog publishes + Klaviyo campaign created automatically.
- **Ramon schedules manually.** Campaign is ready with send time pre-set, but not scheduled. Ramon reviews and clicks Schedule.
- **Dashboard auto-trigger:** Selecting a topic posts a message to #chloebot which triggers the full pipeline (no polling cron).
- **Famous women policy:** Only 5 per month. Must have natural connection to ritual/togetherness. No forced tie-ins.

### Course Link (Updated Mar 7, 2026)
- **Use all7s.co/courses** (NOT canastacourse.com) for all blog CTAs and links going forward

### Template System (Hardcoded, Mar 13 2026)
- **Ramon mandate: if it CAN be hardcoded via .py, hardcode it.**
- All emails rendered via `templates/render_email.py` with fixed template files
- Templates lock in: Klaviyo tags (`{{ person.first_name|default:'friend' }}`), greetings, sign-offs, coupon codes, URLs, P.S. rotation
- LLM only supplies dynamic body content. No more regenerating structural elements.
- Applies to everything going forward, not just emails.

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
- **CAN schedule campaigns via API** but Ramon prefers to schedule manually. Set up everything (send time, template) but do NOT call `/api/campaign-send-jobs`. Ramon clicks Schedule in Klaviyo after review.
- **Campaign name vs subject:** Campaign name includes `#N` (internal tracking). Email subject does NOT (customer-facing). Example: campaign "The Sunday Ritual #5: ..." → subject "The Sunday Ritual: ..."

### Klaviyo Deliverability (Mar 7, 2026)
- All emails landing in Gmail Promotions tab (both HTML and plain text)
- Sender reputation issue: all7s.co is new sending domain, ~70 recipients is too small for Gmail to differentiate
- Fix is time + engagement signals (opens, replies, manual moves to Primary). No quick fix.

## Infrastructure & Integrations

### ClickUp
- **Task ID auto-recognition:** Any string matching `86ewr*` or `86ewt*` = ClickUp task ID → look up in `clickup_config.json` → `task_to_cron` to resolve cron job name + UUID. No prefix needed from Ramon.
- All 40+ cron jobs tracked as tasks in ClickUp (list 901816342276)
- Integration script auto-posts comments and marks complete
- ClickUp is Ramon's source of truth for cron job status
- **Cron Registry Self-Healing:** Daily sync auto-re-enables disabled jobs (unless marked Retired/Intentionally Disabled), detects ClickUp overdue tasks (2+ days). `openclaw cron list` only shows enabled jobs — disabled ones still exist in `jobs.json`.

### BigQuery Data Infrastructure (Deployed Mar 6-15, 2026)
- **BigQuery dataset:** `amazon_raw` in project `lustrous-bounty-460801-b9` (39+ tables)
- **Historical SQLite data migrated** (159,423 rows across 5 tables). BQ is sole data store.
- **SQLite fully retired (Mar 15):** amazon.db is a frozen archive. No active script reads or writes. 8 scripts migrated from dual-write/SQLite reads to BQ-only.
- **Airbyte: DECOMMISSIONED (Mar 15).** All connections, sources, and BQ destination deleted. ~$10/mo saved.
- **Replacement architecture (built Mar 11-15):**
  - **Tier 1: Amazon Ads email reports** — 5 daily reports (Campaign, Placement, Targeting, Advertised Product, Search Term) delivered to Gmail → `ads_report_processor.py` → BQ. Wired into `gmail_inbox_router.py` (Mar 14). BQ tables: `ads_console_campaigns`, `ads_console_search_terms`, `ads_console_targets`, `ads_console_placements`, `ads_console_products`
  - **Tier 2: SP-API scheduled reports** — 14 schedules (8 types × 2 marketplaces), hourly polling via `scheduled_report_poller.py`. Settlement reports auto-detected.
  - **Tier 3: On-demand reports** — 3/day staggered (7AM Inventory Planning, 8AM Merchant Listings, 9AM Sales & Traffic). Gentle approach: 1/hour, never parallel.
  - **Tier 4: Financial Events API** — daily 5:30 AM, 30-day lookback. QBO prep.
- **SP-API rate limit strategy:** 2-hour gaps between all calls. Bursts cause Amazon to flake.
- **Settlement Report:** API access confirmed. 90-day retention. Build when QBO comes (~Q2). ClickUp: 86ewvn06j
- **Attribution API:** Access confirmed. Advertiser: Smart Buyers United (580509897613930109). Build when off-Amazon campaigns launch. ClickUp: 86ewvn0mt
- Account under Ramon's company domain. Chloe (chloemercer32) has admin access.

### GA4 Access (Added Mar 14, 2026)
- Service account granted Viewer access to GA4 property `properties/521314991` (all7s.co)
- Account: 381679081
- Libraries: `google-analytics-data`, `google-analytics-admin` installed
- Working: can pull activeUsers, pageViews, sessionDuration, traffic sources, etc.
- **Integrate into:** Monthly SEO Strategy Review cron (runs 3rd of each month, 10 AM EST, job `467a1910`)
- Also useful for: GSC Weekly Report enrichment, content performance tracking

### Google Drive Sync
- Skills + scripts synced nightly to Drive for Ramon's review
- Internal files are source of truth; Drive stays current
- Service account: `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`

### Gmail Hook Security
- Tiered routing: `@goven.com`/`@all7s.co` → trusted session; all others → untrusted (restricted)

### Gmail Processing (Updated Mar 17, 2026)
- **gog gmail watch serve is the PRIMARY system** — runs via OpenClaw gateway, catches emails near-instantly via Google Pub/Sub push
- Process restarts daily at 3:15 AM with gateway restart, subscription auto-renews every 720 min
- **Polling cron is the BACKUP** — "Gmail Inbox Processor" runs every 30 min (`61b00e02`, ClickUp `86ewwxu07`) as safety net
- Processes ALL email types: HARO/SOS, Amazon Ads reports, trusted senders, external
- Playbook: `playbooks/gmail-poll-safety-net.md`
- **Mar 17 incident:** 4 Ads report emails forwarded in rapid succession caused processing queue pileup + LLM timeout → circuit breaker tripped. Root cause was manual rapid-fire forwarding, not a watcher bug.
- LaunchAgent `ai.openclaw.tailscale-retry` still exists for Tailscale boot reliability
- gog OAuth app on Google Production status (permanent tokens)
- TODO: File gog bug report on GitHub for the stale historyId issue

### OpenClaw Configuration
- Model lineup: Claude Opus 4.6 (main), OpenAI Codex 5.2 (fallback), Gemini Flash (heartbeat)
- Slack `textChunkLimit` set to 800 chars (auto-chunks messages)
- `blockStreaming: true` enabled (prevents message overwrites)
- **Gateway self-restart is broken.** Auto-update cron killed the gateway twice (Mar 9-10). Replaced with external LaunchAgent `ai.openclaw.auto-update` (3:15 AM) + `ai.openclaw.gateway-watchdog` (every 5 min). Never let gateway restart itself.
- **`openclaw cron run` (manual trigger) does NOT work.** Only schedule-based auto-fire works. For manual reruns, run underlying scripts directly. Gateway restart auto-fires missed jobs (schedule-based catchup).
- **Dual-process port conflict:** If `openclaw gateway install` runs while foreground gateway is active, creates port 18789 conflict. Always stop existing process first.
- **OpenClaw Update Check** (`851a2dd4`): Daily 2:28 PM, alerts #chloebot only when update exists. Waits for Ramon's explicit approval. ClickUp: `86ewwejxm`.

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
- **SQP ClickUp rule (Ramon, Mar 16 2026):** ALL SQP cron runs (main + retries) MUST comment/complete task `86ewr9282` only. Never log to `86ewub625` or any other task. This is hardcoded in `clickup_config.json`.

### Cron Job Rules
- Runaway/duplicate/wasteful crons: act immediately (disable), report after
- Default `wakeMode: "now"` for scheduled jobs
- Retry wrapper (`retry_wrapper.sh`) for Amazon API jobs
- Empty Gmail webhook notifications: fixed (gmail-security.js returns null for blank emails)
- **`--no-deliver` flag** for jobs that handle their own ClickUp logging (prevents phantom "Message failed" errors from OpenClaw's announce layer)
- **Facebook scraper dud rate:** ~1-in-15 runs produce no data (LLM fluke). Ramon says investigate only on back-to-back duds.

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
- **Gift Bag Policy (Mar 16, 2026):** Disregard all gift bag / bulk giveaway opportunities. Only pursue placements requiring 1 free set max.
- Scoring threshold: >= 70 out of 100
- Draft packages emailed to `ramon@goven.com` (never contact reporters directly)
- Notifications in `#mar_marketing` (C9T8MAM71)
- Silent when no qualifying hits
- **Backlink priority:** all7s.co ALWAYS primary link, Amazon only when reporter explicitly asks
- Rationale: all7s.co has zero DA, every editorial backlink builds foundation for organic traffic. Amazon doesn't need our backlinks.
- Vision: end Amazon dependency, build DTC, expand to Walmart/Target/B2B. Can't do Meta ads profitably at $26 AOV, but building SEO now for when $60 premium set launches.
- Sheet: `1ekrQwL_OHI784GFm-E8KSPynNP4w4MyDYWKh3jELokc` (Opportunities tab)
- Columns: Date, Source, Outlet, Summary, Reporter Name, Reporter Email, AI Score, AI Reasoning, Status, Last Action Date, Lane, Follow-up Due, ETV
- Statuses: Draft 1 Ready → Sent 1 → Sent 2 → Sent 3 → Closed/Replied
- BCC learning loop: Ramon BCCs chloemercer32@gmail.com when he sends a pitch → I study his edits, update pitch database, advance row status
- **Ramon's pitch style (locked in after 8+ observations):**
  - ~100-120 words, one-scroll length
  - Opens with specific reference to reporter's article/segment
  - Core message: 4-player game → weekly social commitment → real friendships
  - Offers complimentary set for review
  - Links to all7s.co product page (not Amazon)
  - No product image attachments for cold outreach (text-only)
  - Sign-off varies by warmth: "Warmly, Ramon" (cold) or "Best, Ramon" (established relationship)
  - No em dashes, conversational but professional
  - **Follow-up strategy:** Focuses on "demo potential" for TV (rotating trays are visual), emphasizes "recap" and "reconnecting with friends" angle. Ends with "Thanks for your time either way."
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
- **Opportunity Selection Feedback (Mar 13, 2026):** Avoid "Thought Leadership" or "Product Placement" opportunities that are too far removed from the core product (games) or brand mission (social connection), even if the target audience matches. Skip niche interior design details (Regency-core kitchens, furniture materials, rug layering) or unrelated lifestyle roundups (skin care). Stick to opportunities where the board game or ritual tie-in is central and natural.

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
- Pinned comment: single version for ALL platforms — "Comment START" (no more "DM me START" variant)
- Will switch pinned comment to "SUNDAY" for B2
- Description CTA: "comment START for..." line in all descriptions. No "follow @playall7s" (Ramon prefers emails over followers, tags all7s as collaborator instead)
- After Ramon says "done": update spreadsheet + move video from To Post → Posted in Drive

### Comment Automation (Updated Mar 12, 2026)
- IG/FB: ManyChat (comment trigger → DM → collect email → Klaviyo)
- TikTok: TikTok's native automation (comment trigger → sends all7s.co/sunday link)
- YouTube: Manual (Ramon replies)
- ManyChat has separate Klaviyo API keys (don't share Chloe's keys)
- Will transition to "SUNDAY" keyword for B2+

### Social Media Best Practices (Mar 14)
- **Pinned comments:** Use for conversation starters, NOT CTA. Keep CTA in description only.
- **Thumbnails (B2+):** Agency to include 1-second title card frame at video start for cover selection.
- **Hashtags:** 3-5 specific. Avoid generic (#love, #inspo). Include 1 branded (#all7sgames).
- **First engagement happened** (Mar 9): "START" comment on TikTok + FB engagement on Batch 1 content.

### Product Assets (Correct Links)
- **Canasta Cards Deluxe Game Set ($27):** https://www.all7s.co/products/canasta-cards-deluxe-game-set
- **Main Website:** https://all7s.co
- **Canasta Course:** https://all7s.co/courses

## Amazon Pricing Strategy (STP/PED) — Mar 10
- **Strikethrough Pricing (STP)** driven by Amazon's median price over rolling window
- **CAN2P problem:** Liquidation sales ($8.99-$9.99) from Dec-Jan polluted the median. Hold $12.99, check mid-April.
- **CANSET works perfectly:** Clean price history at $26.99, spike works instantly.
- **Coupon trick:** Coupon-clipped sales register at LIST price for STP calculations. Good for seeding high data points.
- **90-day STP refresh cycle:** Every 90 days per SKU, spike price 25-35% above everyday for a few sales, drop back.

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

## Amazon Seller Central Access (Updated Mar 15)
- Account: yamaris@goven.com (NOT chloemercer32)
- TOTP secret stored in `~/amazon-data/.env` as `AMAZON_TOTP_SECRET` (the LFR7... Amazon-generated one)
- **Full autonomous login capability confirmed:** email → password → TOTP
- Ramon logged in manually to get past 2SV enrollment loop; browser now authenticated
- Auto-forward rule being set up: yamaris@goven.com → chloemercer32@gmail.com
- **IDR portal** (Inventory Defect & Reimbursement) replaces manual auditing for warehouse damage/lost claims
- Browser 2FA needed for IDR portal access — pending Ramon's help

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
- **Postiz self-hosting:** Deployed on Mac mini (Docker, `http://localhost:4007` / `https://192.168.68.200:4008`). Login: `ramon@goven.com` / `PostizAll7s!`. Self-signed cert (10yr) for HTTPS. Next: Ramon connecting social accounts, then needs Meta app + Google OAuth + TikTok dev app. TikTok needs HTTPS/public domain (Tailscale funnel). Revisit for batch video scheduling automation.
- **Credential files in Downloads:** Delete `bigquery_service_account_key.json` and `airbyte-seller-central-creds.rtf`
- **Browser 2FA for IDR portal:** Needed for FBA reimbursement IDR scraping (Part 1). Ramon will help soon.

## Engineering Philosophy (Mar 13, 2026)
- **"If it CAN be hardcoded, it should. If it can't, then LLMs it is."** — Ramon's directive
- Avoid hallucinations and inconsistencies above all
- LLM tokens are acceptable cost, but deterministic code is always preferred
- 20+ cron jobs converted from LLM-heavy → thin wrapper (cron_runner.sh)
- Gmail inbox processing: Python router (`gmail_inbox_router.py`) handles deterministic routes, LLM only for HARO/SOS + BCC learning
- `vine_order_processor.py` replaced the LLM playbook that was corrupting sheet data
- Reimbursement audit: fully hardcoded Python, LLM only for IDR browser scrape
- **Cron timeout lesson:** When converting crons, always match outer `timeoutSeconds` to script's actual runtime + 60s buffer

### Augusta Rule Write-Up (Monthly)
- Cron: `f285d81f` — 1st of every month at 10 AM EST
- ClickUp: `86ewwg5wj`
- Reads all memory files from previous month, compiles narrative meeting notes, emails to ramon@goven.com

## FBA Reimbursement System (Built Mar 14-15, 2026)

### Architecture (Redesigned Mar 15 — fully hardcoded)
**Old approach (Mar 14):** Inventory Ledger analysis → generate case text → file manually. Found 2 major bugs:
1. Not netting found/recovered entries against damage/lost entries (false positives)
2. Counting disposition transfers as "lost" (CPC compliance removals appeared as losses)
- Impact: 16 cases ($1,058) → 5 real cases ($42.90) after bug fixes

**New approach (Mar 15):** Three-part Monday audit (Python, no LLM):
1. **Shipment discrepancies** — SP-API Inbound Shipments, wait for CLOSED, verify via browser
2. **Sizing/fee changes** — weekly baseline comparison (56 ASINs in Sizing_Baseline tab)
3. **Fee tier checks** — compare Amazon's measured dimensions vs known specs
- Plus: **IDR Portal scrape** — separate small LLM cron (9:15 AM) for browser-only check
- Script: `monday_reimbursement_audit.py` (self-contained: checks + Slack alerts + ClickUp logging)

### IDR Portal Key Discovery
- Amazon's IDR portal now auto-detects eligible claims. Ledger-based audits generate false positives Amazon already resolved.
- US (90 days): 316 defect units, **0 eligible**, 279 resolved ($262.77 reimbursed)
- CA (90 days): 31 defect units, **0 eligible**, 28 resolved (CA$8.16 reimbursed)
- `GET_FBA_FULFILLMENT_INVENTORY_ADJUSTMENTS_DATA` report type is DEPRECATED (blocked by Amazon)
- SP-API `QuantityReceived` lags behind Amazon's actual reconciliation — browser is source of truth

### Key Rules
- Amazon reason codes: Q = transferred to defective, M = misplaced, P = transfer to defective disposition, F = found
- Policy: reimbursements for inventory lost BEFORE customer order = manufacturing cost, not sales price
- Claim windows: Lost/damaged warehouse 60d, Customer returns 60-120d, Inbound 9mo, Fee overcharges 90d
- Broken 6-pack theory: CAN6P breaking → individual CAN2P scans. Check offsetting +/- across related SKUs.

### Crons
- `794f8248` — Weekly Reimbursement Reports (Sun 11PM) — ClickUp `86ewy25ca` (BQ data refresh)
- `23c02425` — Monday Reimbursement Audit (Mon 9AM) — ClickUp `86ewy6f50` (hardcoded Python)
- `21f0dca5` — IDR Browser Check (Mon 9:15AM) — small LLM job
- `7a36e0cd` — Weekly Reimbursement Monitor — **DISABLED** (superseded by Monday audit)

## Rolling Jokers CPC Compliance (Mar 12)
- Glass marbles failed lead content test (components 19, 21, 22, 24)
- Two fixes needed: (1) compliant marbles (acrylic recommended), (2) proper tracking labels
- 1,500 units in stock, selling ~18/month ($40 price, down from $75)
- Chinese copycats destroyed pricing power. Plan: recoup via trickle sales + DTC upsell through Canasta list.
- Age rating 8+ was a mistake (triggers CPC). Audience is adults.
- Marble sourcing in progress. Tip: ask suppliers for existing CPSIA/EN-71 reports before samples.

## B2B Wholesale Strategy (Mar 12)
- **Faire is primary B2B channel** (net 60, free returns, discovery)
- **Blocked until:** New PO with smaller carton sizes (6 or 12-unit, ETA May-June 2026)
- **Key targets:** Barnes & Noble (distributor says "ideal"), Books-A-Million, indie retailers (Playmobil CC list)
- **Walmart.com:** Has account, full API available. Relaunch with PPC.
- **Needs before execution:** B2B landing pages, sell sheet PDF, Faire API key, Walmart API credentials
- Playbook: `playbooks/b2b-wholesale-strategy.md`

## eBay Sync (Mar 14)
- ASIN-based dedup to prevent duplicate listings
- **Ramon's pricing rules:** All clothing $16.99, shoes $29.99. Manual override via sheet column E.
- Skip no-op API calls (compare before calling)

## PR Sheet Off-by-One Bug (CRITICAL — Mar 12)
- **ALWAYS read back target row content BEFORE writing to verify it's the right opportunity**
- Formula: data_index 0 = sheet row 2. data_index N = sheet row N+2.
- Bug hit twice: wrote to wrong row both times.

## Working With Ramon

- Filter all advice through: "Does this help All7s, Canasta, community, or email growth?"
- No multi-brand distractions
- No launch-more-products-for-growth mentality
- Structured plans > chaotic tactics
