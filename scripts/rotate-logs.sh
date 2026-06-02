#!/usr/bin/env bash

set -euo pipefail

# Rotate NanoClaw's launchd-redirected logs.
#
# launchd holds StandardOutPath/StandardErrorPath open, so the process must
# reopen them after rotation. We do that with a GRACEFUL restart
# (unload + load) — NEVER `launchctl kickstart -k`, which triggers a WhatsApp
# session conflict that wipes store/auth (see memory: kickstart wipes auth).
#
# Size-gated: only rotates a log past THRESHOLD_BYTES, so most runs no-op and
# no restart happens. History is preserved (gzipped archives, keep KEEP newest).

LOG_DIR="/Users/gio/.nanoclaw/logs"
PLIST="$HOME/Library/LaunchAgents/com.nanoclaw.plist"
THRESHOLD_BYTES=$((500 * 1024 * 1024)) # 500 MiB
KEEP=10
LOGS=(nanoclaw.log nanoclaw.error.log)

ts="$(date +%Y%m%d-%H%M%S)"
rotated=()

for name in "${LOGS[@]}"; do
  f="$LOG_DIR/$name"
  [ -f "$f" ] || continue
  size="$(stat -f '%z' "$f")"
  if [ "$size" -gt "$THRESHOLD_BYTES" ]; then
    mv "$f" "$f.$ts"
    rotated+=("$f.$ts")
  fi
done

# Reopen logs only if we actually rotated something.
if [ "${#rotated[@]}" -gt 0 ]; then
  launchctl unload "$PLIST" 2>/dev/null || true
  sleep 2
  launchctl load "$PLIST" 2>/dev/null || true

  for moved in "${rotated[@]}"; do
    gzip "$moved"
  done
fi

# Prune: keep the newest KEEP gzipped archives per log. (bash 3.2 compatible —
# macOS default bash has no mapfile.)
for name in "${LOGS[@]}"; do
  ls -t "$LOG_DIR/$name".*.gz 2>/dev/null | tail -n +$((KEEP + 1)) | while IFS= read -r o; do
    [ -n "$o" ] && rm -f "$o"
  done
done
