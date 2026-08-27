#!/usr/bin/env python3
"""Send morning digest via Microsoft Graph (for Cursor cloud automations).

Requires these environment variables (set in Cursor Cloud Agent secrets):
  MS_TENANT_ID, MS_CLIENT_ID, MS_CLIENT_SECRET, MS_SENDER, MS_RECIPIENT

Azure app needs Application permission Mail.Send with admin consent.
"""

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        print(f"Missing required env var: {name}", file=sys.stderr)
        sys.exit(2)
    return value


def get_token(tenant_id: str, client_id: str, client_secret: str) -> str:
    data = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default",
            "grant_type": "client_credentials",
        }
    ).encode()
    req = urllib.request.Request(
        f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token",
        data=data,
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read().decode())
    return payload["access_token"]


def send_mail(token: str, sender: str, recipient: str, subject: str, body: str) -> None:
    message = {
        "message": {
            "subject": subject,
            "body": {"contentType": "Text", "content": body},
            "toRecipients": [{"emailAddress": {"address": recipient}}],
        },
        "saveToSentItems": True,
    }
    req = urllib.request.Request(
        f"https://graph.microsoft.com/v1.0/users/{urllib.parse.quote(sender)}/sendMail",
        data=json.dumps(message).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req) as resp:
        if resp.status not in (200, 202):
            raise RuntimeError(f"Unexpected Graph status: {resp.status}")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: send_via_graph.py <requirements.json> <subject>", file=sys.stderr)
        sys.exit(1)

    requirements_path, subject = sys.argv[1], sys.argv[2]
    tenant_id = require_env("MS_TENANT_ID")
    client_id = require_env("MS_CLIENT_ID")
    client_secret = require_env("MS_CLIENT_SECRET")
    sender = require_env("MS_SENDER")
    recipient = require_env("MS_RECIPIENT")

    import subprocess

    body = subprocess.check_output(
        [sys.executable, os.path.join(os.path.dirname(__file__), "format_digest.py"), requirements_path],
        text=True,
    )

    token = get_token(tenant_id, client_id, client_secret)
    send_mail(token, sender, recipient, subject, body)
    print(f"Email sent to {recipient}")


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as exc:
        print(exc.read().decode(), file=sys.stderr)
        sys.exit(1)
