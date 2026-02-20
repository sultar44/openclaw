# Chloe's Cron Job Board

*Last updated: 2026-02-09 20:30 EST*

## Daily Schedule

| Time (EST) | Job | Duration | What It Does |
|------------|-----|----------|--------------|
| **6:00 AM** | Daily Amazon Collection | ~5 min | FBA Inventory + Orders (US + CA) |
| **6:30 AM** | Daily PPC Collection | ~10 min | Campaigns, Keywords, Search Terms (US + CA) |
| **7:00 AM** | Daily Rank Collection | ~5 min | Keyword rankings from DataDive (15 radars) |
| **10AM, 1PM, 4PM, 7PM, 10PM** | Rank Retry | ~1 min | Retry if morning rank collection incomplete |

## Weekly Schedule

| Day/Time | Job | Duration | What It Does |
|----------|-----|----------|--------------|
| **Monday 6:00 AM** | Weekly SQP Collection | ~20 min | Brand Analytics for 14 ASINs × 2 countries |
| **Mon-Wed 9AM, 12PM, 3PM, 6PM, 9PM** | SQP Retry | ~1 min | Retry if SQP data not yet available |

## One-Time Jobs

| Scheduled | Job | Duration | What It Does |
|-----------|-----|----------|--------------|
| **Tonight 10:30 PM** | Facebook Canasta Scraper | ~30 min | Scrape ~1 month of FB group posts for strategy insights |

---

## Estimated Daily Compute Time

| Category | Est. Minutes/Day |
|----------|------------------|
| Morning data collection (6-7 AM) | 20 min |
| Retry checks (if needed) | 5 min |
| **Total typical day** | **~25 min** |

## Estimated Weekly Compute Time

| Category | Est. Minutes/Week |
|----------|-------------------|
| Daily jobs × 7 | 175 min |
| Weekly SQP | 20 min |
| SQP retries (if needed) | 15 min |
| **Total typical week** | **~3.5 hours** |

---

## Job Details

### Daily Amazon Collection
- **Script:** `~/amazon-data/collectors/daily_collection.py`
- **Data:** Inventory snapshots, order history
- **Tables:** `inventory_snapshot`, `sales_daily`
- **Notification:** Only on failure

### Daily PPC Collection
- **Script:** `~/amazon-data/collectors/daily_ppc.py`
- **Data:** SP campaigns, keywords, search terms
- **Tables:** `ppc_campaigns`, `ppc_keywords`, `ppc_search_terms`
- **Notification:** Only on failure

### Daily Rank Collection
- **Script:** `~/amazon-data/collectors/daily_ranks.py`
- **Data:** Organic keyword rankings (DataDive)
- **Tables:** `keyword_ranking`
- **Notification:** Only on first failure

### Weekly SQP Collection
- **Script:** `~/amazon-data/collectors/weekly_sqp.py`
- **Data:** Search Query Performance per ASIN
- **Tables:** `search_query_performance`
- **Notification:** On failure + eventual success

### Facebook Canasta Scraper (One-time)
- **Script:** Browser automation
- **Data:** FB group discussions → strategy.jsonl
- **Notification:** Email summary when complete

---

## Capacity

**Current load:** Light (~3.5 hours/week automated)

**Available for:**
- ✅ More scheduled reports
- ✅ Ad-hoc analysis requests
- ✅ Building new tools
- ✅ Real-time chat assistance

The automated jobs run in isolated sessions, so they don't interrupt our conversations.
