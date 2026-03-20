"""One-time migration: split monolithic logs into indexed individual files.

Run: python3 -m george.migrate_logs
"""

from __future__ import annotations

import re
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
LOGS = DATA / "logs"


def migrate_conversations() -> None:
    """Split conversations.md into individual files + INDEX.md."""
    src = LOGS / "conversations.md"
    if not src.exists():
        print("conversations.md not found, skipping.")
        return

    dest = LOGS / "conversations"
    if dest.exists() and (dest / "INDEX.md").exists():
        print("conversations/ already exists with INDEX.md, skipping. Delete to re-migrate.")
        return

    dest.mkdir(parents=True, exist_ok=True)

    content = src.read_text()

    # Parse entries: each starts with ## YYYY-MM-DD HH:MM — command
    entries: list[dict] = []
    current: dict | None = None

    for line in content.split("\n"):
        header_match = re.match(
            r"^## (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) — (.+)$", line
        )
        if header_match:
            if current:
                entries.append(current)
            date_str = header_match.group(1)
            time_str = header_match.group(2)
            command_raw = header_match.group(3).strip()
            # Normalize command: "/coach:checkin" -> "checkin", "session" -> "session"
            command = command_raw.replace("/coach:", "").replace(" ", "-").lower()
            current = {
                "date": date_str,
                "time": time_str,
                "command": command,
                "lines": [],
            }
        elif current is not None:
            current["lines"].append(line)

    if current:
        entries.append(current)

    if not entries:
        print("No conversation entries found.")
        return

    # Build index and write individual files
    index_lines = [
        "# Conversation Index",
        "<!-- newest first, one line per entry -->",
    ]

    for entry in entries:
        body = "\n".join(entry["lines"]).strip()

        # Extract summary from first ### Summary section or first paragraph
        summary = _extract_summary(body)

        time_compact = entry["time"].replace(":", "")
        filename = f"{entry['date']}-{time_compact}-{entry['command']}.md"

        file_content = (
            f"---\n"
            f"date: {entry['date']}\n"
            f'time: "{entry["time"]}"\n'
            f"command: {entry['command']}\n"
            f"summary: {summary}\n"
            f"---\n\n"
            f"{body}\n"
        )
        (dest / filename).write_text(file_content)

        index_lines.append(
            f"- {entry['date']} {entry['time']} | {entry['command']} | {summary}"
        )

    (dest / "INDEX.md").write_text("\n".join(index_lines) + "\n")

    # Backup original
    backup = LOGS / "conversations.md.bak"
    shutil.move(str(src), str(backup))
    print(f"Migrated {len(entries)} conversations -> {dest}/")
    print(f"Original backed up to {backup}")


def migrate_daily_log() -> None:
    """Split daily-log.md into individual day files + INDEX.md."""
    src = LOGS / "daily-log.md"
    if not src.exists():
        print("daily-log.md not found, skipping.")
        return

    dest = LOGS / "daily"
    if dest.exists() and (dest / "INDEX.md").exists():
        print("daily/ already exists with INDEX.md, skipping. Delete to re-migrate.")
        return

    dest.mkdir(parents=True, exist_ok=True)

    content = src.read_text()

    # Parse entries: each starts with ## YYYY-MM-DD — Weekday
    entries: list[dict] = []
    current: dict | None = None

    for line in content.split("\n"):
        header_match = re.match(
            r"^## (\d{4}-\d{2}-\d{2}) — (\w+)$", line
        )
        if header_match:
            if current:
                entries.append(current)
            current = {
                "date": header_match.group(1),
                "weekday": header_match.group(2),
                "lines": [],
            }
        elif current is not None:
            current["lines"].append(line)

    if current:
        entries.append(current)

    if not entries:
        print("No daily log entries found.")
        return

    # Build index (newest first) and write individual files
    index_lines = [
        "# Daily Log Index",
        "<!-- newest first, one line per day -->",
    ]

    # Entries are oldest-first in the file; reverse for index
    for entry in reversed(entries):
        body = "\n".join(entry["lines"]).strip()
        summary = _extract_daily_summary(body)

        filename = f"{entry['date']}.md"
        file_content = (
            f"---\n"
            f"date: {entry['date']}\n"
            f"weekday: {entry['weekday']}\n"
            f"summary: {summary}\n"
            f"---\n\n"
            f"{body}\n"
        )
        (dest / filename).write_text(file_content)

        index_lines.append(f"- {entry['date']} | {summary}")

    (dest / "INDEX.md").write_text("\n".join(index_lines) + "\n")

    # Backup original
    backup = LOGS / "daily-log.md.bak"
    shutil.move(str(src), str(backup))
    print(f"Migrated {len(entries)} daily entries -> {dest}/")
    print(f"Original backed up to {backup}")


def _extract_summary(body: str) -> str:
    """Extract a one-line summary from a conversation body."""
    # Try ### Summary section
    match = re.search(r"### Summary\n+(.+?)(?:\n\n|\n###|\Z)", body, re.DOTALL)
    if match:
        # Take first sentence or first 120 chars
        text = match.group(1).strip().split("\n")[0]
        if len(text) > 120:
            text = text[:117] + "..."
        return text

    # Fallback: first non-empty line
    for line in body.split("\n"):
        line = line.strip()
        if line and not line.startswith("#"):
            if len(line) > 120:
                line = line[:117] + "..."
            return line

    return "No summary"


def _extract_daily_summary(body: str) -> str:
    """Extract a one-line summary from a daily log body."""
    # Look for key data: planned session, readiness, RPE
    parts = []

    # Session info
    session_match = re.search(r"Planned session:\s*(.+?)(?:\s*\||\n)", body)
    if session_match:
        parts.append(session_match.group(1).strip())

    # Readiness
    readiness_match = re.search(r"Readiness:\s*(\w+)", body)
    if readiness_match:
        parts.append(f"Readiness {readiness_match.group(1)}")

    # RPE
    rpe_match = re.search(r"RPE:\s*(\d+/\d+)", body)
    if rpe_match:
        parts.append(f"RPE {rpe_match.group(1)}")

    if parts:
        summary = ". ".join(parts)
        if len(summary) > 120:
            summary = summary[:117] + "..."
        return summary

    # Fallback: first non-empty, non-header line
    for line in body.split("\n"):
        line = line.strip().lstrip("- ")
        if line and not line.startswith("#"):
            if len(line) > 120:
                line = line[:117] + "..."
            return line

    return "No summary"


def main() -> None:
    print("Migrating logs to indexed format...\n")
    migrate_conversations()
    print()
    migrate_daily_log()
    print("\nDone.")


if __name__ == "__main__":
    main()
