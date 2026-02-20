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

if "$PYTHON_BIN" "$WORKSPACE/automation/sqlite_backup_to_gdrive.py"; then
  notify "✅ SQLite backup completed successfully ($(TZ=America/New_York date '+%Y-%m-%d %H:%M:%S %Z'))." "${SYNC_SUCCESS_CHANNEL:-C0AELHCGW4F}"
else
  notify "🚨 SQLite backup FAILED ($(TZ=America/New_York date '+%Y-%m-%d %H:%M:%S %Z')). Check $WORKSPACE/backups/logs/sqlite_backup.log" "${SYNC_FAILURE_CHANNEL:-C0AD9AZ7R6F}"
  exit 1
fi
