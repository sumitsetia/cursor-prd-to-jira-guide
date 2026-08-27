#!/usr/bin/env python3
"""Format requirements.json into a plain-text email body."""

import json
import sys
from datetime import date, datetime


def parse_date(value: str):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    return None


def main() -> None:
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    requirements = data.get("requirements", [])
    open_items = [r for r in requirements if r.get("status", "open") != "done"]
    today = date.today()

    overdue = []
    due_today = []
    upcoming = []
    no_deadline = []

    for item in open_items:
        deadline_raw = item.get("deadline", "").strip()
        if not deadline_raw or deadline_raw.lower() in {"none", "n/a", "tbd"}:
            no_deadline.append(item)
            continue
        deadline = parse_date(deadline_raw)
        if deadline is None:
            no_deadline.append(item)
        elif deadline < today:
            overdue.append(item)
        elif deadline == today:
            due_today.append(item)
        else:
            upcoming.append(item)

    lines = [
        "Good morning, Sumit!",
        "",
        f"You have {len(open_items)} open requirement(s).",
        "",
    ]

    def section(title: str, items: list[dict]) -> None:
        if not items:
            return
        lines.append(title)
        lines.append("-" * len(title))
        for item in items:
            req_id = item.get("id", "?")
            lines.append(f"[{req_id}] {item.get('what', '(no description)')}")
            lines.append(f"  When: {item.get('when', '—')}")
            lines.append(f"  For:  {item.get('who', '—')}")
            lines.append(f"  How:  {item.get('how', '—')}")
            lines.append(f"  Due:  {item.get('deadline', '—')}")
            lines.append("")
        lines.append("")

    section("OVERDUE", overdue)
    section("DUE TODAY", due_today)
    section("UPCOMING", upcoming)
    section("NO DEADLINE", no_deadline)

    if not open_items:
        lines.append("No open requirements. Add new ones anytime in Cursor.")

    lines.extend(
        [
            "—",
            "Managed by your Cursor reminding assistant.",
            f"Source: {path}",
        ]
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
