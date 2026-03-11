---
model: sonnet
---

# /coach:debrief — Post-Session Debrief

Structured logging after every training session. Captures subjective and objective data, flags issues, and provides brief feedback.

## Instructions

### Pre-flight check
Before proceeding, verify that `data/references/athlete-profile.md` and `data/current-plan.md` exist and contain populated content (not just headers). If either is missing or empty → stop and tell the athlete: "It looks like onboarding hasn't been completed yet. Run `/coach:onboard` first to set up your profile and plan."

Load the coach agent from `.claude/agents/coach.md` and alert rules from `.claude/agents/alerts.md`.

Read today's planned session from the intervals.icu calendar (see `.claude/services/coach/intervals-icu.md` Section 6 — query today's events). The calendar is the source of truth for planned workouts, including any modifications made during checkin. Read `data/current-plan.md` for context (phase, rationale, decisions) and `data/memory/coach-memory.md` for context (injury history, open follow-ups, patterns).

### Identify the session to debrief

Pull both planned events and completed activities upfront, then match them explicitly.

**Step 1 — Pull data from intervals.icu:**

1. Pull today's **calendar events** (WORKOUT category only) from the API
2. Pull today's **activities** from the API
3. If no activities today, also pull yesterday's activities

**Step 2 — Match activities to calendar events:**

Match by **primary sport type** (Run↔Run, Ride↔Ride, Swim↔Swim, WeightTraining↔WeightTraining). Use event name and planned duration as secondary confirmation signals. A match means same sport type on the same day.

**Step 3 — Handle the result:**

| Scenario | Action |
|----------|--------|
| **One activity, one matching event** (types align) | Confirm the pairing: "You had [event name] on the plan and completed [activity type] [duration] — debriefing that one?" |
| **One activity, no matching event** (type mismatch or no event for that day) | Flag the mismatch: "The plan had [event name / type], but you did [activity type] instead. Did you swap sessions, or was this an extra?" |
| **Multiple activities and/or events** | List all activities and calendar events with their types, then ask which pairing to debrief: "I see these on the plan: (A) Easy Run, (B) Strength. And these completed: (1) Run 45 min, (2) WeightTraining 40 min. Which pairing are we debriefing?" |
| **No activities found** (today or yesterday) | Check if a calendar event exists for today. If yes: "You had [event name] planned but I don't see a synced activity. Did you complete it externally (Hevy, pool timer, etc.) or skip it?" If no event either: "No planned session or activity found — what are we debriefing?" |
| **Activity exists, no calendar events at all** | Unplanned session: "I don't see anything on the calendar for today, but you did [activity type] [duration]. Unplanned session? Confirm and we'll log it." |

### Pull activity data from intervals.icu

Once the session-to-event pairing is confirmed, extract from the matched activity:

1. **Key metrics:** duration, distance, avg HR, max HR, avg pace/power, TSS/training load, zone distribution
2. **Compare plan vs. actual:** use the **matched calendar event** as the reference. Was the prescribed distance/duration roughly hit? Was intensity in the right zone? If a session swap occurred (e.g., ran instead of planned strength), note it explicitly in the comparison and in the daily log.

Present a summary:
> "Session recorded: 11.2 km easy run in 67 min, avg HR 138, avg pace 5:59/km, training load 58. The plan was 11.2 km Easy at 6:00/km — looks spot on."

Then ask only for what the API can't tell you.

## Ask the Athlete (only subjective data)

The API already has distance, duration, HR, pace, power, and training load. Ask only for:

1. **RPE (0–10)** + how it compared to the plan (easier / as expected / harder)
2. **Pain or niggles (0–10):** where, when it started, how it changed during the session
3. **Fueling** (for sessions >75 min or `[FUEL]`-tagged): what product, how much (g carbs/h), at what intervals, GI response (good / mild issues / problems), energy levels through session. Log to `coach-memory.md` → Race Rehearsal Log.
4. **For key sessions:** did you hit pacing/power targets? If not, why? (cross-reference with API data)
5. **One sentence: "What did you learn?"**

## Processing

After collecting the data:

1. **Pacing adherence** (for key sessions): Compare planned workout targets (from the matched calendar event description — parsed intervals, pace/power/HR targets) against actual activity metrics (avg pace, avg power, HR zones, lap splits). Report adherence:
   - Target vs actual for each structured interval (if available)
   - Overall session: on-target / slightly over / significantly over or under
   - Note any drift patterns (e.g., started on target, faded in final intervals)
   - Log pacing adherence summary in the daily log entry.

2. **Check alerts:** Apply alert rules from `.claude/agents/alerts.md`:
   - Pain ≥ 4/10 or worsening trend? → Flag and recommend modification tomorrow.
   - RPE much higher than expected for the prescribed intensity? → Note potential fatigue accumulation.
   - GI issues during fueling practice? → Adjust fueling plan for next long session.

3. **Provide brief feedback:**
   - Affirm what went well (use specific observations, not generic praise)
   - If something needs attention, frame as a collaborative next step
   - Connect to the bigger picture (what this session contributes to the plan)

4. **Update the daily log** — append session data to `data/logs/daily-log.md` under today's date (add a `### Session Debrief` subsection if the morning check-in entry already exists, or create a new date entry):

   ```
   ### Session Debrief
   - Session: [type] — [distance] in [duration], avg HR [X], avg pace/power [X]
   - Plan vs. actual: [comparison]
   - RPE: [X]/10 ([easier / as expected / harder])
   - Pain: [X]/10 — [location, details if any]
   - Fueling: [details if applicable — product, g/h, GI response]
   - Pacing adherence: [on-target / over / under — key session only]
   - Learning: "[athlete's response]"
   - Alerts: [any triggered]
   ```

5. **Update memory** — write to `data/memory/coach-memory.md`:
   - **Key Learnings:** If the athlete's "what did you learn?" response contains an insight worth preserving, add it with a date stamp.
   - **Injury & Health History:** If pain ≥ 4/10 or any new injury signal, append with date, location, severity, and context.
   - **Athlete Patterns:** If a debrief-relevant pattern is emerging (e.g., consistently higher RPE than expected on Thursdays, recurring calf tightness after intervals), note it.
   - **Open Follow-ups:** If an injury or concern needs monitoring, add a follow-up item.
   - **Race Rehearsal Log:** If fueling was practiced (sessions >75 min), update "Nutrition Products Tested" with product, GI outcome. If swim was open water, update "Open Water Swimming." If brick session, note transition practice.
   - **Swim Development:** If this was a swim course session, update "Lesson Progress" with lesson content and any technique cues that worked. Check off "Open Water Readiness" items as they're achieved.

6. **If this was the last session of the week:** suggest running `/coach:review` for the weekly review.

7. **Log conversation** — append to `data/logs/conversations.md`:

   ```
   ## YYYY-MM-DD HH:MM — /coach:debrief

   ### Summary
   [2–3 sentences: what was discussed, what was decided]

   ### Key Points
   - [Topics covered, athlete inputs, coach recommendations]
   - [Modifications made, concerns raised, patterns noted]

   ### Action Items
   - [Commitments, follow-ups, things to check next time — or "None"]
   ```

## Output

Keep it concise — the athlete just finished training. Provide:

1. **Acknowledgment** of the session (1–2 sentences)
2. **Any flags** that need attention (pain, unexpected RPE, GI issues)
3. **One forward-looking note** (what to pay attention to next session)
