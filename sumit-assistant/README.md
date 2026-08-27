# Sumit's Reminding Assistant (repo mirror)

Personal requirement tracker with a **daily Slack digest at 8:00 AM Central**.

| Path | Purpose |
|------|---------|
| `requirements.json` | Requirements (synced with OneDrive) |
| `scripts/format_digest_slack.py` | Formats the Slack message |
| `scripts/send_slack_webhook.py` | Optional local send via Slack webhook |
| `automation-morning-digest.prefill.json` | Draft for Cursor Automation editor |

## OneDrive source of truth (local)

`/Users/ssetia/Library/CloudStorage/OneDrive-WarnerBros.Discovery/Documents/sumit_assistant/requirements.json`

When adding requirements in Cursor, both files are updated.

---

## Cursor Automation setup (recommended)

### Step 1 — Connect Slack to Cursor

1. Go to [cursor.com/dashboard](https://cursor.com/dashboard) → **Integrations**
2. Connect **Slack** and authorize your WBD workspace
3. Confirm the Cursor app can post messages

### Step 2 — Create the automation

Open **[cursor.com/automations/new](https://cursor.com/automations/new)** and configure:

| Field | Value |
|-------|-------|
| **Name** | Morning Requirements Digest (Slack) |
| **Trigger** | Scheduled → **8:00 AM** → **Central Time** → **Every day** |
| **Repository** | `sumitsetia/cursor-prd-to-jira-guide` on branch `master` |
| **Tools** | Enable **Send to Slack** |
| **Slack destination** | **DM yourself** (easiest) or a private channel like `#sumit-reminders` |

### Step 3 — Paste this prompt

```
You are Sumit's reminding assistant. Every morning at 8 AM Central, send a Slack digest of open requirements.

1. Read `sumit-assistant/requirements.json` in this repository.
2. Run `python3 sumit-assistant/scripts/format_digest_slack.py sumit-assistant/requirements.json` to build the message.
3. Use Send to Slack to deliver the digest. Prefer a DM to Sumit (automation owner).
4. Lead with a one-line summary (count of open items, anything overdue or due today).

Group items as: OVERDUE, DUE TODAY, UPCOMING, NO DEADLINE. Include for each: id, what, when, who, how, deadline.

Do not modify requirements unless entries are clearly duplicates. Do not open a pull request. If there are zero open requirements, still send a short "no open requirements" Slack message.
```

Save and **Activate**.

---

## Optional local fallback (Slack webhook)

If you also want reminders when your Mac runs locally (without waiting for cloud automation):

1. In Slack: **Apps** → **Incoming Webhooks** → create webhook for a DM or private channel
2. Save the URL:

```bash
echo 'SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL' >> ~/.sumit-assistant.env
```

3. Test:

```bash
python3 sumit-assistant/scripts/send_slack_webhook.py sumit-assistant/requirements.json
```

---

## Add requirements

Tell Cursor in chat:

- **What to do** / **When to do** / **Who is this for** / **How to do** / **Deadline**

Example:

```
What: Send weekly C360 metrics deck
When: Every Friday before noon
Who: Data leadership
How: Export from Snowflake, attach xlsx
Deadline: 2026-09-05
```

---

## Shortcuts in Cursor

Type `/` in Agent chat to use these slash commands:

| Command | What it does |
|---------|----------------|
| `/add-reminder` | Add a new item (asks for missing fields) |
| `/list-reminders` | Show all open items |
| `/mark-reminder-done` | Mark an item complete |

**Examples:**

```
/add-reminder What: Review Q3 roadmap | When: Before Monday standup | Who: Product team | How: Read Confluence doc and leave comments | Deadline: 2026-09-01
```

```
/list-reminders
```

```
/mark-reminder-done REQ-001
```

**Keyboard shortcut:** `Cmd+Shift+R` opens Agent chat — then type `/add-reminder`.

Commands live in `~/.cursor/commands/` (all projects) and `.cursor/commands/` (this repo).
