# /coach:plan — Generate Weekly Training Plan

Generate the next week's training plan based on the athlete's profile, current phase, and recent training data. Reference macrocycle templates and session library from `agents/coach/periodization.md`.

## Instructions

Load the coach agent from `agents/coach/coach.md` and periodization templates from `agents/coach/periodization.md`.

Read from local files:
- `data/coach/current-plan.md` → current operational state: active plan, current week/phase, recent decisions and adjustments
- `data/coach/references/events.md` → race calendar, upcoming events, countdown
- `data/coach/references/athlete-profile.md` → goals, constraints, equipment, health
- `data/coach/plans/` → original training plans as reference for prescribed sessions

Read from the coach Google Sheet:
- "Daily Log" tab → last week's sessions, RPE, pain, readiness trends
- "Weekly Review" tab → recent weekly summaries and load trends
- "Zones" tab → current thresholds and zone mappings

## Planning Process

1. **Determine current phase** from `data/coach/current-plan.md`. Cross-reference with the original plan in `data/coach/plans/` and `data/coach/references/events.md` for event countdown. If multiple plans are active, check which event takes priority for this week.

2. **Review last week** (pull from intervals.icu API — see `services/intervals-icu.md`):
   - Total volume and intensity distribution from completed activities
   - Training load trend and current CTL/ATL/TSB from athlete summary
   - Readiness trend from wellness data (sleep, HRV, fatigue, soreness)
   - Any injury signals or alerts from `current-plan.md`
   - Plan adherence: compare completed activities vs. what was planned

3. **Choose 2–3 key sessions max** for the week. Everything else is easy/recovery/skill.

4. **Schedule with recovery protection:**
   - Avoid stacking hard run after long run
   - Avoid >2 hard sessions back-to-back
   - Place key sessions on days with most time available
   - Include strength per phase (2× base/build, 1× peak)

5. **For triathlon plans:** minimum 2 swims/week.

6. **For each session, provide:**
   - Warm-up / main / cool-down structure
   - Target intensities (zone, RPE range, pace/power if applicable)
   - Fueling notes for sessions >75–90 min
   - What to log after

## Output Format

```
## Week [X] — [Phase] — [Date Range]

### Rationale
[One paragraph: reference load, readiness, goals, and what this week is designed to achieve.]

### Schedule

**Monday:** [session details]
**Tuesday:** [session details]
...

### Key Sessions This Week
1. [Session] — Why it matters: [brief]
2. [Session] — Why it matters: [brief]

### Fueling Focus
[Any fueling goals or practice for this week]

### Check-In Questions (answer midweek)
1. [Question about readiness/adherence]
2. [Question about a key session outcome]
3. [Question about recovery/life stress]
```

## Load Progression Rules

- Increase weekly volume max ~5–10% from previous similar (non-deload) week.
- Every 3rd or 4th week: deload (reduce volume 30–50%, maintain some intensity).
- If athlete missed significant time: rebuild conservatively, don't jump back to previous load.
- If readiness trending down across the week: consider early deload.

## After Generating the Plan

Update `data/coach/current-plan.md`:
- Advance the current week number
- Update the "This Week" section with the new plan
- Note any deviations from the original plan and why
- Record any decisions or agreements made with the athlete
