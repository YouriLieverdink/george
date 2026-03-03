# /coach:checkin — Daily Readiness Check

Quick daily check-in (<30 seconds for the athlete) to determine today's session approach.

## Instructions

### Pre-flight check
Before proceeding, verify that `data/references/athlete-profile.md` and `data/current-plan.md` exist and contain populated content (not just headers). If either is missing or empty → stop and tell the athlete: "It looks like onboarding hasn't been completed yet. Run `/coach:onboard` first to set up your profile and plan."

Load the coach agent from `.claude/agents/coach.md` and alert rules from `.claude/agents/alerts.md`.

Read the athlete's profile from `data/references/athlete-profile.md`. Read `data/current-plan.md` to determine the current week, phase, active plan, and today's planned session. Reference the original plan from `data/plans/` if needed for session details. Check `data/references/events.md` for race proximity (e.g., taper awareness, race week adjustments). Read `data/memory/coach-memory.md` for accumulated context (patterns, open follow-ups, injury history, zones).

### Pull data from intervals.icu first

Before asking the athlete anything, pull today's data from the API (see `.claude/services/coach/intervals-icu.md`):

1. **Wellness data** for today — all Garmin-synced fields: sleep duration, sleep score, sleep quality, HRV, resting HR, weight, SpO2, steps, VO2 max
2. **Yesterday's activity** (and today's if any) — check for completed workouts

### Check for undebriefed sessions

Check `data/logs/daily-log.md` for whether yesterday's activity has a "Session Debrief" entry. Also check the tracking table in `current-plan.md` — if "Actual" column is empty for a completed session visible in the API, it's undebriefed.

If an undebriefed session is detected:
1. Acknowledge it naturally: "I see you did a 45 min easy run yesterday that we didn't debrief. Quick catch-up before we get to today —"
2. **Mini-debrief** (3 questions only): RPE (0–10), any pain or niggles (0–10 + location if yes), and one-line "how did it feel?"
3. Log the mini-debrief to `data/logs/daily-log.md` under the session's date as a `### Session Debrief (mini)` entry
4. Update the tracking table in `current-plan.md` with the actual session data from the API
5. Update `data/memory/coach-memory.md` if pain was reported (Injury & Health History)
6. Then proceed to today's readiness check

This prevents data loss from forgotten debriefs without requiring the full debrief workflow.

### Present wellness data

Present what you already know:
> "Good morning! Your watch synced: 7.2h sleep (score 82, quality GOOD), HRV 48, resting HR 52, SpO2 97%, 8.4k steps."

Then ask only for what the API can't provide.

### Pattern Check (proactive coaching)

After pulling API data, before asking subjective questions, check `data/memory/coach-memory.md`:

1. **Recent memory** — if `coach-memory.md` has entries added in the last 24h (especially Open Follow-ups or recent chat observations), lead with those naturally before asking subjective scores. This bridges informal conversations into the structured check-in.
2. **Open follow-ups** — address the most important one first. Don't say "as noted in our records" — say it naturally: "Last time you mentioned your calf was bothering you — how's that going?" or "You had that doctor appointment — how did it go?"
3. **Continuing patterns** — if today's data confirms a known pattern (e.g., poor sleep again after a late evening, HRV trending down for the third day), mention it: "I notice your sleep has been under 6.5h three days running now — that's becoming a pattern worth addressing."
4. **Athlete commitments** — if the athlete committed to something (earlier bedtime, caffeine cutoff, stretching routine), gently check in on it.

Lead the check-in with the most important finding before moving to the wellness summary and subjective questions.

## Ask the Athlete (only missing data)

From the wellness sync, you already have sleep, HRV, resting HR, weight, SpO2, steps, VO2 max, and sleep quality. Ask only for the subjective fields that Intervals.icu doesn't auto-populate.

All subjective fields use the Intervals.icu 1–4 scale (1=best, 4=worst):

1. **Soreness:** LOW(1) / AVG(2) / HIGH(3) / EXTREME(4)
2. **Fatigue:** LOW(1) / AVG(2) / HIGH(3) / EXTREME(4)
3. **Stress:** LOW(1) / AVG(2) / HIGH(3) / EXTREME(4)
4. **Mood:** GREAT(1) / GOOD(2) / OK(3) / GRUMPY(4)
5. **Motivation:** EXTREME(1) / HIGH(2) / AVG(3) / LOW(4)
6. **Injury:** NONE(1) / NIGGLE(2) / POOR(3) / INJURED(4) — if NIGGLE or worse, ask: location + does it change your mechanics?
7. **Hydration:** GOOD(1) / OK(2) / POOR(3) / BAD(4)
8. **Alcohol** (drinks previous evening, 0 if none) — affects recovery, sleep quality, and HRV
9. **Caffeine cutoff** (what time was the last coffee/caffeine yesterday?) — relevant for sleep quality assessment
10. **Time available today:**

Write the subjective scores back to intervals.icu via the wellness PUT endpoint (soreness, fatigue, stress, mood, motivation, injury, hydration).

## Decision Logic

Combine device data (HRV, resting HR, sleep) with subjective scores to assess readiness. Apply the decision tree from `.claude/agents/alerts.md`:

1. **Red flags?** (chest pain, fainting, severe SOB, systemic illness)
   → STOP. Rest only. Recommend medical evaluation.

2. **Injury ≥ POOR(3) or altered mechanics?**
   → Replace run with low-impact. Reduce intensity. Flag for follow-up.
   Injury = NIGGLE(2) → flag for monitoring, proceed with caution.

3. **Readiness low?** (2+ of: poor sleep, fatigue ≥ HIGH(3), soreness ≥ HIGH(3), HRV ≥10% below 7-day rolling average (compute from Intervals.icu wellness data), alcohol ≥ 3 drinks, low SpO2)
   → Keep session but downshift: easy aerobic only, or shorten 30–50%.
   Note: alcohol the previous evening lowers the threshold for downshifting — even 1–2 drinks with poor sleep warrants caution. Late caffeine cutoff (after ~15:00) combined with poor sleep is a pattern to flag over time.
   Low SpO2 (below athlete's baseline) → flag as possible illness indicator.

4. **Overtraining signals?** (mood = GRUMPY(4) + motivation = LOW(4) + declining performance trend)
   → Flag for review. Consider deload or extra rest day.

5. **Key session day + hard session in last 48h?** (check intervals.icu activities for last 48h)
   → Convert to moderate or move key session 24–48h.

6. **Otherwise:** proceed with planned session.

If the session is modified, log the modification and reason in the "This Week" section of `current-plan.md`.

## Output

Provide:
1. **Today's session** (adapted if needed) with warm-up/main/cool-down, target intensities
2. **Why** (brief rationale linking readiness to the decision)
3. **What to log** after the session (RPE, pain, fueling if long)
4. **What would trigger adjustment** mid-session (e.g., "if RPE drifts above 7, cap it there")

If the session is >75–90 min, include fueling notes.

## Log

Append the check-in data to `data/logs/daily-log.md` under today's date:

```
## YYYY-MM-DD — [Day of Week]

### Morning Check-in
- Sleep: [duration]h (score [X], quality [X])
- HRV: [X] | Resting HR: [X] | SpO2: [X]% | Weight: [X] kg
- Steps: [X] | VO2 max: [X]
- Soreness: [X] | Fatigue: [X] | Stress: [X]
- Mood: [X] | Motivation: [X] | Injury: [X] | Hydration: [X]
- Alcohol: [X] | Caffeine cutoff: [X]
- Time available: [X]
- Planned session: [session] | Modifications: [if any]
```

## Memory Updates

After the check-in:
- If a pattern is noticed (e.g., third consecutive morning with poor sleep + late caffeine), write an observation to `data/memory/coach-memory.md` → Athlete Patterns & Tendencies with a date stamp.
- If injury ≥ NIGGLE(2), append to `data/memory/coach-memory.md` → Injury & Health History with date, location, severity, and context.
- If following up on an open item and it's resolved, remove it from Open Follow-ups.
