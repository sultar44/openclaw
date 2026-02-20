#!/usr/bin/env python3
"""
Helper to extract and save a single Facebook post.
Uses the fb_scraper module for processing and storage.
"""
import json
import sys
import os

# Import from fb_scraper.py in the same directory
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from fb_scraper import create_strategy_entry, save_strategy, post_exists, is_canasta_related

def classify_position(text: str) -> str:
    """Classify a comment's position: for, against, or neutral."""
    text_lower = text.lower()
    
    for_patterns = ["yes", "correct", "right", "agree", "exactly", "true", 
                   "you can", "you should", "that's right", "absolutely"]
    
    against_patterns = ["no", "wrong", "incorrect", "disagree", "can't",
                       "cannot", "shouldn't", "not allowed", "never"]
    
    for pattern in for_patterns:
        if pattern in text_lower:
            return "for"
    
    for pattern in against_patterns:
        if pattern in text_lower:
            return "against"
    
    return "neutral"


def parse_and_save_post(raw_data):
    """Parse raw data from browser and save as strategy entry."""
    try:
        data = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
    except:
        return {'saved': False, 'error': 'Failed to parse JSON'}
    
    post_id = data.get('post_id', '')
    
    # Check if already exists
    if post_exists(post_id):
        return {'saved': False, 'post_id': post_id, 'duplicate': True}
    
    question = data.get('question', '')
    author = data.get('author', '')
    author_badge = data.get('author_badge', '')
    post_date = data.get('post_date', '')
    url = data.get('url', '')
    context = data.get('context', '')
    
    # Check if canasta-related
    if not is_canasta_related(question):
        return {'saved': False, 'post_id': post_id, 'not_canasta': True}
    
    # Process comments - add position classification
    responses = []
    for comment in data.get('comments', []):
        text = comment.get('text', '')
        responses.append({
            'author': comment.get('author', ''),
            'badge': comment.get('badge', ''),
            'text': text,
            'reactions': comment.get('reactions', 0),
            'position': classify_position(text)
        })
    
    # Create entry using fb_scraper's function
    entry = create_strategy_entry(
        post_id=post_id,
        post_url=url,
        post_date=post_date,
        author=author,
        author_badge=author_badge if author_badge else None,
        question=question,
        context=context,
        responses=responses
    )
    
    if entry is None:
        return {'saved': False, 'post_id': post_id, 'skip_reason': 'duplicate or not canasta related'}
    
    # Save to file
    save_strategy(entry)
    return {'saved': True, 'post_id': post_id, 'entry_id': entry.get('id')}


if __name__ == "__main__":
    raw = sys.stdin.read()
    result = parse_and_save_post(raw)
    print(json.dumps(result))
