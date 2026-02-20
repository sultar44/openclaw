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

if "$WORKSPACE/automation/git_autosync.sh"; then
  log_msg "✅ Git auto-sync completed successfully ($(TZ=America/New_York date '+%Y-%m-%d %H:%M:%S %Z'))." "${SYNC_SUCCESS_CHANNEL:-C0AELHCGW4F}"
else
  log_msg "🚨 Git auto-sync failed ($(TZ=America/New_York date '+%Y-%m-%d %H:%M:%S %Z')). Check $WORKSPACE/backups/logs/git_autosync.log" "${SYNC_FAILURE_CHANNEL:-C0AD9AZ7R6F}"
  exit 1
fi
