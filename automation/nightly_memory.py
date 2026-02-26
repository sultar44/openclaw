#!/usr/bin/env python3
"""
Nightly Memory Digest
Scans today's session transcripts and extracts key content for memory files.
Output: markdown summary ready for memory/YYYY-MM-DD.md
"""
import json, os, sys
from datetime import datetime, date
from pathlib import Path

SESSIONS_DIR = Path(os.path.expanduser("~/.openclaw/agents/main/sessions"))

def get_sessions_for_date(target_date):
    """Find session files modified on the target date."""
    sessions = []
    for f in SESSIONS_DIR.glob("*.jsonl"):
        if '.deleted.' in f.name:
            continue
        mtime = datetime.fromtimestamp(f.stat().st_mtime).date()
        if mtime == target_date:
            sessions.append(f)
    return sessions

def extract_messages(session_file, max_msgs=200):
    """Extract user and assistant text messages from a session JSONL."""
    messages = []
    try:
        with open(session_file) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    if d.get("type") != "message":
                        continue
                    msg = d.get("message", {})
                    role = msg.get("role", "")
                    if role not in ("user", "assistant"):
                        continue
                    
                    # Extract text content from content list
                    content = msg.get("content", "")
                    text = ""
                    if isinstance(content, str):
                        text = content
                    elif isinstance(content, list):
                        parts = []
                        for part in content:
                            if isinstance(part, dict) and part.get("type") == "text":
                                parts.append(part.get("text", ""))
                        text = "\n".join(parts)
                    
                    if not text or len(text) < 10:
                        continue
                    # Skip noise
                    if text.strip() in ("HEARTBEAT_OK", "NO_REPLY"):
                        continue
                    if "Read HEARTBEAT.md" in text[:60]:
                        continue
                    
                    ts = d.get("timestamp", "")
                    messages.append({
                        "role": role,
                        "text": text[:2000],
                        "ts": ts,
                    })
                    
                    if len(messages) >= max_msgs:
                        break
                except (json.JSONDecodeError, KeyError):
                    continue
    except Exception as e:
        print(f"Error reading {session_file.name}: {e}", file=sys.stderr)
    return messages

def format_for_summary(sessions_data):
    """Format extracted messages for AI processing."""
    output = []
    for session_file, messages in sessions_data:
        if len(messages) < 2:
            continue
        # Count user messages to gauge significance
        user_msgs = [m for m in messages if m["role"] == "user"]
        if not user_msgs:
            continue
        
        output.append(f"\n### Session ({len(messages)} messages, {len(user_msgs)} from user)")
        output.append("---")
        for msg in messages:
            prefix = "USER:" if msg["role"] == "user" else "CHLOE:"
            text = msg["text"][:800]
            output.append(f"{prefix} {text}\n")
    return "\n".join(output)

def main():
    if len(sys.argv) > 1:
        target = date.fromisoformat(sys.argv[1])
    else:
        target = date.today()
    
    sessions = get_sessions_for_date(target)
    print(f"Date: {target} | Sessions found: {len(sessions)}")
    
    if not sessions:
        print("No sessions found.")
        return
    
    sessions_data = []
    for sf in sorted(sessions, key=lambda x: x.stat().st_mtime):
        messages = extract_messages(sf)
        if messages:
            sessions_data.append((sf, messages))
    
    significant = [(sf, msgs) for sf, msgs in sessions_data 
                   if sum(1 for m in msgs if m["role"] == "user") >= 1]
    
    print(f"Sessions with user content: {len(significant)}")
    
    summary = format_for_summary(significant)
    
    outfile = f"/tmp/memory_digest_{target.isoformat()}.md"
    with open(outfile, "w") as f:
        f.write(f"# Session Transcripts for {target}\n\n")
        f.write(summary)
    
    size = os.path.getsize(outfile)
    print(f"Output: {outfile} ({size:,} bytes)")
    
    # Print first portion for the agent
    if "--preview" in sys.argv:
        print("\n" + "=" * 60)
        print(summary[:8000])

if __name__ == "__main__":
    main()
