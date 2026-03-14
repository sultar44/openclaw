#!/usr/bin/env python3
"""
Email template renderer for All7s emails.

Hardcodes everything that CAN be hardcoded (greeting, personalization tags,
sign-offs, coupon codes, URLs, P.S. rotation). The LLM only supplies the
dynamic body content.

Usage:
    python render_email.py better-hand --title "..." --body "..." --challenge "..." --ps-index 0
    python render_email.py sunday-ritual --body "..." --blog-url "..." --ps-index 0
    python render_email.py better-hand --json '{"title":"...","body":"...","challenge":"...","ps_index":0}'

Output: rendered plain-text email to stdout.
"""

import argparse
import json
import sys
import os

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))

# ── Hardcoded P.S. rotations ──────────────────────────────────────────────

BETTER_HAND_PS = [
    "P.S. Got a Canasta story that still makes you laugh? Reply and tell us. We collect the best ones.",
    "P.S. What's your go-to opening strategy? Hit reply and tell us. We read every one.",
    "P.S. Did last week's tip change anything at your table? Reply and tell us. We love hearing what works.",
]

SUNDAY_RITUAL_PS = [
    "P.S. What does your Sunday ritual look like? Reply and tell us. We read every one.",
    "P.S. Hit reply and tell me, do you have a regular game night? Or has it been a while? I read every one.",
    "P.S. Who taught you to play cards? Reply and tell me. I'd love to hear that story.",
    "P.S. What's the one game that always comes out when friends visit? Hit reply and tell me.",
    "P.S. Ever had a game night that turned into something unforgettable? Reply and tell me. I read every one.",
]


def load_template(name: str) -> str:
    path = os.path.join(TEMPLATE_DIR, f"{name}.txt")
    with open(path, "r") as f:
        return f.read()


def render_better_hand(title: str, body: str, challenge: str, ps_index: int = 0) -> str:
    template = load_template("better-hand")
    ps = BETTER_HAND_PS[ps_index % len(BETTER_HAND_PS)]
    return template.replace("{TITLE}", title).replace("{BODY}", body).replace("{CHALLENGE}", challenge).replace("{PS}", ps)


def render_sunday_ritual(body: str, blog_url: str, ps_index: int = 0) -> str:
    template = load_template("sunday-ritual")
    ps = SUNDAY_RITUAL_PS[ps_index % len(SUNDAY_RITUAL_PS)]
    return template.replace("{BODY}", body).replace("{BLOG_URL}", blog_url).replace("{PS}", ps)


def main():
    parser = argparse.ArgumentParser(description="Render All7s email templates")
    parser.add_argument("template", choices=["better-hand", "sunday-ritual"])
    parser.add_argument("--title", help="Strategy tip title (better-hand)")
    parser.add_argument("--body", help="Main body content")
    parser.add_argument("--challenge", help="Try-this-weekend challenge (better-hand)")
    parser.add_argument("--blog-url", help="Blog post URL (sunday-ritual)")
    parser.add_argument("--ps-index", type=int, default=0, help="P.S. rotation index (0-2)")
    parser.add_argument("--json", dest="json_input", help="JSON string with all fields")

    args = parser.parse_args()

    # Allow JSON input for easier programmatic use
    if args.json_input:
        data = json.loads(args.json_input)
        args.body = data.get("body", args.body)
        args.title = data.get("title", args.title)
        args.challenge = data.get("challenge", args.challenge)
        args.blog_url = data.get("blog_url", args.blog_url)
        args.ps_index = data.get("ps_index", args.ps_index or 0)

    if args.template == "better-hand":
        if not all([args.title, args.body, args.challenge]):
            print("Error: better-hand requires --title, --body, and --challenge", file=sys.stderr)
            sys.exit(1)
        print(render_better_hand(args.title, args.body, args.challenge, args.ps_index))

    elif args.template == "sunday-ritual":
        if not all([args.body, args.blog_url]):
            print("Error: sunday-ritual requires --body and --blog-url", file=sys.stderr)
            sys.exit(1)
        print(render_sunday_ritual(args.body, args.blog_url, args.ps_index))


if __name__ == "__main__":
    main()
