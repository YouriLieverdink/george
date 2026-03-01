# /coach:checkin — Daily Readiness Check

Quick daily check-in (<30 seconds for the athlete) to determine today's session approach. Log results to the "Daily Log" tab of the coach Google Sheet.

## Instructions

Load the coach agent from `agents/coach/coach.md` and alert rules from `agents/coach/alerts.md`.

Read the athlete's profile from `data/coach/references/athlete-profile.md` and today's planned session from `data/coach/plans/current-plan.md`. Check `data/coach/references/events.md` for any upcoming race context (e.g., taper awareness, race week adjustments).

## Ask the Athlete (keep it quick)

Collect these six data points:

1. **Sleep:** hours + quality (0–10)
2. **Stress:** (0–10)
3. **Fatigue:** (0–10)
4. **Soreness:** (0–10)
5. **Pain:** (0–10) + location + does it change your mechanics?
6. **Time available today:**

## Decision Logic

Apply the decision tree from `agents/coach/alerts.md`:

1. **Red flags?** (chest pain, fainting, severe SOB, systemic illness)
   → STOP. Rest only. Recommend medical evaluation.

2. **Pain ≥ 4/10 or altered mechanics?**
   → Replace run with low-impact. Reduce intensity. Flag for follow-up.

3. **Readiness low?** (2+ of: poor sleep, fatigue ≥ 7, soreness ≥ 7)
   → Keep session but downshift: easy aerobic only, or shorten 30–50%.

4. **Key session day + hard session in last 48h?**
   → Convert to moderate or move key session 24–48h.

5. **Otherwise:** proceed with planned session.

## Output

Provide:
1. **Today's session** (adapted if needed) with warm-up/main/cool-down, target intensities
2. **Why** (brief rationale linking readiness to the decision)
3. **What to log** after the session (RPE, pain, fueling if long)
4. **What would trigger adjustment** mid-session (e.g., "if RPE drifts above 7, cap it there")

If the session is >75–90 min, include fueling notes.

## Log

Write the check-in data to the "Daily Log" tab: date, sleep, stress, fatigue, soreness, pain, time available, planned session, any modifications made.
