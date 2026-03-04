# PR Discovery - Monthly Outreach Pipeline Builder

## Trigger
Cron fires every Monday at 10 AM EST, but **only runs on the 1st Monday of the month.**

**First step every run:** Check if today's date is between the 1st and 7th. If not, reply HEARTBEAT_OK and exit. This ensures we only run on the first Monday.

## Goal
Find new gift guide / product roundup pages that are good candidates for proactive outreach. Add qualified ones to the Outreach tab.

## Search Query Pool
Rotate through ~5 queries per run. Over 4 months, we cycle through all of them.

### Core Queries (always relevant)
1. "best card games for seniors"
2. "best canasta sets"
3. "card games for older adults"
4. "gifts for women over 50"
5. "gifts for empty nesters"
6. "retirement gifts for women"
7. "gifts for grandmothers"
8. "best board games for adults"
9. "social games for seniors"
10. "brain games for older adults"

### Seasonal Queries (prioritize by month)
**Jan-Mar (Spring prep):**
11. "mother's day gifts older women"
12. "spring gift guide women"
13. "easter gifts grandma"

**Apr-Jun (Summer prep):**
14. "father's day gifts card games"
15. "summer activities seniors"
16. "graduation gifts adults"

**Jul-Sep (Holiday prep):**
17. "holiday gift guide women over 50"
18. "christmas gifts for seniors"
19. "best holiday gifts grandparents"

**Oct-Dec (Year-end + New Year):**
20. "new year party games adults"
21. "best games of [year]"
22. "winter activities seniors"

## Query Selection Logic
Each run:
1. Pick 3 core queries (rotate: use queries not searched recently, track in state file)
2. Pick 2 seasonal queries matching the current quarter
3. Total: 5 queries per run

## Search Method
Use DataForSEO SERP API:
```python
from dataforseo_api import api_post

results = api_post('serp/google/organic/live/advanced', [{
    'keyword': query,
    'location_code': 2840,  # US
    'language_code': 'en',
    'depth': 30,  # Top 30 results
}])
```

Cost: ~$0.002 per query = $0.01 per run for SERP queries.
Domain rank checks: ~$0.01 each = up to $0.20 for 20 new domains.
Total budget cap per run: $0.50.

## Qualification Criteria (ALL must pass)

1. **Format check:** URL must be a list/guide/roundup/review (look for keywords in title: "best", "top", "guide", "gifts", "review", "favorite")
2. **Not already tracked:** URL not already in the Outreach tab
3. **Not on Blacklist:** Publication not on the Blacklist tab
4. **ETV >= 1,000:** Run domain rank check via DataForSEO
5. **Freshness:** Page updated within last 2 years (check date in SERP snippet or metadata)
6. **Relevance:** Our product category fits the list (card games, board games, gifts for women 50+, seniors, social games). Disqualify if the list is strictly about video games, children's games, or unrelated categories.
7. **Not a competitor:** Not a game company's own blog/site (skip boardgamegeek.com listings, publisher blogs, etc.)
8. **Contact findable:** There's an identifiable author/editor (not just "Staff" with no contact)

## For Each Qualified Page

1. Record: Publication, Article Title, Guide URL, Guide Type, ETV
2. Research the author/editor name and email (web search)
3. Determine "Last Updated" from SERP data or page metadata
4. Calculate Expected Update and Pitch Window (same 8-week-before logic)
5. Add to Outreach tab with Status: "Queued"

## State Tracking
Keep a state file at `~/amazon-data/collectors/pr_discovery_state.json`:
```json
{
    "last_run": "2026-03-03",
    "queries_searched": {
        "best card games for seniors": "2026-03-03",
        "gifts for women over 50": "2026-03-03"
    },
    "urls_checked": ["https://example.com/..."]
}
```

This prevents re-checking the same URLs and ensures query rotation.

## Output

- **New rows added:** Add to Outreach tab directly
- **ClickUp:** Post comment to task with summary (X queries searched, Y new opportunities found)
- **High-value alert:** If any new find has ETV > 100,000, message #chloebot
- **Zero found:** Silent. Log to ClickUp only. No Slack message.

## Time Cap
Max session time: 15 minutes. If the session exceeds this, wrap up with whatever was found and log.

## Notes
- Always link to all7s.co in any future drafts (backlink strategy)
- Sender email: ramon@all7s.co
- Same Placements tab cooldown rules apply
- Same ETV threshold applies
- Deduplicate against existing Outreach rows before adding
