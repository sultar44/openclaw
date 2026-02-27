# The Sunday Ritual Email

## Purpose
Drafts "The Sunday Ritual" newsletter email AND companion blog post featuring a famous person with a Canasta connection.

## Schedule
- **Cron:** `0 21 * * 4` (UTC)
- **Frequency:** Thursdays at 9:00 PM UTC (4:00 PM EST)

## Execution
```bash
# AI-driven drafting task
# Read: ~/.openclaw/workspace/playbooks/sunday-ritual-email.md
# Read: ~/.openclaw/workspace/canasta-rules/sunday-ritual-log.jsonl
# Post draft for Ramon's approval
```

## Behavior
- Feature a famous person with a verified Canasta connection (not previously used — check log)
- **Email:** ~200-250 words, warm storytelling tone
- **Blog post:** 400-600 words with image suggestion for header
- PS rotation: course → social → engagement (same rotation as Better Hand, check log)
- **Humanizer rules apply:** no em dashes, no AI tells
- Log entry to `sunday-ritual-log.jsonl` after draft posted
- Post both drafts for Ramon's approval before publishing

## Error Handling
- If can't find unused famous person, research and verify before using
- If playbook missing, log error and skip

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** Ramon (drafts for approval via Slack)

## Dependencies
- `~/.openclaw/workspace/playbooks/sunday-ritual-email.md`
- `~/.openclaw/workspace/canasta-rules/sunday-ritual-log.jsonl`
- Humanizer skill rules
- Shopify API (blog post publishing)
- Klaviyo (email send after approval)
- Image hosting via Shopify Image Host article (ID: 618201022747)
