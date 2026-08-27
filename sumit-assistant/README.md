# Sumit's Reminding Assistant (repo mirror)

This folder mirrors the OneDrive tracker so **Cursor Automations** (cloud) can read requirements.

| Path | Purpose |
|------|---------|
| `requirements.json` | Requirements (synced with OneDrive) |
| `scripts/format_digest.py` | Formats the email body |
| `scripts/send_via_graph.py` | Sends email via Microsoft Graph (cloud) |
| `automation-morning-digest.prefill.json` | Draft for Cursor Automation editor |

## OneDrive source of truth (local)

`/Users/ssetia/Library/CloudStorage/OneDrive-WarnerBros.Discovery/Documents/sumit_assistant/requirements.json`

When adding requirements in Cursor, both files are updated.

## Cursor Automation setup

1. Commit and push this folder to `sumitsetia/cursor-prd-to-jira-guide`.
2. Open the **Agents Window** and say: **Create a Cursor automation from `sumit-assistant/automation-morning-digest.prefill.json`**
3. In the editor, set schedule timezone to **Central Time (CST/CDT)** and confirm cron **8:00 AM daily**.
4. Attach repository `sumitsetia/cursor-prd-to-jira-guide` on branch `master`.

## Email from cloud (optional Graph setup)

Add these secrets in [Cursor Cloud Agents settings](https://cursor.com/dashboard?tab=cloud-agents):

| Secret | Example |
|--------|---------|
| `MS_TENANT_ID` | WBD tenant ID |
| `MS_CLIENT_ID` | Azure app client ID |
| `MS_CLIENT_SECRET` | Azure app secret |
| `MS_SENDER` | `sumit.setia@wbd.com` |
| `MS_RECIPIENT` | `sumit.setia@wbd.com` |

Azure app needs **Application** permission `Mail.Send` with admin consent.

Without Graph secrets, the automation still runs and prints the digest in the run log.

## Local fallback (Outlook on Mac)

If your Mac is on at 8 AM, the OneDrive launchd job can still send via Outlook:

```bash
bash "/Users/ssetia/Library/CloudStorage/OneDrive-WarnerBros.Discovery/Documents/sumit_assistant/scripts/send_morning_digest.sh"
```
