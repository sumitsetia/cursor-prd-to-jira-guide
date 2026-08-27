#!/usr/bin/env python3
"""Format requirements.json into a plain-text digest."""

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


def deadline_sort_key(item: dict):
    deadline_raw = item.get("deadline", "").strip()
    if not deadline_raw or deadline_raw.lower() in {"none", "n/a", "tbd"}:
        return (1, date.max)
    parsed = parse_date(deadline_raw)
    if parsed is None:
        return (1, date.max)
    return (0, parsed)


def is_overdue(item: dict, today: date) -> bool:
    deadline_raw = item.get("deadline", "").strip()
    parsed = parse_date(deadline_raw)
    return parsed is not None and parsed < today


def main() -> None:
    path = sys.argv[1]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    open_items = [r for r in data.get("requirements", []) if r.get("status", "open") != "done"]
    open_items.sort(key=deadline_sort_key)
    today = date.today()

    lines = [
        "Good morning, Sumit!",
        "",
        f"You have {len(open_items)} open requirement(s).",
        "",
    ]

    if not open_items:
        lines.append("No open requirements. Add new ones anytime in Cursor.")
    else:
        lines.append("Open requirements (soonest deadline first):")
        lines.append("")
        for item in open_items:
            req_id = item.get("id", "?")
            overdue = is_overdue(item, today)
            marker = "[OVERDUE] " if overdue else ""
            lines.append(f"{marker}[{req_id}] {item.get('what', '(no description)')}")
            lines.append(f"  When: {item.get('when', '—')}")
            lines.append(f"  For:  {item.get('who', '—')}")
            lines.append(f"  How:  {item.get('how', '—')}")
            due = item.get("deadline", "—")
            lines.append(f"  Due:  {due}{'  << OVERDUE' if overdue else ''}")
            lines.append("")

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
