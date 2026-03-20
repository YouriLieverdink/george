"""/raceweek — Race week preparation."""

from __future__ import annotations

from george import claude, dates, files, icu, persona


RACEWEEK_TOOL = {
    "name": "submit_raceweek_result",
    "description": "Submit race week plan with schedule, pacing, logistics, and mental prep.",
    "input_schema": {
        "type": "object",
        "properties": {
            "george_response": {
                "type": "string",
                "description": "George's race week briefing. In character.",
            },
            "race_week_schedule": {
                "type": "string",
                "description": "Day-by-day race week schedule.",
            },
            "pacing_strategy": {
                "type": "string",
                "description": "Race pacing plan with split targets.",
            },
            "nutrition_plan": {
                "type": "string",
                "description": "Pre-race and race day nutrition plan.",
            },
            "logistics_checklist": {
                "type": "string",
                "description": "Race day logistics and equipment checklist.",
            },
            "mental_prep": {
                "type": "string",
                "description": "Mental preparation notes and mantras.",
            },
            "log_entry": {
                "type": "string",
                "description": "Summary for conversations.md.",
            },
        },
        "required": ["george_response", "race_week_schedule", "pacing_strategy", "log_entry"],
    },
}


def run(session) -> None:
    console = session.console
    conversation = session.conversation

    console.print("\n[bold]Race Week Prep[/bold]\n")
    console.print("[dim]Fetching data...[/dim]")

    today = dates.today()

    # Local files
    current_plan = files.read_data("current-plan.md")
    coach_memory = files.read_data("memory/coach-memory.md")
    events = files.read_data("references/events.md")
    athlete_profile = files.read_data("references/athlete-profile.md")

    # ICU data
    try:
        summary = icu.athlete_summary()
    except icu.ICUError:
        summary = {}

    try:
        wellness_7d = icu.wellness(dates.days_ago(7), today)
    except icu.ICUError:
        wellness_7d = []

    system = persona.build_system(command="raceweek", include_alerts=True)

    ctl = summary.get("fitness", "?")
    atl = summary.get("fatigue", "?")
    tsb = summary.get("form", "?")

    context = f"""[RACE WEEK PREP — {today}]

## Current Plan
{current_plan}

## Events
{events}

## Athlete Profile
{athlete_profile}

## Coach Memory
{coach_memory}

## Current Fitness
CTL: {ctl} | ATL: {atl} | TSB: {tsb}

## Recent Wellness
{chr(10).join(f"- {w.get('id','')} sleep:{w.get('sleep','?')}h HRV:{w.get('hrv','?')}" for w in wellness_7d) or 'None'}

---

This is a race week briefing. Cover:
1. Day-by-day schedule (what to do each day this week)
2. Pacing strategy with target splits
3. Nutrition plan (pre-race loading + race day)
4. Logistics checklist (gear, registration, travel)
5. Mental prep (mantras, visualization, race morning routine)

Ask the athlete which race this is for if multiple upcoming. Present the plan, then use submit_raceweek_result."""

    console.print()
    conversation.send(context, system)

    console.print()
    try:
        response = input("you > ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Cancelled.[/dim]")
        return

    if response:
        result = conversation.send_structured(
            f"The athlete said:\n\n{response}\n\nFinalize the race week plan using submit_raceweek_result.",
            system, [RACEWEEK_TOOL]
        )
    else:
        result = conversation.send_structured(
            "The athlete confirmed. Finalize using submit_raceweek_result.",
            system, [RACEWEEK_TOOL]
        )

    if result:
        from rich.markdown import Markdown
        console.print()
        console.print(Markdown(result.get("george_response", "")))

        log_entry = result.get("log_entry", "")
        summary = log_entry.split("\n")[0][:120] if log_entry else "Race week briefing"
        files.write_conversation("raceweek", summary, log_entry)
        console.print("[dim]Conversation logged.[/dim]\n")
