#!/usr/bin/env python3
"""
Strategy Review Web App
A simple local web interface to approve/reject strategy entries.
Run: python review_app.py
Then open: http://localhost:8765
"""

import json
import http.server
import socketserver
from pathlib import Path
from datetime import datetime
from urllib.parse import parse_qs, urlparse

PORT = 8765
STRATEGY_FILE = Path(__file__).parent / 'strategy.jsonl'
BACKUP_DIR = Path(__file__).parent / 'backups'


def load_entries():
    entries = []
    if STRATEGY_FILE.exists():
        with open(STRATEGY_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
    return entries


def save_entries(entries):
    BACKUP_DIR.mkdir(exist_ok=True)
    if STRATEGY_FILE.exists():
        backup_name = f"strategy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jsonl"
        import shutil
        shutil.copy(STRATEGY_FILE, BACKUP_DIR / backup_name)
    
    with open(STRATEGY_FILE, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')


def update_entry(entry_id, new_status, new_question=None, new_answer=None):
    entries = load_entries()
    for e in entries:
        if e.get('id') == entry_id:
            e['status'] = new_status
            e['reviewed_at'] = datetime.now().isoformat()
            if new_question is not None:
                # Store in question field, or title if that's what exists
                if 'question' in e:
                    e['question'] = new_question
                else:
                    e['title'] = new_question
            if new_answer is not None:
                # Store answer in recommendation field (primary)
                e['recommendation'] = new_answer
                # Also update strategy to match for consistency
                e['strategy'] = new_answer
            break
    save_entries(entries)


def get_html_template():
    return '''<!DOCTYPE html>
<html>
<head>
    <title>Canasta Strategy Review</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }
        .header {
            background: #2c5530;
            color: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .header h1 { margin: 0 0 10px 0; }
        .stats {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 10px;
        }
        .stat { text-align: center; }
        .stat-num { font-size: 24px; font-weight: bold; }
        .stat-label { font-size: 12px; opacity: 0.8; }
        .card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .entry-id {
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }
        .source {
            display: inline-block;
            background: #e3f2fd;
            color: #1565c0;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin-bottom: 15px;
        }
        .question-input {
            width: 100%;
            min-height: 80px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            font-family: inherit;
            line-height: 1.4;
            resize: vertical;
            margin-bottom: 15px;
            color: #333;
        }
        .question-input:focus {
            outline: none;
            border-color: #2c5530;
        }
        .section-label {
            font-size: 11px;
            text-transform: uppercase;
            color: #999;
            margin-bottom: 5px;
        }
        .answer-input {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 15px;
            font-family: inherit;
            line-height: 1.6;
            resize: vertical;
            margin-bottom: 15px;
        }
        .answer-input:focus {
            outline: none;
            border-color: #2c5530;
        }
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
        }
        .tag {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
        }
        .buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
        }
        button {
            padding: 15px 40px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            transition: transform 0.1s, box-shadow 0.1s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        button:active { transform: translateY(0); }
        .approve { background: #4caf50; color: white; }
        .reject { background: #f44336; color: white; }
        .skip { background: #9e9e9e; color: white; }
        .done {
            text-align: center;
            padding: 60px 20px;
        }
        .done h2 { color: #4caf50; }
        .nav-info {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 15px;
        }
        .post-date {
            color: #666;
            font-size: 13px;
            margin-bottom: 10px;
        }
        .hint {
            font-size: 12px;
            color: #888;
            margin-top: -10px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Canasta Strategy Review</h1>
        <div class="stats">
            <div class="stat">
                <div class="stat-num">%%PENDING%%</div>
                <div class="stat-label">Pending</div>
            </div>
            <div class="stat">
                <div class="stat-num">%%APPROVED%%</div>
                <div class="stat-label">Approved</div>
            </div>
            <div class="stat">
                <div class="stat-num">%%REJECTED%%</div>
                <div class="stat-label">Rejected</div>
            </div>
        </div>
    </div>
    %%CONTENT%%
</body>
</html>'''


def get_entry_template():
    return '''
    <div class="nav-info">Entry %%CURRENT%% of %%TOTAL%% pending</div>
    <div class="card">
        <div class="entry-id">%%ID%%</div>
        <span class="source">%%SOURCE%%</span>
        %%POST_DATE%%
        
        <div class="section-label">Question</div>
        <textarea class="question-input" id="question">%%QUESTION%%</textarea>
        
        <div class="section-label">Answer</div>
        <textarea class="answer-input" id="answer">%%ANSWER%%</textarea>
        <div class="hint">Edit if needed - changes are saved when you approve</div>
        
        <div class="section-label">Tags</div>
        <div class="tags">%%TAGS%%</div>
        
        <div class="buttons">
            <button class="reject" onclick="submitAction('rejected')">Reject</button>
            <button class="skip" onclick="location.href='/?skip=%%ID%%'">Skip</button>
            <button class="approve" onclick="submitAction('approved')">Approve</button>
        </div>
    </div>
    
    <form id="reviewForm" method="POST" action="/update?id=%%ID%%&status=approved">
        <input type="hidden" name="question" id="questionHidden">
        <input type="hidden" name="answer" id="answerHidden">
    </form>
    
    <script>
    function submitAction(status) {
        const form = document.getElementById('reviewForm');
        form.action = '/update?id=%%ID%%&status=' + status;
        document.getElementById('questionHidden').value = document.getElementById('question').value;
        document.getElementById('answerHidden').value = document.getElementById('answer').value;
        form.submit();
    }
    </script>
'''


def get_done_template():
    return '''
    <div class="card done">
        <h2>All Done!</h2>
        <p>No more pending entries to review.</p>
        <p style="margin-top: 20px;">
            <a href="/" style="color: #2c5530;">Refresh</a>
        </p>
    </div>
'''


class ReviewHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/':
            self.send_review_page(parsed.query)
        else:
            self.send_error(404)
    
    def do_POST(self):
        parsed = urlparse(self.path)
        
        if parsed.path == '/update':
            params = parse_qs(parsed.query)
            entry_id = params.get('id', [None])[0]
            status = params.get('status', [None])[0]
            
            # Read the form data for the answer
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # Parse form data
            new_question = None
            new_answer = None
            if post_data:
                from urllib.parse import unquote_plus
                for part in post_data.split('&'):
                    if '=' in part:
                        key, value = part.split('=', 1)
                        if key == 'question':
                            new_question = unquote_plus(value)
                        elif key == 'answer':
                            new_answer = unquote_plus(value)
            
            if entry_id and status:
                update_entry(entry_id, status, new_question, new_answer)
            
            # Redirect back to main page
            self.send_response(303)
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_error(404)
    
    def send_review_page(self, query):
        entries = load_entries()
        
        # Count stats - include entries with empty/missing status as pending
        pending = [e for e in entries if e.get('status') == 'pending']
        approved_count = len([e for e in entries if e.get('status') == 'approved'])
        rejected_count = len([e for e in entries if e.get('status') == 'rejected'])
        
        # Handle skip
        params = parse_qs(query)
        skip_id = params.get('skip', [None])[0]
        
        if skip_id and len(pending) > 1:
            pending = [e for e in pending if e['id'] != skip_id] + [e for e in pending if e['id'] == skip_id]
        
        if pending:
            entry = pending[0]
            
            # Build tags HTML
            tags_html = ''.join(f'<span class="tag">{t}</span>' for t in entry.get('tags', []))
            
            # Get the answer - prefer recommendation, fall back to strategy
            answer = entry.get('recommendation', '') or entry.get('strategy', '')
            # Escape for HTML textarea
            answer = answer.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            post_date = ''
            if entry.get('post_date'):
                post_date = f'<div class="post-date">{entry["post_date"]}</div>'
            
            question = entry.get('question', entry.get('title', 'No title'))
            # Escape for HTML textarea
            question = question.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            content = get_entry_template()
            content = content.replace('%%ID%%', entry['id'])
            content = content.replace('%%SOURCE%%', entry.get('source', 'unknown'))
            content = content.replace('%%QUESTION%%', question)
            content = content.replace('%%ANSWER%%', answer)
            content = content.replace('%%TAGS%%', tags_html)
            content = content.replace('%%POST_DATE%%', post_date)
            content = content.replace('%%CURRENT%%', '1')
            content = content.replace('%%TOTAL%%', str(len(pending)))
        else:
            content = get_done_template()
        
        html = get_html_template()
        html = html.replace('%%PENDING%%', str(len(pending)))
        html = html.replace('%%APPROVED%%', str(approved_count))
        html = html.replace('%%REJECTED%%', str(rejected_count))
        html = html.replace('%%CONTENT%%', content)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    print(f"\nCanasta Strategy Review")
    print(f"=" * 40)
    print(f"Open in browser: http://localhost:{PORT}")
    print(f"Press Ctrl+C to stop\n")
    
    class ThreadedServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True
    
    with ThreadedServer(("", PORT), ReviewHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
