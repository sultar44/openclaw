# All7s Mission Control

Unified Next.js dashboard for:
- **Cron Calendar** (`/cron`)
- **Canasta Strategy Review** (`/strategy-review`)

## Run locally

```bash
cd /Users/ramongonzalez/.openclaw/workspace/all7s-mission-control
npm install
npm run dev
```

App runs on **http://localhost:8888**.

## Production run

```bash
cd /Users/ramongonzalez/.openclaw/workspace/all7s-mission-control
npm install
npm run build
npm run start
```

## Data sources

- Cron jobs: `openclaw cron list --json`
- Strategy review file: `/Users/ramongonzalez/.openclaw/workspace/canasta-rules/strategy.jsonl`
- Strategy backups: `/Users/ramongonzalez/.openclaw/workspace/canasta-rules/backups/strategy_*.jsonl`

Timezone is fixed to **America/New_York**.

## LaunchAgent migration (replace old mini-sites)

Create and load `~/Library/LaunchAgents/com.all7s.mission-control.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.all7s.mission-control</string>
  <key>ProgramArguments</key>
  <array>
    <string>/opt/homebrew/bin/npm</string>
    <string>run</string>
    <string>start</string>
  </array>
  <key>WorkingDirectory</key>
  <string>/Users/ramongonzalez/.openclaw/workspace/all7s-mission-control</string>
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
  </dict>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>/tmp/all7s-mission-control.log</string>
  <key>StandardErrorPath</key>
  <string>/tmp/all7s-mission-control.log</string>
</dict>
</plist>
```

Then:

```bash
# Stop/disable old services
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.openclaw.strategy-review.plist 2>/dev/null || true
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.chloe.cron-dashboard.plist 2>/dev/null || true
launchctl disable gui/$(id -u)/com.openclaw.strategy-review || true
launchctl disable gui/$(id -u)/com.chloe.cron-dashboard || true

# Build mission control
cd /Users/ramongonzalez/.openclaw/workspace/all7s-mission-control
npm install
npm run build

# Load new service
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.all7s.mission-control.plist
launchctl enable gui/$(id -u)/com.all7s.mission-control
launchctl kickstart -k gui/$(id -u)/com.all7s.mission-control
```
