---
model: opus
---

# /coach:plan — Generate Weekly Training Plan

Generate the next week's training plan based on the athlete's profile, current phase, and recent training data. Reference macrocycle templates and session library from `.claude/agents/periodization.md`.

## Instructions

### Pre-flight check
Before proceeding, verify that `data/references/athlete-profile.md` and `data/current-plan.md` exist and contain populated content (not just headers). If either is missing or empty → stop and tell the athlete: "It looks like onboarding hasn't been completed yet. Run `/coach:onboard` first to set up your profile and plan."

Load the coach agent from `.claude/agents/coach.md`, periodization templates from `.claude/agents/periodization.md` (including ICU structured workout templates), and the intervals.icu API reference from `.claude/services/coach/intervals-icu.md` (Sections 7–11 for event creation, workout library, and workout syntax).

Read from local files:
- `data/current-plan.md` → current operational state: active plan, current week/phase, recent decisions and adjustments
- `data/references/events.md` → race calendar, upcoming events, countdown
- `data/references/athlete-profile.md` → goals, constraints, equipment, health
- `data/plans/` → original training plans as reference for prescribed sessions
- `data/memory/coach-memory.md` → current zones and thresholds, fitness test history, injury history, athlete patterns, open follow-ups
- `data/logs/daily-log.md` → last week's check-in and debrief entries (readiness, RPE, pain trends)
- `data/logs/weekly-reviews.md` → recent weekly summaries and load trends

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
   - ICU workout description using the syntax from `.claude/services/coach/intervals-icu.md` Section 11, adapted from the templates in `.claude/agents/periodization.md` "Intervals.icu Structured Workout Descriptions"
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
- Advance the current week number and phase if needed
- Update the "This Week" section with **rationale only** — why this week looks the way it does, key focus areas, any deviations from the original plan
- Do NOT write per-day session details, tracking tables, or key sessions lists to `current-plan.md` — those live on the ICU calendar
- Record any decisions or agreements made with the athlete

## Sync to Intervals.icu Calendar

After the athlete approves the plan, sync workouts to the intervals.icu workout library and calendar so they sync to Garmin. Uses a persistent library folder ("George's Plan") that gets cleared and refilled each week.

### Workflow

1. **Read credentials:** Load `config/intervals-icu.json` for athlete ID and API key.

2. **Ensure folder exists:** Read `data/memory/coach-memory.md` for `folder_id`.
   - If no `folder_id` found: POST to create folder "George's Plan" (Section 8 of `.claude/services/coach/intervals-icu.md`), store the returned `id` in `data/memory/coach-memory.md` under `## Intervals.icu`.

3. **Clear existing workouts from folder:** GET workouts filtered by `folder_id` (Section 9), then DELETE each one. This ensures the folder only contains the current week.

4. **Create workouts in the folder:** For each training session this week, POST to `/workouts` (Section 9) with:
   - `folder_id`: the persistent folder ID
   - `name`: session title
   - `day`: day within the week (1=Monday, 2=Tuesday, ..., 7=Sunday)
   - `description`: ICU workout syntax (Section 11) with warmup/main/cooldown, targets, and repeats
   - `type`: sport type (`Run`, `Ride`, `Swim`, `WeightTraining`)
   - `moving_time`: planned duration in seconds

   **Special cases:**
   - **Rest days** → skip, do not create workouts
   - **Brick sessions** → two POSTs on the same `day` value (one `Ride`, one `Run`)
   - **Strength** → plain text description (no structured syntax). Calculate `moving_time` from the exercise list using the formula in `.claude/agents/periodization.md` (warmup + exercises × 3 min + cooldown). Include `icu_training_load` using the strength load estimation table from `.claude/agents/periodization.md`.

5. **Apply plan to calendar:** POST to `/events/apply-plan` (Section 10) with `folder_id` and `start_date_local` set to Monday of the target week.

6. **Post week rationale NOTE:** POST a `NOTE` event on Monday (Section 6) with the week rationale, key session notes, and fueling focus. This makes the coaching context visible on the ICU calendar.

7. **Report to athlete:** Confirm how many events were created, the date range, the folder name ("George's Plan"), and remind them to check "Upload planned workouts" is enabled in Intervals.icu settings (Settings → Garmin).

8. **Record sync metadata** in `current-plan.md` (e.g., "Synced to intervals.icu: 2026-03-02 to 2026-03-08, folder: George's Plan")

### Error Handling

| Step | Failure | Action |
|------|---------|--------|
| Folder creation | 400/500 | Abort sync, report error to athlete |
| Clear old workouts | DELETE fails | Log warning, continue — stale workouts may remain |
| Workout creation | Individual 400 | Log, skip that workout, continue with rest |
| Apply-plan | 400/500 | Report error; workouts are in library, can retry apply-plan |
| API unreachable | — | Output the full plan in the conversation so the athlete has it. Skip sync entirely. Note in `current-plan.md` that ICU sync is pending. Retry sync on next command. |

### Mid-week Updates

Mid-week adjustments (from `/coach:checkin` modifying a planned session) operate directly on calendar events, not the library folder. Query events by date range (Section 6) to find the event to modify:

- **Update:** GET events for the date, find the matching event by type/name, then PUT to update the workout description/duration (Section 7)
- **Cancel:** GET events for the date, find the matching event, then DELETE to remove it. POST a `NOTE` event with the cancellation reason.
- **Replace:** POST to `/events` (not `/workouts`) for ad-hoc replacement sessions (Section 7)
