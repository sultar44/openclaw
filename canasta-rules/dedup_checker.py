#!/usr/bin/env python3
"""
Canasta Strategy Duplicate Checker

Checks if a new Q&A entry is a near-duplicate of an existing approved entry.
Used by the scrape pipeline to auto-skip duplicates before they hit the review queue.

Usage:
    # Check a single question against existing entries
    python3 dedup_checker.py --question "Can I open with 5 wilds?"

    # Check a batch file (JSONL) and filter out duplicates
    python3 dedup_checker.py --batch new_entries.jsonl --output filtered.jsonl

    # As a library
    from dedup_checker import is_duplicate
    result = is_duplicate("Can I open with 5 wilds?")
    if result['is_duplicate']:
        print(f"Duplicate of {result['match_id']}: {result['match_question'][:80]}")
"""

import json
import re
import sys
from pathlib import Path

STRATEGY_FILE = Path(__file__).parent / "strategy.jsonl"
SIMILARITY_THRESHOLD = 0.50  # Question similarity threshold for duplicate detection


def normalize_text(text):
    """Convert text to a set of meaningful words for comparison."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = text.split()
    stops = {
        'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'shall', 'can', 'in', 'on', 'at', 'to',
        'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through',
        'during', 'before', 'after', 'above', 'below', 'between', 'out', 'off',
        'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there',
        'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
        'more', 'most', 'other', 'some', 'such', 'no', 'not', 'only', 'own',
        'same', 'so', 'than', 'too', 'very', 'just', 'because', 'as', 'until',
        'while', 'if', 'or', 'and', 'but', 'nor', 'yet', 'it', 'its', 'this',
        'that', 'these', 'those', 'i', 'me', 'my', 'we', 'our', 'you', 'your',
        'he', 'she', 'they', 'them', 'their', 'what', 'which', 'who',
    }
    return set(w for w in words if w not in stops and len(w) > 2)


def jaccard_similarity(text1, text2):
    """Compute Jaccard similarity between two texts."""
    words1 = normalize_text(text1)
    words2 = normalize_text(text2)
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)


def load_approved_entries():
    """Load all approved entries from the strategy file."""
    entries = []
    if not STRATEGY_FILE.exists():
        return entries
    with open(STRATEGY_FILE) as f:
        for line in f:
            if line.strip():
                e = json.loads(line)
                if e.get('status') == 'approved':
                    eid = e.get('id') or e.get('entry_id') or 'unknown'
                    question = e.get('question') or e.get('title') or ''
                    entries.append({'id': eid, 'question': question})
    return entries


def is_duplicate(question, threshold=SIMILARITY_THRESHOLD):
    """
    Check if a question is a near-duplicate of any approved entry.

    Returns:
        dict with keys:
            is_duplicate: bool
            match_id: str or None (ID of the matching entry)
            match_question: str or None (question text of the match)
            similarity: float (highest similarity score found)
    """
    approved = load_approved_entries()
    best_match = None
    best_sim = 0.0

    for entry in approved:
        sim = jaccard_similarity(question, entry['question'])
        if sim > best_sim:
            best_sim = sim
            best_match = entry

    if best_sim >= threshold and best_match:
        return {
            'is_duplicate': True,
            'match_id': best_match['id'],
            'match_question': best_match['question'],
            'similarity': round(best_sim, 3),
        }

    return {
        'is_duplicate': False,
        'match_id': None,
        'match_question': None,
        'similarity': round(best_sim, 3),
    }


def check_batch(input_path, output_path=None):
    """
    Check a batch of new entries (JSONL) against existing approved entries.
    Writes non-duplicate entries to output_path if specified.
    Returns (kept, skipped) counts and skip details.
    """
    approved = load_approved_entries()
    kept = []
    skipped = []

    with open(input_path) as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            question = entry.get('question') or entry.get('title') or ''

            best_sim = 0.0
            best_match = None
            for a in approved:
                sim = jaccard_similarity(question, a['question'])
                if sim > best_sim:
                    best_sim = sim
                    best_match = a

            if best_sim >= SIMILARITY_THRESHOLD and best_match:
                eid = entry.get('id') or entry.get('entry_id') or 'unknown'
                skipped.append({
                    'id': eid,
                    'question': question[:120],
                    'match_id': best_match['id'],
                    'match_question': best_match['question'][:120],
                    'similarity': round(best_sim, 3),
                })
            else:
                kept.append(entry)

    if output_path and kept:
        with open(output_path, 'w') as f:
            for entry in kept:
                f.write(json.dumps(entry) + '\n')

    return len(kept), skipped


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Check for duplicate canasta strategy entries')
    parser.add_argument('--question', type=str, help='Single question to check')
    parser.add_argument('--batch', type=str, help='JSONL file of new entries to check')
    parser.add_argument('--output', type=str, help='Output path for filtered entries (batch mode)')
    parser.add_argument('--threshold', type=float, default=SIMILARITY_THRESHOLD,
                        help=f'Similarity threshold (default: {SIMILARITY_THRESHOLD})')
    args = parser.parse_args()

    if args.question:
        result = is_duplicate(args.question, threshold=args.threshold)
        if result['is_duplicate']:
            print(f"⚠️  DUPLICATE (similarity: {result['similarity']:.0%})")
            print(f"   Matches: [{result['match_id']}] {result['match_question'][:120]}")
        else:
            print(f"✅ UNIQUE (best match: {result['similarity']:.0%})")
        sys.exit(1 if result['is_duplicate'] else 0)

    elif args.batch:
        kept, skipped = check_batch(args.batch, args.output, )
        print(f"Results: {kept} kept, {len(skipped)} skipped as duplicates")
        for s in skipped:
            print(f"  ⚠️  [{s['id']}] → duplicate of [{s['match_id']}] ({s['similarity']:.0%})")
        if args.output:
            print(f"\nFiltered entries saved to: {args.output}")

    else:
        parser.print_help()
