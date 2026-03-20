"""/review — Weekly/monthly trend analysis + plan adaptation."""

from __future__ import annotations

from george import claude, dates, files, icu, persona


REVIEW_TOOL = {
    "name": "submit_review_result",
    "description": "Submit the weekly review with analysis, adaptation decision, and updates.",
    "input_schema": {
        "type": "object",
        "properties": {
            "george_response": {
                "type": "string",
                "description": "George's review presentation to the athlete. In character.",
            },
            "review_summary": {
                "type": "string",
                "description": "Full review summary for weekly-reviews.md. Include load, readiness, adherence, trends.",
            },
            "adaptation_decision": {
                "type": "string",
                "enum": ["continue", "insert_deload", "extend_phase", "simplify", "advance_early"],
                "description": "Plan adaptation decision.",
            },
            "adaptation_rationale": {
                "type": "string",
                "description": "Why this adaptation decision.",
            },
            "current_plan_updates": {
                "type": "string",
                "description": "Updates to apply to current-plan.md (updated week number, phase changes, etc.).",
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
            "week_archive": {
                "type": "string",
                "description": "Content for the weekly archive file.",
            },
        },
        "required": ["george_response", "review_summary", "adaptation_decision", "adaptation_rationale", "memory_updates"],
    },
}


def _fetch_data() -> dict:
    """Fetch all data for weekly review."""
    today = dates.today()
    data = {"today": today}

    # Local files
    data["current_plan"] = files.read_data("current-plan.md")
    data["coach_memory"] = files.read_data("memory/coach-memory.md")
    data["athlete_profile"] = files.read_data("references/athlete-profile.md")
    data["events"] = files.read_data("references/events.md")
    data["daily_log"] = files.read_daily_logs_range(ws, we)

    # ICU — this week
    ws = dates.week_start()
    we = dates.week_end()

    try:
        data["week_activities"] = icu.activities(ws, we)
    except icu.ICUError:
        data["week_activities"] = []

    try:
        data["week_wellness"] = icu.wellness(ws, we)
    except icu.ICUError:
        data["week_wellness"] = []

    try:
        data["athlete_summary"] = icu.athlete_summary()
    except icu.ICUError:
        data["athlete_summary"] = {}

    # Previous weeks for ACWR
    try:
        data["activities_4w"] = icu.activities(dates.days_ago(28), today)
    except icu.ICUError:
        data["activities_4w"] = []

    try:
        data["week_calendar"] = icu.events(ws, we)
    except icu.ICUError:
        data["week_calendar"] = []

    return data


def _compute_analytics(data: dict) -> str:
    """Compute adherence, load metrics, ACWR, overtraining indicators."""
    lines = []

    # This week
    acts = data.get("week_activities", [])
    total_load = sum(a.get("icu_training_load") or 0 for a in acts)
    total_dur = sum(a.get("moving_time") or 0 for a in acts)
    session_count = len(acts)

    lines.append(f"**This week:** {session_count} sessions, {total_dur//60} min, load {total_load:.0f}")

    # Adherence: planned vs completed
    planned = [e for e in data.get("week_calendar", []) if e.get("category") == "WORKOUT"]
    lines.append(f"**Adherence:** {session_count}/{len(planned)} planned sessions completed")

    # Sport breakdown
    by_sport: dict[str, float] = {}
    for a in acts:
        sport = a.get("type", "Other")
        load = a.get("icu_training_load") or 0
        by_sport[sport] = by_sport.get(sport, 0) + load
    if by_sport:
        lines.append(f"**By sport:** {', '.join(f'{s}: {l:.0f}' for s, l in by_sport.items())}")

    # ACWR
    all_acts = data.get("activities_4w", [])
    if all_acts:
        from datetime import date, timedelta
        today_d = date.fromisoformat(dates.today())
        week_loads = []
        for w in range(4):
            start = today_d - timedelta(days=7*(w+1)-1)
            end = today_d - timedelta(days=7*w)
            week_l = sum(
                a.get("icu_training_load") or 0
                for a in all_acts
                if start.isoformat() <= (a.get("start_date_local") or "")[:10] <= end.isoformat()
            )
            week_loads.append(week_l)

        if len(week_loads) >= 2 and sum(week_loads[1:]) > 0:
            chronic = sum(week_loads) / len(week_loads)
            acute = week_loads[0]
            acwr = acute / chronic if chronic > 0 else 0
            lines.append(f"**ACWR:** {acwr:.2f} (acute {acute:.0f} / chronic avg {chronic:.0f})")

    # CTL/ATL/TSB
    summary = data.get("athlete_summary", {})
    if summary:
        ctl = summary.get("fitness")
        atl = summary.get("fatigue")
        tsb = summary.get("form")
        if ctl is not None:
            lines.append(f"**Fitness:** CTL {ctl:.1f} | ATL {atl:.1f} | TSB {tsb:.1f}")

    # Wellness trends
    wellness = data.get("week_wellness", [])
    if wellness:
        hrv_vals = [w["hrv"] for w in wellness if w.get("hrv") is not None]
        sleep_vals = [w["sleep"] for w in wellness if w.get("sleep") is not None]
        rhr_vals = [w["restingHR"] for w in wellness if w.get("restingHR") is not None]

        if hrv_vals:
            lines.append(f"**HRV trend:** {' → '.join(str(int(v)) for v in hrv_vals)} (avg {sum(hrv_vals)/len(hrv_vals):.0f})")
        if sleep_vals:
            lines.append(f"**Sleep avg:** {sum(sleep_vals)/len(sleep_vals):.1f}h")
        if rhr_vals:
            lines.append(f"**rHR trend:** {' → '.join(str(int(v)) for v in rhr_vals)}")

    return "\n".join(lines)


def run(session) -> None:
    console = session.console
    # Review uses opus
    conversation = claude.Conversation(model=claude.OPUS)

    console.print("\n[bold]Weekly Review[/bold]\n")
    console.print("[dim]Fetching data...[/dim]")

    data = _fetch_data()
    analytics = _compute_analytics(data)

    system = persona.build_system(command="review", include_alerts=True, include_periodization=True)

    context = f"""[WEEKLY REVIEW — {data['today']}]

## Computed Analytics
{analytics}

## Daily Logs (this week)
{data['daily_log'] or 'No daily log entries.'}

## Current Plan
{data['current_plan']}

## Coach Memory
{data['coach_memory']}

## Events
{data['events']}

---

Conduct the weekly review:
1. Summarize the week — what was planned, what happened, what deviated
2. Analyze load progression, readiness trends, adherence
3. Check overtraining tier indicators
4. Check ACWR and load spike risk
5. Make an adaptation decision for next week
6. Flag any concerns or follow-ups

Present your analysis, then use submit_review_result to return the structured data."""

    console.print()
    result = conversation.send_structured(context, system, [REVIEW_TOOL])

    if not result:
        console.print("[red]Failed to get structured response.[/red]")
        return

    from rich.markdown import Markdown
    console.print()
    console.print(Markdown(result.get("george_response", "")))

    # Show adaptation decision
    decision = result.get("adaptation_decision", "continue")
    console.print(f"\n[bold]Adaptation: {decision}[/bold]")
    console.print(f"[dim]{result.get('adaptation_rationale', '')}[/dim]")

    # Write review summary
    review_summary = result.get("review_summary", "")
    if review_summary:
        files.append_weekly_reviews(review_summary)
        console.print("[dim]Weekly review logged.[/dim]")

    # Archive the week
    archive = result.get("week_archive", "")
    if archive:
        isoweek = dates.iso_week()
        files.write_archive(f"weekly/{isoweek}.md", archive)
        console.print(f"[dim]Week archived: {isoweek}[/dim]")

    # Memory updates
    for update in result.get("memory_updates", []):
        files.update_coach_memory(update["section"], update["content"])

    # Update current plan
    plan_updates = result.get("current_plan_updates", "")
    if plan_updates:
        current = files.read_data("current-plan.md")
        # Increment week in current plan
        files.update_current_plan(plan_updates if "# Current Plan" in plan_updates else current)

    # Write conversation
    summary = conversation.send_summary(persona.build_system())
    files.write_conversation("review", summary.split("\n")[0][:120], summary)
    console.print("[dim]Conversation logged.[/dim]\n")
