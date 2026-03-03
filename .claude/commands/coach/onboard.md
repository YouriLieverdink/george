---
model: opus
---

# /coach:onboard — Athlete Intake

Collect the athlete's profile to personalize all future coaching.

## Instructions

Load the coach agent from `.claude/agents/coach.md`. Then walk the athlete through the following intake form conversationally — don't dump all questions at once. Group them naturally (event → history → constraints → health).

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
2. Write the profile to `data/references/athlete-profile.md`.
3. Check `data/references/events.md` for the race calendar — confirm events are up to date.
4. Check `data/plans/` for existing training plans — if plans already exist, review them and confirm they align with the athlete's profile and goals.
5. **Seed `data/memory/coach-memory.md`** — create the coaching memory file with initial data from the intake:
   - **Injury & Health History:** any injury history from the intake (date, what happened, resolution)
   - **Athlete Patterns & Tendencies:** known patterns (e.g., sleep habits, caffeine use, scheduling tendencies)
   - **Preferences & Style:** motivation style, identity goals, communication preferences observed during intake
   - **Current Zones:** set up initial zones from previous bests (or note that baseline tests are needed)
   - **Fitness Test History:** any known benchmarks (race times, FTP, CSS)
6. **Establish HRV baseline:** Pull the last 30 days of wellness data from Intervals.icu (see `.claude/services/coach/intervals-icu.md`). If HRV data exists → compute the 30-day HRV average and store it in `data/memory/coach-memory.md` → Athlete Patterns & Tendencies as "HRV baseline: X ms (30-day avg as of YYYY-MM-DD)". If no data or <7 days of data → note in coach-memory that baseline will establish over the first 2 weeks of check-ins.
7. If no plans exist yet, propose macrocycle structures based on events and current fitness.
8. Establish the goal stack: outcome, performance, process, and identity/values goals (store in the athlete profile).
9. **Create `data/current-plan.md`** — the living operational state file. Initialize it with:
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
- Event date (check `data/references/events.md`)

Without these four: output a **draft framework only**, not a full prescription. Flag clearly what's missing.
