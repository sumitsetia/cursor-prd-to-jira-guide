# PRD → Jira Backlog — Cursor Agent Guide

Turn Confluence PRDs into structured Jira backlogs using Cursor + Atlassian MCP.

**Hierarchy:** Initiative → Feature → Capability → Epic → Story

## What's in this repo

| File | Purpose |
|---|---|
| [`prd-to-jira-backlog-guide.md`](./prd-to-jira-backlog-guide.md) | Full playbook — workflow, field templates, prompt examples |
| [`.cursor/rules/prd-to-jira.mdc`](./.cursor/rules/prd-to-jira.mdc) | Cursor rule the agent loads for PRD → Jira tasks |

## Quick start

1. **Clone this repo** (or copy `.cursor/rules/prd-to-jira.mdc` into your project)
2. **Connect Atlassian MCP in Cursor** — see [Connect Atlassian to Cursor](https://wbdstreaming.atlassian.net/wiki/spaces/~6400e33a4307e46ad144cce5/pages/3807610331/Connect+Atlassian+to+Cursor+Step-by-Step+Guide)
3. **Paste a prompt** in Cursor Agent chat:

```
Read this PRD and create Jira Feature + Capabilities following our PRD-to-Jira guide:
[Confluence PRD URL]

Project: MLG
Parent Initiative: WBD-145
Do NOT create Epics or Stories yet — present the breakdown first.
```

## Confluence (team doc)

Published guide: [PRD → Jira Backlog — Cursor Agent Guide](https://wbdstreaming.atlassian.net/wiki/spaces/~6400e33a4307e46ad144cce5/pages/3952084056/PRD+Jira+Backlog+Cursor+Agent+Guide)

## Related WBD standards

- [Product — PRDs and Jira Best Practices](https://wbdstreaming.atlassian.net/wiki/spaces/C360/pages/1310330550/Product+-+PRDs+and+Jira+Best+Practices)
- [Jira Field Standards — Required Fields by Level](https://wbdstreaming.atlassian.net/wiki/spaces/~6400e33a4307e46ad144cce5/pages/3806757531/Jira+Field+Standards+Required+Fields+by+Level)
