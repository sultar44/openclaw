#!/usr/bin/env python3
"""
Facebook Group Scraper for Canasta Strategy
Designed to be run via OpenClaw browser automation.

This script provides helper functions for parsing and storing scraped content.
The actual browser automation is done via OpenClaw's browser tool.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

STRATEGY_FILE = Path(__file__).parent / 'strategy.jsonl'
RULES_FILE = Path(__file__).parent / 'rules.jsonl'
SCRAPE_STATE_FILE = Path(__file__).parent / 'scrape_state.json'

# Keywords to identify canasta-related posts
CANASTA_KEYWORDS = [
    'canasta', 'meld', 'wild', 'wilds', 'joker', 'deuce', '2s', 'twos',
    'natural', 'freeze', 'frozen', 'pack', 'pile', 'discard', 'draw',
    'going out', 'go out', 'open', 'opening', 'talon', 'stock',
    'red three', 'black three', 'seven', 'sevens', '7s', "7's", 'ace', 'aces',
    'partner', 'team', 'points', 'score', 'bonus', 'penalty',
    'clean', 'dirty', 'mixed', 'pure', 'special hand', 'signal', 'signaling'
]

# Keywords that suggest strategy vs rule
STRATEGY_KEYWORDS = [
    'would you', 'should i', 'should you', 'what would', 'best strategy',
    'do you', 'is it wise', 'is it better', 'recommend', 'opinion',
    'how do you', 'when do you', 'when should', 'risky', 'safe',
    'aggressive', 'conservative', 'early game', 'late game', 'depends'
]

RULE_KEYWORDS = [
    'is it allowed', 'can you', 'can i', 'is this legal', 'against the rules',
    'rule says', 'according to', 'what is the rule', 'official rule',
    'must you', 'have to', 'required', 'mandatory', 'illegal'
]


def is_canasta_related(text: str) -> bool:
    """Check if text is about canasta."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in CANASTA_KEYWORDS)


def classify_post(question: str, responses: list) -> str:
    """Classify post as strategy, rule_clarification, or table_rule."""
    text = question.lower()
    
    # Check for rule-related keywords
    if any(kw in text for kw in RULE_KEYWORDS):
        return 'rule_clarification'
    
    # Check for strategy keywords
    if any(kw in text for kw in STRATEGY_KEYWORDS):
        return 'strategy'
    
    # Check responses for hints
    all_responses = ' '.join([r.get('text', '') for r in responses]).lower()
    if 'table rule' in all_responses or 'house rule' in all_responses:
        return 'table_rule'
    
    # Default to strategy
    return 'strategy'


def analyze_responses(responses: list) -> dict:
    """Analyze responses to determine consensus."""
    if not responses:
        return {
            'total_responses': 0,
            'for': 0,
            'against': 0,
            'neutral': 0,
            'top_contributor_consensus': None
        }
    
    positions = {'for': 0, 'against': 0, 'neutral': 0}
    top_contributor_positions = []
    
    for r in responses:
        pos = r.get('position', 'neutral')
        positions[pos] = positions.get(pos, 0) + 1
        
        if r.get('badge') == 'top_contributor':
            top_contributor_positions.append(pos)
    
    # Determine top contributor consensus
    tc_consensus = None
    if top_contributor_positions:
        for_count = top_contributor_positions.count('for')
        against_count = top_contributor_positions.count('against')
        if for_count > against_count:
            tc_consensus = 'for'
        elif against_count > for_count:
            tc_consensus = 'against'
        else:
            tc_consensus = 'split'
    
    return {
        'total_responses': len(responses),
        'for': positions['for'],
        'against': positions['against'],
        'neutral': positions['neutral'],
        'top_contributor_consensus': tc_consensus
    }


def determine_consensus(analysis: dict) -> str:
    """Determine consensus level from analysis."""
    total = analysis['total_responses']
    if total == 0:
        return 'unknown'
    
    for_pct = analysis['for'] / total
    against_pct = analysis['against'] / total
    
    max_pct = max(for_pct, against_pct)
    
    if max_pct >= 0.8:
        return 'strong'
    elif max_pct >= 0.6:
        return 'moderate'
    elif max_pct >= 0.4:
        return 'disputed'
    else:
        return 'split'


def get_next_id() -> str:
    """Get next available FB ID."""
    if not STRATEGY_FILE.exists():
        return 'FB001'
    
    max_num = 0
    with open(STRATEGY_FILE) as f:
        for line in f:
            try:
                entry = json.loads(line)
                id_match = re.match(r'FB(\d+)', entry.get('id', ''))
                if id_match:
                    max_num = max(max_num, int(id_match.group(1)))
            except:
                continue
    
    return f'FB{max_num + 1:03d}'


def post_exists(post_id: str) -> bool:
    """Check if post already exists in database."""
    if not STRATEGY_FILE.exists():
        return False
    
    with open(STRATEGY_FILE) as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry.get('post_id') == post_id:
                    return True
            except:
                continue
    
    return False


def find_related_rules(question: str, context: str = '') -> list:
    """Find related rules from rules.jsonl based on keywords."""
    if not RULES_FILE.exists():
        return []
    
    text = (question + ' ' + context).lower()
    related = []
    
    with open(RULES_FILE) as f:
        for line in f:
            try:
                rule = json.loads(line)
                rule_text = (rule.get('question', '') + ' ' + rule.get('answer', '')).lower()
                
                # Simple keyword overlap check
                overlap = sum(1 for word in text.split() if len(word) > 4 and word in rule_text)
                if overlap >= 2:
                    related.append(rule.get('id'))
            except:
                continue
    
    return related[:5]  # Max 5 related rules


def save_strategy(entry: dict) -> None:
    """Append strategy entry to JSONL file."""
    with open(STRATEGY_FILE, 'a') as f:
        f.write(json.dumps(entry) + '\n')


def load_scrape_state() -> dict:
    """Load scrape state (last scraped date, etc.)."""
    if SCRAPE_STATE_FILE.exists():
        with open(SCRAPE_STATE_FILE) as f:
            return json.load(f)
    return {'last_scrape': None, 'last_post_id': None}


def save_scrape_state(state: dict) -> None:
    """Save scrape state."""
    with open(SCRAPE_STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)


def create_strategy_entry(
    post_id: str,
    post_url: str,
    post_date: str,
    author: str,
    author_badge: Optional[str],
    question: str,
    context: str,
    responses: list,
    source: str = 'facebook_mac'
) -> dict:
    """Create a complete strategy entry."""
    
    # Skip if already exists
    if post_exists(post_id):
        return None
    
    # Skip if not canasta related
    if not is_canasta_related(question):
        return None
    
    entry_type = classify_post(question, responses)
    analysis = analyze_responses(responses)
    consensus = determine_consensus(analysis)
    related = find_related_rules(question, context)
    
    # Generate recommendation based on consensus
    if consensus in ['strong', 'moderate']:
        majority = 'for' if analysis['for'] > analysis['against'] else 'against'
        # Find a representative response from majority
        for r in responses:
            if r.get('position') == majority and r.get('badge') == 'top_contributor':
                recommendation = r.get('text', '')[:200]
                break
        else:
            for r in responses:
                if r.get('position') == majority:
                    recommendation = r.get('text', '')[:200]
                    break
            else:
                recommendation = 'See responses for details'
    else:
        recommendation = 'Community is split. Per less-complexity preference, see detailed responses.'
    
    entry = {
        'id': get_next_id(),
        'type': entry_type,
        'source': source,
        'post_id': post_id,
        'post_url': post_url,
        'post_date': post_date,
        'author': author,
        'author_badge': author_badge,
        'question': question,
        'context': context,
        'responses': responses,
        'analysis': analysis,
        'consensus': consensus,
        'recommendation': recommendation,
        'complexity_note': None,
        'tags': extract_tags(question + ' ' + context),
        'related_rules': related,
        'status': 'pending',
        'scraped_at': datetime.utcnow().isoformat() + 'Z',
        'reviewed_at': None
    }
    
    return entry


def extract_tags(text: str) -> list:
    """Extract relevant tags from text."""
    tags = []
    text_lower = text.lower()
    
    tag_keywords = {
        'wilds': ['wild', 'wilds', 'joker', 'deuce', '2s'],
        'melding': ['meld', 'melding', 'lay down'],
        'opening': ['open', 'opening', 'initial meld'],
        'going_out': ['going out', 'go out', 'close'],
        'discard_pile': ['pile', 'pack', 'discard', 'frozen', 'freeze'],
        'sevens': ['seven', 'sevens', '7s'],
        'aces': ['ace', 'aces', 'natural ace'],
        'threes': ['three', 'red three', 'black three'],
        'scoring': ['points', 'score', 'bonus', 'penalty'],
        'early_game': ['early', 'beginning', 'start'],
        'late_game': ['late', 'end game', 'final'],
        'risk': ['risk', 'risky', 'safe', 'aggressive', 'conservative'],
        'partners': ['partner', 'teammate', 'team']
    }
    
    for tag, keywords in tag_keywords.items():
        if any(kw in text_lower for kw in keywords):
            tags.append(tag)
    
    return tags


if __name__ == '__main__':
    # Test the functions
    print("Strategy scraper helpers loaded.")
    print(f"Strategy file: {STRATEGY_FILE}")
    print(f"Rules file: {RULES_FILE}")
    print(f"Next ID would be: {get_next_id()}")
