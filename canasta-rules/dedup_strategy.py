#!/usr/bin/env python3
"""
Strategy Deduplication System
Uses sentence embeddings to detect semantically similar entries.
"""

import json
import os
import sys
import pickle
import numpy as np
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer

STRATEGY_FILE = Path(__file__).parent / "strategy.jsonl"
EMBEDDINGS_FILE = Path(__file__).parent / "strategy_embeddings.pkl"
SIMILARITY_THRESHOLD = 0.85  # 85% similarity = potential duplicate

# Load model (cached after first load)
_model = None

def get_model():
    global _model
    if _model is None:
        print("Loading embedding model (first time may take a moment)...")
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def load_strategies():
    """Load all strategies from JSONL file."""
    strategies = []
    if STRATEGY_FILE.exists():
        with open(STRATEGY_FILE, 'r') as f:
            for i, line in enumerate(f):
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        entry['_line_num'] = i + 1
                        strategies.append(entry)
                    except json.JSONDecodeError:
                        pass
    return strategies

def get_text_for_embedding(entry):
    """Extract text to embed from an entry."""
    parts = []
    if entry.get('title'):
        parts.append(entry['title'])
    if entry.get('question'):
        parts.append(entry['question'])
    if entry.get('recommendation'):
        parts.append(entry['recommendation'])
    if entry.get('strategy'):
        parts.append(entry['strategy'])
    return " ".join(parts)

def load_embeddings():
    """Load cached embeddings if they exist."""
    if EMBEDDINGS_FILE.exists():
        with open(EMBEDDINGS_FILE, 'rb') as f:
            return pickle.load(f)
    return {}

def save_embeddings(embeddings):
    """Save embeddings cache."""
    with open(EMBEDDINGS_FILE, 'wb') as f:
        pickle.dump(embeddings, f)

def generate_embeddings(strategies, force=False):
    """Generate embeddings for strategies that don't have them."""
    model = get_model()
    embeddings = {} if force else load_embeddings()
    
    texts_to_embed = []
    indices_to_embed = []
    
    for i, entry in enumerate(strategies):
        entry_id = entry.get('id', f"line_{entry.get('_line_num', i)}")
        text = get_text_for_embedding(entry)
        
        if entry_id not in embeddings or force:
            texts_to_embed.append(text)
            indices_to_embed.append((i, entry_id))
    
    if texts_to_embed:
        print(f"Generating embeddings for {len(texts_to_embed)} entries...")
        new_embeddings = model.encode(texts_to_embed, show_progress_bar=len(texts_to_embed) > 10)
        
        for (i, entry_id), embedding in zip(indices_to_embed, new_embeddings):
            embeddings[entry_id] = embedding
        
        save_embeddings(embeddings)
        print(f"Embeddings saved to {EMBEDDINGS_FILE}")
    
    return embeddings

def cosine_similarity(a, b):
    """Calculate cosine similarity between two vectors."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_duplicates(strategies=None, threshold=SIMILARITY_THRESHOLD):
    """Find potential duplicate entries based on semantic similarity."""
    if strategies is None:
        strategies = load_strategies()
    
    embeddings = generate_embeddings(strategies)
    
    # Build list of (entry_id, embedding) pairs
    entries_with_embeddings = []
    for entry in strategies:
        entry_id = entry.get('id', f"line_{entry.get('_line_num', 0)}")
        if entry_id in embeddings:
            entries_with_embeddings.append((entry, embeddings[entry_id]))
    
    # Find similar pairs
    duplicates = []
    checked = set()
    
    print(f"Checking {len(entries_with_embeddings)} entries for duplicates (threshold: {threshold*100:.0f}%)...")
    
    for i, (entry1, emb1) in enumerate(entries_with_embeddings):
        for j, (entry2, emb2) in enumerate(entries_with_embeddings[i+1:], i+1):
            pair_key = (i, j)
            if pair_key in checked:
                continue
            checked.add(pair_key)
            
            sim = cosine_similarity(emb1, emb2)
            if sim >= threshold:
                duplicates.append({
                    'similarity': sim,
                    'entry1': entry1,
                    'entry2': entry2
                })
    
    # Sort by similarity (highest first)
    duplicates.sort(key=lambda x: x['similarity'], reverse=True)
    return duplicates

def check_new_entry(text, threshold=SIMILARITY_THRESHOLD):
    """Check if a new entry is similar to existing entries."""
    strategies = load_strategies()
    embeddings = generate_embeddings(strategies)
    model = get_model()
    
    new_embedding = model.encode([text])[0]
    
    similar = []
    for entry in strategies:
        entry_id = entry.get('id', f"line_{entry.get('_line_num', 0)}")
        if entry_id in embeddings:
            sim = cosine_similarity(new_embedding, embeddings[entry_id])
            if sim >= threshold:
                similar.append({
                    'similarity': sim,
                    'entry': entry
                })
    
    similar.sort(key=lambda x: x['similarity'], reverse=True)
    return similar

def print_entry_short(entry, max_len=80):
    """Print a shortened version of an entry."""
    # Try various text fields
    text = entry.get('recommendation') or entry.get('strategy') or entry.get('question') or entry.get('title') or 'No text'
    rec = text[:max_len]
    if len(text) > max_len:
        rec += "..."
    return rec

def cmd_find_duplicates(args):
    """Find and display duplicate entries."""
    threshold = float(args[0]) if args else SIMILARITY_THRESHOLD
    duplicates = find_duplicates(threshold=threshold)
    
    if not duplicates:
        print(f"\n✓ No duplicates found above {threshold*100:.0f}% similarity threshold.")
        return
    
    print(f"\n{'='*70}")
    print(f"POTENTIAL DUPLICATES FOUND: {len(duplicates)}")
    print(f"{'='*70}\n")
    
    for i, dup in enumerate(duplicates[:20], 1):  # Show top 20
        print(f"--- Match #{i} ({dup['similarity']*100:.1f}% similar) ---")
        e1, e2 = dup['entry1'], dup['entry2']
        print(f"  Entry 1 [{e1.get('id', 'no-id')}] ({e1.get('source', 'unknown')}):")
        print(f"    {print_entry_short(e1)}")
        print(f"  Entry 2 [{e2.get('id', 'no-id')}] ({e2.get('source', 'unknown')}):")
        print(f"    {print_entry_short(e2)}")
        print()
    
    if len(duplicates) > 20:
        print(f"... and {len(duplicates) - 20} more potential duplicates")

def cmd_check(args):
    """Check if text is similar to existing entries."""
    if not args:
        print("Usage: dedup_strategy.py check \"text to check\"")
        return
    
    text = " ".join(args)
    similar = check_new_entry(text)
    
    if not similar:
        print(f"\n✓ No similar entries found (threshold: {SIMILARITY_THRESHOLD*100:.0f}%)")
        return
    
    print(f"\n{'='*70}")
    print(f"SIMILAR ENTRIES FOUND: {len(similar)}")
    print(f"{'='*70}\n")
    
    for i, match in enumerate(similar[:5], 1):
        entry = match['entry']
        print(f"--- Match #{i} ({match['similarity']*100:.1f}% similar) ---")
        print(f"  ID: {entry.get('id', 'no-id')} | Source: {entry.get('source', 'unknown')}")
        print(f"  {print_entry_short(entry, 120)}")
        print()

def cmd_rebuild(args):
    """Rebuild all embeddings from scratch."""
    print("Rebuilding all embeddings...")
    strategies = load_strategies()
    generate_embeddings(strategies, force=True)
    print(f"✓ Generated embeddings for {len(strategies)} entries")

def cmd_stats(args):
    """Show statistics about the strategy database."""
    strategies = load_strategies()
    embeddings = load_embeddings()
    
    sources = {}
    statuses = {}
    for entry in strategies:
        src = entry.get('source', 'unknown')
        status = entry.get('status', 'unknown')
        sources[src] = sources.get(src, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
    
    print(f"\n{'='*50}")
    print("STRATEGY DATABASE STATS")
    print(f"{'='*50}")
    print(f"Total entries: {len(strategies)}")
    print(f"Entries with embeddings: {len(embeddings)}")
    print(f"\nBy source:")
    for src, count in sorted(sources.items(), key=lambda x: -x[1]):
        print(f"  {src}: {count}")
    print(f"\nBy status:")
    for status, count in sorted(statuses.items(), key=lambda x: -x[1]):
        print(f"  {status}: {count}")

def main():
    if len(sys.argv) < 2:
        print("Strategy Deduplication System")
        print("-" * 40)
        print("Commands:")
        print("  find [threshold]  - Find duplicate entries (default threshold: 0.85)")
        print("  check \"text\"      - Check if text is similar to existing entries")
        print("  rebuild           - Rebuild all embeddings from scratch")
        print("  stats             - Show database statistics")
        return
    
    cmd = sys.argv[1].lower()
    args = sys.argv[2:]
    
    if cmd == 'find':
        cmd_find_duplicates(args)
    elif cmd == 'check':
        cmd_check(args)
    elif cmd == 'rebuild':
        cmd_rebuild(args)
    elif cmd == 'stats':
        cmd_stats(args)
    else:
        print(f"Unknown command: {cmd}")

if __name__ == "__main__":
    main()
