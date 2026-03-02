# /coach:raceweek — Race Week Preparation

Race week support: session schedule, logistics, nutrition plan, mental prep, and race-day pacing strategy. Triggers when an event is within 7 days, or run manually anytime.

## Instructions

Load the coach agent from `.claude/agents/coach.md` and alert rules from `.claude/agents/alerts.md`.

Read from local files:
- `data/current-plan.md` → current operational state, taper status
- `data/references/events.md` → target event details (course, distances, conditions, target splits)
- `data/references/athlete-profile.md` → equipment, nutrition, health
- `data/memory/coach-memory.md` → injury history, fitness test results, current zones, athlete patterns, preferences
- `data/logs/daily-log.md` → recent readiness trend (last 7–10 days)

### Pull data from intervals.icu

Before generating the race week plan, pull from the API (see `.claude/services/coach/intervals-icu.md`):

1. **Athlete summary** → current CTL (fitness), ATL (fatigue), TSB (form) — assess race readiness
2. **Wellness for the past 7 days** → sleep, HRV, resting HR trends heading into race week
3. **Activities for the past 14 days** → confirm taper has been executed, check for any unplanned hard efforts

### Assess Race Readiness

Based on the data:
- **Form (TSB):** Is the athlete arriving at the race with positive form? If TSB is negative, note it and adjust expectations.
- **Fatigue trend:** Is fatigue dropping as expected during taper?
- **Sleep trend:** Flag if sleep has been poor — this is the #1 controllable factor in race week.
- **Injury status:** Check memory for any ongoing niggles. If injury ≥ NIGGLE, discuss race-day management.
- **Illness signals:** Any recent HRV drops, elevated resting HR, or low SpO2? Flag immediately.

## Output

### 1. Race Week Session Schedule

Light sessions only — the hay is in the barn. Typical pattern:
- **Mon–Wed:** Short openers with a few race-pace strides/efforts (5–10 min total intensity)
- **Thu–Fri:** Very easy or rest. One short shakeout the day before if the athlete wants it.
- **Race day:** The plan (see pacing strategy below)

For triathlon: include short swims and bike spins to stay loose. No volume.

### 2. Logistics Checklist

Generate a race-specific checklist based on the event type:

**Gear:**
- [ ] Race kit laid out (race belt, visor/cap, sunglasses, socks)
- [ ] Bike checked (tires, brakes, shifting, chain lube) — for triathlon
- [ ] Wetsuit if applicable — for triathlon
- [ ] GPS watch charged + race loaded
- [ ] HR strap
- [ ] Transition bags packed — for triathlon
- [ ] Flat kit (tube, CO2, tire levers) — for triathlon
- [ ] Race number, timing chip collected

**Nutrition (race day):**
- [ ] Pre-race meal planned (2–3h before start, familiar foods)
- [ ] On-course fueling plan: what products, how many, at what intervals
- [ ] Backup fuel (in case aid stations don't have what you expect)
- [ ] Hydration plan (bottles, electrolytes)
- [ ] Post-race recovery food

**Travel/logistics:**
- [ ] Start time and location confirmed
- [ ] Travel to venue planned (parking, transit)
- [ ] Accommodation sorted (if needed)
- [ ] Course maps reviewed
- [ ] Weather forecast checked

Adapt the checklist to the specific event type (marathon vs. triathlon).

### 3. Mental Preparation

- **Process focus:** Remind the athlete of their process goals — this is what they control on race day
- **Mantras:** If the athlete has shared any in previous conversations (check memory), reference them
- **Race-day mindset:** "Execute the plan, trust the training, respond to the body"
- **What-if scenarios:** Brief walk-through of common race-day situations (starting too fast, GI issues, hitting a low patch, weather changes) and the response plan for each

### 4. Race-Day Pacing Strategy

Based on `events.md` target splits, current fitness (CTL), and recent training:

- **Pacing plan** with target splits per discipline/segment
- **Heart rate guardrails** (using zones from memory)
- **Fueling timing** linked to the pacing plan
- **Decision points:** Where in the race to assess and potentially adjust (e.g., "if HR is above X at the half-marathon mark, ease back 10–15 sec/km")

For triathlon: include T1/T2 routines.

### 5. Race Week Nutrition

- **Carb loading protocol** (if applicable — typically 2–3 days before for events >90 min)
- **Hydration focus** — increase fluid intake starting 2–3 days out
- **Foods to avoid** in the final 48h (high fiber, unfamiliar foods, alcohol)
- **Pre-race meal** timing and composition
- **Morning-of routine** (wake time relative to start, meal timing, warm-up)

## After Output

Update `data/current-plan.md`:
- Note that race week plan was generated
- Record any athlete decisions about pacing, nutrition, or logistics

Write any significant athlete inputs to `data/memory/coach-memory.md` (e.g., race-day fears, mental preparation notes, specific equipment decisions).
