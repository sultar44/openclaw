#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="/Users/ramongonzalez/.openclaw/workspace"
BRANCH="main"
LOG_DIR="$WORKSPACE/backups/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/git_autosync.log"

timestamp_human=$(TZ=America/New_York date '+%Y-%m-%d %H:%M:%S %Z')
timestamp_tag=$(TZ=America/New_York date '+%Y%m%d-%H%M%S')

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

cd "$WORKSPACE"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "FAIL: $WORKSPACE is not a git repository"
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  log "FAIL: origin remote not configured"
  exit 1
fi

# Ensure branch
current_branch=$(git branch --show-current)
if [ "$current_branch" != "$BRANCH" ]; then
  log "INFO: switching $current_branch -> $BRANCH"
  git checkout "$BRANCH"
fi

# Stage and commit if needed
git add -A
if ! git diff --cached --quiet; then
  commit_msg="auto-sync: ${timestamp_human} [sync-${timestamp_tag}]"
  git commit -m "$commit_msg"
  git tag -a "autosync-${timestamp_tag}" -m "Automated sync tag ${timestamp_human}"
  log "Committed and tagged autosync-${timestamp_tag}"
else
  log "No local changes to commit"
fi

# Sync from remote with conflict detection (only if remote branch exists)
if git ls-remote --exit-code --heads origin "$BRANCH" >/dev/null 2>&1; then
  log "Fetching origin/$BRANCH"
  git fetch origin "$BRANCH"

  set +e
  git pull --rebase origin "$BRANCH"
  pull_status=$?
  set -e

  if [ "$pull_status" -ne 0 ]; then
    # Best-effort cleanup; only if rebase in progress
    git rebase --abort >/dev/null 2>&1 || true
    log "FAIL: rebase conflict detected while pulling from origin/$BRANCH"
    exit 2
  fi

  log "Pushing commits + tags"
  git push origin "$BRANCH" --follow-tags
else
  log "Remote branch origin/$BRANCH does not exist yet; creating it"
  git push -u origin "$BRANCH" --follow-tags
fi

log "SUCCESS: autosync completed"
