# Canasta Strategy Database Schema

## Overview

Strategy entries are scraped from Facebook groups and community discussions. Unlike rules (which are definitive), strategies represent community wisdom and best practices.

## JSONL Format

File: `strategy.jsonl`

```json
{
  "id": "FB001",
  "type": "strategy|rule_clarification|table_rule",
  "source": "facebook_mac",
  "post_id": "1873734823512175",
  "post_url": "https://www.facebook.com/groups/modernamericancanasta/posts/...",
  "post_date": "2026-02-08",
  "author": "Mitchell Garber",
  "author_badge": "top_contributor",
  
  "question": "Would you meld 4 wild cards that meet the point requirement?",
  "context": "Early in game, almost half of cards still in deck, other team hasn't melded",
  
  "responses": [
    {
      "author": "Gina Kaplan Katz",
      "badge": null,
      "text": "I would not... I only meld wilds if I have at least 5",
      "reactions": 2,
      "position": "against"
    },
    {
      "author": "Shoshana Fluss Pilevsky", 
      "badge": "top_contributor",
      "text": "I would just to get out.. sometimes even with 5 wilds you don't make it",
      "reactions": 2,
      "position": "for"
    }
  ],
  
  "analysis": {
    "total_responses": 22,
    "for": 5,
    "against": 15,
    "neutral": 2,
    "top_contributor_consensus": "against"
  },
  
  "consensus": "moderate",
  "recommendation": "Wait for 5+ wild cards before melding a wilds canasta. The restrictions on using wilds until closed make 4 cards risky.",
  "complexity_note": "Waiting for 5 adds less risk/complexity than going early with 4",
  
  "tags": ["wilds", "melding", "early_game", "risk"],
  "related_rules": ["CS017", "CS018"],
  
  "status": "pending",
  "scraped_at": "2026-02-09T22:00:00Z",
  "reviewed_at": null
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique ID (FB001, FB002, etc.) |
| type | enum | strategy, rule_clarification, table_rule |
| source | string | facebook_mac, facebook_other, reddit, etc. |
| post_id | string | Facebook post ID for deduplication |
| post_url | string | Direct link to post |
| post_date | date | When post was made |
| author | string | Original poster name |
| author_badge | string | top_contributor, admin, moderator, null |
| question | string | The question being asked |
| context | string | Situation/context provided |
| responses | array | All responses with author, text, reactions |
| analysis | object | Summary of response positions |
| consensus | enum | strong, moderate, disputed, split |
| recommendation | string | Our recommended approach |
| complexity_note | string | Note on complexity preference |
| tags | array | Searchable tags |
| related_rules | array | IDs of related rules in rules.jsonl |
| status | enum | pending (needs review), approved, rejected |
| scraped_at | datetime | When scraped |
| reviewed_at | datetime | When Ramon reviewed |

## Consensus Levels

- **strong**: 80%+ agreement among responders
- **moderate**: 60-80% agreement
- **disputed**: 40-60% (near split)
- **split**: Clear camps with valid arguments both ways

## Status Workflow

1. **pending**: Just scraped, needs Ramon's review
2. **approved**: Ramon confirmed, can be used in course/chatbot
3. **rejected**: Not relevant or incorrect

## Complexity Preference

Per Ramon's guidance: when community is split and both positions are valid, prefer the approach that **adds less complexity** to the game.
