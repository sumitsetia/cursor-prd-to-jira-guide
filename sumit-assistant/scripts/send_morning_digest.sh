#!/bin/bash
# Sends a morning digest of open requirements via Microsoft Outlook.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSISTANT_DIR="$(dirname "$SCRIPT_DIR")"
REQUIREMENTS_FILE="$ASSISTANT_DIR/requirements.json"
RECIPIENT="sumit.setia@wbd.com"
LOG_FILE="$ASSISTANT_DIR/digest.log"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

if [[ ! -f "$REQUIREMENTS_FILE" ]]; then
  log "ERROR: requirements file not found at $REQUIREMENTS_FILE"
  exit 1
fi

BODY="$(python3 "$SCRIPT_DIR/format_digest.py" "$REQUIREMENTS_FILE")"
SUBJECT="Your daily requirements digest — $(date '+%A, %B %-d, %Y')"

osascript "$SCRIPT_DIR/send_outlook_email.applescript" "$RECIPIENT" "$SUBJECT" "$BODY"
log "Digest sent to $RECIPIENT"
