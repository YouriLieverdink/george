"""/debrief — Post-session logging + feedback."""

from __future__ import annotations

from george import dates, files, icu, persona


DEBRIEF_TOOL = {
    "name": "submit_debrief_result",
    "description": "Submit the debrief result with feedback, log entry, and memory updates.",
    "input_schema": {
        "type": "object",
        "properties": {
            "george_response": {
                "type": "string",
                "description": "George's debrief feedback to the athlete. In character.",
            },
            "log_entry": {
                "type": "string",
                "description": "Markdown debrief entry for daily-log.md. Include session metrics + subjective data.",
            },
            "memory_updates": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "section": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["section", "content"],
                },
            },
            "alerts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string", "description": "Alert type: pain, rpe_drift, gi, overtraining"},
                        "detail": {"type": "string"},
                        "severity": {"type": "string", "enum": ["flag", "alert", "stop"]},
                    },
                    "required": ["type", "detail", "severity"],
                },
                "description": "Alerts triggered by debrief data.",
            },
        },
        "required": ["george_response", "log_entry", "memory_updates", "alerts"],
    },
}


def _fetch_data() -> dict:
    """Fetch data for debrief."""
    today = dates.today()
    data = {"today": today, "weekday": dates.weekday_name()}

    # ICU data
    try:
        data["today_events"] = icu.events(today, today)
    except icu.ICUError:
        data["today_events"] = []

    try:
        data["today_activities"] = icu.activities(today, today)
    except icu.ICUError:
        data["today_activities"] = []

    # Enrich activities with full detail
    enriched = []
    for act in data["today_activities"]:
        aid = act.get("id")
        if aid:
            try:
                full = icu.activity(str(aid))
                enriched.append(full)
            except icu.ICUError:
                enriched.append(act)
        else:
            enriched.append(act)
    data["enriched_activities"] = enriched

    # Local files
    data["coach_memory"] = files.read_data("memory/coach-memory.md")
    data["current_plan"] = files.read_data("current-plan.md")
    data["daily_log_today"] = files.read_daily_log(dates.today())

    return data


def _match_activity_to_event(activities: list[dict], events: list[dict]) -> list[dict]:
    """Match completed activities to planned events by sport type."""
    matches = []
    used_events = set()

    for act in activities:
        act_type = act.get("type", "").upper()
        best_event = None

        for evt in events:
            eid = evt.get("id")
            if eid in used_events:
                continue
            if evt.get("category") != "WORKOUT":
                continue
            evt_type = (evt.get("type") or "").upper()
            if evt_type == act_type or (not evt_type and not best_event):
                best_event = evt
                if evt_type == act_type:
                    break

        if best_event:
            used_events.add(best_event.get("id"))
            matches.append({"activity": act, "event": best_event})
        else:
            matches.append({"activity": act, "event": None})

    return matches


def _format_activity(act: dict) -> str:
    """Format an activity for Claude context."""
    lines = []
    name = act.get("name", "Unknown")
    atype = act.get("type", "")
    date = (act.get("start_date_local") or "")[:10]

    lines.append(f"**{name}** ({atype}, {date})")

    dur = act.get("moving_time")
    if dur:
        m, s = int(dur) // 60, int(dur) % 60
        lines.append(f"- Duration: {m}:{s:02d}")

    dist = act.get("distance")
    if dist:
        lines.append(f"- Distance: {dist/1000:.1f} km")

    avg_hr = act.get("average_heartrate")
    max_hr = act.get("max_heartrate")
    if avg_hr or max_hr:
        hr_parts = []
        if avg_hr:
            hr_parts.append(f"avg {int(avg_hr)}")
        if max_hr:
            hr_parts.append(f"max {int(max_hr)}")
        lines.append(f"- HR: {' / '.join(hr_parts)}")

    pace = act.get("average_speed")
    if pace and pace > 0:
        secs = 1000 / pace
        pm, ps = int(secs) // 60, int(secs) % 60
        lines.append(f"- Pace: {pm}:{ps:02d} /km")

    load = act.get("icu_training_load")
    if load:
        lines.append(f"- Training load: {int(load)}")

    # Zone times
    zones = act.get("icu_zone_times")
    if zones:
        zone_strs = []
        for i, z in enumerate(zones, 1):
            if z and z > 0:
                zm, zs = int(z) // 60, int(z) % 60
                zone_strs.append(f"Z{i}: {zm}:{zs:02d}")
        if zone_strs:
            lines.append(f"- Zones: {' | '.join(zone_strs)}")

    return "\n".join(lines)


def run(session) -> None:
    console = session.console
    conversation = session.conversation

    console.print("\n[bold]Post-Session Debrief[/bold]\n")
    console.print("[dim]Fetching data...[/dim]")

    data = _fetch_data()

    # Match activities to planned events
    matches = _match_activity_to_event(
        data["enriched_activities"], data["today_events"]
    )

    # Build context
    system = persona.build_system(command="debrief", include_alerts=True)

    activities_text = ""
    if matches:
        parts = []
        for m in matches:
            act_text = _format_activity(m["activity"])
            evt = m.get("event")
            if evt:
                planned = f"Planned: {evt.get('name', '?')} ({evt.get('type', '?')}, {evt.get('moving_time', 0)//60 if evt.get('moving_time') else '?'} min)"
                parts.append(f"{act_text}\n{planned}")
            else:
                parts.append(f"{act_text}\nPlanned: no matching event found")
        activities_text = "\n\n".join(parts)
    else:
        activities_text = "No activities recorded today."

    context = f"""[DEBRIEF DATA — {data['today']} ({data['weekday']})]

## Today's Completed Activities
{activities_text}

## Today's Check-in
{data['daily_log_today'] or 'No check-in today.'}

## Current Plan
{data['current_plan']}

## Coach Memory
{data['coach_memory']}

---

Review the planned vs actual comparison. Then ask the athlete for subjective feedback:
- RPE (1-10)
- Pain (0-10, location if any)
- Fueling (what they ate/drank, any GI issues)
- Key learnings or observations
- Anything else relevant from open follow-ups in coach memory

Be concise. One question block, not one at a time."""

    # Claude call 1: ask subjective questions
    console.print()
    conversation.send(context, system)

    # Get answers
    console.print()
    try:
        answers = input("you > ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Debrief cancelled.[/dim]")
        return

    if not answers:
        console.print("[dim]No input — debrief cancelled.[/dim]")
        return

    # Claude call 2 (structured): feedback + log entry
    interpret_prompt = f"""The athlete answered:

{answers}

Based on their answers and the activity data:
1. Give feedback as George — acknowledge, observe, adjust
2. Generate a detailed debrief log entry for daily-log.md
3. Note memory updates (learnings, injury status changes, patterns)
4. Flag any alerts (pain ≥4, RPE drift from expected, GI issues, injury signals)

Use the submit_debrief_result tool."""

    console.print("\n[dim]Processing...[/dim]")
    result = conversation.send_structured(interpret_prompt, system, [DEBRIEF_TOOL])

    if not result:
        console.print("[red]Failed to get structured response.[/red]")
        return

    # Display response
    from rich.markdown import Markdown
    console.print()
    console.print(Markdown(result.get("george_response", "")))

    # Show alerts
    for alert in result.get("alerts", []):
        severity = alert.get("severity", "flag")
        color = {"flag": "yellow", "alert": "red", "stop": "bold red"}.get(severity, "yellow")
        console.print(f"\n[{color}]{severity.upper()}: {alert['type']} — {alert['detail']}[/{color}]")

    # Write daily log
    log_entry = result.get("log_entry", "")
    if log_entry:
        # Build summary from activity info
        act_names = [m["activity"].get("name", "?") for m in matches] if matches else ["No activity"]
        daily_summary = f"Debrief: {', '.join(act_names)}"
        files.write_daily_log(data["today"], daily_summary, log_entry)
        console.print("[dim]Daily log updated.[/dim]")

    # Memory updates
    for update in result.get("memory_updates", []):
        files.update_coach_memory(update["section"], update["content"])

    # Write conversation
    summary = conversation.send_summary(persona.build_system())
    files.write_conversation("debrief", summary.split("\n")[0][:120], summary)
    console.print("[dim]Conversation logged.[/dim]\n")
