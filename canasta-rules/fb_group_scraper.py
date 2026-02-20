#!/usr/bin/env python3
"""
Facebook Group Scraper using Chrome DevTools Protocol.
Connects to the existing OpenClaw browser instance.
"""

import asyncio
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

# Local imports
from fb_scraper import (
    create_strategy_entry, 
    save_strategy, 
    is_canasta_related,
    post_exists,
    get_next_id,
    STRATEGY_FILE
)

try:
    import websockets
except ImportError:
    print("Installing websockets...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "websockets", "-q"])
    import websockets

try:
    import httpx
except ImportError:
    print("Installing httpx...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "httpx", "-q"])
    import httpx

CDP_PORT = 18800
CDP_HTTP = f"http://127.0.0.1:{CDP_PORT}"

def count_entries():
    """Count entries in strategy.jsonl"""
    if not STRATEGY_FILE.exists():
        return 0
    with open(STRATEGY_FILE) as f:
        return sum(1 for line in f if line.strip())

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


class FacebookScraper:
    def __init__(self):
        self.ws = None
        self.msg_id = 0
        self.posts_scanned = 0
        self.entries_added = 0
        self.errors = []
        
    async def connect(self):
        """Connect to the browser via CDP."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{CDP_HTTP}/json")
            pages = resp.json()
            
        fb_page = None
        for page in pages:
            if 'modernamericancanasta' in page.get('url', ''):
                fb_page = page
                break
        
        if not fb_page:
            raise Exception("Facebook group tab not found")
            
        ws_url = fb_page['webSocketDebuggerUrl']
        print(f"Connecting to: {ws_url}")
        self.ws = await websockets.connect(ws_url)
        return True
        
    async def send_command(self, method, params=None):
        """Send a CDP command and wait for result."""
        self.msg_id += 1
        msg = {"id": self.msg_id, "method": method, "params": params or {}}
        await self.ws.send(json.dumps(msg))
        
        while True:
            response = await self.ws.recv()
            data = json.loads(response)
            if data.get("id") == self.msg_id:
                return data.get("result", {})
                
    async def evaluate(self, expression):
        """Evaluate JavaScript in the page."""
        result = await self.send_command("Runtime.evaluate", {
            "expression": expression,
            "returnByValue": True,
            "awaitPromise": True
        })
        return result.get("result", {}).get("value")
        
    async def scroll_and_load(self, scroll_count=30, delay=3):
        """Scroll down to load posts."""
        print(f"Scrolling {scroll_count} times with {delay}s delays...")
        
        for i in range(scroll_count):
            await self.evaluate("window.scrollBy(0, 2000)")
            print(f"  Scroll {i+1}/{scroll_count}...")
            await asyncio.sleep(delay)
            
        print("Scrolling complete, waiting for final load...")
        await asyncio.sleep(5)
        
    async def extract_posts(self):
        """Extract all posts from the page."""
        js_code = '''
        (() => {
            const posts = [];
            const feed = document.querySelector('[role="feed"]');
            if (!feed) return JSON.stringify({error: "Feed not found"});
            
            const commentButtons = feed.querySelectorAll('button[aria-label*="comments"], div[aria-label*="comments"]');
            
            commentButtons.forEach((btn, idx) => {
                try {
                    let container = btn.closest('[role="article"]') || btn.parentElement.parentElement.parentElement.parentElement.parentElement;
                    if (!container) return;
                    
                    const authorLink = container.querySelector('h2 a, h3 a, [data-ad-rendering-role="profile_name"] a');
                    const author = authorLink ? authorLink.textContent.trim() : 'Unknown';
                    
                    const textContainers = container.querySelectorAll('[data-ad-rendering-role="story_message"], [dir="auto"]');
                    let text = '';
                    textContainers.forEach(t => {
                        if (t.textContent.length > 20) {
                            text = t.textContent.trim();
                        }
                    });
                    
                    const badgeEl = container.querySelector('[aria-label*="contributor"], [aria-label*="Admin"]');
                    const badge = badgeEl ? badgeEl.textContent.trim() : null;
                    
                    const timeLinks = container.querySelectorAll('a[href*="/posts/"]');
                    let postUrl = '';
                    let postId = '';
                    timeLinks.forEach(tl => {
                        const href = tl.getAttribute('href');
                        if (href && href.includes('/posts/')) {
                            postUrl = href;
                            const match = href.match(/posts\\/(\\d+)/);
                            if (match) postId = match[1];
                        }
                    });
                    
                    const dateEl = container.querySelector('a[href*="/posts/"] span, [aria-label*="ago"]');
                    const dateText = dateEl ? dateEl.textContent : '';
                    
                    const commentMatch = btn.textContent.match(/(\\d+)\\s*comment/i);
                    const commentCount = commentMatch ? parseInt(commentMatch[1]) : 0;
                    
                    if (text && postId) {
                        posts.push({
                            idx: idx,
                            post_id: postId,
                            author: author,
                            badge: badge,
                            text: text.substring(0, 1000),
                            date: dateText,
                            url: 'https://www.facebook.com' + postUrl.split('?')[0],
                            comment_count: commentCount
                        });
                    }
                } catch(e) {}
            });
            
            return JSON.stringify(posts);
        })()
        '''
        
        result = await self.evaluate(js_code)
        if result:
            try:
                return json.loads(result)
            except:
                return []
        return []
        
    async def get_post_comments(self, post_url):
        """Navigate to a post and extract comments."""
        await self.send_command("Page.navigate", {"url": post_url})
        await asyncio.sleep(4)
        
        # Click "View more comments" buttons
        for _ in range(3):
            await self.evaluate('''
                document.querySelectorAll('div[role="button"]').forEach(b => {
                    if (b.textContent.includes('View more') || b.textContent.includes('more comment')) {
                        b.click();
                    }
                });
            ''')
            await asyncio.sleep(1)
        
        js_code = '''
        (() => {
            const comments = [];
            const commentArticles = document.querySelectorAll('div[aria-label*="Comment by"], article[aria-label*="Comment by"]');
            
            commentArticles.forEach(c => {
                try {
                    const label = c.getAttribute('aria-label') || '';
                    const authorMatch = label.match(/Comment by ([^\\d]+)/);
                    const author = authorMatch ? authorMatch[1].trim() : '';
                    
                    const badgeEl = c.querySelector('[aria-label*="contributor"], a[href*="badge"]');
                    const badge = badgeEl ? 'top_contributor' : null;
                    
                    const textEl = c.querySelector('[dir="auto"]');
                    const text = textEl ? textEl.textContent.trim() : '';
                    
                    const reactBtn = c.querySelector('div[aria-label*="reaction"]');
                    const reactMatch = reactBtn ? reactBtn.getAttribute('aria-label').match(/(\\d+)/) : null;
                    const reactions = reactMatch ? parseInt(reactMatch[1]) : 0;
                    
                    if (author && text) {
                        comments.push({
                            author: author,
                            badge: badge,
                            text: text.substring(0, 500),
                            reactions: reactions
                        });
                    }
                } catch(e) {}
            });
            
            return JSON.stringify(comments);
        })()
        '''
        
        result = await self.evaluate(js_code)
        try:
            return json.loads(result) if result else []
        except:
            return []
            
    async def process_post(self, post):
        """Process a single post and save if relevant."""
        self.posts_scanned += 1
        
        if post_exists(post['post_id']):
            print(f"  Skipping (duplicate): {post['post_id']}")
            return False
            
        if not is_canasta_related(post['text']):
            print(f"  Skipping (not canasta-related): {post['text'][:50]}...")
            return False
            
        print(f"  Processing: {post['text'][:50]}...")
        
        try:
            comments = await self.get_post_comments(post['url'])
            
            processed_comments = []
            for c in comments:
                c['position'] = classify_position(c['text'])
                processed_comments.append(c)
                
            entry = create_strategy_entry(
                post_id=post['post_id'],
                post_url=post['url'],
                post_date=post.get('date', ''),
                author=post['author'],
                author_badge=post.get('badge'),
                question=post['text'],
                context='',
                responses=processed_comments,
                source='facebook_mac'
            )
            
            if entry:
                save_strategy(entry)
                self.entries_added += 1
                print(f"    Saved! ({len(processed_comments)} comments)")
                return True
            else:
                print(f"    Already exists or not relevant")
                return False
                
        except Exception as e:
            self.errors.append(f"Error processing {post['post_id']}: {str(e)}")
            print(f"    Error: {e}")
            return False
            
    async def run(self, scroll_count=30):
        """Main scraping routine."""
        print("="*60)
        print("Facebook Canasta Group Scraper")
        print(f"Starting at: {datetime.now()}")
        print("="*60)
        
        initial_count = count_entries()
        print(f"Initial entries: {initial_count}")
        
        try:
            await self.connect()
            print("Connected to browser!")
            
            await self.scroll_and_load(scroll_count=scroll_count)
            
            print("\nExtracting posts from feed...")
            posts = await self.extract_posts()
            print(f"Found {len(posts)} posts")
            
            group_url = "https://www.facebook.com/groups/modernamericancanasta"
            
            for i, post in enumerate(posts):
                print(f"\n[{i+1}/{len(posts)}] Post ID: {post['post_id']}")
                await self.process_post(post)
                
                await self.send_command("Page.navigate", {"url": group_url})
                await asyncio.sleep(2)
                
        except Exception as e:
            self.errors.append(f"Fatal error: {str(e)}")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            if self.ws:
                await self.ws.close()
                
        return {
            "posts_scanned": self.posts_scanned,
            "entries_added": self.entries_added,
            "errors": self.errors,
            "total_entries": count_entries()
        }


async def main():
    scraper = FacebookScraper()
    results = await scraper.run(scroll_count=30)
    
    print("\n" + "="*60)
    print("SCRAPING COMPLETE")
    print("="*60)
    print(f"Posts scanned: {results['posts_scanned']}")
    print(f"New entries added: {results['entries_added']}")
    print(f"Total entries in database: {results['total_entries']}")
    if results['errors']:
        print(f"Errors: {len(results['errors'])}")
        for e in results['errors'][:5]:
            print(f"  - {e}")
            
    with open(Path(__file__).parent / 'scrape_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    return results


if __name__ == "__main__":
    asyncio.run(main())
