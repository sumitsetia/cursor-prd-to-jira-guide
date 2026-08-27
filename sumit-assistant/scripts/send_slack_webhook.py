#!/usr/bin/env python3
"""Send digest to Slack via incoming webhook (optional local fallback).

Set SLACK_WEBHOOK_URL in your environment or in ~/.sumit-assistant.env
"""

import json
import os
import sys
import urllib.request
from pathlib import Path


def load_webhook_url() -> str:
    url = os.environ.get("SLACK_WEBHOOK_URL", "").strip()
    if url:
        return url

    env_file = Path.home() / ".sumit-assistant.env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if line.startswith("SLACK_WEBHOOK_URL="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return ""


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: send_slack_webhook.py <requirements.json>", file=sys.stderr)
        sys.exit(1)

    webhook = load_webhook_url()
    if not webhook:
        print("Missing SLACK_WEBHOOK_URL", file=sys.stderr)
        sys.exit(2)

    import subprocess

    script_dir = Path(__file__).resolve().parent
    body = subprocess.check_output(
        [sys.executable, str(script_dir / "format_digest_slack.py"), sys.argv[1]],
        text=True,
    )

    payload = json.dumps({"text": body}).encode()
    req = urllib.request.Request(
        webhook,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Slack webhook failed: {resp.status}")

    print("Slack digest sent")


if __name__ == "__main__":
    main()
