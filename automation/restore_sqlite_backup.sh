#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: $0 <encrypted_backup_file.tar.gz.enc> <restore_dir>"
  exit 1
fi

ENC_FILE="$1"
RESTORE_DIR="$2"

if [ -z "${BACKUP_PASSPHRASE:-}" ]; then
  echo "BACKUP_PASSPHRASE env var is required"
  exit 1
fi

mkdir -p "$RESTORE_DIR"
TMP_TAR="$RESTORE_DIR/restore-$(date +%Y%m%d-%H%M%S).tar.gz"

/opt/homebrew/bin/openssl enc -d -aes-256-cbc -pbkdf2 -in "$ENC_FILE" -out "$TMP_TAR" -pass "pass:${BACKUP_PASSPHRASE}"
tar -xzf "$TMP_TAR" -C "$RESTORE_DIR"

echo "Restore complete: $RESTORE_DIR"
echo "Decrypted archive retained at: $TMP_TAR"
