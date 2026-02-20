#!/usr/bin/env python3
"""
Scrape session script - processes extracted Facebook post data
"""

import sys
sys.path.insert(0, '/Users/ramongonzalez/.openclaw/workspace/canasta-rules')

from fb_scraper import create_strategy_entry, save_entry, count_entries, is_canasta_related

# Track stats
initial_count = count_entries()
posts_scanned = 0
entries_added = 0
errors = []

# Extracted posts from the Facebook group snapshot
posts_data = [
    {
        "post_id": "1875001833385474",
        "author": "Ester Himelblum-Zeller",
        "author_badge": None,
        "question": "I'm a fairly new player to Canasta and I have a question about the 3s. Red Three's I understand you place out and gets counted towards your points. What about the Black 3s. On line they are used as blockers but nobody I know uses them that way. They use them like the Red Three's. What is the correct way?",
        "post_date": "3 hours ago",
        "url": "https://www.facebook.com/groups/modernamericancanasta/posts/1875001833385474/",
        "comments": [
            {
                "author": "Beth F. Levine",
                "badge": "Top contributor",
                "text": "It looks like you got this info from a Google search or AI inquiry. It is wrong. Buy the book Modern American Canasta...",
                "reactions": 1,
                "position": "against"
            },
            {
                "author": "Andi Stone Katz",
                "badge": "Top contributor",
                "text": "Both color 3's are used the same way.",
                "reactions": 1,
                "position": "for"
            }
        ]
    },
    {
        "post_id": "1859923298226661",
        "author": "Ellen Krell Seckler",
        "author_badge": None,
        "question": "Can your initial meld be just a dirty ace canasta or do you still need a 3 of a kind?",
        "post_date": "2 weeks ago",
        "url": "https://www.facebook.com/groups/modernamericancanasta/posts/1859923298226661/",
        "comments": [
            {
                "author": "Bonnie Esserman Gershenzon",
                "badge": "Top contributor",
                "text": "Absolutely need 3 of a kind 'meld' and points required (ie 125, 155 and 180).",
                "reactions": 0,
                "position": "against"
            },
            {
                "author": "Rona Goldfarb",
                "badge": None,
                "text": "No. Not ever...",
                "reactions": 5,
                "position": "against"
            }
        ]
    },
    {
        "post_id": "1865524517666539",
        "author": "Joyce Gruber Zappulla",
        "author_badge": None,
        "question": "A question came up in yesterday's game. If a player picks the final card, can they use all of their cards on their melds, with the exception of a card to throw on the discard pile. This would leave the player with no cards.",
        "post_date": "1 week ago",
        "url": "https://www.facebook.com/groups/modernamericancanasta/posts/1865524517666539/",
        "comments": [
            {
                "author": "Andrea Butterweich",
                "badge": None,
                "text": "Except for special hands you always need a discard",
                "reactions": 0,
                "position": "against"
            },
            {
                "author": "Stephanie Adler Calliott",
                "badge": None,
                "text": "If I'm reading this correctly, yes -- if you have two closed canastas. No, if you don't. You'd need a discard and card in your...",
                "reactions": 3,
                "position": "neutral"
            }
        ]
    },
    {
        "post_id": "1864183751133949",
        "author": "Catherine Komor Merritt",
        "author_badge": None,
        "question": "When playing 2 person… how many cards are dealt?",
        "post_date": "1 week ago",
        "url": "https://www.facebook.com/groups/modernamericancanasta/posts/1864183751133949/",
        "comments": [
            {
                "author": "Fran Ofshe Korman",
                "badge": None,
                "text": "15 cards are dealt with 2 players and you pick 2 cards not 1.",
                "reactions": 3,
                "position": "for"
            },
            {
                "author": "Jeffrey Lynn",
                "badge": None,
                "text": "13, draw 2 at a time, no pair hands. I have played it many times",
                "reactions": 0,
                "position": "for"
            }
        ]
    },
    {
        "post_id": "1864291697789821",
        "author": "Sharon Twomey",
        "author_badge": None,
        "question": "Anyone have rules/tips for playing 6 person Canasta? Three teams",
        "post_date": "1 week ago",
        "url": "https://www.facebook.com/groups/modernamericancanasta/posts/1864291697789821/",
        "comments": [
            {
                "author": "Andrea Butterweich",
                "badge": None,
                "text": "I like playing with 3 teams when there's 6 people. One team rotates out for a hand, keep 3 columns for scoring so each team gets their points.",
                "reactions": 1,
                "position": "for"
            }
        ]
    },
    {
        "post_id": "1861340331418291",
        "author": "Faye Gilad",
        "author_badge": None,
        "question": "When playing yesterday, a player only had wild cards in hand, therefore a wild card was used as a discard. On next pick another wild card was obtained. Now she had 4 wilds in hand. Player wanted to use one of the wilds to close a meld of fives on the table for a mixed canasta and then discard a wild card. Is this allowed to be done?",
        "post_date": "2 weeks ago",
        "url": "https://www.facebook.com/groups/modernamericancanasta/posts/1861340331418291/",
        "comments": [
            {
                "author": "Heidi Sue",
                "badge": "All-star contributor",
                "text": "Yes. As long as she only has wild cards in her hand, she can close other canastas & then use another wild card to discard to...",
                "reactions": 4,
                "position": "for"
            }
        ]
    }
]

# Process each post
for post in posts_data:
    posts_scanned += 1
    
    # Check if canasta-related
    if not is_canasta_related(post['question']):
        print(f"Skipping non-canasta post: {post['post_id']}")
        continue
    
    try:
        entry = create_strategy_entry(
            post_id=post['post_id'],
            author=post['author'],
            author_badge=post['author_badge'],
            question=post['question'],
            post_date=post['post_date'],
            comments=post['comments'],
            url=post['url']
        )
        
        if save_entry(entry):
            entries_added += 1
            print(f"✓ Added: {post['post_id']} - {post['question'][:50]}...")
        else:
            print(f"○ Duplicate: {post['post_id']}")
    except Exception as e:
        errors.append(f"Error processing {post['post_id']}: {str(e)}")
        print(f"✗ Error: {post['post_id']} - {e}")

# Summary
final_count = count_entries()
print(f"\n=== Summary ===")
print(f"Posts scanned: {posts_scanned}")
print(f"New entries added: {entries_added}")
print(f"Total entries now: {final_count}")
if errors:
    print(f"Errors: {len(errors)}")
    for e in errors:
        print(f"  - {e}")
