"""/checkin — Daily readiness check → adapted session."""

from __future__ import annotations

from george import claude, dates, files, icu, persona, readiness


CHECKIN_TOOL = {
    "name": "submit_checkin_result",
    "description": "Submit the check-in result with readiness assessment, session decision, and log entry.",
    "input_schema": {
        "type": "object",
        "properties": {
            "george_response": {
                "type": "string",
                "description": "George's response to the athlete after processing their answers. In character.",
            },
            "subjective_wellness": {
                "type": "object",
                "description": "Subjective wellness scores to write to ICU (1-4 scale). Only include fields the athlete provided.",
                "properties": {
                    "soreness": {"type": "integer", "enum": [1, 2, 3, 4]},
                    "fatigue": {"type": "integer", "enum": [1, 2, 3, 4]},
                    "stress": {"type": "integer", "enum": [1, 2, 3, 4]},
                    "mood": {"type": "integer", "enum": [1, 2, 3, 4]},
                    "motivation": {"type": "integer", "enum": [1, 2, 3, 4]},
                    "injury": {"type": "integer", "enum": [1, 2, 3, 4]},
                    "hydration": {"type": "integer", "enum": [1, 2, 3, 4]},
                },
            },
            "readiness_score": {
                "type": "integer",
                "description": "Final readiness score 0-100 after incorporating subjective data.",
            },
            "readiness_band": {
                "type": "string",
                "enum": ["GREEN", "AMBER", "YELLOW", "ORANGE", "RED"],
            },
            "session_decision": {
                "type": "string",
                "enum": ["execute", "modify", "replace", "cancel"],
                "description": "Decision for today's planned session.",
            },
            "modified_session": {
                "type": "string",
                "description": "If session_decision is modify/replace, describe the modified session. Empty if execute/cancel.",
            },
            "log_entry": {
                "type": "string",
                "description": "Markdown content for daily-log.md under today's date. Include all check-in data.",
            },
            "memory_updates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "section": {"type": "string", "description": "coach-memory.md H2 section name"},
                        "content": {"type": "string", "description": "Content to append to that section"},
                    },
                    "required": ["section", "content"],
                },
                "description": "Updates to append to coach-memory.md sections. Empty array if none.",
            },
            "icu_actions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "action": {"type": "string", "enum": ["create", "update", "delete"]},
                        "event_id": {"type": "string", "description": "For update/delete"},
                        "data": {"type": "object", "description": "For create/update — event data"},
                    },
                    "required": ["action"],
                },
                "description": "ICU calendar actions to execute. Empty array if none.",
            },
        },
        "required": [
            "george_response", "readiness_score", "readiness_band",
            "session_decision", "log_entry", "memory_updates", "icu_actions",
        ],
    },
}


def _fetch_data() -> dict:
    """Fetch all data needed for check-in."""
    today = dates.today()
    data = {"today": today, "weekday": dates.weekday_name()}

    # Local files
    data["athlete_profile"] = files.read_data("references/athlete-profile.md")
    data["current_plan"] = files.read_data("current-plan.md")
    data["coach_memory"] = files.read_data("memory/coach-memory.md")
    data["events"] = files.read_data("references/events.md")
    data["conversation_index"] = files.read_conversation_index()
    data["daily_log_today"] = files.read_daily_log(dates.today())

    # ICU data — each wrapped for resilience
    try:
        data["wellness"] = icu.wellness(dates.days_ago(7), today)
    except icu.ICUError as e:
        data["wellness"] = []
        data["wellness_error"] = str(e)

    try:
        data["calendar"] = icu.events(dates.week_start(), dates.week_end())
    except icu.ICUError as e:
        data["calendar"] = []
        data["calendar_error"] = str(e)

    try:
        data["yesterday_activities"] = icu.activities(dates.yesterday(), today)
    except icu.ICUError as e:
        data["yesterday_activities"] = []

    return data


def _compute_partial_readiness(wellness_data: list[dict]) -> readiness.ReadinessResult | None:
    """Compute readiness from device data only (before subjective input)."""
    if not wellness_data:
        return None

    today = dates.today()
    today_wellness = None
    for w in wellness_data:
        if w.get("id") == today:
            today_wellness = w
            break

    if not today_wellness:
        return None

    # Compute HRV/rHR baselines from the wellness data we have
    hrv_values = [w["hrv"] for w in wellness_data if w.get("hrv") is not None]
    rhr_values = [w["restingHR"] for w in wellness_data if w.get("restingHR") is not None]
    hrv_baseline = sum(hrv_values) / len(hrv_values) if hrv_values else None
    rhr_baseline = sum(rhr_values) / len(rhr_values) if rhr_values else None

    return readiness.compute(
        wellness=today_wellness,
        hrv_baseline=hrv_baseline,
        rhr_baseline=rhr_baseline,
    )


def _format_wellness_summary(wellness_data: list[dict]) -> str:
    """Format wellness data for Claude context."""
    if not wellness_data:
        return "No wellness data available."

    lines = []
    for w in wellness_data:
        d = w.get("id", "?")
        parts = [d]
        if w.get("sleep") is not None:
            s = f"sleep {w['sleep']:.1f}h"
            if w.get("sleepScore") is not None:
                s += f" (score {w['sleepScore']})"
            parts.append(s)
        if w.get("hrv") is not None:
            parts.append(f"HRV {w['hrv']}")
        if w.get("restingHR") is not None:
            parts.append(f"rHR {w['restingHR']}")
        if w.get("spO2") is not None:
            parts.append(f"SpO2 {w['spO2']}%")
        lines.append(" | ".join(parts))

    return "\n".join(lines)


def _format_calendar(events: list[dict]) -> str:
    """Format calendar events for Claude context."""
    if not events:
        return "No calendar events."

    lines = []
    for e in events:
        d = (e.get("start_date_local") or "")[:10]
        cat = e.get("category", "")
        name = e.get("name", "")
        sport = e.get("type", "")
        dur = e.get("moving_time")
        dur_str = f" ({int(dur)//60} min)" if dur else ""
        eid = e.get("id", "")

        if cat == "WORKOUT":
            desc = e.get("description", "")
            desc_preview = f"\n  {desc[:200]}" if desc else ""
            lines.append(f"- {d} | {cat} | {name} | {sport}{dur_str} | id:{eid}{desc_preview}")
        elif cat == "NOTE":
            desc = e.get("description", "")[:100]
            lines.append(f"- {d} | NOTE | {name}: {desc}")
        else:
            lines.append(f"- {d} | {cat} | {name}")

    return "\n".join(lines)


def run(session) -> None:
    console = session.console
    conversation = session.conversation

    console.print("\n[bold]Daily Check-in[/bold]\n")
    console.print("[dim]Fetching data...[/dim]")

    # Step 1: Fetch all data
    data = _fetch_data()

    # Step 2: Compute partial readiness
    partial = _compute_partial_readiness(data["wellness"])
    partial_str = ""
    if partial and partial.score >= 0:
        partial_str = (
            f"\nPartial readiness (device data only, before subjective): "
            f"{partial.score}/100 ({partial.band})\n"
            f"Components: {', '.join(f'{c.name}: {c.score:.0f} ({c.raw_value})' for c in partial.components)}\n"
            f"Missing (need athlete input): {', '.join(partial.missing) if partial.missing else 'none'}"
        )

    # Step 3: Build context for Claude call 1
    system = persona.build_system(command="checkin", include_alerts=True)

    context = f"""[CHECK-IN DATA — {data['today']} ({data['weekday']})]

## Wellness (last 7 days)
{_format_wellness_summary(data['wellness'])}
{"⚠ Wellness API error: " + data.get('wellness_error', '') if 'wellness_error' in data else ''}

## This Week's Calendar
{_format_calendar(data['calendar'])}
{"⚠ Calendar API error: " + data.get('calendar_error', '') if 'calendar_error' in data else ''}

## Yesterday's Activities
{_format_calendar(data['yesterday_activities']) if data['yesterday_activities'] else 'None'}

{partial_str}

## Today's Daily Log (if already started)
{data['daily_log_today'] or 'No entry yet.'}

## Current Plan
{data['current_plan']}

## Coach Memory
{data['coach_memory']}

## Events
{data['events']}

## Conversation Timeline
{data['conversation_index'] or 'No conversations yet.'}

---

Present the morning wellness summary, note any patterns or concerns, show today's planned session, and ask the athlete the subjective questions you need (soreness, fatigue, mood, motivation, injury status, stress, hydration, alcohol, caffeine cutoff, time available, anything else relevant from coach memory follow-ups). Be concise."""

    # Claude call 1: present data + ask questions
    console.print()
    conversation.send(context, system)

    # Step 4: Get athlete's answers
    console.print()
    try:
        answers = input("you > ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Check-in cancelled.[/dim]")
        return

    if not answers:
        console.print("[dim]No input — check-in cancelled.[/dim]")
        return

    # Step 5: Claude call 2 (structured) — interpret + decide
    interpret_prompt = f"""The athlete answered:

{answers}

Based on their answers AND all the data from the check-in context:

1. Interpret their subjective scores (map to 1-4 scale for each wellness field)
2. Compute the final readiness score incorporating both device + subjective data
3. Make a session decision for today's planned session
4. Generate the daily log entry
5. Note any memory updates (patterns, follow-ups, learnings)
6. List any ICU calendar actions needed (modify/cancel today's event if session changes)

Use the submit_checkin_result tool to return your structured result."""

    console.print("\n[dim]Processing...[/dim]")
    result = conversation.send_structured(interpret_prompt, system, [CHECKIN_TOOL])

    if not result:
        console.print("[red]Failed to get structured response.[/red]")
        return

    # Step 6: Display George's response
    from rich.markdown import Markdown
    console.print()
    console.print(Markdown(result.get("george_response", "")))

    # Show readiness score
    score = result.get("readiness_score", -1)
    band = result.get("readiness_band", "UNKNOWN")
    band_colors = {"GREEN": "green", "AMBER": "yellow", "YELLOW": "bright_yellow", "ORANGE": "dark_orange", "RED": "red"}
    color = band_colors.get(band, "dim")
    console.print(f"\n[{color}]Readiness: {score}/100 ({band})[/{color}]")

    decision = result.get("session_decision", "")
    if decision:
        console.print(f"Session: {decision}")
        if result.get("modified_session"):
            console.print(f"  → {result['modified_session']}")

    # Step 7: Execute writes
    # Write subjective wellness to ICU
    subj = result.get("subjective_wellness")
    if subj:
        try:
            icu.wellness_put(data["today"], subj)
            console.print("[dim]Wellness scores synced.[/dim]")
        except icu.ICUError as e:
            console.print(f"[dim]Wellness sync failed: {e}[/dim]")

    # Execute ICU actions
    for action in result.get("icu_actions", []):
        try:
            if action["action"] == "create":
                icu.event_create(action.get("data", {}))
            elif action["action"] == "update" and action.get("event_id"):
                icu.event_update(action["event_id"], action.get("data", {}))
            elif action["action"] == "delete" and action.get("event_id"):
                icu.event_delete(action["event_id"])
        except icu.ICUError as e:
            console.print(f"[dim]ICU action failed: {e}[/dim]")

    # Write daily log
    log_entry = result.get("log_entry", "")
    if log_entry:
        daily_summary = f"Readiness {score} {band}. {result.get('session_decision', '')}"
        files.write_daily_log(data["today"], daily_summary, log_entry)
        console.print("[dim]Daily log updated.[/dim]")

    # Apply memory updates
    for update in result.get("memory_updates", []):
        files.update_coach_memory(update["section"], update["content"])

    # Write conversation
    summary = conversation.send_summary(persona.build_system())
    files.write_conversation("checkin", summary.split("\n")[0][:120], summary)
    console.print("[dim]Conversation logged.[/dim]\n")
