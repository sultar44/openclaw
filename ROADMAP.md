# ROADMAP.md — Chloe + Ramon 12-Month Plan

*Last updated: 2026-03-03*

---

## ✅ COMPLETED

### Research & Data
- [x] **Facebook demographic scraping** — Canasta group research running nightly (10:30 PM)
- [x] **Canasta strategy database** — 90 entries, deduplicated, ready for chatbot

### Automation
- [x] **Wholesale repricing system** — Auto-reads Column M, submits to Amazon Listings API
- [x] **FBM inventory adjustments** — Column N triggers quantity updates
- [x] **Daily PPC collection** — 6:30 AM EST, stores in `ppc_campaigns/keywords/search_terms`
- [x] **Daily rank tracking** — 7:00 AM EST via DataDive Rank Radar API

---

## 🔧 IN PROGRESS / BLOCKED

### Cron Reliability
- [ ] **OpenClaw cron investigation** — Jobs not triggering reliably
- [ ] **launchd fallback** — Backup system cron created, monitoring

### Integrations
- [ ] **eBay connection** — Waiting for dev account approval (~1 day)
  - Sync inventory between Amazon FBM and eBay
  - Auto-adjust eBay quantities when wholesale sells

---

## 📋 TO DO — By Priority

### Phase 1: Quick Wins (Next 2-4 weeks)

| Task | Description | Effort |
|------|-------------|--------|
| ~~eBay inventory sync~~ | ✅ Done — eBay API connected, syncs with wholesale runs | Done |
| ~~Listing Monitor~~ | ✅ Done — BSR, strikethrough, coupon tracking via Keepa | Done |
| ~~GSC integration~~ | ✅ Done — Weekly reports, historical data in SQLite | Done |
| ~~Wholesale BSR tracking~~ | ✅ Done — Keepa BSR for FBA shipping decisions | Done |
| Competitor monitoring | Track prices, reviews, new products on competing ASINs | 2-3 days |
| FBA Reimbursement Generator | Scan shipments → identify reimbursable cases → draft claims | 2-3 days |
| Deep Product Research | Reviews + Reddit scraping for Canasta insights, feature gaps | 3-5 days |
| Warehouse SKU alerts | ✅ Done — Column H "needs SKU" alerts to #chloebot | Done |

### Phase 2: Supply Chain (1-2 months)

| Task | Description | Effort |
|------|-------------|--------|
| ~~AWD integration~~ | ✅ Done — AWD monitoring + replenishment recommendations | Done |
| FBA restock alerts | 🔧 In progress — "Ship XXX units to US/CA" based on velocity + lead time | 3-5 days |
| PO projection model | 🔧 In progress — Forecast demand → recommend China PO quantities + timing | 1 week |
| Canada manual process docs | Document current CA workflow, identify automation points | 1 day |

### Phase 3: Marketing & Content (2-4 months)

| Task | Description | Effort |
|------|-------------|--------|
| ~~Klaviyo integration~~ | ✅ Done — API connected, flows built | Done |
| Sunday Ritual content engine | 🔧 In progress — Tracker for article ideas, drafts, publish dates, performance metrics | 1-2 days |
| Short-form video analytics | Track views, engagement, comments across platforms; identify what works | 2-3 days |
| Short-form video ideas | Research trends, generate ideas for approval | Ongoing |
| Video scripts | Write scripts based on approved ideas | Ongoing |
| Newsletter topics | 🔧 In progress — Research + propose weekly/biweekly topics | Ongoing |
| Newsletter drafts | Write full drafts for approval | Ongoing |
| Blog research | 🔧 In progress — SEO keyword research, competitor content gaps | 2-3 days |
| Blog writing | Draft posts for approval | Ongoing |
| PR outreach system | ✅ Done — Reactive (HARO/SOS) + Proactive (cold pitches) + Monthly discovery | Done |

### Phase 4: PPC & Listings (2-4 months)

| Task | Description | Effort |
|------|-------------|--------|
| PPC spend analysis | Identify waste, optimization opportunities | 1-2 days |
| PPC reporting dashboard | Weekly/monthly summaries, trend analysis | 2-3 days |
| Listing optimization audit | Analyze titles, bullets, images, A+ content | 2 days |
| Keyword gap analysis | Find missing keywords vs competitors | 1-2 days |

### Phase 5: Customer Tools (4-8 months)

| Task | Description | Effort |
|------|-------------|--------|
| Canasta Q&A chatbot | Use strategy database for customer-facing answers | 1-2 weeks |
| Local game table finder (MVP) | Web form → searchable directory of players/tables | 1-2 weeks |
| Course engagement tracking | Kajabi analytics → identify drop-off, hot leads | 3-5 days |

### Phase 6: Finance & Accounting (4-8 months)

| Task | Description | Effort |
|------|-------------|--------|
| QBO API integration | Connect QuickBooks Online API, pull financial data/reports | 1 week |
| A2X replacement | Map Amazon settlement reports → QBO journal entries, replace A2X | 2-3 weeks |

### Phase 7: Apps & Advanced (6-12 months)

| Task | Description | Effort |
|------|-------------|--------|
| Canasta scoring app (iOS/Android) | Photo → AI score extraction, ~$3/month subscription | 2-3 months |
| AI video creation | Topic research → script → AI-generated videos | Ongoing |
| Demand forecasting model | ML-based prediction using historical data | 2-3 weeks |

---

## ❓ UNKNOWNS / DECISIONS NEEDED

- **Multiple agents?** — Currently single agent. Revisit when workflows get complex.
- **Cron reliability** — Root cause TBD. launchd backup in place.
- **PPC strategy** — Need to understand current approach before recommending changes.

---

## 📝 Notes

### Effort Estimates
- "Days" = focused work sessions, not calendar days
- Ongoing = recurring task, not one-time

### Priority Principles
1. Revenue-protecting automation first (inventory, supply chain)
2. Revenue-generating content second (marketing, ads)
3. New revenue streams third (apps, chatbot)

### Not Doing
- Profitability dashboard (Sellerboard handles this well)
- Profit OS daily digest (Sellerboard covers it)
- Multiple brand expansion (All7s focus only)

---

*This is a living document. Update as priorities shift.*
