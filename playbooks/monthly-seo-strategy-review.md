# Monthly SEO Strategy Review

**Schedule:** 1st Monday of each month, 10 AM EST
**Output:** HTML report emailed to ramon@goven.com + summary in #chloebot
**Data sources:** GSC data (SQLite), DataForSEO APIs, all7s.co sitemap

## Sections

### 1. Page Health Audit
- Pull all indexed pages from GSC data (`keyword_ranking` / GSC tables in amazon.db)
- Crawl all7s.co sitemap to get full page list
- Flag issues:
  - Pages not indexed by Google
  - Thin content (<500 words)
  - Missing or duplicate H1 tags
  - No internal links pointing to/from page
  - Broken links (4xx/5xx)
- Use DataForSEO On-Page API for technical checks
- Output: table of issues ranked by priority (critical → low)

### 2. Keyword Gap Analysis
- Compare current rankings (GSC data) vs target keywords (DataForSEO)
- Identify high-volume keywords we're not covering at all
- Map opportunities to:
  - Existing pages that could be optimized (add keyword, improve content)
  - New blog articles needed
- Output: "Write these 3 articles" proposals with:
  - Target keyword
  - Monthly search volume
  - Suggested angle/title
  - Competitor examples ranking for that term

### 3. DA Building Opportunities
- Internal linking audit: are pages linking to each other properly?
- Competitor backlink analysis via DataForSEO:
  - Who links to canasta competitors but not us?
  - Resource pages, directories, communities we're missing
- Cross-reference with PR system (avoid duplicating active outreach)
- Suggest specific plays: guest posts, resource page submissions, content partnerships

## Report Format
- HTML email attachment (styled like the Feb 2025 SEO audit)
- Executive summary at top (3-5 bullet points of what changed since last month)
- Each section with clear action items
- Month-over-month comparison when data exists

## Execution Notes
- Timeout: 120 seconds (this job does multiple API calls)
- Log results to ClickUp task via clickup_integration.py
- If DataForSEO budget is low (<$1 remaining), skip expensive API calls and note in report
- Always check DataForSEO balance before making calls ($0.50/day cap, $10 floor)

## Delivery
- Email HTML report to ramon@goven.com
- Post summary to #chloebot (C0AD9AZ7R6F)
- ClickUp: mark task complete on success
