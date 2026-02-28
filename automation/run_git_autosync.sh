#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/Users/ramongonzalez/.openclaw/workspace"
ENV_FILE="$WORKSPACE/.automation.env"

if [ -f "$ENV_FILE" ]; then
  set -a
  source "$ENV_FILE"
  set +a
fi

log_msg() {
  local msg="$1"
  echo "$msg"
  if command -v openclaw >/dev/null 2>&1; then
    openclaw message send \
      --url "${OPENCLAW_GATEWAY_URL:-ws://127.0.0.1:18789}" \
      --token "${OPENCLAW_GATEWAY_TOKEN:-}" \
      --channel slack \
      --target "$2" \
      --message "$msg" >/dev/null 2>&1 || true
  fi
}

PYTHON_BIN="/Users/ramongonzalez/amazon-data/.venv/bin/python"

clickup_log() {
  local status="$1"
  local summary="$2"
  "$PYTHON_BIN" /Users/ramongonzalez/amazon-data/collectors/clickup_integration.py \
    --cron-id launchd_git_sync --status "$status" --summary "$summary" >/dev/null 2>&1 || true
}

TIMESTAMP="$(TZ=America/New_York date '+%Y-%m-%d %H:%M:%S %Z')"

if "$WORKSPACE/automation/git_autosync.sh"; then
  clickup_log "success" "Git auto-sync completed successfully ($TIMESTAMP)"
else
  clickup_log "critical" "Git auto-sync FAILED ($TIMESTAMP). Check $WORKSPACE/backups/logs/git_autosync.log"
  log_msg "🚨 Git auto-sync failed ($TIMESTAMP). Check $WORKSPACE/backups/logs/git_autosync.log" "C0AD9AZ7R6F"
  exit 1
fi
