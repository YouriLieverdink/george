"""/postrace — Post-race debrief + recovery plan."""

from __future__ import annotations

from george import claude, dates, files, icu, persona


POSTRACE_TOOL = {
    "name": "submit_postrace_result",
    "description": "Submit post-race debrief with race report, recovery plan, and updates.",
    "input_schema": {
        "type": "object",
        "properties": {
            "george_response": {
                "type": "string",
                "description": "George's post-race response. In character.",
            },
            "race_report": {
                "type": "string",
                "description": "Full race report for archive.",
            },
            "recovery_plan": {
                "type": "string",
                "description": "Recovery plan — days of rest, return-to-training protocol.",
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
            "current_plan_updates": {
                "type": "string",
                "description": "Updates to current-plan.md for post-race phase.",
            },
        },
        "required": ["george_response", "race_report", "recovery_plan", "memory_updates"],
    },
}


def run(session) -> None:
    console = session.console
    conversation = session.conversation

    console.print("\n[bold]Post-Race Debrief[/bold]\n")
    console.print("[dim]Fetching data...[/dim]")

    today = dates.today()

    # Fetch recent activities (race should be in last 3 days)
    try:
        recent_acts = icu.activities(dates.days_ago(3), today)
    except icu.ICUError:
        recent_acts = []

    # Enrich
    enriched = []
    for act in recent_acts:
        aid = act.get("id")
        if aid:
            try:
                enriched.append(icu.activity(str(aid)))
            except icu.ICUError:
                enriched.append(act)
        else:
            enriched.append(act)

    current_plan = files.read_data("current-plan.md")
    coach_memory = files.read_data("memory/coach-memory.md")
    events = files.read_data("references/events.md")

    system = persona.build_system(command="postrace", include_alerts=True)

    # Format activities
    act_text = ""
    for a in enriched:
        name = a.get("name", "?")
        atype = a.get("type", "?")
        dur = a.get("moving_time")
        dur_str = f"{int(dur)//3600}:{(int(dur)%3600)//60:02d}" if dur else "?"
        dist = a.get("distance")
        dist_str = f"{dist/1000:.1f} km" if dist else "?"
        avg_hr = a.get("average_heartrate")
        load = a.get("icu_training_load")
        act_text += f"- {name} ({atype}): {dur_str}, {dist_str}, avg HR {int(avg_hr) if avg_hr else '?'}, load {int(load) if load else '?'}\n"

    context = f"""[POST-RACE DEBRIEF — {today}]

## Recent Activities
{act_text or 'No activities found.'}

## Current Plan
{current_plan}

## Events
{events}

## Coach Memory
{coach_memory}

---

Conduct a post-race debrief. Ask the athlete:
1. Which race was this?
2. How did it go overall? (emotional response first)
3. Pacing — did you stick to the plan?
4. Nutrition — did the fueling strategy work?
5. What went well? What would you change?
6. Any pain or injury concerns?
7. How do you feel right now?

Then generate: race report, recovery plan, and plan updates."""

    console.print()
    conversation.send(context, system)

    console.print()
    try:
        response = input("you > ").strip()
    except (KeyboardInterrupt, EOFError):
        console.print("\n[dim]Cancelled.[/dim]")
        return

    if not response:
        console.print("[dim]No input — cancelled.[/dim]")
        return

    result = conversation.send_structured(
        f"The athlete said:\n\n{response}\n\nProcess the debrief using submit_postrace_result.",
        system, [POSTRACE_TOOL]
    )

    if not result:
        console.print("[red]Failed to get structured response.[/red]")
        return

    from rich.markdown import Markdown
    console.print()
    console.print(Markdown(result.get("george_response", "")))

    # Archive race report
    race_report = result.get("race_report", "")
    if race_report:
        # Try to identify the race name
        race_name = "race"
        for line in race_report.split("\n"):
            if line.startswith("#"):
                race_name = line.strip("#").strip().lower().replace(" ", "-")[:40]
                break
        files.write_archive(f"races/{today}-{race_name}.md", race_report)
        console.print(f"[dim]Race report archived.[/dim]")

    # Recovery plan display
    recovery = result.get("recovery_plan", "")
    if recovery:
        console.print(f"\n[bold]Recovery Plan[/bold]")
        console.print(Markdown(recovery))

    # Memory updates
    for update in result.get("memory_updates", []):
        files.update_coach_memory(update["section"], update["content"])

    # Update current plan
    plan_updates = result.get("current_plan_updates", "")
    if plan_updates:
        files.update_current_plan(plan_updates)

    # Write conversation
    summary = conversation.send_summary(persona.build_system())
    files.write_conversation("postrace", summary.split("\n")[0][:120], summary)
    console.print("[dim]Conversation logged.[/dim]\n")
