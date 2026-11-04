import importlib.util
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
