#!/usr/bin/env python3
"""Format requirements.json into a Slack-friendly digest."""

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
    overdue_count = sum(1 for item in open_items if is_overdue(item, today))

    lines = [
        f"*Good morning, Sumit!* :sunrise:",
        f"You have *{len(open_items)}* open requirement(s) for *{today.strftime('%A, %B %-d, %Y')}*.",
        "",
    ]

    if overdue_count:
        lines.append(f"🔴 *{overdue_count} overdue* — sorted by deadline (soonest first).")
        lines.append("")

    if not open_items:
        lines.append("_No open requirements. Add new ones anytime in Cursor._")
    else:
        lines.append("*Open requirements* _(soonest deadline first)_")
        lines.append("")
        for item in open_items:
            req_id = item.get("id", "?")
            overdue = is_overdue(item, today)
            prefix = "🔴 " if overdue else ""
            lines.append(f"• {prefix}`[{req_id}]` *{item.get('what', '(no description)')}*")
            lines.append(f"  _When:_ {item.get('when', '—')}")
            lines.append(f"  _For:_ {item.get('who', '—')}")
            lines.append(f"  _How:_ {item.get('how', '—')}")
            if overdue:
                lines.append(f"  _Due:_ 🔴 *{item.get('deadline', '—')}* _(OVERDUE)_")
            else:
                lines.append(f"  _Due:_ *{item.get('deadline', '—')}*")
            lines.append("")

    lines.append("—")
    lines.append("_Managed by your Cursor reminding assistant._")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
