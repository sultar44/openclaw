#!/usr/bin/env python3
"""Fix the 'Community is split' entries with proper recommendations."""

import json
from pathlib import Path
from datetime import datetime

STRATEGY_FILE = Path(__file__).parent / 'strategy.jsonl'

# Proper recommendations applying "less complexity" rule
FIXES = {
    "FB001": {
        "recommendation": "Strategic choice, not a rules question. Generally: Don't open with 4 wilds early - you lose flexibility and give opponents information. Keep wilds for picking piles and completing canastas.",
        "strategy": "Early game, preserve wild cards rather than melding them for opening points. The pack access and canasta completion value exceeds the opening benefit.",
        "tags": ["wilds", "opening", "early_game", "strategy"]
    },
    "FB004": {
        "recommendation": "No. You cannot pick the pile to form a splash as your opening meld. You need a natural pair already in hand to legally pick the pile. The 7th card completes the splash AFTER you've legally picked.",
        "strategy": "To pick the pile for opening: you must have a natural pair in hand that matches the top discard, plus meet the point threshold. You cannot count cards you'll gain from the pile toward opening requirements.",
        "tags": ["pile_picking", "splash", "opening", "rules"]
    },
    "FB005": {
        "recommendation": "Two questions answered: (1) A mixed wild canasta (5 twos + 2 jokers = 7 cards) earns the 2,500 bonus - that's correct. (2) Asking partner is BINDING - if they say yes, you MUST go out. If they say no, you cannot go out that turn.",
        "strategy": "The 'asking to go out' rule is strict: partner's answer is binding. Plan your hand before asking.",
        "tags": ["wild_canasta", "going_out", "partner_permission", "rules"]
    },
    "FB006": {
        "recommendation": "No. You must always discard to end your turn. The only exception is going out - and even then, most rules require a final discard. Drawing the last card doesn't exempt you from discarding.",
        "strategy": "Every turn ends with a discard. If you cannot legally discard (only wilds in hand, pack frozen), you're stuck.",
        "tags": ["discarding", "turn_structure", "endgame", "rules"]
    },
    "FB011": {
        "recommendation": "Not a valid pairs hand because it contains wild cards (the 2,2). A special pairs hand requires exactly 7 NATURAL pairs - no wild cards allowed. The 2s are wilds, not a natural pair.",
        "strategy": "Special hands (pairs, garbage) must be entirely natural cards. Any wild card invalidates the special hand.",
        "tags": ["special_hands", "pairs", "wilds", "rules"]
    },
    "FB013": {
        "recommendation": "Signaling (for jokers or anything else) is a partnership/table convention, not an official rule. There's no standard signal - agree with your partner before play.",
        "strategy": "Partnership signals are table rules. Common conventions exist but vary. Discuss with partner pregame.",
        "tags": ["signaling", "partnership", "table_rules", "conventions"]
    },
    "FB014": {
        "recommendation": "Yes, it's a double penalty. You get the 2,500 point penalty for failing to complete the pure canasta, AND those cards count against you at face value (aces = 20 each, 7s = 5 each). Both penalties apply.",
        "strategy": "Aces and 7s in hand at game end: 2,500 penalty per incomplete set PLUS the card point values. Very costly - prioritize completing or avoiding these melds.",
        "tags": ["aces", "sevens", "penalties", "scoring", "rules"]
    },
    "FB015": {
        "recommendation": "An open (incomplete) wild canasta is NOT a canasta - it's just a meld. You cannot go out without 2 complete canastas. The cards in an open wild meld count against you at face value (50 per joker, 20 per 2) plus you may face the 2,500 penalty if you started it and can't finish.",
        "strategy": "Never start a wild canasta unless you can complete it. An abandoned wild meld is extremely costly.",
        "tags": ["wild_canasta", "incomplete_meld", "going_out", "penalties", "rules"]
    },
    "FB022": {
        "recommendation": "No. You cannot discard a joker (wild card) as your final card if you have any other legal discard option. Since you had a jack, you must discard the jack. The joker must be melded or held.",
        "strategy": "Wild cards can only be discarded if they're your ONLY card, and even then it freezes the pack. Never plan to go out by discarding a wild.",
        "tags": ["wilds", "discarding", "going_out", "rules"]
    },
    "FB023": {
        "recommendation": "Yes, a discarded wild card freezes the pack. The wild goes sideways on the pile to indicate frozen status. If someone picks the pile after the wild, they only get cards down to (and including) the wild - nothing below it.",
        "strategy": "Discarding a wild is rare and defensive - it freezes the pack and limits what opponents can pick up.",
        "tags": ["wilds", "frozen_pack", "discarding", "rules"]
    }
}


def fix_entries():
    entries = []
    with open(STRATEGY_FILE, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    fixed = 0
    for e in entries:
        if e['id'] in FIXES:
            fix = FIXES[e['id']]
            e['recommendation'] = fix['recommendation']
            e['strategy'] = fix.get('strategy', e.get('strategy', ''))
            e['tags'] = fix.get('tags', e.get('tags', []))
            e['fixed_at'] = datetime.now().isoformat()
            fixed += 1
            print(f"✓ Fixed {e['id']}")
    
    # Save
    with open(STRATEGY_FILE, 'w') as f:
        for e in entries:
            f.write(json.dumps(e) + '\n')
    
    print(f"\n✓ Fixed {fixed} entries")


if __name__ == '__main__':
    fix_entries()
