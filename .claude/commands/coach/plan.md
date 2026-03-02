# /coach:plan — Generate Weekly Training Plan

Generate the next week's training plan based on the athlete's profile, current phase, and recent training data. Reference macrocycle templates and session library from `.claude/.claude/agents/periodization.md`.

## Instructions

Load the coach agent from `.claude/agents/coach.md`, periodization templates from `.claude/.claude/agents/periodization.md` (including ICU structured workout templates), and the intervals.icu API reference from `.claude/services/coach/intervals-icu.md` (Sections 7–8 for event creation and workout syntax).

Read from local files:
- `data/current-plan.md` → current operational state: active plan, current week/phase, recent decisions and adjustments
- `data/references/events.md` → race calendar, upcoming events, countdown
- `data/references/athlete-profile.md` → goals, constraints, equipment, health
- `data/plans/` → original training plans as reference for prescribed sessions

Read from the coach Google Sheet:
- "Daily Log" tab → last week's sessions, RPE, pain, readiness trends
- "Weekly Review" tab → recent weekly summaries and load trends
- "Zones" tab → current thresholds and zone mappings

## Planning Process

1. **Determine current phase** from `data/current-plan.md`. Cross-reference with the original plan in `data/plans/` and `data/references/events.md` for event countdown. If multiple plans are active, check which event takes priority for this week.

2. **Review last week** (pull from intervals.icu API — see `.claude/services/coach/intervals-icu.md`):
   - Total volume and intensity distribution from completed activities
   - Training load trend and current CTL/ATL/TSB from athlete summary
   - Readiness trend from wellness data (sleep, HRV, resting HR, fatigue, soreness, mood, motivation, weight, injury status)
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
   - ICU workout description using the syntax from `.claude/services/coach/intervals-icu.md` Section 8, adapted from the templates in `.claude/agents/periodization.md` "Intervals.icu Structured Workout Descriptions"
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

Update `data/current-plan.md`:
- Advance the current week number
- Update the "This Week" section with the new plan
- Note any deviations from the original plan and why
- Record any decisions or agreements made with the athlete

## Sync to Intervals.icu Calendar

After the athlete approves the plan, create structured workout events on the intervals.icu calendar so they sync to Garmin:

1. **Build POST payload per session** using the intervals.icu API (Section 7 of `.claude/services/coach/intervals-icu.md`):
   - `start_date_local`: the scheduled date
   - `category`: `"WORKOUT"`
   - `name`: session title
   - `type`: sport type (`Run`, `Ride`, `Swim`, `WeightTraining`)
   - `description`: ICU workout syntax with warmup/main/cooldown, targets, and repeats
   - `moving_time`: planned duration in seconds

2. **Handle special cases:**
   - **Brick sessions** → create two separate events (one `Ride`, one `Run`) on the same date
   - **Rest days** → skip, do not create events
   - **Strength** → create event with plain text description (no structured syntax). Calculate `moving_time` from the exercise list using the formula in `.claude/agents/periodization.md` (warmup + exercises × 3 min + cooldown) rather than a fixed value. Include `"icu_training_load"` in the payload using the strength load estimation table from `.claude/agents/periodization.md`.

3. **POST each event** and store the returned event `id` in `current-plan.md` alongside each session (enables mid-week PUT/DELETE updates)

4. **Report sync result** to the athlete: confirm how many events were created, the date range, and remind them to check "Upload planned workouts" is enabled in Intervals.icu settings (Settings → Garmin)

5. **Note sync date range** in `current-plan.md` (e.g., "Synced to intervals.icu: 2026-03-02 to 2026-03-08")

6. **Error handling:**
   - If a single event POST fails (400/409): log the error, continue with the remaining events, report which session failed
   - If the API is unreachable: skip sync entirely, note in `current-plan.md` that sync was skipped, the athlete can still follow the plan from markdown

7. **Mid-week updates** (from `/coach:checkin` modifying a planned session):
   - Use PUT with the stored event `id` to update the workout description/duration
   - Use DELETE if a session is cancelled entirely
   - Create a new POST if a replacement session is added
