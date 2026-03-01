# /coach:debrief — Post-Session Debrief

Structured logging after every training session. Captures subjective and objective data, flags issues, and provides brief feedback. Log results to the "Daily Log" tab.

## Instructions

Load the coach agent from `agents/coach/coach.md` and alert rules from `agents/coach/alerts.md`.

Read today's planned session from `data/current-plan.md` (the "This Week" section) to compare plan vs. actual. If a session was modified during checkin, the modification will already be noted there.

### Pull activity data from intervals.icu first

Before asking the athlete anything, pull today's completed activity from the API (see `services/intervals-icu.md`):

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

1. **Check alerts:** Apply alert rules from `agents/coach/alerts.md`:
   - Pain ≥ 4/10 or worsening trend? → Flag and recommend modification tomorrow.
   - RPE much higher than expected for the prescribed intensity? → Note potential fatigue accumulation.
   - GI issues during fueling practice? → Adjust fueling plan for next long session.

2. **Provide brief feedback:**
   - Affirm what went well (use specific observations, not generic praise)
   - If something needs attention, frame as a collaborative next step
   - Connect to the bigger picture (what this session contributes to the plan)

3. **Update the Daily Log** with: actual session, RPE, pain, fueling data, notes, any alerts triggered.

4. **If this was the last session of the week:** suggest running `/coach:review` for the weekly review.

## Output

Keep it concise — the athlete just finished training. Provide:

1. **Acknowledgment** of the session (1–2 sentences)
2. **Any flags** that need attention (pain, unexpected RPE, GI issues)
3. **One forward-looking note** (what to pay attention to next session)
