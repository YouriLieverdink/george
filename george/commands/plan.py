"""/plan — Generate next week's training plan."""

from __future__ import annotations

from george import claude, dates, files, icu, persona


PLAN_TOOL = {
    "name": "submit_plan_result",
    "description": "Submit the weekly plan with workouts, rationale, and plan updates.",
    "input_schema": {
        "type": "object",
        "properties": {
            "george_response": {
                "type": "string",
                "description": "George's presentation of the plan to the athlete. In character.",
            },
            "week_rationale": {
                "type": "string",
                "description": "Rationale for the week — why this structure, what it targets.",
            },
            "workouts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "day": {"type": "integer", "description": "1=Mon, 7=Sun"},
                        "sport": {"type": "string", "description": "Run, Ride, Swim, VirtualRide, WeightTraining, Other"},
                        "duration_minutes": {"type": "integer"},
                        "description": {"type": "string", "description": "Full workout description including warmup/cooldown"},
                        "training_load_estimate": {"type": "integer"},
                        "category": {"type": "string", "enum": ["WORKOUT", "NOTE"], "description": "WORKOUT for sessions, NOTE for coaching notes"},
                    },
                    "required": ["name", "day", "sport", "duration_minutes", "description"],
                },
            },
            "week_note": {
                "type": "string",
                "description": "Coaching note for the week to add as a NOTE event on Monday.",
            },
            "current_plan_updates": {
                "type": "string",
                "description": "Updated 'This Week' section content for current-plan.md.",
            },
        },
        "required": ["george_response", "week_rationale", "workouts", "current_plan_updates"],
    },
}


def _fetch_data() -> dict:
    """Fetch all data needed for plan generation."""
    today = dates.today()
    data = {"today": today}

    # Local files
    data["current_plan"] = files.read_data("current-plan.md")
    data["coach_memory"] = files.read_data("memory/coach-memory.md")
    data["athlete_profile"] = files.read_data("references/athlete-profile.md")
    data["events"] = files.read_data("references/events.md")

    # Active plan from plans/
    # Read both plans for reference
    data["plan_70_3"] = files.read_file("data/plans/ironman-70.3.md")
    data["plan_marathon"] = files.read_file("data/plans/marathon-sub345.md")

    # ICU data — last 2 weeks
    try:
        data["activities_2w"] = icu.activities(dates.days_ago(14), today)
    except icu.ICUError:
        data["activities_2w"] = []

    try:
        data["wellness_2w"] = icu.wellness(dates.days_ago(14), today)
    except icu.ICUError:
        data["wellness_2w"] = []

    try:
        data["athlete_summary"] = icu.athlete_summary()
    except icu.ICUError:
        data["athlete_summary"] = {}

    try:
        data["this_week_calendar"] = icu.events(dates.week_start(), dates.week_end())
    except icu.ICUError:
        data["this_week_calendar"] = []

    return data


def _compute_analytics(data: dict) -> str:
    """Compute weekly load totals, adherence, intensity distribution."""
    activities = data.get("activities_2w", [])
    if not activities:
        return "No activity data for analytics."

    # Split into this week and last week
    ws = dates.week_start()
    this_week = [a for a in activities if (a.get("start_date_local") or "")[:10] >= ws]
    last_week = [a for a in activities if (a.get("start_date_local") or "")[:10] < ws]

    def week_stats(acts):
        total_load = sum(a.get("icu_training_load") or 0 for a in acts)
        total_dur = sum(a.get("moving_time") or 0 for a in acts)
        count = len(acts)
        return {"load": total_load, "duration_min": total_dur // 60, "sessions": count}

    tw = week_stats(this_week)
    lw = week_stats(last_week)

    lines = [
        f"This week so far: {tw['sessions']} sessions, {tw['duration_min']} min, load {tw['load']:.0f}",
        f"Last week: {lw['sessions']} sessions, {lw['duration_min']} min, load {lw['load']:.0f}",
    ]

    # CTL/ATL/TSB
    summary = data.get("athlete_summary", {})
    if summary:
        ctl = summary.get("fitness")
        atl = summary.get("fatigue")
        tsb = summary.get("form")
        if ctl is not None:
            lines.append(f"CTL: {ctl:.1f} | ATL: {atl:.1f} | TSB: {tsb:.1f}")

    return "\n".join(lines)


def run(session) -> None:
    console = session.console
    # Plan uses opus
    conversation = claude.Conversation(model=claude.OPUS)

    console.print("\n[bold]Weekly Plan Generation[/bold]\n")
    console.print("[dim]Fetching data...[/dim]")

    data = _fetch_data()
    analytics = _compute_analytics(data)

    # Read periodization reference
    periodization = files.read_agent("periodization.md")

    system = persona.build_system(command="plan", include_alerts=True, include_periodization=True)

    context = f"""[PLAN GENERATION — {data['today']}]

## Computed Analytics
{analytics}

## Current Plan
{data['current_plan']}

## Coach Memory
{data['coach_memory']}

## Athlete Profile
{data['athlete_profile']}

## Events
{data['events']}

## Reference Plans
### IRONMAN 70.3 Plan
{data['plan_70_3'][:3000] if data['plan_70_3'] else 'Not available'}

### Marathon Plan
{data['plan_marathon'][:3000] if data['plan_marathon'] else 'Not available'}

## Last 2 Weeks Activities (summary)
{chr(10).join(f"- {(a.get('start_date_local') or '')[:10]} {a.get('type','')} {a.get('name','')} load:{a.get('icu_training_load',0):.0f}" for a in data.get('activities_2w', [])) or 'None'}

## Last 2 Weeks Wellness Trends
{chr(10).join(f"- {w.get('id','')} sleep:{w.get('sleep','?')}h HRV:{w.get('hrv','?')} rHR:{w.get('restingHR','?')}" for w in data.get('wellness_2w', [])) or 'None'}

---

Generate the next week's training plan. Consider:
1. Current phase and progression from the macro timeline
2. Load progression — reference last week's load and ACWR guidelines
3. Fixed commitments (swim course Wednesday)
4. Open follow-ups and injury monitoring from coach memory
5. Athlete preferences from coach memory
6. Upcoming events from events.md

Include specific, named mobility exercises in warmup/cooldown per athlete preferences.
Use HR-based targets for running (zones not calibrated). RPE for swimming.

Present the plan to the athlete, then use submit_plan_result to return the structured data."""

    # Single Claude call (structured, opus)
    console.print()
    conversation.send(context, system)

    # Ask for approval
    console.print()
    try:
        approval = input("you > ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Plan generation cancelled.[/dim]")
        return

    if not approval:
        console.print("[dim]No input — plan cancelled.[/dim]")
        return

    # Structured call to get the final plan data
    structure_prompt = f"""The athlete responded:

{approval}

If they approved (or approved with modifications), finalize the plan using submit_plan_result.
If they want changes, describe what you'd adjust and still submit the modified plan.
If they rejected entirely, submit an empty workouts array."""

    console.print("\n[dim]Finalizing plan...[/dim]")
    result = conversation.send_structured(structure_prompt, system, [PLAN_TOOL])

    if not result or not result.get("workouts"):
        console.print("[dim]No plan to sync.[/dim]")
        return

    from rich.markdown import Markdown
    console.print()
    console.print(Markdown(result.get("george_response", "")))

    # Sync to ICU
    console.print("\n[dim]Syncing to intervals.icu...[/dim]")

    # Read folder info from coach memory
    import re
    memory = files.read_data("memory/coach-memory.md")
    folder_match = re.search(r"folder_id:\s*(\d+)", memory)

    if not folder_match:
        console.print("[red]No workout folder found in coach memory. Create one in intervals.icu first.[/red]")
        return

    folder_id = folder_match.group(1)

    # Delete existing workouts in the folder
    try:
        existing = icu.workouts(folder_id)
        for w in existing:
            wid = w.get("id")
            if wid:
                icu.workout_delete(str(wid))
    except icu.ICUError:
        pass

    # Create new workouts
    for workout in result["workouts"]:
        category = workout.get("category", "WORKOUT")
        wdata = {
            "folder_id": int(folder_id),
            "day": workout["day"],
            "name": workout["name"],
            "type": workout.get("sport", "Run"),
            "description": workout.get("description", ""),
            "moving_time": workout.get("duration_minutes", 0) * 60,
            "category": category,
        }
        try:
            icu.workout_create(wdata)
        except icu.ICUError as e:
            console.print(f"[dim]Failed to create workout '{workout['name']}': {e}[/dim]")

    # Apply plan to calendar
    from george.dates import parse_date, week_start
    from datetime import timedelta, date as date_type

    next_monday = date_type.fromisoformat(week_start()) + timedelta(days=7)
    try:
        icu.events_apply_plan(folder_id, next_monday.isoformat())
        console.print("[dim]Plan applied to calendar.[/dim]")
    except icu.ICUError as e:
        console.print(f"[dim]Failed to apply plan: {e}[/dim]")

    # Update current-plan.md
    plan_updates = result.get("current_plan_updates", "")
    if plan_updates:
        # Replace the "This Week" section
        current = files.read_data("current-plan.md")
        this_week_marker = "## This Week"
        prev_weeks_marker = "## Previous Weeks"

        if this_week_marker in current and prev_weeks_marker in current:
            before = current[:current.index(this_week_marker)]
            after = current[current.index(prev_weeks_marker):]
            updated = before + "## This Week\n\n" + plan_updates + "\n\n" + after
            files.update_current_plan(updated)
            console.print("[dim]Current plan updated.[/dim]")

    # Write conversation
    summary = conversation.send_summary(persona.build_system())
    files.write_conversation("plan", summary.split("\n")[0][:120], summary)
    console.print("[dim]Conversation logged.[/dim]\n")
