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

### Sunday Ritual (Sunday, community/story email)
- Stories about women who built connection on purpose
- Two pillars: Famous women (15 figures) + Ritual themes (15 topics)
- **No selling** — this is the community email
- Plain text HTML only (Georgia 20px, 1.5 line height, no images/logos)
- PS rotation: 3/5 reply prompts, 2/5 with one link (builds Gmail reputation)
- Sender: "Ramon from All7s" <hello@all7s.co>
- Multi-phase workflow: Thu draft → Ramon review → revisions → publish blog + Klaviyo
- Evergreen flow (not campaigns) — each subscriber gets #1 first, then weekly

### Deliverability Rules (all relationship emails)
- Plain text HTML, no Klaviyo templates, no images/logos/social icons
- Minimize links (1 content link + unsubscribe)
- Klaviyo personalization: `{{ person.first_name|default:'friend' }}`

## Klaviyo API Notes
- Can't create flows via API (UI-only)
- Can't PATCH campaign-owned templates (create standalone + assign)
- Can't schedule campaigns via API (UI-only)

## Infrastructure & Integrations

### ClickUp
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

## SEO Baseline (Feb 2025)
- all7s.co ranks for ZERO keywords in top 100 (starting from scratch)
- Google has 78 pages indexed
- GSC Weekly Report runs Mondays 9 AM
- DataForSEO set up with $0.50/day budget cap, $10 min balance floor
- Top target keywords: "canasta rules" (12,100/mo), "how to play canasta" (6,600/mo)

## Working With Ramon

- Filter all advice through: "Does this help All7s, Canasta, community, or email growth?"
- No multi-brand distractions
- No launch-more-products-for-growth mentality
- Structured plans > chaotic tactics
