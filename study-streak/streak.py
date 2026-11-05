#!/usr/bin/env python3
"""Tiny local tracker for daily study sessions."""

from __future__ import annotations

import argparse
import json
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data.json")


def load_sessions() -> set[date]:
    if not DATA_FILE.exists():
        return set()
    try:
        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid data file: {DATA_FILE}") from error
    return {date.fromisoformat(item) for item in raw}


def save_sessions(sessions: set[date]) -> None:
    DATA_FILE.write_text(
        json.dumps(sorted(item.isoformat() for item in sessions), indent=2) + "\n",
        encoding="utf-8",
    )


def current_streak(sessions: set[date]) -> int:
    streak = 0
    cursor = date.today()
    while cursor in sessions:
        streak += 1
        cursor -= timedelta(days=1)
    return streak


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track daily study activity.")
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument("--mark", action="store_true", help="mark today as active")
    actions.add_argument("--stats", action="store_true", help="show activity statistics")
    actions.add_argument("--export", action="store_true", help="print all active dates")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    sessions = load_sessions()

    if args.mark:
        sessions.add(date.today())
        save_sessions(sessions)
        print(f"Marked today. Current streak: {current_streak(sessions)} day(s).")
    elif args.stats:
        print(f"Active days: {len(sessions)}")
        print(f"Current streak: {current_streak(sessions)} day(s).")
    elif args.export:
        print("\n".join(item.isoformat() for item in sorted(sessions)))
    else:
        build_parser().print_help()


if __name__ == "__main__":
    main()
