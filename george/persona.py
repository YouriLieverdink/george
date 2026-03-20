"""George system prompt assembly from .claude/agents/coach.md."""

from __future__ import annotations

from george import files


# Cached at session start
_base_persona: str | None = None


def _load_base() -> str:
    """Load coach.md and strip the YAML frontmatter."""
    global _base_persona
    if _base_persona is None:
        raw = files.read_agent("coach.md")
        # Strip YAML frontmatter (---)
        if raw.startswith("---"):
            end = raw.index("---", 3)
            raw = raw[end + 3:].strip()
        _base_persona = raw
    return _base_persona


def build_system(
    command: str | None = None,
    include_alerts: bool = False,
    include_periodization: bool = False,
) -> str:
    """Build the full system prompt for a Claude call.

    command: the slash command context (e.g., 'checkin', 'debrief')
    include_alerts: include alerts.md content
    include_periodization: include periodization.md content
    """
    from george import dates
    from datetime import datetime

    now = datetime.now()
    date_block = (
        f"# CURRENT DATE: {dates.today()} ({dates.weekday_name()}) {now.strftime('%H:%M')}\n\n"
        f"This is the authoritative date/time. The user message contains a [TODAY] section "
        f"with what is actually happening today. Trust THAT over anything in conversation logs. "
        f"Conversation logs were written on earlier dates — their 'today/tonight/tomorrow' "
        f"refers to THEIR date, not now."
    )

    parts = [date_block, _load_base()]

    if include_alerts:
        alerts = files.read_agent("alerts.md")
        if alerts.startswith("---"):
            end = alerts.index("---", 3)
            alerts = alerts[end + 3:].strip()
        parts.append(f"\n\n---\n\n# Alert Rules Reference\n\n{alerts}")

    if include_periodization:
        peri = files.read_agent("periodization.md")
        if peri.startswith("---"):
            end = peri.index("---", 3)
            peri = peri[end + 3:].strip()
        parts.append(f"\n\n---\n\n# Periodization Reference\n\n{peri}")

    # Behavioral constraint
    parts.append(
        "\n\n---\n\n"
        "# Behavioral Constraint\n\n"
        "All data is pre-assembled in the user message. Do NOT attempt to fetch data, "
        "use tools, or call APIs. All objective metrics, wellness data, calendar events, "
        "and file contents have already been gathered by the system.\n\n"
        "Respond as George. Stay in character. Follow the persona voice strictly."
    )

    if command:
        parts.append(f"\n\nCurrent interaction: /{command}")

    return "\n".join(parts)
