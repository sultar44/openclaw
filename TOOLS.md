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
- **Logged into:** Gmail (chloemercer32@gmail.com), Facebook (Chloe Mercer), Amazon Ads (yamaris@goven.com)
- **Passkey popup disabled:** Chrome Preferences modified to suppress WebAuthn conditional UI
- **Amazon Ads reauth:** See `playbooks/amazon-ads-reauth.md` — use stored credentials, don't ask for master password for operational tasks
- **Amazon Seller Central:** Full autonomous login capability (email + password + TOTP)
  - Account: yamaris@goven.com (NOT chloemercer32 — that account is unused)
  - Password: `AMAZON_SC_PASSWORD` in `~/amazon-data/.env`
  - TOTP secret: `AMAZON_TOTP_SECRET` in `~/amazon-data/.env`
  - Login flow: email → password → (possible email verification code from yamaris@goven.com, forwarded to chloemercer32) → TOTP
  - Sessions last ~1-2 weeks before re-auth needed
  - Auto-forward rule being set up: yamaris@goven.com → chloemercer32@gmail.com for Amazon verification emails

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
- **Partial failure:** Comment on task + message to #chloelogs (C0AELHCGW4F)
- **Critical failure:** Comment on task + message to #chloebot (C0AD9AZ7R6F)
- **No more routine logging to #chloelogs** — only partial failures go there

### 🚨 Cron Creation Checklist (MANDATORY)
Every new cron job requires ALL FOUR in the same action. No exceptions:
1. **Create the cron job** in OpenClaw
2. **Create a ClickUp task** in list 901816342276
3. **Add a row to the Cron Registry sheet** (`1aPek6nXAht0BYkO5fR-ildJ4u7gnOFSsXMyqjDXMPDQ`, tab: Cron Registry)
4. **Update `clickup_config.json`** with cron_id → task_id mapping

The Cron Registry sheet is the source of truth. The daily sync (6:15 AM) catches orphans, but that's the safety net, not the process.

If a cron job is **recreated** (new ID), update the sheet row + clickup_config.json immediately.

---

## Cron Jobs

**Default:** Always use `wakeMode: "now"` for scheduled jobs (daily/weekly/monthly).

- `"now"` = triggers immediately at scheduled time ✅
- `"next-heartbeat"` = waits for heartbeat, unreliable for timed jobs ❌

**Cron Registry Sheet:** `1aPek6nXAht0BYkO5fR-ildJ4u7gnOFSsXMyqjDXMPDQ` (tab: Cron Registry)
- Source of truth for all cron jobs, ClickUp mappings, objectives, outcomes
- Daily sync playbook: `playbooks/cron-registry-sync.md`

**Logging:** All cron jobs log to ClickUp (not Slack) by default:
- Post execution comment to the matching ClickUp task via `clickup_integration.py`
- Mark task "complete" on success
- **Partial failures** → ClickUp comment + announce to #chloelogs (C0AELHCGW4F)
- **Critical failures** → ClickUp comment + announce to #chloebot (C0AD9AZ7R6F)
- **Successes** → ClickUp comment only (no Slack message)
- Config: `~/amazon-data/collectors/clickup_config.json` (local cache, sheet is authority)

**Important:** Just putting "send a message to channel X" in the payload text doesn't work for isolated sessions. You MUST set the delivery config explicitly.

---

## Product Review Task Memory

- Persistent instructions saved at: `/Users/ramongonzalez/.openclaw/workspace/playbooks/product-review-writing.md`
- Use this playbook whenever Ramon asks for Amazon product review writing.

## Email Template Rule (Ramon mandate, Mar 13 2026)

- **If it CAN be hardcoded via .py, hardcode it.** No exceptions.
- All emails use templates in `templates/` rendered by `templates/render_email.py`
- Hardcoded: Klaviyo personalization tags, greetings, sign-offs, coupon codes, URLs, P.S. rotation
- LLM only supplies the dynamic content (body text, titles, challenges)
- **Any new email type** must get a template file + renderer function before the first send
- This applies to everything, not just emails. Anything repeatable that has fixed parts should be templated.

## Email Post-Processing Rule (Ramon preference)

- **After processing any forwarded email** (SOS, HARO, BCC learning loop, sold/ship-now, or any other), **archive it** in Gmail
- This keeps Chloe's inbox as a "failure detector" — unprocessed emails remain visible
- Use `gog gmail modify <messageId> --remove-labels INBOX` to archive

## Email Processing Alert Rule (Added Mar 12, 2026)

- **Every email that gets archived MUST produce a confirmation alert in #chloelogs (C0AELHCGW4F)**
- No silent archiving — Ramon needs proof of life that emails are being processed
- One-line alert with emoji prefix: 📬 HARO/SOS, 📊 Ads reports, 📦 Vine/FBM, 📨 other
- Format: `{emoji} {type}: {from or subject} — {outcome}`
- See `playbooks/gmail-poll-safety-net.md` for full routing details

## Email Trigger Policy (Updated Mar 11, 2026)

- **Primary: Polling cron every 30 min** — "Gmail Inbox Processor" (`61b00e02`)
- Gmail Pub/Sub watcher is broken (stale historyId bug in gog) — do not rely on it
- Cron checks full inbox, classifies each email, processes via appropriate playbook
- Playbook: `playbooks/gmail-poll-safety-net.md`
- Create a playbook in `playbooks/` for each email trigger type

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
- **Always use `includeItemsFromAllDrives=True`** on all `files().list()` calls — all folders are on a Shared Drive
- Without these flags, the SA gets 404s or empty results even on files it has access to
- The SA email: `openclaw-sheets@lustrous-bounty-460801-b9.iam.gserviceaccount.com`
- Credentials: `~/amazon-data/google_sheets_credentials.json`
- Scopes needed: `drive` and `drive.file`
