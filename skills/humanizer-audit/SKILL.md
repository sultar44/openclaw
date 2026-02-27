# Humanizer Audit

## Purpose
Reviews Wikipedia's "Signs of AI writing" article, compares findings to the current humanizer skill rules, implements improvements, and adds regression tests.

## Schedule
- **Cron:** `0 22 4 * *` (America/New_York)
- **Frequency:** Monthly on the 4th at 10:00 PM EST

## Execution
```bash
# AI-driven audit task
# 1. Fetch/review Wikipedia "Signs of AI writing" article
# 2. Compare to humanizer skill at /opt/homebrew/lib/node_modules/openclaw/skills/operator-humanizer
# 3. Implement improvements to skill rules
# 4. Add regression tests for new patterns
```

## Behavior
- Scrape or fetch current Wikipedia article on AI writing tells
- Compare each identified pattern against current humanizer rules
- If new patterns found: implement detection/replacement rules
- Add regression tests for each new rule
- Skill location: `/opt/homebrew/lib/node_modules/openclaw/skills/operator-humanizer`
- Also check `~/.openclaw/workspace/skills/operator-humanizer` if local copy exists
- Timeout: 2400s

## Error Handling
- If Wikipedia unavailable, use cached/known patterns and log
- Never break existing rules — only add or improve

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** None (improvements applied silently)

## Dependencies
- Wikipedia access (web search/browser)
- Humanizer skill at `/opt/homebrew/lib/node_modules/openclaw/skills/operator-humanizer`
- Write access to skill files
