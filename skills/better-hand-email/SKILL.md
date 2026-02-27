# The Better Hand Email

## Purpose
Drafts Friday's "The Better Hand" newsletter email with a Canasta strategy tip, following humanizer rules and brand voice.

## Schedule
- **Cron:** `0 21 * * 3` (UTC)
- **Frequency:** Wednesdays at 9:00 PM UTC (4:00 PM EST)

## Execution
```bash
# AI-driven drafting task
# Read: ~/.openclaw/workspace/playbooks/better-hand-email.md
# Read: ~/.openclaw/workspace/canasta-rules/better-hand-log.jsonl
# Pick strategy tip from: ~/.openclaw/workspace/canasta-rules/strategy.jsonl
# Post draft for Ramon's approval
```

## Behavior
- Pick ONE unused, approved strategy tip from `strategy.jsonl`
- Follow playbook format in `playbooks/better-hand-email.md`
- PS rotation: course → social → engagement (check log for last used)
- **Humanizer rules apply:** no em dashes, no AI tells, no "I'd be happy to", no "Great question!"
- Log entry to `better-hand-log.jsonl` after draft posted
- Post draft to Ramon for approval before sending

## Error Handling
- If no approved strategy tips available, alert Ramon
- If playbook missing, log error and skip

## Alerts & Delivery
- **Log to:** #chloe-logs (C0AELHCGW4F)
- **Alert to:** Ramon (draft for approval via Slack)

## Dependencies
- `~/.openclaw/workspace/playbooks/better-hand-email.md`
- `~/.openclaw/workspace/canasta-rules/better-hand-log.jsonl`
- `~/.openclaw/workspace/canasta-rules/strategy.jsonl`
- Humanizer skill rules
- Klaviyo (for final send after approval)
