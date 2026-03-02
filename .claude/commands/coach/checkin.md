# /coach:checkin — Daily Readiness Check

Quick daily check-in (<30 seconds for the athlete) to determine today's session approach. Log results to the "Daily Log" tab of the coach Google Sheet.

## Instructions

Load the coach agent from `.claude/agents/coach.md` and alert rules from `.claude/agents/alerts.md`.

Read the athlete's profile from `data/references/athlete-profile.md`. Read `data/current-plan.md` to determine the current week, phase, active plan, and today's planned session. Reference the original plan from `data/plans/` if needed for session details. Check `data/references/events.md` for race proximity (e.g., taper awareness, race week adjustments).

### Pull data from intervals.icu first

Before asking the athlete anything, pull today's data from the API (see `.claude/services/coach/intervals-icu.md`):

1. **Wellness data** for today — all Garmin-synced fields: sleep duration, sleep score, sleep quality, HRV, resting HR, weight, SpO2, steps, VO2 max
2. **Yesterday's activity** if not yet debriefed — check if there's a completed workout to acknowledge

Present what you already know:
> "Good morning! Your watch synced: 7.2h sleep (score 82, quality GOOD), HRV 48, resting HR 52, SpO2 97%, 8.4k steps. Yesterday's run: 8.1 km, 49 min, avg HR 142."

Then ask only for what the API can't provide.

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

3. **Readiness low?** (2+ of: poor sleep, fatigue ≥ HIGH(3), soreness ≥ HIGH(3), HRV significantly below baseline, alcohol ≥ 3 drinks, low SpO2)
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

Write the check-in data to the "Daily Log" tab: date, sleep (duration + score + quality), HRV, resting HR, weight, SpO2, soreness, fatigue, stress, mood, motivation, injury, hydration, alcohol, caffeine cutoff, time available, planned session, any modifications made.
