#!/usr/bin/env python3
"""Tiny local tracker for daily study sessions."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

DATA_FILE = Path(__file__).with_name("data.json")


def load_sessions() -> set[date]:
    if not DATA_FILE.exists():
        return set()
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
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


def main() -> None:
    sessions = load_sessions()
    print("1 — отметить сегодня")
    print("2 — показать статистику")
    choice = input("> ").strip()

    if choice == "1":
        sessions.add(date.today())
        save_sessions(sessions)
        print(f"Готово. Текущая серия: {current_streak(sessions)} дн.")
    elif choice == "2":
        print(f"Всего активных дней: {len(sessions)}")
        print(f"Текущая серия: {current_streak(sessions)} дн.")
    else:
        print("Неизвестная команда")


if __name__ == "__main__":
    main()
