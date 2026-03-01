# /coach:onboard — Athlete Intake

Collect the athlete's profile to personalize all future coaching. Store answers in the "Profile" tab of the coach Google Sheet.

## Instructions

Load the coach agent from `agents/coach/coach.md`. Then walk the athlete through the following intake form conversationally — don't dump all questions at once. Group them naturally (event → history → constraints → health).

## Intake Questions

Ask one group at a time, confirm understanding, then move on:

**Event & Goals**
1. What is your event (70.3 / marathon / ultra) and date?
2. Primary goal (finish / time / qualify) and secondary goals?
3. Course and conditions if known (heat, altitude, terrain)?

**Training History**
4. Training history: last 6–8 weeks average volume (swim/bike/run/strength) and longest session in each discipline?
5. Previous bests (5k/10k/half/full; FTP; swim times if known)?
6. Training age (years consistently training endurance)?

**Constraints & Equipment**
7. Days/week available, max time on weekdays, max time on weekends, preferred rest day, travel dates?
8. Equipment: HR strap? Power meter? Treadmill? Pool access?

**Health & Safety**
9. Injury history past 12 months?
10. Injury status now (0–10 pain; where; does it change your form)?
11. Any medical conditions or medications that affect exercise safety? (If yes → require clinician clearance before proceeding.)

**Nutrition & Recovery**
12. Known GI issues, allergies, preferences, caffeine tolerance?
13. Sleep: average hours/night, shift work, biggest barriers?

## After Intake

1. Summarize the athlete profile back to them for confirmation.
2. Write the profile to `data/coach/references/athlete-profile.md`.
3. Check `data/coach/references/events.md` for the race calendar — confirm events are up to date.
4. Check `data/coach/plans/` for existing training plans — if plans already exist, review them and confirm they align with the athlete's profile and goals.
5. Set up initial zones in the "Zones" tab of the coach Google Sheet (from previous bests or schedule a baseline test).
6. If no plans exist yet, propose macrocycle structures based on events and current fitness.
7. Establish the goal stack: outcome, performance, process, and identity/values goals (store in the athlete profile).
8. **Create `data/coach/current-plan.md`** — the living operational state file. Initialize it with:
   - Which plan(s) from `plans/` are active and for which event
   - The current week and phase
   - Any immediate adjustments based on the intake (e.g., if the athlete is joining mid-plan, note where they're picking up)
   - Agreed goals and priorities
   - The "Decisions & Agreements" log (empty, ready for entries)

See the current-plan.md structure below for the expected format.

## Minimum Viable Data

If the athlete cannot provide everything, you MUST have at minimum:
- Current training volume
- Injury status
- Available days/time
- Event date (check `data/coach/references/events.md`)

Without these four: output a **draft framework only**, not a full prescription. Flag clearly what's missing.
