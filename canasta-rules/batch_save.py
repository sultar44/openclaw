#!/usr/bin/env python3
"""
Batch save posts from a JSON file.
Usage: python3 batch_save.py < posts.json
"""
import json
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from extract_post import parse_and_save_post

def main():
    data = json.load(sys.stdin)
    posts = data if isinstance(data, list) else [data]
    
    saved = 0
    skipped = 0
    duplicates = 0
    not_canasta = 0
    errors = []
    
    for post in posts:
        try:
            result = parse_and_save_post(post)
            if result.get('saved'):
                saved += 1
                print(f"✓ Saved {result.get('post_id')} as {result.get('entry_id')}")
            elif result.get('duplicate'):
                duplicates += 1
            elif result.get('not_canasta'):
                not_canasta += 1
            else:
                skipped += 1
        except Exception as e:
            errors.append(str(e))
    
    print(f"\n=== Summary ===")
    print(f"Saved: {saved}")
    print(f"Duplicates: {duplicates}")
    print(f"Not canasta: {not_canasta}")
    print(f"Skipped: {skipped}")
    if errors:
        print(f"Errors: {len(errors)}")
        for e in errors[:5]:
            print(f"  - {e}")

if __name__ == "__main__":
    main()
