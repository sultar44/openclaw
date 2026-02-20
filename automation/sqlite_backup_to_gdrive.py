#!/usr/bin/env python3
import datetime as dt
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tarfile
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TZ = 'America/New_York'
WORKSPACE = Path('/Users/ramongonzalez/.openclaw/workspace')
BACKUP_ROOT = WORKSPACE / 'backups'
STAGING_DIR = BACKUP_ROOT / 'staging'
LOG_DIR = BACKUP_ROOT / 'logs'
META_DIR = BACKUP_ROOT / 'meta'

# Auto-discovery roots (can be overridden via BACKUP_SCAN_ROOTS)
DEFAULT_SCAN_ROOTS = [
    '/Users/ramongonzalez/.openclaw/workspace',
    '/Users/ramongonzalez/amazon-data',
]
EXCLUDE_PARTS = {'.git', '.venv', 'node_modules', '__pycache__', '.DS_Store'}
DB_EXTENSIONS = {'.db', '.sqlite', '.sqlite3'}


def run(cmd):
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def now_stamp():
    return dt.datetime.now().strftime('%Y%m%d-%H%M%S')


def ensure_dirs():
    for p in [BACKUP_ROOT, STAGING_DIR, LOG_DIR, META_DIR]:
        p.mkdir(parents=True, exist_ok=True)


def parse_scan_roots():
    raw = os.environ.get('BACKUP_SCAN_ROOTS', '')
    if not raw.strip():
        return [Path(p) for p in DEFAULT_SCAN_ROOTS]
    return [Path(p.strip()).expanduser() for p in raw.split(',') if p.strip()]


def discover_sqlite_files(roots):
    found = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob('*'):
            if not path.is_file():
                continue
            if any(part in EXCLUDE_PARTS for part in path.parts):
                continue
            if path.suffix.lower() in DB_EXTENSIONS:
                found.append(path)
                continue
            # Heuristic: no extension but SQLite header
            if path.suffix == '':
                try:
                    with path.open('rb') as f:
                        hdr = f.read(16)
                    if hdr.startswith(b'SQLite format 3'):
                        found.append(path)
                except Exception:
                    pass
    return sorted(set(found))


def validate_sqlite(path):
    try:
        with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
            conn.execute('PRAGMA quick_check;').fetchall()
        return True
    except Exception:
        return False


def make_tar(sqlite_files, out_tar):
    with tarfile.open(out_tar, 'w:gz') as tar:
        for db in sqlite_files:
            arc = str(db).lstrip('/')
            tar.add(db, arcname=arc)


def encrypt_file(in_file, out_file, passphrase):
    cmd = [
        '/opt/homebrew/bin/openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-salt',
        '-in', str(in_file), '-out', str(out_file), '-pass', f'pass:{passphrase}'
    ]
    run(cmd)


def build_drive_service(sa_json):
    scopes = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(sa_json, scopes=scopes)
    return build('drive', 'v3', credentials=creds)


def upload_to_drive(service, folder_id, file_path):
    metadata = {'name': file_path.name, 'parents': [folder_id]}
    media = MediaFileUpload(str(file_path), resumable=False)
    created = service.files().create(body=metadata, media_body=media, fields='id,name,createdTime').execute()
    return created


def cleanup_old_backups(service, folder_id, keep=7):
    query = f"'{folder_id}' in parents and trashed=false"
    resp = service.files().list(q=query, fields='files(id,name,createdTime)', orderBy='createdTime desc', pageSize=200).execute()
    files = resp.get('files', [])
    old = files[keep:]
    for f in old:
        service.files().delete(fileId=f['id']).execute()
    return len(old)


def main():
    ensure_dirs()
    stamp = now_stamp()
    log_file = LOG_DIR / 'sqlite_backup.log'

    passphrase = os.environ.get('BACKUP_PASSPHRASE', '')
    if not passphrase:
        raise RuntimeError('BACKUP_PASSPHRASE env var is required')

    folder_id = os.environ.get('GDRIVE_FOLDER_ID', '').strip()
    if not folder_id:
        raise RuntimeError('GDRIVE_FOLDER_ID env var is required')

    sa_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON', '/Users/ramongonzalez/amazon-data/google_sheets_credentials.json')

    roots = parse_scan_roots()
    sqlite_files = discover_sqlite_files(roots)
    if not sqlite_files:
        raise RuntimeError('No SQLite databases discovered')

    valid = [p for p in sqlite_files if validate_sqlite(p)]
    if not valid:
        raise RuntimeError('No valid SQLite databases found after validation')

    tar_path = STAGING_DIR / f'sqlite-backup-{stamp}.tar.gz'
    enc_path = STAGING_DIR / f'sqlite-backup-{stamp}.tar.gz.enc'
    manifest = META_DIR / f'sqlite-backup-{stamp}.json'

    make_tar(valid, tar_path)
    encrypt_file(tar_path, enc_path, passphrase)

    service = build_drive_service(sa_json)
    uploaded = upload_to_drive(service, folder_id, enc_path)
    deleted = cleanup_old_backups(service, folder_id, keep=7)

    record = {
        'timestamp': stamp,
        'roots': [str(r) for r in roots],
        'db_count': len(valid),
        'db_files': [str(v) for v in valid],
        'archive': str(enc_path),
        'drive_file': uploaded,
        'deleted_old_count': deleted,
    }
    manifest.write_text(json.dumps(record, indent=2))

    with log_file.open('a') as f:
        f.write(json.dumps({'ok': True, **record}) + '\n')

    # cleanup local staging older than 8 days
    cutoff = dt.datetime.now() - dt.timedelta(days=8)
    for p in STAGING_DIR.glob('sqlite-backup-*'):
        if dt.datetime.fromtimestamp(p.stat().st_mtime) < cutoff:
            p.unlink(missing_ok=True)

    print(f"Backup OK: {uploaded.get('name')} (removed old: {deleted})")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        with (LOG_DIR / 'sqlite_backup.log').open('a') as f:
            f.write(json.dumps({'ok': False, 'error': str(e), 'ts': now_stamp()}) + '\n')
        print(f'Backup FAILED: {e}', file=sys.stderr)
        sys.exit(1)
