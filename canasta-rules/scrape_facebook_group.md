# Facebook Group Scraper Instructions

## For OpenClaw to Execute

This document describes the scraping procedure for the Modern American Canasta Facebook group.

### Target Group
- **URL:** https://www.facebook.com/groups/modernamericancanasta
- **Source ID:** `facebook_mac`

### Scraping Procedure

1. **Navigate to group**
   ```
   browser navigate to https://www.facebook.com/groups/modernamericancanasta
   ```

2. **Scroll to load posts**
   - For first run: scroll ~30 times to load ~1 month of posts
   - For daily runs: scroll ~5 times to load recent posts
   - Wait 2-3 seconds between scrolls for content to load

3. **For each post in feed:**
   
   a. **Extract post content:**
      - Post ID (from URL or data attribute)
      - Author name
      - Author badge (top_contributor, admin, etc.)
      - Post date
      - Question/content text
   
   b. **Check if canasta-related:**
      - Skip birthday wishes, group announcements, etc.
      - Look for canasta keywords
   
   c. **Click to expand comments:**
      - Click on the post or "View more answers"
      - Wait for modal to load
   
   d. **Extract all comments:**
      - Author name and badge
      - Comment text
      - Reaction count
      - Classify position: for/against/neutral
   
   e. **Close modal and continue**

4. **Process each post:**
   - Use `fb_scraper.py` helper functions
   - Create strategy entry
   - Check for duplicates (skip if post_id exists)
   - Save to `strategy.jsonl`

5. **Update scrape state:**
   - Record last scrape timestamp
   - Record newest post ID seen

### Position Classification

When extracting comments, classify each as:

- **for**: Agrees with the proposed action, says "yes", "I would", "go for it"
- **against**: Disagrees, says "no", "I would not", "don't", "wait"
- **neutral**: Provides context but no clear position, "it depends", asks clarifying questions

### Complexity Preference

When generating recommendations for split decisions:
- Prefer the simpler approach
- "Wait" is simpler than "act now"
- "Don't meld" is simpler than "meld with conditions"
- Fewer exceptions = less complexity

### Output

Each scraped post becomes an entry in `strategy.jsonl` with:
- `status: "pending"` (awaiting Ramon's review)
- Full question and all responses preserved
- Analysis of community consensus
- Recommended approach

### Schedule

- **First run:** After 10pm, scrape ~1 month
- **Daily runs:** After 10pm, scrape since last run
- **Report:** Email summary to ramon@goven.com

---

## Manual Test Command

To test scraping one post manually:

1. Open browser to the group
2. Take snapshot of first post
3. Extract: author, date, question, comment count
4. Click to expand comments
5. Take snapshot of comments
6. Extract all comment data
7. Run through `fb_scraper.create_strategy_entry()`
8. Verify entry looks correct
