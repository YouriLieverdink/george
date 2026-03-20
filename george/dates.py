"""Date helpers — today, week ranges, ISO weeks."""

from __future__ import annotations

from datetime import date, timedelta


def today() -> str:
    """Today's date as YYYY-MM-DD."""
    return date.today().isoformat()


def yesterday() -> str:
    return (date.today() - timedelta(days=1)).isoformat()


def days_ago(n: int) -> str:
    return (date.today() - timedelta(days=n)).isoformat()


def days_from_now(n: int) -> str:
    return (date.today() + timedelta(days=n)).isoformat()


def week_start(d: date | None = None) -> str:
    """Monday of the week containing d (default: today)."""
    d = d or date.today()
    monday = d - timedelta(days=d.weekday())
    return monday.isoformat()


def week_end(d: date | None = None) -> str:
    """Sunday of the week containing d (default: today)."""
    d = d or date.today()
    sunday = d + timedelta(days=6 - d.weekday())
    return sunday.isoformat()


def iso_week(d: date | None = None) -> str:
    """ISO week label like '2026-W12'."""
    d = d or date.today()
    year, week, _ = d.isocalendar()
    return f"{year}-W{week:02d}"


def weekday_name(d: date | None = None) -> str:
    """Short weekday name like 'Mon', 'Tue'."""
    d = d or date.today()
    return ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][d.weekday()]


def parse_date(s: str) -> date:
    """Parse YYYY-MM-DD string to date."""
    return date.fromisoformat(s)


def days_until(target: str) -> int:
    """Days from today to a target date string."""
    return (parse_date(target) - date.today()).days


def date_range(oldest: str, newest: str) -> list[str]:
    """All dates from oldest to newest inclusive."""
    start = parse_date(oldest)
    end = parse_date(newest)
    return [(start + timedelta(days=i)).isoformat() for i in range((end - start).days + 1)]
