# /coach:postrace — Post-Race Debrief & Recovery

Structured post-race debrief: pull race data, capture the experience, write a race report, generate a recovery protocol, and update the training plan.

## Instructions

Load the coach agent from `.claude/agents/coach.md` and alert rules from `.claude/agents/alerts.md`.

Read from local files:
- `data/current-plan.md` → current operational state, what was planned for race day
- `data/references/events.md` → race details (target splits, goals)
- `data/memory/coach-memory.md` → pre-race state, injury history, zones, patterns

### Pull race data from intervals.icu

Before asking the athlete anything, pull the race activity from the API (see `.claude/services/coach/intervals-icu.md`):

1. **Get race-day activity** — find the activity matching the race date and type
2. **Extract race metrics:** total time, distance, avg/max HR, pace/power per split (use laps if available), zone distribution, training load, elevation
3. **For triathlon:** pull all race-day activities (swim, bike, run) separately if recorded as individual activities

Present a data summary:
> "Race recorded: Marathon of Groningen — 42.2 km in 3:52:14, avg HR 158, avg pace 5:30/km. Splits: [first half 1:53, second half 1:59]."

### Ask the Athlete

Then ask for the subjective experience:

1. **Overall: How was it?** (open-ended — let them talk first)
2. **Pacing execution:** Did you stick to the plan? Where did it go well / fall apart?
3. **Fueling execution:** What did you eat/drink, when, any GI issues?
4. **Body:** Any pain, niggles, or mechanical issues during the race?
5. **Mental game:** Any low points? What got you through them? Any unexpected highs?
6. **What would you do differently?**
7. **What are you most proud of?**

## Processing

### 1. Write Race Report

Create `data/archive/races/YYYY-MM-DD-race-name.md` with:

```
# Race Report — [Race Name] — [Date]

## Event Details
- Event: [name]
- Date: [date]
- Distance: [distance]
- Conditions: [weather, course notes]

## Results
- Finish time: [time]
- Goal: [what was the target] → [met / missed / exceeded]
- Splits: [table of splits with HR, pace]

## Execution
- Pacing: [summary]
- Fueling: [summary]
- Body: [summary]
- Mental: [summary]

## Key Takeaways
1. [What went well]
2. [What to improve]
3. [What surprised you]

## Coach Notes
- [Observations from the data + athlete feedback]
- [Implications for future training/racing]
```

### 2. Write Insights to Memory

Update `data/memory/coach-memory.md`:
- **Key Learnings:** Race insights worth carrying forward (pacing lessons, fueling discoveries, mental strategies that worked)
- **Injury & Health History:** Any race-day injury signals
- **Patterns:** Any confirmed patterns (e.g., "tends to go out too fast", "GI issues with gel brand X")
- **Fitness Test History:** Race result as a performance benchmark (e.g., marathon time as a running fitness marker)

### 3. Generate Recovery Protocol

Based on the race distance, intensity, and athlete's post-race state:

**Week 1 post-race (days 1–7):**
- Days 1–3: Complete rest or very gentle walking only
- Days 4–5: Light cross-training if feeling good (easy swim, gentle spin)
- Days 6–7: Easy 20–30 min jog if legs allow — no pace pressure

**Week 2 post-race (days 8–14):**
- Gradual return to easy training
- No intensity work
- Listen to the body — soreness and fatigue are normal
- Resume strength with light loads only

**Guidelines:**
- No racing or hard efforts for at least 2 weeks (marathon) or 3 weeks (70.3)
- Sleep and nutrition are the primary recovery tools
- Monitor for post-race blues (common) — acknowledge the emotional drop after a big goal

Adapt the protocol based on:
- Race distance and intensity
- How the athlete felt during and after
- Injury signals from the race
- What's next on the calendar (`events.md`)

### 4. Update Events

Mark the completed event in `data/references/events.md`:
- Add actual finish time
- Add a "Completed" marker
- Link to race report

### 5. Update Current Plan

Update `data/current-plan.md`:
- Note race completion and result
- Insert recovery protocol as the next 1–2 weeks
- Adjust the macro timeline if needed (e.g., if the athlete needs extra recovery)

## Output

1. **Race summary** — data + athlete experience combined (2–3 paragraphs)
2. **What went well** — specific, evidence-based affirmations
3. **What to carry forward** — 2–3 actionable insights for future training/racing
4. **Recovery plan** — the next 1–2 weeks, day by day
5. **What's next** — brief look ahead at the next training phase or event

Keep the tone celebratory and forward-looking. The athlete just accomplished something significant — lead with that.

## Prompt

$ARGUMENTS
