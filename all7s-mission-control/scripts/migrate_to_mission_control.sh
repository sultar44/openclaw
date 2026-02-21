#!/usr/bin/env bash
set -euo pipefail

UID_NUM=$(id -u)

launchctl bootout gui/${UID_NUM} ~/Library/LaunchAgents/com.openclaw.strategy-review.plist 2>/dev/null || true
launchctl bootout gui/${UID_NUM} ~/Library/LaunchAgents/com.chloe.cron-dashboard.plist 2>/dev/null || true
launchctl disable gui/${UID_NUM}/com.openclaw.strategy-review || true
launchctl disable gui/${UID_NUM}/com.chloe.cron-dashboard || true

cd /Users/ramongonzalez/.openclaw/workspace/all7s-mission-control
npm install
npm run build

launchctl bootstrap gui/${UID_NUM} ~/Library/LaunchAgents/com.all7s.mission-control.plist
launchctl enable gui/${UID_NUM}/com.all7s.mission-control
launchctl kickstart -k gui/${UID_NUM}/com.all7s.mission-control

echo "Mission Control is now serving on port 8888"
