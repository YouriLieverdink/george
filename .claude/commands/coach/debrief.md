# /coach:debrief — Post-Session Debrief

Structured logging after every training session. Captures subjective and objective data, flags issues, and provides brief feedback. Log results to the "Daily Log" tab.

## Instructions

Load the coach agent from `agents/coach/coach.md` and alert rules from `agents/coach/alerts.md`.

Read today's planned session from `data/coach/current-plan.md` (the "This Week" section) to compare plan vs. actual. If a session was modified during checkin, the modification will already be noted there.

## Ask the Athlete

Collect these data points after the session:

1. **RPE (0–10)** + how it compared to the plan (easier / as expected / harder)
2. **Pain or niggles (0–10):** where, when it started, how it changed during the session
3. **Fueling:** what and how much (carbs/h, fluids/h), GI response (good / mild issues / problems)
4. **For key sessions:** did you hit pacing/power targets? If not, why?
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
