---
model: opus
---

# /coach:review — Weekly & Monthly Review

Analyze training trends, assess progress, and adapt the plan.

## Instructions

### Pre-flight check
Before proceeding, verify that `data/references/athlete-profile.md` and `data/current-plan.md` exist and contain populated content (not just headers). If either is missing or empty → stop and tell the athlete: "It looks like onboarding hasn't been completed yet. Run `/coach:onboard` first to set up your profile and plan."

Load the coach agent from `.claude/agents/coach.md` and alert rules from `.claude/agents/alerts.md`.

Read from local files:
- `data/current-plan.md` → current operational state, recent decisions, this week's plan and modifications
- `data/references/events.md` → race calendar, event countdown
- `data/references/athlete-profile.md` → goals and constraints
- `data/plans/` → original plan(s) as reference for what was prescribed vs. what happened
- `data/memory/coach-memory.md` → accumulated context: patterns, injury history, open follow-ups, zones, fitness tests
- `data/logs/daily-log.md` → daily check-in and debrief entries from the review period
- `data/logs/weekly-reviews.md` → previous review summaries for trend comparison

## Weekly Review (run every week)

### Pull data from intervals.icu

Before analysis, pull the week's data from the API (see `.claude/services/coach/intervals-icu.md`):

1. **Activities for the past 7 days** — all completed workouts with duration, distance, HR, pace/power, training load
2. **Wellness for the past 7 days** — Garmin-synced: sleep (duration + score + quality), HRV, resting HR, weight, SpO2, VO2 max, steps. Subjective: soreness, fatigue, stress, mood, motivation, injury, hydration
3. **Athlete summary** — current CTL (fitness), ATL (fatigue), TSB (form)

This gives you hard data for the analysis rather than relying on memory or self-reports.

### Analyze

1. **Load trend** (from intervals.icu activities):
   - Total volume this week vs. previous weeks (km, hours)
   - Intensity distribution: zone time from activities (how much easy vs. moderate vs. hard)
   - Total training load (icu_training_load sum) and CTL/ATL/TSB trend
   - Compare to plan: did load land where intended? Cross-reference `current-plan.md`.

2. **Readiness trend** (from intervals.icu wellness):
   - Sleep duration, score, and quality pattern across the week
   - HRV trend (stable, declining, improving vs. baseline)
   - Resting HR trend (rising resting HR = fatigue accumulation)
   - Fatigue and soreness trajectory from subjective scores
   - Weight trend (flag rapid unintended loss/gain — RED-S indicator)
   - VO2 max trend (improvement indicator over mesocycle)
   - Mood and motivation trajectory (overtraining signals — GRUMPY + LOW motivation + declining performance)
   - SpO2 trend (sustained low = illness indicator)
   - Injury status trend (niggle progressing? resolving?)

3. **Key workout outcomes** (from intervals.icu activity details + current-plan.md):
   - Did the athlete hit process goals (pacing, fueling, technique)?
   - Planned vs. actual: compare prescribed paces/intensities with what the API shows
   - Where did sessions go better or worse than expected?
   - Any sessions modified or skipped? Why? (check current-plan.md modifications)

4. **Injury/health signals:**
   - New pain or worsening trends across the week
   - Persistent soreness that isn't resolving
   - Any alerts triggered during the week

5. **Adherence:**
   - Sessions completed vs. planned
   - Reasons for any gaps (fatigue? time? motivation? injury?)

### Decide

Based on the analysis, determine:
- **Continue as planned:** adapting safely, readiness stable, hitting targets
- **Modify next week:** fatigue accumulating, insert deload or reduce intensity
- **Escalate:** red flags present, refer or shift to recovery protocol

### Output

```
## Weekly Review — Week [X] — [Date Range]

### Summary
[2–3 sentences: how the week went overall]

### Load
- Volume: [X hours / X km] (vs. [previous week])
- Key sessions completed: [X/Y]
- Intensity distribution: [approximately X% easy, Y% moderate, Z% hard]

### Readiness
- Sleep: [trend — duration, score, quality]
- Fatigue: [trend]
- Soreness: [trend]
- Mood / Motivation: [trend]
- Weight: [trend]
- VO2 max: [trend]
- Injury: [status]

### Wins
- [What went well — specific]

### Concerns
- [What needs attention — specific]

### Adjustment for Next Week
- [What changes and why]

### Questions for the Athlete
1. [Targeted question about something observed]
2. [Question about goals/motivation/barriers]
```

Append the review to `data/logs/weekly-reviews.md`.

## Monthly Review (run every 4 weeks)

In addition to the weekly review, the monthly review adds:

1. **Benchmark assessment:**
   - Is it time for a re-test (submax or TT)? If the athlete is stable, schedule one.
   - Compare current performance indicators to the start of the mesocycle.

2. **Zone update:**
   - If re-test was done: update thresholds and zones in `data/memory/coach-memory.md` → Current Zones and Fitness Test History sections.
   - Flag that load metrics (TSS etc.) will shift with new thresholds.

3. **Mesocycle evaluation:**
   - Did this mesocycle achieve its objectives?
   - Is the athlete on track for the macrocycle timeline? Cross-check `data/references/events.md`.
   - Do phases need to shift (extend base, compress build, etc.)?
   - Record any structural changes or phase shifts in `data/current-plan.md` under "Decisions & Agreements".

4. **Profile freshness check:**
   - Read `data/references/athlete-profile.md` — check the `## Last Updated` date.
   - If >4 weeks old: review health, current training status, equipment, and constraints. Update any stale fields and set the date to today.

5. **Goal stack check:**
   - Revisit outcome, performance, process, and identity goals.
   - Are they still relevant? Need updating?

6. **Forward plan:**
   - Outline the next mesocycle's focus and targets.
   - Identify any upcoming scheduling conflicts (travel, work, life events).

## After Every Review

### Daily log rotation (monthly)

At the start of every review, check whether the current month differs from the earliest entries in `data/logs/daily-log.md`. If the log contains entries from a previous month:

1. Extract all entries from the previous month(s)
2. Write them to `data/archive/logs/YYYY-MM.md` (e.g., `2026-02.md`)
3. Remove those entries from `daily-log.md`, keeping only the current month's entries
4. Preserve the file header in `daily-log.md`

This prevents the daily log from growing indefinitely. The archived logs remain available for historical analysis.

### Archive the completed week

Write the completed week to `data/archive/weekly/YYYY-WNN.md` (e.g., `2026-W09.md`). Include the full week section from `current-plan.md`: schedule, tracking table, modifications, and key sessions.

Then update `data/current-plan.md`:
- Remove the completed week's detail from "This Week" (replace with the new week or leave empty for `/coach:plan`)
- Update `## Previous Weeks` to reference the archive file instead of holding inline content:
  ```
  ## Previous Weeks
  - Week 1 (Mar 2–8): `data/archive/weekly/2026-W09.md`
  ```
- Update current week/phase if advancing
- Log any new decisions or agreements
- Record any plan deviations and their rationale
- For monthly reviews: update the phase overview if mesocycle targets shifted

### Memory maintenance

Update `data/memory/coach-memory.md`:

1. **Synthesize the week's observations** — if patterns emerged from daily check-ins (e.g., sleep consistently poor mid-week, fatigue spiking after long runs), write them to Athlete Patterns & Tendencies.
2. **Check open follow-ups** — resolve any that were addressed this week, add new ones if needed.
3. **Update injury history** — if an injury signal appeared, progressed, or resolved this week, update the entry.
4. **Prune stale entries** — entries in Athlete Patterns & Tendencies older than 12 weeks that haven't been reobserved should be archived to `data/memory/archive/YYYY-MM.md` and removed from the main file. Keep Injury & Health History entries permanently (they're date-stamped and compact). Keep Fitness Test History and Current Zones permanently.
5. **Update preferences** — if the athlete responded particularly well (or poorly) to a coaching approach this week, note it.
