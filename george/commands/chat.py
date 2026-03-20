"""/chat — Freeform conversation with George."""

from __future__ import annotations

from datetime import datetime

from george import files, icu, persona, dates


def _build_today_section() -> str:
    """Build an explicit 'what is happening today' section from ICU calendar."""
    today = dates.today()
    lines = [f"**Today is {today} ({dates.weekday_name()}), {datetime.now().strftime('%H:%M')}.**"]

    try:
        today_events = icu.events(today, today)
        if today_events:
            lines.append("Today's calendar:")
            for e in today_events:
                cat = e.get("category", "")
                name = e.get("name", "")
                if cat == "WORKOUT":
                    sport = e.get("type", "")
                    lines.append(f"- {cat}: {name} ({sport})")
                elif cat == "NOTE":
                    desc = (e.get("description") or "")[:100]
                    lines.append(f"- NOTE: {name} — {desc}")
                else:
                    lines.append(f"- {cat}: {name}")
        else:
            lines.append("No sessions planned for today.")
    except icu.ICUError:
        lines.append("(Calendar unavailable)")

    # Check today's daily log to see what already happened
    today_log = files.read_daily_log(dates.today())
    if today_log:
        lines.append(f"\nAlready logged today:\n{today_log[:500]}")
    else:
        lines.append("No check-in or debrief logged yet today.")

    return "\n".join(lines)


def _build_context() -> str:
    """Assemble context for chat."""
    parts = []

    current_plan = files.read_data("current-plan.md")
    if current_plan:
        parts.append(f"## Current Plan\n\n{current_plan}")

    coach_memory = files.read_data("memory/coach-memory.md")
    if coach_memory:
        parts.append(f"## Coach Memory\n\n{coach_memory}")

    events = files.read_data("references/events.md")
    if events:
        parts.append(f"## Events\n\n{events}")

    convo_index = files.read_conversation_index()
    if convo_index:
        parts.append(f"## Conversation Timeline\n\n{convo_index}")

    daily_index = files.read_daily_index()
    if daily_index:
        parts.append(f"## Daily Log Timeline\n\n{daily_index}")

    return "\n\n---\n\n".join(parts)


def run(session, initial_message: str | None = None) -> None:
    """Run freeform chat. Multi-turn until user types a slash command or exits."""
    console = session.console
    conversation = session.conversation
    system = persona.build_system(command="chat")

    today_section = _build_today_section()
    context = _build_context()

    if initial_message:
        # Today section goes LAST (right before the message) for recency bias
        user_msg = (
            f"[CONTEXT]\n{context}\n[/CONTEXT]\n\n"
            f"[TODAY — AUTHORITATIVE]\n{today_section}\n[/TODAY]\n\n"
            f"{initial_message}"
        )
        conversation.send(user_msg, system)
    else:
        console.print("[dim]Chat with George. Type a /command or press Ctrl+C to exit chat.[/dim]\n")

    # Multi-turn loop
    while True:
        try:
            user_input = input("you > ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input:
            continue

        if user_input.startswith("/"):
            console.print(f"[dim]Exiting chat. Use {user_input} from the main prompt.[/dim]")
            break

        # Subsequent messages don't need full context — it's in conversation history
        conversation.send(user_input, system)
