#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/Users/ramongonzalez/.openclaw/workspace"
ENV_FILE="$WORKSPACE/.automation.env"
PYTHON_BIN="/Users/ramongonzalez/amazon-data/.venv/bin/python"

if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

notify() {
  local msg="$1"
  local channel="$2"
  openclaw message send \
    --url "${OPENCLAW_GATEWAY_URL:-ws://127.0.0.1:18789}" \
    --token "${OPENCLAW_GATEWAY_TOKEN:-}" \
    --channel slack \
    --target "$channel" \
    --message "$msg" >/dev/null 2>&1 || true
}

clickup_log() {
  local status="$1"
  local summary="$2"
  "$PYTHON_BIN" /Users/ramongonzalez/amazon-data/collectors/clickup_integration.py \
    --cron-id launchd_sqlite_backup --status "$status" --summary "$summary" >/dev/null 2>&1 || true
}

TIMESTAMP="$(TZ=America/New_York date '+%Y-%m-%d %H:%M:%S %Z')"

if "$PYTHON_BIN" "$WORKSPACE/automation/sqlite_backup_to_gdrive.py"; then
  clickup_log "success" "SQLite backup completed successfully ($TIMESTAMP)"
else
  clickup_log "critical" "SQLite backup FAILED ($TIMESTAMP). Check $WORKSPACE/backups/logs/sqlite_backup.log"
  notify "🚨 SQLite backup FAILED ($TIMESTAMP). Check $WORKSPACE/backups/logs/sqlite_backup.log" "C0AD9AZ7R6F"
  exit 1
fi
