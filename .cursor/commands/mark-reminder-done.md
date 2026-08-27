---
description: Remove a completed reminder from Sumit's list by id or task name
---

# Mark reminder done

Remove a completed requirement from the list (do not keep it).

Match by `REQ-###` id or partial task `what` name. **Delete** the entry from both OneDrive and `sumit-assistant/requirements.json` — do not set `status: done`.

## Push to GitHub (required)

```bash
git add sumit-assistant/requirements.json
git commit -m "Remove <REQ-ID>: <short what summary>"
git push origin master
```

Only commit `sumit-assistant/requirements.json`. Confirm with id and push status.
