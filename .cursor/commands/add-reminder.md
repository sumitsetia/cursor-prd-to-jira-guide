---
description: Add a new item to Sumit's reminding assistant list (what, when, who, how, deadline)
---

# Add reminder

Add a requirement to Sumit's reminding assistant.

## Parse user input

Text after `/add-reminder` may include some or all fields. Extract when present:

| Field | JSON key |
|-------|----------|
| What to do | `what` |
| When to do | `when` |
| Who is this for | `who` |
| How to do | `how` |
| Deadline | `deadline` (`YYYY-MM-DD` or `TBD`) |

If any required field is missing, ask **one** short message listing only the missing fields.

## Save to both files (keep in sync)

1. `/Users/ssetia/Library/CloudStorage/OneDrive-WarnerBros.Discovery/Documents/sumit_assistant/requirements.json`
2. `sumit-assistant/requirements.json` in this repository

For each new entry set:
- `id`: next `REQ-###` (increment from highest existing)
- `created`: today as `YYYY-MM-DD`
- `status`: `open`

## Confirm

Reply with a brief summary table of the saved entry. Do not delete existing entries.
