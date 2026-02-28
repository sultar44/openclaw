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

## ClickUp Integration

- **Workspace:** Goven (team 1235857)
- **Chloe's account:** chloemercer32@gmail.com (user ID: 107688256)
- **API Key:** In `~/amazon-data/.env` as `CLICKUP_API_KEY`
- **Task List:** "Chloe Automated Tasks" in BIZ: Corporate (list ID: 901816342276)
- **Config:** `~/amazon-data/collectors/clickup_config.json` (cron→task mapping)
- **Integration script:** `~/amazon-data/collectors/clickup_integration.py`

### Execution Logging Protocol
- **All executions:** Post comment on ClickUp task with status + summary
- **Success:** Mark task "complete" (recurring tasks auto-reopen on next due date)
- **Partial failure:** Comment on task + message to #chloe-logs (C0AELHCGW4F)
- **Critical failure:** Comment on task + message to #chloebot (C0AD9AZ7R6F)
- **No more routine logging to #chloe-logs** — only partial failures go there

### Adding New Cron Jobs
When creating a new cron job, also:
1. Create a ClickUp task in list 901816342276
2. Add the cron_id → task_id mapping to `clickup_config.json`
3. Set due date and recurrence matching the cron schedule

---

## Cron Jobs

**Default:** Always use `wakeMode: "now"` for scheduled jobs (daily/weekly/monthly).

- `"now"` = triggers immediately at scheduled time ✅
- `"next-heartbeat"` = waits for heartbeat, unreliable for timed jobs ❌

**Logging:** All cron jobs log to ClickUp (not Slack) by default:
- Post execution comment to the matching ClickUp task via `clickup_integration.py`
- Mark task "complete" on success
- **Partial failures** → ClickUp comment + announce to #chloe-logs (C0AELHCGW4F)
- **Critical failures** → ClickUp comment + announce to #chloebot (C0AD9AZ7R6F)
- **Successes** → ClickUp comment only (no Slack message)
- Config: `~/amazon-data/collectors/clickup_config.json`

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

## Shopify Blog Image Hosting

**Problem:** Shopify doesn't support base64 inline images, and no file upload API access.
**Solution:** Use a permanent hidden article (ID: 618201022747, "Image Host - Do Not Delete") to host inline images.

**Process for blog images:**
1. Download and verify image with vision before using
2. Upload as featured image on the Image Host article via API (base64 attachment)
3. Grab the CDN URL from the response
4. Reference the CDN URL in the actual blog article's HTML
5. **Never delete the Image Host article** — it kills the CDN URLs

**Image Specs:**
- Email: 600px wide, 3:2 ratio, <100KB, JPG, 72 DPI
- Blog header: 1200px wide, 3:2 ratio, <200KB (use article featured image API)
- Blog inline: 800-1000px wide, <150KB (host via Image Host article)

## Google Drive API (Service Account)

- **Always use `supportsAllDrives=True`** on all Drive API calls (get, update, list, etc.)
- Without it, the SA gets 404 even on files it has Editor access to
- The SA email: `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`
- Credentials: `~/amazon-data/google_sheets_credentials.json`
- Scopes needed: `drive` and `drive.file`
