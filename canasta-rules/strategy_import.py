#!/usr/bin/env python3
"""
Import strategy tips from internal documents (Tips & Tricks).
These are pre-approved since they're Ramon's internal docs.
"""

import json
from datetime import datetime
from pathlib import Path

STRATEGY_FILE = Path(__file__).parent / 'strategy.jsonl'

# Strategy tips extracted from Tips & Tricks doc
# Format for internal docs is simpler - no community discussion
STRATEGY_TIPS = [
    # Hand Management & Card Economy
    {
        "id": "TT-S001",
        "type": "strategy",
        "source": "tips_doc",
        "category": "hand_management",
        "title": "Keep cards in hand",
        "strategy": "Do not empty your hand matching every partner meld early. Holding cards preserves access to the pack and keeps options open.",
        "tags": ["hand_management", "card_economy", "early_game", "pile_access"],
    },
    {
        "id": "TT-S002",
        "type": "strategy",
        "source": "tips_doc",
        "category": "hand_management",
        "title": "Track aces and sevens",
        "strategy": "Track aces and sevens relentlessly. Avoid holding more than two aces or two sevens when aces are not yet safely mixed on the table.",
        "tags": ["aces", "sevens", "tracking", "risk_management"],
    },
    {
        "id": "TT-S003",
        "type": "strategy",
        "source": "tips_doc",
        "category": "hand_management",
        "title": "Discard singles first",
        "strategy": "Prefer shedding higher-value singles early to keep lower points on the table for safer access later.",
        "tags": ["discarding", "early_game", "card_economy"],
    },
    {
        "id": "TT-S004",
        "type": "strategy",
        "source": "tips_doc",
        "category": "hand_management",
        "title": "Evaluate special hand early",
        "strategy": "At the start of each hand, evaluate distance to a special hand before committing to ordinary melds. Decide early whether you aim for pairs or the zip code.",
        "tags": ["special_hands", "early_game", "planning"],
    },
    
    # Discarding & Defense
    {
        "id": "TT-S005",
        "type": "strategy",
        "source": "tips_doc",
        "category": "discarding",
        "title": "Watch every discard",
        "strategy": "Watch every discard, especially partner discards. That is live information for safety and bait.",
        "tags": ["discarding", "defense", "observation", "partners"],
    },
    {
        "id": "TT-S006",
        "type": "strategy",
        "source": "tips_doc",
        "category": "discarding",
        "title": "Don't throw aces after partner opens with aces",
        "strategy": "Do not throw an ace immediately after your partner opens with aces. Give them time to use partner aces to pick a future pack.",
        "tags": ["aces", "partners", "discarding", "pack_picking"],
    },
    {
        "id": "TT-S007",
        "type": "strategy",
        "source": "tips_doc",
        "category": "discarding",
        "title": "Sevens management partnership",
        "strategy": "Sevens management is partnership strategy. Many teams allow a seven discard right after opening, especially when the opener's hand is short, or when targeting higher opening thresholds.",
        "tags": ["sevens", "partners", "discarding", "strategy"],
    },
    {
        "id": "TT-S008",
        "type": "strategy",
        "source": "tips_doc",
        "category": "discarding",
        "title": "Avoid loading pile with sevens",
        "strategy": "Avoid loading the pile with sevens. Opponents picking that pile may convert it into a pure sevens canasta.",
        "tags": ["sevens", "pile", "defense"],
    },
    {
        "id": "TT-S009",
        "type": "strategy",
        "source": "tips_doc",
        "category": "discarding",
        "title": "Late game baiting",
        "strategy": "Baiting late, you may throw a tempting rank that traps opponents into taking a bad pile filled with aces or sevens that will hurt them at scoring.",
        "tags": ["baiting", "late_game", "advanced", "defense"],
    },
    {
        "id": "TT-S010",
        "type": "strategy",
        "source": "tips_doc",
        "category": "discarding",
        "title": "Safe discard based on closed ranks",
        "strategy": "Safe discard selection depends on what is already closed. If foes closed jacks, a jack becomes safer. If fours are dead, a four is safer.",
        "tags": ["discarding", "safety", "observation"],
    },
    
    # When to Close/Wait
    {
        "id": "TT-S011",
        "type": "strategy",
        "source": "tips_doc",
        "category": "closing",
        "title": "Close mixed canasta early when risky",
        "strategy": "Closing a mixed canasta early is wise when your partner has few cards or when opponents have multiple threes down. Reduce risk, bank the base points.",
        "tags": ["closing", "canastas", "risk_management"],
    },
    {
        "id": "TT-S012",
        "type": "strategy",
        "source": "tips_doc",
        "category": "closing",
        "title": "Leave meld open only with upside",
        "strategy": "Leave a meld open only when the timing supports higher upside and opponents are unlikely to punish you.",
        "tags": ["closing", "timing", "risk_management"],
    },
    {
        "id": "TT-S013",
        "type": "strategy",
        "source": "tips_doc",
        "category": "closing",
        "title": "High-value canasta decisions",
        "strategy": "Waiting one draw to try to complete a high-value canasta can swing thousands of points. Think, do not autopilot a pile pick that locks you into a lower ceiling.",
        "tags": ["closing", "scoring", "decision_making"],
    },
    
    # Pack/Pile Calculations
    {
        "id": "TT-S014",
        "type": "strategy",
        "source": "tips_doc",
        "category": "pile_picking",
        "title": "Compare outcomes before taking late pile",
        "strategy": "Before taking a late pile, compare two outcomes: your projected score if you pass versus if you take the pile, including hits for aces and sevens remaining in hand. Take only if the swing is favorable.",
        "tags": ["pile_picking", "late_game", "scoring", "math"],
    },
    {
        "id": "TT-S015",
        "type": "strategy",
        "source": "tips_doc",
        "category": "pile_picking",
        "title": "Count threes carefully",
        "strategy": "Count threes carefully. Their swing can erase or create a lead late in the deal.",
        "tags": ["threes", "scoring", "late_game"],
    },
    
    # Partnering & Table Info
    {
        "id": "TT-S016",
        "type": "strategy",
        "source": "tips_doc",
        "category": "partners",
        "title": "Agree on signals with partner",
        "strategy": "Agree with your partner on signals for aces and sevens policy and safe throws.",
        "tags": ["partners", "signals", "communication", "pregame"],
    },
    {
        "id": "TT-S017",
        "type": "strategy",
        "source": "tips_doc",
        "category": "partners",
        "title": "Announce card count",
        "strategy": "Keep your card count visible. Announce when at three or fewer cards. Announce the turn card.",
        "tags": ["partners", "communication", "card_count"],
    },
    {
        "id": "TT-S018",
        "type": "strategy",
        "source": "tips_doc",
        "category": "partners",
        "title": "Rack layout gives information",
        "strategy": "One straight rack reveals less information than multi-level racks. Multi-level racks expose your grouping and pairs to observant opponents. Sorting and handling matter - the less you reveal through spacing and rack layout, the better.",
        "tags": ["information", "defense", "rack_management"],
    },
    
    # Tournament Play
    {
        "id": "TT-S019",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tournament",
        "title": "Maximize points over time in tournaments",
        "strategy": "In tournament play, maximize team points over time. Do not rush to end low-scoring deals unless time and position demand it.",
        "tags": ["tournament", "pacing", "scoring"],
    },
    {
        "id": "TT-S020",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tournament",
        "title": "Pacing and time management",
        "strategy": "Pacing matters. Manage time within each round. Aim to finish all four deals. If time expires mid-round in a tournament, the unfinished deal yields zero for both sides.",
        "tags": ["tournament", "pacing", "time_management"],
    },
    
    # Tactical Snippets
    {
        "id": "TT-S021",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tactics",
        "title": "Early discard priority",
        "strategy": "Early with no wilds, discard a four or five before faces. Face cards tend to be hoarded longer.",
        "tags": ["early_game", "discarding", "card_priority"],
    },
    {
        "id": "TT-S022",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tactics",
        "title": "Hold zip code pieces",
        "strategy": "Hold potential zip code pieces until you see a path. Do not break them prematurely.",
        "tags": ["special_hands", "zip_code", "hand_management"],
    },
    {
        "id": "TT-S023",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tactics",
        "title": "Close when partner is low",
        "strategy": "With partner at three cards, closing a mixed canasta now is safer than chasing extra points.",
        "tags": ["closing", "partners", "risk_management"],
    },
    {
        "id": "TT-S024",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tactics",
        "title": "Avoid giving pile access late",
        "strategy": "When both sides already closed multiple canastas and the pile is full of bad ranks, avoid throws that open the pile for them.",
        "tags": ["late_game", "defense", "pile"],
    },
    {
        "id": "TT-S025",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tactics",
        "title": "Leave fifth ace in hand",
        "strategy": "When you open with aces, leave the fifth ace in hand. Preserve partner's ability to pick a future pile topped with an ace.",
        "tags": ["aces", "opening", "partners", "pile_picking"],
    },
    {
        "id": "TT-S026",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tactics",
        "title": "Two-digit mental counter for tracking",
        "strategy": "Track sevens and aces with a simple two-digit mental counter. Tens place for aces. Ones place for sevens. Update every time you see one.",
        "tags": ["tracking", "aces", "sevens", "mental_game"],
    },
    
    # Protect the Pack
    {
        "id": "TT-S027",
        "type": "strategy",
        "source": "tips_doc",
        "category": "pack_protection",
        "title": "Mindful of player to the left",
        "strategy": "Be mindful of the person to the left when protecting the pack, but if you can, be mindful of everyone.",
        "tags": ["pack_protection", "defense", "position"],
    },
    {
        "id": "TT-S028",
        "type": "strategy",
        "source": "tips_doc",
        "category": "pack_protection",
        "title": "Throw matching rank to protect pack",
        "strategy": "Already have your own meld of 4s? Protect the pack by throwing a 4. It's more important to protect the pack than to have a bigger meld of 4s.",
        "tags": ["pack_protection", "discarding", "priority"],
    },
    {
        "id": "TT-S029",
        "type": "strategy",
        "source": "tips_doc",
        "category": "pack_protection",
        "title": "Keep extra wild for pack protection",
        "strategy": "Can close a canasta with 1 wild? Throw a 2nd wild so you have another card to throw to protect the pack. It still counts as mixed whether it has 1 or 2 wilds.",
        "tags": ["pack_protection", "wilds", "closing"],
    },
    {
        "id": "TT-S030",
        "type": "strategy",
        "source": "tips_doc",
        "category": "pack_protection",
        "title": "Never throw the 5th seven or ace",
        "strategy": "Be aware of how many 7s or aces are in the pack. Never throw the 5th to give opponents a pure canasta.",
        "tags": ["aces", "sevens", "pack_protection", "counting"],
    },
    
    # Hot Seat & Signaling
    {
        "id": "TT-S031",
        "type": "strategy",
        "source": "tips_doc",
        "category": "position",
        "title": "Hot seat awareness",
        "strategy": "If right hand opponent melded, you are in the hot seat. You need to be aware of what opponent on the left has thrown to not give the pack.",
        "tags": ["position", "defense", "pack_protection", "awareness"],
    },
    {
        "id": "TT-S032",
        "type": "strategy",
        "source": "tips_doc",
        "category": "signaling",
        "title": "When signaling is discarded",
        "strategy": "Signaling is discarded when you are melding, when you need 180, or when the right partner has melded.",
        "tags": ["signaling", "partners", "communication"],
    },
    
    # Endgame Decisions
    {
        "id": "TT-S033",
        "type": "strategy",
        "source": "tips_doc",
        "category": "endgame",
        "title": "Which card to throw with 4 left",
        "strategy": "Have 4 cards left with 2 aces and 2 7s? Throw the one with the fewest in the pack - minimize risk of giving away a pure canasta.",
        "tags": ["endgame", "aces", "sevens", "decision_making"],
    },
    {
        "id": "TT-S034",
        "type": "strategy",
        "source": "tips_doc",
        "category": "endgame",
        "title": "Baiting with 3 of a kind",
        "strategy": "When you have 3 of a kind, throw one - it might bait them to give you a card you can use to pick the pack with your pair.",
        "tags": ["baiting", "pile_picking", "tactics"],
    },
    
    # Opening Threshold Strategy
    {
        "id": "TT-S035",
        "type": "strategy",
        "source": "tips_doc",
        "category": "opening",
        "title": "At 180, throw low cards",
        "strategy": "At 180 opening requirement, throw low cards even if you have a pair. You probably can't open with them anyway.",
        "tags": ["opening", "discarding", "thresholds"],
    },
    
    # Special Situations
    {
        "id": "TT-S036",
        "type": "strategy",
        "source": "tips_doc",
        "category": "scoring",
        "title": "Rush to end with 3s advantage",
        "strategy": "Have a lot of 3s? Push for that 2nd canasta - they're worth a lot of points. Other team has a lot of 3s and no closed canasta? Rush to close the round to give them penalty points.",
        "tags": ["threes", "scoring", "closing", "endgame"],
    },
    {
        "id": "TT-S037",
        "type": "strategy",
        "source": "tips_doc",
        "category": "scoring",
        "title": "Place jokers before 2s",
        "strategy": "Don't get stuck with jokers in hand at the end of a round. Always place them first vs 2s - they are a much bigger penalty in hand than melded.",
        "tags": ["wilds", "jokers", "scoring", "penalty"],
    },
    {
        "id": "TT-S038",
        "type": "strategy",
        "source": "tips_doc",
        "category": "tactics",
        "title": "Safe cards for high pile counts",
        "strategy": "Keep safe cards for higher discard pile counts. Throw risky cards when the pile count is low.",
        "tags": ["pile", "risk_management", "discarding"],
    },
]


def import_strategies():
    """Add strategy tips to strategy.jsonl."""
    
    # Read existing strategies
    existing = []
    existing_ids = set()
    
    if STRATEGY_FILE.exists():
        with open(STRATEGY_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    existing.append(entry)
                    existing_ids.add(entry['id'])
    
    # Add new strategies
    added = 0
    timestamp = datetime.now().isoformat()
    
    with open(STRATEGY_FILE, 'a') as f:
        for tip in STRATEGY_TIPS:
            if tip['id'] not in existing_ids:
                # Add metadata
                tip['status'] = 'approved'  # Internal docs are pre-approved
                tip['created_at'] = timestamp
                
                f.write(json.dumps(tip) + '\n')
                added += 1
                print(f"  ✓ {tip['id']}: {tip['title']}")
    
    print(f"\n✓ Added {added} strategy tips to strategy.jsonl")
    print(f"  Total entries now: {len(existing) + added}")


if __name__ == '__main__':
    print("Importing strategy tips from Tips & Tricks doc...\n")
    import_strategies()
