"""/status — Dashboard. NO Claude call. Pure script output."""

from __future__ import annotations

import re
from datetime import date

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from george import dates, files, icu


def _parse_events_md() -> list[dict]:
    """Parse events.md for race calendar."""
    content = files.read_data("references/events.md")
    events = []
    current: dict | None = None

    for line in content.split("\n"):
        if line.startswith("### "):
            if current:
                events.append(current)
            current = {"name": line[4:].strip()}
        elif current and line.startswith("- **Date"):
            m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if m:
                current["date"] = m.group(1)
            elif ":" in line:
                current["date_text"] = line.split(":", 2)[-1].strip()
        elif current and line.startswith("- **Priority"):
            current["priority"] = line.split(":")[-1].strip()
        elif current and line.startswith("- **Dates"):
            m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if m:
                current["date"] = m.group(1)

    if current:
        events.append(current)

    return events


def _parse_current_plan() -> dict:
    """Extract key info from current-plan.md."""
    content = files.read_data("current-plan.md")
    info = {}

    for line in content.split("\n"):
        if "**Current week:**" in line:
            info["week"] = line.split("**Current week:**")[-1].strip()
        elif "**Current phase:**" in line:
            info["phase"] = line.split("**Current phase:**")[-1].strip()
        elif "**Event date:**" in line:
            m = re.search(r"(\d{4}-\d{2}-\d{2})", line)
            if m:
                info.setdefault("event_dates", []).append(m.group(1))

    return info


def run(session) -> None:
    console = session.console if hasattr(session, "console") else Console()
    today = dates.today()
    console.print(f"\n[dim]{today} — {dates.weekday_name()}[/dim]")

    # Read local data
    plan_info = _parse_current_plan()
    race_events = _parse_events_md()

    # Phase info
    week = plan_info.get("week", "?")
    phase = plan_info.get("phase", "?")
    console.print(f"\n[bold]{phase}[/bold] — {week}")

    # Race countdown
    race_table = Table(show_header=False, box=None, padding=(0, 2))
    race_table.add_column("Event", style="bold")
    race_table.add_column("Date")
    race_table.add_column("Countdown", style="cyan")

    for evt in race_events:
        d = evt.get("date")
        if d:
            try:
                days_left = dates.days_until(d)
                if days_left >= 0:
                    countdown = f"{days_left} days"
                    priority = evt.get("priority", "")
                    name = evt.get("name", "")
                    if priority:
                        name = f"[{priority}] {name}"
                    race_table.add_row(name, d, countdown)
            except ValueError:
                pass

    if race_table.row_count > 0:
        console.print()
        console.print(race_table)

    # ICU data — wrapped in try/except for API unavailable
    try:
        # Today's events
        today_events = icu.events(today, today)
        if today_events:
            console.print(f"\n[bold]Today's sessions:[/bold]")
            for evt in today_events:
                cat = evt.get("category", "")
                name = evt.get("name", "")
                sport = evt.get("type", "")
                if cat == "WORKOUT":
                    dur_s = evt.get("moving_time")
                    dur = f" ({int(dur_s)//60} min)" if dur_s else ""
                    console.print(f"  {sport} — {name}{dur}")
                elif cat == "NOTE":
                    desc = evt.get("description", "")[:80]
                    console.print(f"  [dim]NOTE: {name} — {desc}[/dim]")
                elif cat == "SICKNESS":
                    console.print(f"  [red]SICKNESS marker[/red]")
        else:
            console.print(f"\n[dim]No sessions planned for today.[/dim]")
    except icu.ICUError as e:
        console.print(f"\n[dim]Calendar unavailable: {e}[/dim]")

    try:
        # Athlete summary
        summary = icu.athlete_summary()
        if summary:
            ctl = summary.get("fitness")
            atl = summary.get("fatigue")
            tsb = summary.get("form")
            parts = []
            if ctl is not None:
                parts.append(f"CTL [bold]{ctl:.0f}[/bold]")
            if atl is not None:
                parts.append(f"ATL {atl:.0f}")
            if tsb is not None:
                color = "green" if tsb > 0 else "red" if tsb < -20 else "yellow"
                parts.append(f"TSB [{color}]{tsb:.0f}[/{color}]")
            if parts:
                console.print(f"\n{'  |  '.join(parts)}")
    except icu.ICUError:
        pass

    try:
        # Last activity
        yesterday = dates.yesterday()
        recent = icu.activities(dates.days_ago(3), today)
        if recent:
            last = recent[-1]
            a_date = (last.get("start_date_local") or "")[:10]
            a_type = last.get("type", "")
            a_name = last.get("name", "")
            a_dur = last.get("moving_time")
            dur_str = f" ({int(a_dur)//60} min)" if a_dur else ""
            a_load = last.get("icu_training_load")
            load_str = f" load {int(a_load)}" if a_load else ""
            console.print(f"\n[dim]Last session: {a_date} {a_type} {a_name}{dur_str}{load_str}[/dim]")
    except icu.ICUError:
        pass

    console.print()
