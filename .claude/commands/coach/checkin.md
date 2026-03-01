# /coach:checkin — Daily Readiness Check

Quick daily check-in (<30 seconds for the athlete) to determine today's session approach. Log results to the "Daily Log" tab of the coach Google Sheet.

## Instructions

Load the coach agent from `agents/coach/coach.md` and alert rules from `agents/coach/alerts.md`.

Read the athlete's profile from `data/coach/references/athlete-profile.md`. Read `data/coach/current-plan.md` to determine the current week, phase, active plan, and today's planned session. Reference the original plan from `data/coach/plans/` if needed for session details. Check `data/coach/references/events.md` for race proximity (e.g., taper awareness, race week adjustments).

### Pull data from intervals.icu first

Before asking the athlete anything, pull today's data from the API (see `services/intervals-icu.md`):

1. **Wellness data** for today — sleep duration, sleep quality, HRV, resting HR (synced from wearable)
2. **Yesterday's activity** if not yet debriefed — check if there's a completed workout to acknowledge

Present what you already know:
> "Good morning! Your watch synced: 7.2h sleep, HRV 48, resting HR 52. Yesterday's run: 8.1 km, 49 min, avg HR 142."

Then ask only for what the API can't provide.

## Ask the Athlete (only missing data)

From the wellness sync, you may already have sleep and HRV. Ask only for what's missing:

1. **Sleep quality** (0–10) — if not synced or if you want a subjective feel beyond device score
2. **Stress:** (0–10)
3. **Fatigue:** (0–10)
4. **Soreness:** (0–10)
5. **Pain:** (0–10) + location + does it change your mechanics?
6. **Time available today:**

Optionally write the subjective scores back to intervals.icu via the wellness PUT endpoint.

## Decision Logic

Combine device data (HRV, resting HR, sleep) with subjective scores to assess readiness. Apply the decision tree from `agents/coach/alerts.md`:

1. **Red flags?** (chest pain, fainting, severe SOB, systemic illness)
   → STOP. Rest only. Recommend medical evaluation.

2. **Pain ≥ 4/10 or altered mechanics?**
   → Replace run with low-impact. Reduce intensity. Flag for follow-up.

3. **Readiness low?** (2+ of: poor sleep, fatigue ≥ 7, soreness ≥ 7, HRV significantly below baseline)
   → Keep session but downshift: easy aerobic only, or shorten 30–50%.

4. **Key session day + hard session in last 48h?** (check intervals.icu activities for last 48h)
   → Convert to moderate or move key session 24–48h.

5. **Otherwise:** proceed with planned session.

If the session is modified, log the modification and reason in the "This Week" section of `current-plan.md`.

## Output

Provide:
1. **Today's session** (adapted if needed) with warm-up/main/cool-down, target intensities
2. **Why** (brief rationale linking readiness to the decision)
3. **What to log** after the session (RPE, pain, fueling if long)
4. **What would trigger adjustment** mid-session (e.g., "if RPE drifts above 7, cap it there")

If the session is >75–90 min, include fueling notes.

## Log

Write the check-in data to the "Daily Log" tab: date, sleep, stress, fatigue, soreness, pain, time available, planned session, any modifications made.
