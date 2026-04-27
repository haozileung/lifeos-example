#!/usr/bin/env python3
"""
Collect current week's LifeOS notes for weekly report generation.

Usage:
    collect-week-notes.py [--week YYYY-Www] [--vault /path/to/vault]

Output: Prints aggregated content to stdout. Exits 0 on success, 1 on error.
"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys


def get_week_range(year: int, week: int) -> tuple[datetime, datetime]:
    """Return (monday, sunday) for the given ISO year and week."""
    monday = datetime.fromisocalendar(year, week, 1)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def collect_notes(vault: Path, year: int, week: int) -> str:
    """Collect weekly note + daily notes content. Return aggregated markdown."""
    period_root = vault / "0.PeriodicNotes" / str(year)
    if not period_root.exists():
        return ""

    lines = []
    week_str = f"{year}-W{week:02d}"

    # Weekly note
    weekly_path = period_root / "Weekly" / f"{week_str}.md"
    if weekly_path.exists():
        lines.append(f"## 周报笔记: {weekly_path.relative_to(vault)}\n")
        lines.append(weekly_path.read_text(encoding="utf-8", errors="replace"))
        lines.append("\n---\n")

    # Daily notes in this week
    monday, sunday = get_week_range(year, week)
    daily_dir = period_root / "Daily"
    if not daily_dir.exists():
        return "\n".join(lines)

    current = monday
    while current <= sunday:
        mm = f"{current.month:02d}"
        dd_str = current.strftime("%Y-%m-%d")
        daily_path = daily_dir / mm / f"{dd_str}.md"
        if daily_path.exists():
            lines.append(f"\n## 日报: {dd_str}\n")
            lines.append(daily_path.read_text(encoding="utf-8", errors="replace"))
            lines.append("\n---\n")
        current += timedelta(days=1)

    return "\n".join(lines).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect current week's LifeOS notes")
    parser.add_argument("--week", metavar="YYYY-Www", help="e.g. 2026-W09")
    parser.add_argument("--vault", type=Path, default=None, help="Vault root path")
    args = parser.parse_args()

    vault = args.vault or Path.cwd()
    if not (vault / "0.PeriodicNotes").exists():
        print("Error: 0.PeriodicNotes not found. Is this a LifeOS vault?", file=sys.stderr)
        return 1

    if args.week:
        try:
            y, w = args.week.split("-")
            year, week = int(y), int(w.lstrip("W"))
        except ValueError:
            print("Error: --week must be like 2026-W09", file=sys.stderr)
            return 1
    else:
        now = datetime.now()
        year, week, _ = now.isocalendar()

    content = collect_notes(vault, year, week)
    if not content.strip():
        print(f"No notes found for {year}-W{week:02d}", file=sys.stderr)
        return 0

    print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
