---
description: Mark a reminding assistant item as done by id or description
---

# Mark reminder done

Mark a requirement as complete.

Match by `REQ-###` id or partial `what` text. Update both OneDrive and `sumit-assistant/requirements.json`. Set `status` to `done`.

## Push to GitHub (required)

```bash
git add sumit-assistant/requirements.json
git commit -m "Mark <REQ-ID> done: <short what summary>"
git push origin master
```

Only commit `sumit-assistant/requirements.json`. Confirm with id and push status.
