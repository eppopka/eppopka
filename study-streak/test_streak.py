import importlib.util
import json
from datetime import date, timedelta
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("streak.py")
SPEC = importlib.util.spec_from_file_location("streak", MODULE_PATH)
streak = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(streak)


def test_current_streak_counts_consecutive_days():
    today = date.today()
    sessions = {today, today - timedelta(days=1), today - timedelta(days=2)}
    assert streak.current_streak(sessions) == 3


def test_current_streak_is_zero_when_today_is_missing():
    assert streak.current_streak({date.today() - timedelta(days=1)}) == 0


def test_sessions_are_saved_in_sorted_json(tmp_path):
    streak.DATA_FILE = tmp_path / "data.json"
    sessions = {date(2026, 11, 6), date(2026, 11, 4)}
    streak.save_sessions(sessions)
    assert json.loads(streak.DATA_FILE.read_text()) == ["2026-11-04", "2026-11-06"]


def test_missing_data_file_starts_empty(tmp_path):
    streak.DATA_FILE = tmp_path / "missing.json"
    assert streak.load_sessions() == set()
