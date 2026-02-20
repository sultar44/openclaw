#!/usr/bin/env python3
"""
Strategy Entry Management Tool
Approve, reject, or list pending strategy entries.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

STRATEGY_FILE = Path(__file__).parent / 'strategy.jsonl'
BACKUP_DIR = Path(__file__).parent / 'backups'


def load_entries():
    """Load all strategy entries."""
    entries = []
    if STRATEGY_FILE.exists():
        with open(STRATEGY_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
    return entries


def save_entries(entries):
    """Save all entries back to file."""
    BACKUP_DIR.mkdir(exist_ok=True)
    
    # Backup first
    if STRATEGY_FILE.exists():
        backup_name = f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        STRATEGY_FILE.rename(BACKUP_DIR / backup_name)
    
    with open(STRATEGY_FILE, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')


def list_pending():
    """List all pending entries."""
    entries = load_entries()
    pending = [e for e in entries if e.get('status') == 'pending']
    
    if not pending:
        print("No pending entries.")
        return
    
    print(f"\n{'='*60}")
    print(f"PENDING STRATEGY ENTRIES ({len(pending)} total)")
    print(f"{'='*60}\n")
    
    for e in pending:
        print(f"ID: {e['id']}")
        print(f"Source: {e.get('source', 'unknown')}")
        if e.get('post_date'):
            print(f"Date: {e['post_date']}")
        print(f"Question: {e.get('question', e.get('title', 'N/A'))[:80]}")
        if e.get('recommendation'):
            print(f"Recommendation: {e['recommendation'][:80]}")
        print(f"Tags: {', '.join(e.get('tags', []))}")
        print("-" * 40)


def list_all():
    """List all entries with status counts."""
    entries = load_entries()
    
    by_status = {}
    for e in entries:
        status = e.get('status', 'unknown')
        by_status[status] = by_status.get(status, 0) + 1
    
    by_source = {}
    for e in entries:
        source = e.get('source', 'unknown')
        by_source[source] = by_source.get(source, 0) + 1
    
    print(f"\nTotal entries: {len(entries)}")
    print(f"\nBy status:")
    for status, count in sorted(by_status.items()):
        print(f"  {status}: {count}")
    print(f"\nBy source:")
    for source, count in sorted(by_source.items()):
        print(f"  {source}: {count}")


def approve(entry_id):
    """Approve an entry by ID."""
    entries = load_entries()
    found = False
    
    for e in entries:
        if e['id'] == entry_id:
            e['status'] = 'approved'
            e['reviewed_at'] = datetime.now().isoformat()
            found = True
            print(f"✓ Approved: {entry_id}")
            break
    
    if found:
        save_entries(entries)
    else:
        print(f"Entry not found: {entry_id}")


def reject(entry_id):
    """Reject an entry by ID."""
    entries = load_entries()
    found = False
    
    for e in entries:
        if e['id'] == entry_id:
            e['status'] = 'rejected'
            e['reviewed_at'] = datetime.now().isoformat()
            found = True
            print(f"✗ Rejected: {entry_id}")
            break
    
    if found:
        save_entries(entries)
    else:
        print(f"Entry not found: {entry_id}")


def remove(entry_id):
    """Permanently remove an entry by ID."""
    entries = load_entries()
    original_count = len(entries)
    entries = [e for e in entries if e['id'] != entry_id]
    
    if len(entries) < original_count:
        save_entries(entries)
        print(f"✗ Removed: {entry_id}")
    else:
        print(f"Entry not found: {entry_id}")


def approve_all_from_source(source):
    """Approve all entries from a specific source."""
    entries = load_entries()
    count = 0
    
    for e in entries:
        if e.get('source') == source and e.get('status') == 'pending':
            e['status'] = 'approved'
            e['reviewed_at'] = datetime.now().isoformat()
            count += 1
    
    if count > 0:
        save_entries(entries)
        print(f"✓ Approved {count} entries from {source}")
    else:
        print(f"No pending entries from {source}")


def show_entry(entry_id):
    """Show full details of an entry."""
    entries = load_entries()
    
    for e in entries:
        if e['id'] == entry_id:
            print(json.dumps(e, indent=2))
            return
    
    print(f"Entry not found: {entry_id}")


def generate_report():
    """Generate a report of all pending entries for email."""
    entries = load_entries()
    pending = [e for e in entries if e.get('status') == 'pending']
    
    if not pending:
        return "No pending strategy entries to review."
    
    report = []
    report.append(f"CANASTA STRATEGY ENTRIES - PENDING REVIEW")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} EST")
    report.append(f"Total pending: {len(pending)}")
    report.append("=" * 60)
    report.append("")
    
    # Group by source
    by_source = {}
    for e in pending:
        source = e.get('source', 'unknown')
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(e)
    
    for source, source_entries in by_source.items():
        report.append(f"\n--- {source.upper()} ({len(source_entries)} entries) ---\n")
        
        for e in source_entries:
            report.append(f"[{e['id']}]")
            if e.get('question'):
                report.append(f"Q: {e['question'][:100]}...")
            elif e.get('title'):
                report.append(f"Title: {e['title']}")
            if e.get('strategy'):
                report.append(f"Strategy: {e['strategy'][:100]}...")
            if e.get('recommendation'):
                report.append(f"Recommendation: {e['recommendation'][:100]}...")
            report.append(f"Tags: {', '.join(e.get('tags', []))}")
            report.append("")
    
    report.append("=" * 60)
    report.append("To approve: python manage_strategy.py approve <ID>")
    report.append("To reject: python manage_strategy.py reject <ID>")
    report.append("To remove: python manage_strategy.py remove <ID>")
    
    return "\n".join(report)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_strategy.py pending       - List pending entries")
        print("  python manage_strategy.py list          - List all entries summary")
        print("  python manage_strategy.py show <ID>     - Show entry details")
        print("  python manage_strategy.py approve <ID>  - Approve entry")
        print("  python manage_strategy.py reject <ID>   - Reject entry")
        print("  python manage_strategy.py remove <ID>   - Remove entry permanently")
        print("  python manage_strategy.py approve-source <source> - Approve all from source")
        print("  python manage_strategy.py report        - Generate email report")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'pending':
        list_pending()
    elif cmd == 'list':
        list_all()
    elif cmd == 'show' and len(sys.argv) > 2:
        show_entry(sys.argv[2])
    elif cmd == 'approve' and len(sys.argv) > 2:
        approve(sys.argv[2])
    elif cmd == 'reject' and len(sys.argv) > 2:
        reject(sys.argv[2])
    elif cmd == 'remove' and len(sys.argv) > 2:
        remove(sys.argv[2])
    elif cmd == 'approve-source' and len(sys.argv) > 2:
        approve_all_from_source(sys.argv[2])
    elif cmd == 'report':
        print(generate_report())
    else:
        print(f"Unknown command: {cmd}")
