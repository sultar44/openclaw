# Canasta Rules Knowledge Base Schema

## Purpose
A structured database of Canasta rules and Q&A pairs for:
1. Advanced Canasta course creation
2. Facebook group moderation
3. Future AI chatbot
4. Future scoring aid

## Philosophy
- **When community is split → prefer less complexity**
- Rules must be approved by Ramon before being marked "confirmed"
- Source all rules from: course scripts, tips doc, or Facebook research

## Data Format: JSONL

Each line in `rules.jsonl` is a JSON object with:

```json
{
  "id": "unique-id",
  "category": "category-name",
  "question": "The question as players commonly ask it",
  "answer": "The community-consensus answer",
  "explanation": "Optional deeper explanation",
  "consensus": "strong|moderate|disputed|pending",
  "source": "course_script|tips_doc|facebook_research",
  "status": "pending|approved|rejected",
  "variations": ["Alternative rules some tables use"],
  "tags": ["beginner", "advanced", "edge_case"],
  "added": "2026-02-07",
  "approved_by": "ramon|null"
}
```

## Categories

| Category | Description |
|----------|-------------|
| `setup` | Game setup, dealing, initial meld requirements |
| `drawing` | Drawing from stock or discard pile |
| `melding` | Creating and adding to melds |
| `wild_cards` | Jokers and 2s usage |
| `freezing` | Frozen pile rules |
| `canastas` | Clean/dirty canasta rules |
| `going_out` | Requirements and process for going out |
| `scoring` | Point values and scoring rules |
| `special_hands` | Special hand rules |
| `special_cards` | 3s (red/black) and other special cards |
| `partners` | Partnership play rules |
| `etiquette` | Common table etiquette |

## Consensus Levels

- **strong**: Community overwhelmingly agrees (90%+)
- **moderate**: Clear majority agrees (70-90%)
- **disputed**: Community is split; we chose "less complexity"
- **pending**: Not yet verified against community

## Workflow

1. Extract rules from source documents → status: "pending"
2. Ramon reviews → status: "approved" or "rejected"
3. Once approved, can be used in course/chatbot/moderation
