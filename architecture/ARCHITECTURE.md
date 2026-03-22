# System Architecture — All7s Operations Platform

*Created: March 21, 2026*
*Status: Living document — update as we migrate*

---

## Principles

1. **Single source of truth** — every config, routing rule, and format standard lives in ONE place
2. **Fail loud** — every process must announce failures. Silent failures are bugs.
3. **Port reservation** — documented, enforced, no squatting
4. **Process registry** — if it runs persistently, it's in the manifest
5. **Idempotent scripts** — safe to re-run without duplication
6. **LLM-last** — if a script can do it, don't burn tokens

---

## Port Reservations

| Port  | Owner                     | Notes                          |
|-------|---------------------------|--------------------------------|
| 18789 | OpenClaw Gateway          | Primary gateway                |
| 18800 | OpenClaw Browser (Chrome) | Browser automation             |
| 18801 | Review Scraper Server     | `review_scraper.py` HTTP mode  |
| 18802 | (reserved)                | Future service                 |
| 18803 | (reserved)                | Future service                 |

**Rule:** Before binding a port, check this table. If not listed, add it here first.

---

## Service Manifest

### Tier 1: Always Running (LaunchAgents)

| Service | Plist | Interval | Purpose | Health Check |
|---------|-------|----------|---------|-------------|
| OpenClaw Gateway | `ai.openclaw.gateway` | boot | Core platform | `curl localhost:18789/health` |
| Gateway Watchdog | `ai.openclaw.gateway-watchdog` | 60s | Restarts gateway if down | Check log for recent run |
| Gmail Watcher Monitor | `ai.openclaw.gmail-watcher-monitor` | 300s | Ensures gog watcher alive | Check log for recent run |
| Auto-Update | `ai.openclaw.auto-update` | daily 3:15AM | Updates OpenClaw binary | Log for success/fail |
| Tailscale Retry | `ai.openclaw.tailscale-retry` | boot | Tailscale boot reliability | `tailscale status` |

### Tier 2: Gateway-Managed (gog watcher)

| Service | Managed By | Purpose | Restart Policy |
|---------|-----------|---------|----------------|
| Gmail Pub/Sub Watcher | Gateway hook | Real-time email processing | Gateway restart restores |

### Tier 3: Scheduled (OpenClaw Cron)

See **Cron Registry Sheet** (`1aPek6nXAht0BYkO5fR-ildJ4u7gnOFSsXMyqjDXMPDQ`) — source of truth for all 51 jobs.

### Disabled/Retired

| Service | Status | Notes |
|---------|--------|-------|
| `com.openclaw.gdrive-sync` | Disabled plist | Replaced by cron-based sync |
| `com.all7s.daily-amazon` | Dead (exit 0) | Legacy, safe to remove |
| Airbyte | Decommissioned Mar 15 | All connections deleted |
| `cron_watchdog.py` | Retired | Replaced by `cron_missing_checker.py` |

---

## Shared Configuration

All routing rules, alert destinations, and format standards are defined in:

```
~/amazon-data/shared_config/
├── config.py          # Main config module (import shared_config)
├── alert_channels.py  # Slack channel IDs and routing
├── email_routing.py   # Email classification rules
├── format_standards.py # Alert formatting templates
└── __init__.py
```

**Rule:** Scripts MUST import from `shared_config` instead of hardcoding channel IDs, routing rules, or format strings.

### Migration Path
- New scripts: MUST use shared_config from day one
- Existing scripts: Migrate when next touched (boy scout rule)
- Track migration status in `shared_config/MIGRATION.md`

---

## Email Processing Architecture

```
Inbound Email
    │
    ├──[Real-time] Gmail Pub/Sub → gog watcher → gateway hook → gmail_inbox_router.py
    │
    └──[Backup] Polling cron (every 30 min) → gmail_inbox_router.py
                                                     │
                    ┌────────────────────────────────┤
                    │              │                  │                │
              Amazon Ads     HARO/SOS          Trusted Sender    External
              reports        pr_bcc_processor   (forward/act)    (classify)
                    │              │                  │
              ads_report_     PR pipeline       Type-specific
              processor.py                      playbook
```

**Single router:** `gmail_inbox_router.py` is the ONE place that decides where an email goes.
**Routing rules:** Defined in `shared_config/email_routing.py`, imported by the router.

---

## Alert Architecture

```
Alert Source (any script/cron)
    │
    ├── slack_notify.py (direct, zero LLM)
    │       │
    │       ├── #chloebot (C0AD9AZ7R6F) — critical alerts, human-facing
    │       ├── #chloelogs (C0AELHCGW4F) — operational logs, partial failures
    │       └── (other channels as needed)
    │
    └── clickup_integration.py (task logging)
            │
            ├── Post comment with execution details
            ├── Mark complete on success
            └── Reopen on failure (if recurring)
```

**Alert levels** (defined in `shared_config/alert_channels.py`):
- `CRITICAL` → #chloebot + ClickUp comment
- `WARNING` → #chloelogs + ClickUp comment  
- `INFO` → ClickUp comment only
- `SUCCESS` → ClickUp comment only (mark complete)

---

## Data Flow Architecture

```
Amazon SP-API ──→ BQ (amazon_raw)
Amazon Ads API ──→ BQ (amazon_raw)
Amazon Ads Emails ──→ ads_report_processor.py ──→ BQ
Keepa API ──→ BQ
DataDive API ──→ BQ
GA4 ──→ BQ (on-demand)
GSC ──→ BQ (weekly)

BQ ──→ Google Sheets (dashboards, reports)
BQ ──→ Slack alerts (threshold-based)
```

**SQLite is frozen.** `amazon.db` exists as archive only. No reads, no writes.

---

## Standards for New Processes

### Before Creating Anything New

1. **Check this document** — does a similar process already exist?
2. **Reserve resources** — ports, file paths, sheet tabs
3. **Use shared_config** — no hardcoded channel IDs or routing rules

### New Cron Job Checklist

1. Create the cron job in OpenClaw
2. Create a ClickUp task in list `901816342276`
3. Add row to Cron Registry sheet
4. Update `clickup_config.json` with mapping
5. Script must handle its own logging (slack_notify + clickup_integration)
6. Use `gemini-flash` model unless job genuinely needs reasoning

### New Script Checklist

1. Import `shared_config` for channels, routing, formatting
2. Include proper error handling with alert escalation
3. Add to this manifest if it runs persistently
4. Document port usage if it binds one
5. Add integration test or health check

### New LaunchAgent Checklist

1. Add to Service Manifest above
2. Include health check method
3. Log to `~/.openclaw/logs/`
4. Document restart policy

---

## Known Technical Debt

| Item | Priority | Notes |
|------|----------|-------|
| `com.all7s.daily-amazon` LaunchAgent | Low | Dead, safe to remove |
| `gdrive-sync` disabled plist | Low | Cleanup |
| Dual routing logic (watcher hook + polling cron) | Medium | Unify via shared_config |
| `clickup_config.json` has stale entries for old cron IDs | Medium | Sync script handles this |
| 80 entries in cron_to_task but only 51 active crons | Low | Old IDs from recreated jobs |
| Gateway watchdog runs every 60s (comment says 5 min) | Low | Fix comment or interval |

---

## File Map

```
~/amazon-data/
├── collectors/          # All Python scripts (80+)
├── shared_config/       # NEW: shared configuration module
├── templates/           # Email templates + renderer
├── playbooks/           # Operational playbooks
├── .env                 # Credentials (protected)
├── google_sheets_credentials.json
└── .venv/               # Python virtual environment

~/.openclaw/
├── workspace/           # Chloe's workspace (this repo)
│   ├── architecture/    # THIS document
│   ├── memory/          # Daily logs
│   ├── playbooks/       # Task playbooks
│   └── skills/          # Custom skills
├── hooks/               # Gateway hooks
│   └── transforms/      # Hook transforms
├── scripts/             # Shell scripts for LaunchAgents
├── logs/                # LaunchAgent logs
└── browser/             # Browser automation data
```
