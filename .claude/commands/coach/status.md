---
model: haiku
---

# /coach:status — Quick Status Dashboard

Lightweight snapshot of where you are. No logging, no modifications, no subjective questions.

## Instructions

Load the coach agent from `.claude/agents/coach.md`.

Read from local files:
- `data/current-plan.md` → current week, phase, rationale (does NOT contain the session schedule)
- `data/references/events.md` → race calendar for countdowns
- `data/memory/coach-memory.md` → open follow-ups, injury status

### Pull from intervals.icu

Pull from the API (see `.claude/services/coach/intervals-icu.md`):
- **Today's calendar events** (Section 6) → today's planned session (source of truth for the schedule)
- **Athlete summary** → current CTL (fitness), ATL (fatigue), TSB (form)
- **Most recent activity** → last completed session

If the API is unavailable, note "API unavailable" in the fitness and session lines. Ask the athlete what's planned if they need session info.

## Output

A concise dashboard — aim for 5–7 lines:

```
Week [X]/[total] — [Phase] | [Next race]: [days] days | [Other race]: [days] days
Today: [Day] — [Planned session or Rest]
Fitness: CTL [X] | ATL [X] | TSB [sign][X] ([fresh/tired/neutral])
Last session: [type] [duration] ([date])
Open flags: [any open follow-ups or injury notes, or "None"]
```

### TSB interpretation
- TSB > +10: fresh (well-rested, may be losing fitness if prolonged)
- TSB +5 to +10: fresh (good for key sessions or racing)
- TSB -5 to +5: neutral (normal training)
- TSB -10 to -5: tired (accumulating fatigue)
- TSB < -10: very tired (monitor closely, deload may be needed)

### Notes
- Do not append to any log files
- Do not ask the athlete any questions
- Do not modify `current-plan.md`
- If it's a rest day, say so — don't suggest training
