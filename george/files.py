"""Read/write data files, indexed log system."""

from __future__ import annotations

import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

CONVERSATIONS_DIR = DATA / "logs" / "conversations"
DAILY_DIR = DATA / "logs" / "daily"


def _ensure_parents(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def ensure_log_dirs() -> None:
    """Create indexed log directories if missing."""
    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)
    DAILY_DIR.mkdir(parents=True, exist_ok=True)


# --- Read helpers ---


def read_file(relative_path: str) -> str:
    """Read a data file by path relative to project root. Returns empty string if missing."""
    path = ROOT / relative_path
    if path.exists():
        return path.read_text()
    return ""


def read_data(name: str) -> str:
    """Read a file from data/. E.g. read_data('current-plan.md')."""
    return read_file(f"data/{name}")


def read_agent(name: str) -> str:
    """Read an agent file. E.g. read_agent('coach.md')."""
    return read_file(f".claude/agents/{name}")


# --- Indexed log reads ---


def read_conversation_index() -> str:
    """Read conversations/INDEX.md. Always loaded for timeline context."""
    path = CONVERSATIONS_DIR / "INDEX.md"
    if path.exists():
        return path.read_text()
    return ""


def read_daily_index() -> str:
    """Read daily/INDEX.md. Always loaded for timeline context."""
    path = DAILY_DIR / "INDEX.md"
    if path.exists():
        return path.read_text()
    return ""


def read_conversation(filename: str) -> str:
    """Read one conversation file by filename."""
    path = CONVERSATIONS_DIR / filename
    if path.exists():
        return path.read_text()
    return ""


def read_daily_log(date_str: str) -> str:
    """Read one day's log file."""
    path = DAILY_DIR / f"{date_str}.md"
    if path.exists():
        return path.read_text()
    return ""


def read_daily_logs_range(oldest: str, newest: str) -> str:
    """Read multiple days' log files (for /review). Returns concatenated content."""
    from george.dates import date_range
    parts = []
    for d in date_range(oldest, newest):
        content = read_daily_log(d)
        if content:
            parts.append(content)
    return "\n\n---\n\n".join(parts)


# --- Indexed log writes ---


def write_conversation(command: str, summary: str, content: str) -> None:
    """Write a conversation file + prepend to INDEX.md.

    Args:
        command: the command name (checkin, debrief, chat, etc.)
        summary: one-line summary for the index
        content: full markdown content (without frontmatter)
    """
    ensure_log_dirs()
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    filename = f"{date_str}-{now.strftime('%H%M')}-{command}.md"

    # Write individual file with frontmatter
    file_content = (
        f"---\n"
        f"date: {date_str}\n"
        f'time: "{time_str}"\n'
        f"command: {command}\n"
        f"summary: {summary}\n"
        f"---\n\n"
        f"{content}\n"
    )
    (CONVERSATIONS_DIR / filename).write_text(file_content)

    # Prepend to INDEX.md
    index_path = CONVERSATIONS_DIR / "INDEX.md"
    existing = index_path.read_text() if index_path.exists() else "# Conversation Index\n<!-- newest first, one line per entry -->\n"

    # Insert new entry after the header lines
    lines = existing.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("#") or line.startswith("<!--"):
            insert_at = i + 1
        else:
            break

    new_entry = f"- {date_str} {time_str} | {command} | {summary}"
    lines.insert(insert_at, new_entry)
    index_path.write_text("\n".join(lines))


def write_daily_log(date_str: str, summary: str, content: str) -> None:
    """Write/append to a day's log file + update INDEX.md.

    Args:
        date_str: YYYY-MM-DD
        summary: one-line summary for the index
        content: markdown content to write/append
    """
    ensure_log_dirs()
    d = date.fromisoformat(date_str)
    weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][d.weekday()]

    path = DAILY_DIR / f"{date_str}.md"

    if path.exists():
        # Append to existing day file
        existing = path.read_text()
        path.write_text(existing.rstrip() + "\n\n" + content + "\n")
        # Update the summary in the index (replace existing line for this date)
        _update_daily_index_entry(date_str, summary)
    else:
        # Create new day file with frontmatter
        file_content = (
            f"---\n"
            f"date: {date_str}\n"
            f"weekday: {weekday}\n"
            f"summary: {summary}\n"
            f"---\n\n"
            f"{content}\n"
        )
        path.write_text(file_content)
        # Prepend to INDEX.md
        _prepend_daily_index_entry(date_str, summary)


def _prepend_daily_index_entry(date_str: str, summary: str) -> None:
    """Add a new entry to the top of the daily INDEX.md."""
    index_path = DAILY_DIR / "INDEX.md"
    existing = index_path.read_text() if index_path.exists() else "# Daily Log Index\n<!-- newest first, one line per day -->\n"

    lines = existing.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("#") or line.startswith("<!--"):
            insert_at = i + 1
        else:
            break

    new_entry = f"- {date_str} | {summary}"
    lines.insert(insert_at, new_entry)
    index_path.write_text("\n".join(lines))


def _update_daily_index_entry(date_str: str, summary: str) -> None:
    """Update an existing date's entry in daily INDEX.md, or add if missing."""
    index_path = DAILY_DIR / "INDEX.md"
    if not index_path.exists():
        _prepend_daily_index_entry(date_str, summary)
        return

    existing = index_path.read_text()
    # Try to find and replace existing line for this date
    pattern = re.compile(rf"^- {re.escape(date_str)} \|.*$", re.MULTILINE)
    new_entry = f"- {date_str} | {summary}"

    if pattern.search(existing):
        updated = pattern.sub(new_entry, existing)
        index_path.write_text(updated)
    else:
        _prepend_daily_index_entry(date_str, summary)

    # Also update frontmatter summary in the day file
    day_path = DAILY_DIR / f"{date_str}.md"
    if day_path.exists():
        content = day_path.read_text()
        content = re.sub(
            r"^(summary: ).*$",
            rf"\g<1>{summary}",
            content,
            count=1,
            flags=re.MULTILINE,
        )
        day_path.write_text(content)


# --- Legacy write helpers (unchanged) ---


def append_weekly_reviews(content: str) -> None:
    """Append an entry to weekly-reviews.md."""
    path = DATA / "logs" / "weekly-reviews.md"
    existing = path.read_text() if path.exists() else ""

    marker = "<!-- Entries will be appended below this line. -->"
    if marker in existing:
        idx = existing.index(marker) + len(marker)
        updated = existing[:idx] + "\n\n" + content + existing[idx:]
    else:
        updated = existing.rstrip() + "\n\n" + content + "\n"

    path.write_text(updated)


def update_coach_memory(section: str, content: str) -> None:
    """Append content to a specific section in coach-memory.md.

    section: the H2 header text, e.g. 'Open Follow-ups'
    content: text to append at the end of that section
    """
    path = DATA / "memory" / "coach-memory.md"
    existing = path.read_text() if path.exists() else ""

    header = f"## {section}"
    if header not in existing:
        # Section doesn't exist — append it
        updated = existing.rstrip() + f"\n\n{header}\n\n{content}\n"
    else:
        idx = existing.index(header) + len(header)
        rest = existing[idx:]
        # Find next H2
        next_h2 = rest.find("\n## ")
        if next_h2 >= 0:
            insert_at = idx + next_h2
            updated = existing[:insert_at].rstrip() + "\n" + content + "\n" + existing[insert_at:]
        else:
            updated = existing.rstrip() + "\n" + content + "\n"

    path.write_text(updated)


def update_current_plan(content: str) -> None:
    """Overwrite current-plan.md with new content."""
    path = DATA / "current-plan.md"
    path.write_text(content)


def write_archive(relative_path: str, content: str) -> None:
    """Write an archive file (e.g., 'weekly/2026-W10.md')."""
    path = DATA / "archive" / relative_path
    _ensure_parents(path)
    path.write_text(content)
