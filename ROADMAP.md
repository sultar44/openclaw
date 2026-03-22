# ROADMAP.md — Chloe + Ramon Plan

*Last updated: 2026-03-21*

---

## ✅ COMPLETED

### Research & Data
- [x] Facebook demographic scraping — Canasta group research
- [x] Canasta strategy database — 90 entries, deduplicated
- [x] Deep product research — Review scraping (weekly), bad review alerts
- [x] Competitor monitoring — Weekly price tracking via Keepa, >15% drop alerts
- [x] GSC integration — Weekly reports, historical data in BQ
- [x] GA4 integration — Service account connected, pageViews/traffic/sessions available

### Automation & Infrastructure
- [x] Wholesale repricing system — Auto-reads Column M, submits to Amazon Listings API
- [x] Wholesale BSR tracking — Keepa BSR for FBA shipping decisions
- [x] FBM inventory adjustments — Column N triggers quantity updates
- [x] Daily PPC collection — 6:30 AM EST
- [x] Daily rank tracking — 7:00 AM EST via DataDive Rank Radar
- [x] Cron reliability — launchd watchdog, gateway restart system, cron registry self-healing
- [x] eBay sync — Inventory/pricing sync between Amazon FBM and eBay
- [x] Listing Monitor — BSR, strikethrough, coupon tracking (Mon-Fri)
- [x] Warehouse SKU alerts — Column H "needs SKU" alerts
- [x] FBA Reimbursement system — Monday audit + IDR portal checks
- [x] BigQuery migration — 39+ tables, SQLite retired, Airbyte decommissioned
- [x] SP-API scheduled reports — 14 schedules, hourly polling
- [x] On-demand reports — Inventory Planning, Merchant Listings, Sales & Traffic
- [x] Financial Events API — Daily 5:30 AM, 30-day lookback

### Supply Chain
- [x] AWD integration — Monitoring + replenishment recommendations
- [x] FBA restock alerts — Velocity-based "ship X units" recommendations
- [x] PO projection model — Demand forecasting for China PO quantities + timing

### Marketing & Content
- [x] Klaviyo integration — API connected, flows built, campaigns automated
- [x] Sunday Ritual content engine — Full pipeline (draft → blog → Klaviyo), dashboard auto-trigger
- [x] Email template system — Hardcoded templates, LLM only for dynamic content
- [x] PR outreach system — Reactive (HARO/SOS) + Proactive + Monthly discovery
- [x] Blog writing system — SEO research, content pipeline, Shopify publishing
- [x] Short-form video scripts — Batch 1 complete, posted

### Integrations
- [x] ClickUp integration — 40+ cron jobs tracked, auto-comments, auto-complete
- [x] Gmail processing — Pub/Sub watcher + polling backup, full email routing
- [x] Google Sheets service account — Automated reads/writes
- [x] Google Drive sync — Skills + scripts synced nightly

---

## 📋 PRIORITY ORDER — What's Next

### 1. 🎯 PPC Optimization (NEXT)
| Task | Description | Status |
|------|-------------|--------|
| PPC spend analysis | Identify waste, optimization opportunities | Not started |
| PPC reporting dashboard | Weekly/monthly summaries, trend analysis, actionable flags | Not started |
| Listing optimization audit | Analyze titles, bullets, images, A+ content | Not started |
| Keyword gap analysis | Find missing keywords vs competitors | Not started |

*Ball is in Ramon's court to kick this off.*

### 2. 💰 Financial Reporting / QBO
| Task | Description | Status |
|------|-------------|--------|
| QBO API integration | Connect QuickBooks Online, pull financial data | Not started |
| A2X replacement | Map settlement reports → QBO journal entries | Not started |
| Cashflow modeling | Projections, reorder timing, cash conversion | Not started |

*Financial Events API already collecting daily. Settlement report API access confirmed.*

### 3. 📱 All7s Social
| Task | Description | Status |
|------|-------------|--------|
| Video analytics | Track views, engagement, identify what works | APIs connected, discuss Mon 3/24 |
| Batch 2 content | Next round of video scripts + posting | After Batch 1 analysis |
| Social strategy refinement | What's working, what to double down on | Ongoing |

### 4. 🤝 Influencer Management
| Task | Description | Status |
|------|-------------|--------|
| Outreach system | Identify, contact, manage influencer relationships | Not started |
| Tracking/reporting | ROI measurement on influencer partnerships | Not started |

### 5. 🏪 B2B / Wholesale
| Task | Description | Status |
|------|-------------|--------|
| Faire launch | Primary B2B channel | Blocked until smaller cartons (May-June) |
| Walmart.com relaunch | Account exists, has API | Needs PPC plan |
| B2B collateral | Sell sheets, landing pages | Not started |
| Barnes & Noble / Books-A-Million | Distributor says "ideal" | After Faire proves concept |

*Ramon has ideas — schedule B2B vision discussion.*

### 6. 🎬 AI Video Creation
| Task | Description | Status |
|------|-------------|--------|
| Tool evaluation | Test AI video generation tools, assess quality | Not started |
| Pipeline | Topic research → script → AI-generated videos | Not started |

### 7. 🔮 Future / Apps
| Task | Description | Status |
|------|-------------|--------|
| Canasta scoring app | Photo → AI score, ~$3/mo subscription | Not started |
| Local game table finder | Searchable player/table directory | Not started |
| Paid advanced Canasta course | Kajabi | Not started |
| Premium $60 Canasta set | Q4 2026 target | Sourcing not started |
| Mexican Train Dominoes | Strongest next product candidate | Research only |

---

## 🟡 OPEN MINOR ITEMS
- [ ] Canada manual process docs — Document CA workflow, identify automation points
- [ ] Short-form video analytics — APIs connected, discussion Monday 3/24
- [ ] CAN2PPLS + CAN6PPLS launch prep — Product arriving, needs listing + PPC plan
- [ ] Rolling Jokers CPC compliance — Need compliant marbles + tracking labels
- [ ] Attribution API build — Access confirmed, build when off-Amazon campaigns launch

---

## 📝 Notes

### Priority Principles
1. Revenue-protecting automation first (inventory, supply chain) ✅ DONE
2. Revenue-optimizing (PPC, financial visibility) ← **WE ARE HERE**
3. Revenue-generating content (marketing, social, influencers)
4. New revenue streams (B2B, apps, new products)

### Not Doing
- Multiple brand expansion (All7s focus only)
- Profitability dashboard (Sellerboard handles this)
- Demand forecasting ML model (PO projection covers needs)

---

*Living document. Updated as priorities shift.*
