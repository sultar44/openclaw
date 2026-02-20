# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## My Identity (for external accounts)

- **Name:** Chloe Mercer
- **Email:** chloemercer32@gmail.com
- **Persona:** 50-year-old woman who loves Canasta
- **Avatar:** `chloe-avatar.png` (pending)

---

## Browser

- **OpenClaw browser profile:** `openclaw` (Chrome, full control)
- **User data:** `/Users/ramongonzalez/.openclaw/browser/openclaw/user-data`
- **Logged into:** Gmail (chloemercer32@gmail.com), Facebook (Chloe Mercer)

---

## Email

- **Address:** chloemercer32@gmail.com
- **SMTP:** Gmail with app password
- **Utility:** `/Users/ramongonzalez/amazon-data/collectors/email_util.py`
- **Can:** Send emails with attachments to anyone

## Google Sheets (Operational Rule)

- **Preferred writer identity:** `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`
- **Fallback/browser identity:** `chloemercer32@gmail.com`
- **Rule:** For all automated sheet writes (including Vine Review Writer), always use the service account identity for stability.

---

## Amazon SP-API

- **Location:** `~/amazon-data/`
- **Database:** `~/amazon-data/amazon.db` (SQLite)
- **Credentials:** `~/amazon-data/.env` (🔐 protected by master password)
- **Marketplaces:** US (ATVPDKIKX0DER), CA (A2EUQ1WTGCTBG2)
- **Collectors:** `~/amazon-data/collectors/`
- **Reports:** `~/amazon-data/reports/`

### Available Reports
- FBA Inventory (current stock levels)
- Restock Recommendations (Amazon's suggested replenishment)
- Orders (by date range)
- More available — see `list_reports.py`

---

## Amazon Ads API (PPC)

- **Credentials:** In `~/amazon-data/.env`
- **Profiles:** US (973179741133617), CA (4084371223098403)
- **Collector:** `~/amazon-data/collectors/daily_ppc.py`
- **Tables:** `ppc_campaigns`, `ppc_keywords`, `ppc_search_terms`
- **Schedule:** Daily 6:30 AM EST

---

## DataDive Rank Radar API

- **Credentials:** `DATADIVE_API_KEY` in `~/amazon-data/.env`
- **Collector:** `~/amazon-data/collectors/daily_ranks.py`
- **Table:** `keyword_ranking`
- **Radars:** 15 (US + CA combined)
- **Schedule:** Daily 7:00 AM EST + retries every 3h

---

## Keepa API (BSR Data)

- **Credentials:** `KEEPA_API_KEY` in `~/amazon-data/.env`
- **Token rate:** 5 tokens/minute (renews Dec 1, 2026)
- **Cost:** ~1 token per ASIN
- **Collector:** `~/amazon-data/collectors/bsr_checker.py`
- **Schedule:** Sunday & Wednesday 9 PM EST
- **Purpose:** Fetch BSR for wholesale items to identify FBA shipping candidates
- **Threshold:** Only write BSR to sheet if < 400,000

---

---

## Cron Jobs

**Default:** Always use `wakeMode: "now"` for scheduled jobs (daily/weekly/monthly).

- `"now"` = triggers immediately at scheduled time ✅
- `"next-heartbeat"` = waits for heartbeat, unreliable for timed jobs ❌

**Logging:** All cron jobs must announce to **#chloe-logs** (C0AELHCGW4F):
- Set `delivery: {mode: "announce", channel: "slack", to: "C0AELHCGW4F"}`
- Include status summary in the job's final response
- Format: `"Job Name completed - [brief status with key metrics]"`
- This is for logging only — not for listening/instructions

**Important:** Just putting "send a message to channel X" in the payload text doesn't work for isolated sessions. You MUST set the delivery config explicitly.

---

## Product Review Task Memory

- Persistent instructions saved at: `/Users/ramongonzalez/.openclaw/workspace/playbooks/product-review-writing.md`
- Use this playbook whenever Ramon asks for Amazon product review writing.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

---

Add whatever helps you do your job. This is your cheat sheet.
