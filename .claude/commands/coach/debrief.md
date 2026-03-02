# /coach:debrief — Post-Session Debrief

Structured logging after every training session. Captures subjective and objective data, flags issues, and provides brief feedback.

## Instructions

### Pre-flight check
Before proceeding, verify that `data/references/athlete-profile.md` and `data/current-plan.md` exist and contain populated content (not just headers). If either is missing or empty → stop and tell the athlete: "It looks like onboarding hasn't been completed yet. Run `/coach:onboard` first to set up your profile and plan."

Load the coach agent from `.claude/agents/coach.md` and alert rules from `.claude/agents/alerts.md`.

Read today's planned session from `data/current-plan.md` (the "This Week" section) to compare plan vs. actual. If a session was modified during checkin, the modification will already be noted there. Read `data/memory/coach-memory.md` for context (injury history, open follow-ups, patterns).

### Pull activity data from intervals.icu first

Before asking the athlete anything, pull today's completed activity from the API (see `.claude/services/coach/intervals-icu.md`):

1. **Get today's activities** — find the most recent one matching the expected type (Run, Ride, Swim, etc.)
2. **Extract key metrics:** duration, distance, avg HR, max HR, avg pace/power, TSS/training load, zone distribution
3. **Compare plan vs. actual:** was the prescribed distance/duration roughly hit? Was intensity in the right zone?

Present a summary:
> "Session recorded: 11.2 km easy run in 67 min, avg HR 138, avg pace 5:59/km, training load 58. The plan was 11.2 km Easy at 6:00/km — looks spot on."

Then ask only for what the API can't tell you.

## Ask the Athlete (only subjective data)

The API already has distance, duration, HR, pace, power, and training load. Ask only for:

1. **RPE (0–10)** + how it compared to the plan (easier / as expected / harder)
2. **Pain or niggles (0–10):** where, when it started, how it changed during the session
3. **Fueling** (for sessions >75 min): what and how much, GI response (good / mild issues / problems)
4. **For key sessions:** did you hit pacing/power targets? If not, why? (cross-reference with API data)
5. **One sentence: "What did you learn?"**

## Processing

After collecting the data:

1. **Check alerts:** Apply alert rules from `.claude/agents/alerts.md`:
   - Pain ≥ 4/10 or worsening trend? → Flag and recommend modification tomorrow.
   - RPE much higher than expected for the prescribed intensity? → Note potential fatigue accumulation.
   - GI issues during fueling practice? → Adjust fueling plan for next long session.

2. **Provide brief feedback:**
   - Affirm what went well (use specific observations, not generic praise)
   - If something needs attention, frame as a collaborative next step
   - Connect to the bigger picture (what this session contributes to the plan)

3. **Update the daily log** — append session data to `data/logs/daily-log.md` under today's date (add a `### Session Debrief` subsection if the morning check-in entry already exists, or create a new date entry):

   ```
   ### Session Debrief
   - Session: [type] — [distance] in [duration], avg HR [X], avg pace/power [X]
   - Plan vs. actual: [comparison]
   - RPE: [X]/10 ([easier / as expected / harder])
   - Pain: [X]/10 — [location, details if any]
   - Fueling: [details if applicable]
   - Learning: "[athlete's response]"
   - Alerts: [any triggered]
   ```

4. **Update memory** — write to `data/memory/coach-memory.md`:
   - **Key Learnings:** If the athlete's "what did you learn?" response contains an insight worth preserving, add it with a date stamp.
   - **Injury & Health History:** If pain ≥ 4/10 or any new injury signal, append with date, location, severity, and context.
   - **Athlete Patterns:** If a debrief-relevant pattern is emerging (e.g., consistently higher RPE than expected on Thursdays, recurring calf tightness after intervals), note it.
   - **Open Follow-ups:** If an injury or concern needs monitoring, add a follow-up item.

5. **If this was the last session of the week:** suggest running `/coach:review` for the weekly review.

## Output

Keep it concise — the athlete just finished training. Provide:

1. **Acknowledgment** of the session (1–2 sentences)
2. **Any flags** that need attention (pain, unexpected RPE, GI issues)
3. **One forward-looking note** (what to pay attention to next session)
