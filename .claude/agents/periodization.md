---
name: periodization
description: Periodization templates and session library for building and adapting training plans
tools: Read, Grep, Glob
---

# Periodization Templates & Session Library

Reference material for the coach agent when building and adapting training plans.

## Periodization Architecture

### Definitions
- **Macrocycle:** Full plan from today to goal race (e.g., 12/20/40 weeks)
- **Mesocycle:** Training block (~3–6 weeks) with a specific purpose (base, build, peak, taper)
- **Microcycle:** Typically 7 days — the weekly pattern of stress + recovery

### Planning Flow

```
Collect athlete profile + constraints
  → Set event + date + A/B/C goals
  → Baseline assessment: tests + recent training load + injury risk
  → Define macrocycle phases: base → build → peak → taper
  → For each mesocycle: set targets for volume, intensity, skills, strength
  → For each microcycle (week): schedule key sessions + recovery
  → Daily monitoring: objective + subjective readiness
    → Ready? Execute + log → Weekly review
    → Not ready? Adjust: reduce intensity/volume or replace session → Weekly review
  → Adapting + progressing safely? Continue.
  → Not adapting? Modify next mesocycle: deload, shift intensities, refer if red flags.
```

### Plan-Generation First Principles

1. **Specificity with progression:** gradually shift toward event-specific demands while retaining enough easy volume for aerobic development.
2. **"Hard days hard, easy days easy":** maintain polarization-ish separation to protect recovery capacity for quality.
3. **Strength as injury-performance support:** 2×/week in base/build, maintain 1×/week near peak/taper.
4. **Taper as fatigue shedding:** reduce volume 40–60% while largely maintaining intensity; ≤21 days progressive.
5. **Never out-optimize safety:** red flags → recovery/referral, not "push through."
6. **Injury prevention built in:** during volume ramps and return-from-break, include activation routines from `.claude/agents/alerts.md` → Prevention Routines by Region for any areas with niggle history.

## Intensity Distribution Targets

3-zone model mapping: Easy = Z1+Z2, Moderate = Z3, Hard = Z4+Z5.

| Phase | Easy | Moderate | Hard |
|-------|------|----------|------|
| Rebuild/Base | 80-85% | 10-15% | ≤5% |
| Build | 75-80% | 10-15% | 10-15% |
| Peak | 70-75% | 10-15% | 15-20% |
| Taper | 80-85% | 10% | 5-10% |
| Deload | 85-90% | 5-10% | <5% |

Deviation >5 percentage points in any category warrants discussion during `/coach:review`.

Exclude beginner swim sessions and strength training from the intensity distribution calculation — these are developing technical proficiency and neuromuscular adaptation respectively, not contributing to aerobic load distribution.

---

## IRONMAN 70.3 Macrocycle Blueprints

**Race demands:** Sustained aerobic durability, high fueling competence, discipline integration (bricks, transitions).

### 12-Week (rapid consolidation — assumes existing base)

| Phase | Weeks | Objectives | Load pattern |
|---|---|---|---|
| Base | 3–4 | Consolidate aerobic base, establish brick habit | 2:1 or 3:1 load:deload |
| Build | 5–6 | Race-specific pacing + fueling practice | 2:1 or 3:1 |
| Peak | 1–2 | Sharpen with race-simulation sessions | Reduced volume |
| Taper | 1–2 | Shed fatigue, maintain intensity touches | Progressive reduction |

**Key sessions emphasis:** Long bike with race-pace blocks; brick (bike→run); steady long run; technique swims.

### 20-Week (durable build)

| Phase | Weeks | Objectives | Load pattern |
|---|---|---|---|
| General prep | 4 | Movement quality, strength foundation | 3:1 |
| Base | 6 | Aerobic development across disciplines | 3:1 |
| Build | 6 | Progressive race simulation, sustained efforts | 3:1 |
| Peak | 2 | Race-specific sharpening | Reduced |
| Taper | 2 | Fatigue shedding | Progressive reduction |

**Added emphasis:** Sustained tempo/threshold work; longer bricks; open-water skills.

### 40-Week (full development)

| Phase | Weeks | Objectives | Load pattern |
|---|---|---|---|
| Transition | 2–4 | Active recovery, cross-training | Low |
| Aerobic base | 12–16 | Big aerobic development, biomechanics, technique | 3:1 with periodic resets |
| Build | 12–14 | Progressive race-specific work | 3:1 |
| Specific/Peak | 4–6 | Race rehearsal, sharpening | Reduced |
| Taper | 2–3 | Full fatigue shed | Progressive reduction |

**Added emphasis:** High consistency; progressive long-ride extension; race rehearsal days.

---

## Marathon Macrocycle Blueprints

**Race demands:** Aerobic base, lactate/threshold sustainable pace, running economy, fueling tolerance. Explicitly manage musculoskeletal risk due to run impact.

### 12-Week (assumes existing base)

| Phase | Weeks | Objectives | Load pattern |
|---|---|---|---|
| Base | 3 | Consolidate running base | 2:1 or 3:1 |
| Build | 5–6 | Marathon-specific work | 2:1 or 3:1 |
| Peak | 1–2 | Final long run + MP blocks | Reduced |
| Taper | 2 | Volume down, intensity maintained | Progressive |

**Key sessions:** Long run with MP segments; threshold tempo; limited VO₂ intervals.

### 20-Week (robust build)

| Phase | Weeks | Objectives | Load pattern |
|---|---|---|---|
| General base | 6–8 | Aerobic + strength foundation | 3:1 |
| Strength + endurance build | 6 | Economy + fatigue resistance | 3:1 |
| Marathon-specific | 4–6 | MP blocks, fueling practice, long runs | 3:1 |
| Taper | 2–3 | Shed fatigue | Progressive |

### 40-Week (full development, multi-peak option)

| Phase | Weeks | Objectives | Load pattern |
|---|---|---|---|
| Transition | 2–4 | Recovery | Low |
| Aerobic base | 12–16 | Big durability, injury prevention | 3:1 + reduced-impact weeks |
| Build | 10–12 | Progressive mileage ramp | 3:1 |
| Marathon-specific | 6–8 | Race simulation | 3:1 |
| Taper | 2–3 | Volume down | Progressive |

---

## Sample Weekly Plans

These are templates — always adapt to athlete constraints, fatigue, time, and injury risk. Intensities assume zones are individualized.

### 70.3 — Mid-Build (12-week cycle)

| Day | Session | Intensity | Log/Ask |
|---|---|---|---|
| Mon | Swim technique + easy (45–60 min) + mobility (10–15 min) | Easy | Shoulder comfort; sleep quality |
| Tue | Bike intervals (60–75 min) + brick run (15–25 min) | High bike; easy run | Power/HR/RPE; brick coordination |
| Wed | Run aerobic (45–70 min) + strength (40–55 min) | Easy–moderate | Strength technique quality |
| Thu | Swim endurance (60–75 min) | Mostly easy | Include steady aerobic pulls |
| Fri | Bike aerobic (75–120 min) | Easy | Fueling practice (carb + fluids) |
| Sat | Long bike (2.5–4 h) with race-pace blocks + brick run (20–40 min) | Moderate | Race fueling; pacing discipline |
| Sun | Long run (75–110 min) easy or steady finish | Easy→moderate | Adjust if fatigue high |

### 70.3 — Late-Base / Early-Build (20-week cycle)

| Day | Session | Intensity | Log/Ask |
|---|---|---|---|
| Mon | Off or recovery swim (30–45 min) + mobility | Very easy | Weekly readiness check-in |
| Tue | Run tempo (e.g., 3×10 min) + strides | Moderate | RPE + niggles |
| Wed | Bike aerobic (75–120 min) + strength | Easy | Posterior chain + calf focus |
| Thu | Swim aerobic intervals (e.g., 10×200) | Moderate | Technique under fatigue |
| Fri | Easy run (40–60 min) | Easy | Sleep + stress monitoring |
| Sat | Long bike 3–5 h + brick 15–25 min | Easy–moderate | Fueling rehearsal; GI feedback |
| Sun | Long run 90–130 min easy + optional short swim | Easy | "Keep it easy" enforcement |

### 70.3 — Aerobic Base (40-week cycle)

| Day | Session | Intensity | Log/Ask |
|---|---|---|---|
| Mon | Swim technique (45–60) + strength (45–60) | Easy | Movement quality |
| Tue | Bike endurance (90–150) | Easy | Aerobic development |
| Wed | Run endurance (50–80) + drills/strides | Easy | Running economy focus |
| Thu | Swim aerobic (60–75) | Easy–moderate | Consistent volume |
| Fri | Bike cadence skills (60–90) + mobility | Easy | Low stress |
| Sat | Long bike (2.5–4) + brick jog (10–20) | Easy | Brick habit, minimal stress |
| Sun | Long run (70–110) | Easy | Strict easy intensity |

### Marathon — Peak-Specific (12-week cycle)

| Day | Session | Intensity | Log/Ask |
|---|---|---|---|
| Mon | Rest or very easy run 30–45 + mobility | Very easy | Soreness check |
| Tue | Threshold/tempo (e.g., 2×20 min) | Moderate | Pacing discipline |
| Wed | Easy run 45–70 + strength (30–45) | Easy | Strength kept modest |
| Thu | MP blocks (e.g., 3×5 km) | Moderate | Fueling timing practice |
| Fri | Easy run 30–50 | Easy | Sleep focus |
| Sat | Long run 28–35 km with MP finish | Easy→moderate | GI + pacing discipline |
| Sun | Recovery run 30–50 or off | Very easy | Injury risk gate |

### Marathon — Mid-Build (20-week cycle)

| Day | Session | Intensity | Log/Ask |
|---|---|---|---|
| Mon | Off or recovery run 30–40 | Very easy | Weekly check-in |
| Tue | VO₂-style intervals (limited dose) | High | Keep constrained to robustness |
| Wed | Easy run 50–80 + strength (45–60) | Easy | Strength supports economy |
| Thu | Tempo / steady (e.g., 40 min steady) | Moderate | Avoid grey zone creep |
| Fri | Easy run 30–60 | Easy | Form drills |
| Sat | Long run 22–30 km easy | Easy | Add fueling practice late |
| Sun | Easy run 45–70 | Easy | Aerobic density |

### Marathon — Aerobic Base (40-week cycle)

| Day | Session | Intensity | Log/Ask |
|---|---|---|---|
| Mon | Easy run 40–60 + mobility | Easy | Consistency priority |
| Tue | Hill sprints (short) + easy volume | Mostly easy | Neuromuscular stimulus |
| Wed | Easy run 50–80 + strength | Easy | Strength base |
| Thu | Aerobic steady (light progression run) | Easy→moderate | Controlled effort |
| Fri | Off or 30–45 easy | Very easy | Sleep focus |
| Sat | Long run 90–150 min easy | Easy | Walk breaks allowed |
| Sun | Easy run 40–70 | Easy | Keep total load manageable |

---

## Deload Week Pattern

All blueprints reference "3:1 load:deload" — here's what a deload week actually looks like:

### Volume & Intensity
- **Volume reduction:** 30–50% from the peak week of the mesocycle (not from the average)
- **Keep one intensity touch:** One shorter key session at race-relevant intensity (e.g., 2×8 min tempo instead of 3×15 min). This preserves neuromuscular adaptations without adding fatigue.
- **Drop one key session:** Replace the second hard session with easy aerobic work
- **Strength:** Reduce to 1×/week at light load (1–2 sets, familiar movements only)
- **Long session:** Shorten by 30–40% — still go long-ish, just shorter

### What It Looks Like in Practice
- Easy sessions stay easy but get shorter
- Total weekly hours drop noticeably — the athlete should feel "too fresh"
- No new stimuli — nothing unfamiliar or exploratory
- Sleep and nutrition become the priority

### Signs the Deload Is Working (expect within 3–5 days)
- HRV stabilizes or rises toward baseline
- Resting HR drops back toward baseline
- Mood and motivation improve
- Soreness resolves
- Athlete feels restless or eager to train hard again

### Signs It's Not Enough
- HRV still suppressed after 5 days
- Fatigue persists into the second half of the week
- Mood remains flat or worsening
- → Consider extending the deload by 2–3 days, or flag for overtraining screening

## Plan Adaptation Decision Rules

Four decision rules evaluated during `/coach:review`. Precedence: **Safety > Adaptation > Progression > Schedule.**

### Insert Deload

Trigger if ANY:
- CTL drop >5 pts without a planned deload
- Adherence <60% for 2 consecutive weeks
- Fatigue HIGH 4+/7 days
- 2+ key sessions failed (RPE way above target, bailed, or couldn't complete)
- HRV 7-day avg >15% below 30-day baseline

### Extend Phase

Trigger if ANY:
- Phase objectives not met (check `current-plan.md` phase goals)
- <2% threshold improvement after a full mesocycle
- Adherence <70% due to illness/injury/life (not motivation — that's simplification)
- >1 week modified due to injury

### Simplify Plan

Trigger if ANY:
- Adherence <50% for 2 consecutive weeks (time or motivation)
- Same session skipped 3+/4 weeks
- Mood OK(3)/GRUMPY(4) >50% of days over 2 weeks

Action: reduce weekly sessions by 1, protect key sessions first, cut the lowest-priority session.

### Advance Early

Trigger if ALL:
- Adherence >90%
- Key sessions hitting targets
- Readiness stable (no fatigue/soreness trending up)
- CTL trending up

Action: advance 1 week early with a transitional week (slightly higher volume than deload, slightly lower than full load).

---

## Session Library ("Recipes")

### Swim: Technique + Aerobic (triathlon)
- **Warm-up:** 300–600 easy + drills (catch, body position)
- **Main:** 8–12×100 @ easy-moderate with 15–20s rest; focus form under light fatigue
- **Cool-down:** 200 easy
- **Progression:** increase main-set volume 5–15% only if technique holds. Ask: "What broke down first?"

### Bike: Threshold Development (FTP-anchored)
- **Warm-up:** 15–20 min easy + 3×1 min fast spin
- **Main:** 3×10–15 min @ upper Z3/Z4, 5 min easy between
- **Cool-down:** 10–15 min easy
- **Note:** FTP/thresholds must be current — stale values distort zones and TSS

### Run: Tempo (marathon / half marathon)
- **Warm-up:** 10–20 min easy + drills + strides
- **Main:** 20–40 min tempo (or 2×20 min) at "comfortably hard" (controlled breathing)
- **Cool-down:** 10–15 min easy
- **Safety:** if pain alters gait → stop, switch to easy walk/bike, log as alert

### Brick Session (70.3 specific)
- **Bike:** 2–3 h with 2×30 min at race pace; fueling practice
- **Transition:** quick change (simulate race)
- **Run:** 20–45 min easy-to-steady (not a race)
- **Purpose:** neuromuscular adaptation + pacing discipline. Ask for GI feedback + perceived coordination.

### Strength Training Templates

#### Phase Periodization

| Training Phase | Strength Phase | Sets × Reps | RPE | Frequency |
|----------------|---------------|-------------|-----|-----------|
| Rebuild | Anatomical Adaptation | 2-3 × 12-15 | 5-6 | 2×/week |
| Base | Hypertrophy / Max Strength | 3-4 × 8-12 or 3-4 × 4-6 | 7-8 | 2×/week |
| Build | Power Endurance | 2-3 × 8-12 circuit | 6-7 | 2→1×/week |
| Peak/Taper | Maintenance | 2 × 6-8 | 6-7 | 1×/week |

#### Exercise Pools

**Upper body:** bench press, T-bar row (no BB/DB rows — athlete preference), OHP, pull-ups, farmers walk, accessories (face pulls, bicep curls, tricep pushdowns)

**Lower body:** squat (back or front), RDL or trap-bar deadlift, split squat/lunges, calf raises, core (pallof press, dead bug, ab wheel), accessories (leg curl, leg extension)

**Athlete-specific notes:** check `coach-memory.md` → Preferences & Style for equipment availability and exercise substitutions. When in doubt, default to the simplest compound movement.

#### Sample Sessions by Phase

**Anatomical Adaptation (Rebuild):**
- Warmup: 10 min mobility + activation
- Goblet squat 2×15, RDL 2×15, Split squat 2×12 each
- Bench press 2×15, T-bar row 2×15
- Calf raises 2×15, Pallof press 2×12 each
- Cooldown: 5 min stretching

**Max Strength (Base):**
- Warmup: 10 min mobility + activation
- Back squat 4×6, RDL 3×8
- Bench press 3×8, Pull-ups 3×8
- Calf raises 3×15, Farmers walk 3×30m
- Ab wheel 3×10
- Cooldown: 5 min stretching

**Power Endurance (Build):**
- Warmup: 10 min mobility + activation
- Circuit (2-3 rounds, minimal rest between exercises):
  Trap-bar deadlift ×10, Split squat ×10 each, Push-ups ×12
  T-bar row ×10, Calf raises ×15, Pallof press ×10 each
- Cooldown: 5 min stretching

**Maintenance (Peak/Taper):**
- Warmup: 10 min mobility + activation
- Back squat 2×6, RDL 2×6
- Bench press 2×8, T-bar row 2×8
- Calf raises 2×12
- Cooldown: 5 min stretching

#### Scheduling Rules
- No strength + key endurance session on the same day
- 48h between sessions targeting the same muscle groups
- Place strength on easy-endurance days or rest days
- Reduce strength volume/intensity the day before a key session

#### ICU Format
- **Type:** `WeightTraining`
- **Description:** plain text (no ICU step syntax — see note in Intervals.icu section)
- **moving_time:** calculate from exercise list (warmup + exercises × 3 min + cooldown) × 60
- **icu_training_load:** use the Strength Load Estimation table

---

## Intervals.icu Structured Workout Descriptions

ICU syntax templates for each session type. Use these as starting points when generating the `description` field for calendar events (see `.claude/services/coach/intervals-icu.md` Section 7–8). Adapt durations, intensities, and repeats to the athlete's current phase, fitness, and zones.

### Swim: Technique + Aerobic

**name:** `Swim: Technique + Aerobic`
**type:** `Swim`
**moving_time:** `3600` (60 min)

```
Warmup
- 300mtr Z1
- 4x 50mtr drills intensity=rest

Main set
8x
- 100mtr Z2
- 20s intensity=rest

Cooldown
- 200mtr Z1
```

### Bike: Threshold Development

**name:** `Bike: Threshold`
**type:** `Ride`
**moving_time:** `4500` (75 min)

```
Warmup
- 15m Z2
- 3x 1m 95rpm Z2
Cooldown after warmup spins

Main set
3x
- 12m 95% 90rpm
- 5m Z1

Cooldown
- 10m Z1
```

### Run: Tempo

**name:** `Run: Tempo`
**type:** `Run`
**moving_time:** `3600` (60 min)

```
Warmup
- 15m Z1 Pace
- 4x 20s strides 95% Pace

Main set
2x
- 15m 85% Pace
- 3m Z1 Pace

Cooldown
- 10m Z1 Pace
```

### Brick: Bike (separate Ride event)

**name:** `Brick Bike: Race-Pace Blocks`
**type:** `Ride`
**moving_time:** `10800` (3 h)

```
Warmup
- 20m Z2

Main set
- 30m 85%
- 10m Z2
- 30m 85%
- 10m Z2
- 60m Z2

Cooldown
- 20m Z1
```

### Brick: Run (separate Run event)

**name:** `Brick Run: Easy-to-Steady`
**type:** `Run`
**moving_time:** `1800` (30 min)

```
Warmup
- 5m Z1 Pace

Main set
- 15m Z2 Pace

Cooldown
- 10m Z1 Pace
```

### Strength: Phase-Specific Templates

Note: Strength descriptions must NOT use ICU step syntax (`- Xm`, `- 5m`, etc.) because the parser treats them as timed steps and overrides `moving_time` with the sum of parsed durations instead of the intended total. Use plain text without `- ` dash prefixes, and write `min` instead of `m` for durations.

**Anatomical Adaptation** (Rebuild phase)
**name:** `Strength: Anatomical Adaptation`
**type:** `WeightTraining`
**moving_time:** `2700` (45 min) | **icu_training_load:** `25`

```
Warmup
10 min mobility + activation

Main set
Goblet squat 2x15
RDL 2x15
Split squat 2x12 each
Bench press 2x15
T-bar row 2x15
Calf raises 2x15
Pallof press 2x12 each

Cooldown
5 min stretching
```

**Max Strength** (Base phase)
**name:** `Strength: Max Strength`
**type:** `WeightTraining`
**moving_time:** `3000` (50 min) | **icu_training_load:** `40`

```
Warmup
10 min mobility + activation

Main set
Back squat 4x6
RDL 3x8
Bench press 3x8
Pull-ups 3x8
Calf raises 3x15
Farmers walk 3x30m
Ab wheel 3x10

Cooldown
5 min stretching
```

**Power Endurance** (Build phase)
**name:** `Strength: Power Endurance`
**type:** `WeightTraining`
**moving_time:** `2400` (40 min) | **icu_training_load:** `30`

```
Warmup
10 min mobility + activation

Main set (circuit, 2-3 rounds)
Trap-bar deadlift x10
Split squat x10 each
Push-ups x12
T-bar row x10
Calf raises x15
Pallof press x10 each

Cooldown
5 min stretching
```

**Maintenance** (Peak/Taper phase)
**name:** `Strength: Maintenance`
**type:** `WeightTraining`
**moving_time:** `1800` (30 min) | **icu_training_load:** `15`

```
Warmup
10 min mobility + activation

Main set
Back squat 2x6
RDL 2x6
Bench press 2x8
T-bar row 2x8
Calf raises 2x12

Cooldown
5 min stretching
```

---

## Travel & Disruption Protocol

When the athlete has travel periods, vacations, or life disruptions that interrupt normal training:

### Pre-travel (week before departure)

- **Front-load key sessions** earlier in the week before travel begins
- Complete any threshold or key workout at least 2 days before departure
- Last session before travel: easy, short, confidence-building
- No new stimuli — nothing unfamiliar that could cause soreness during travel

### During travel

- **Minimum viable movement:** 20–30 min easy activity (walk, jog, bodyweight) to maintain habit and mobility
- **Opportunistic training:** use what's available — hotel gym, running from accommodation, open-water swimming if at the coast. No rigid schedule.
- **Respect the vacation:** if the athlete values relationship time or exploration over training (check Preferences & Style in memory), keep suggestions minimal. A 30-min morning jog before the day starts is the sweet spot.
- **What counts:** hiking, walking tours, swimming, cycling tours — log as cross-training. It's not nothing.
- **What doesn't count toward plan:** don't try to hit prescribed intervals or key sessions. Travel training is maintenance, not progression.

### Post-travel (return)

- **Days 1–2:** Easy movement only — walk, light jog, swim. Reestablish routine.
- **Day 3:** First normal easy session. Assess: how does the body feel?
- **Days 4–5:** Resume normal training load if readiness is good. If jetlagged, fatigued, or ill → extend easy days.
- **No catch-up:** missed training is gone. Resume the plan from where the calendar says, not from where you left off. Adjust the week's total load downward if needed.

### Time zone changes (>3 hours)

- Shift training time by ~1 hour per day toward the destination schedule
- First 2–3 days in new zone: easy sessions only, prioritize sleep adaptation
- Expect HRV disruption for 2–5 days — don't react to it with training changes
- Melatonin timing and light exposure matter more than training for jet lag recovery

---

## Heat Acclimation Protocol

For warm-weather races (e.g., IRONMAN 70.3 Greece in late October — Mediterranean climate).

### When to start

- **6–8 weeks before race day** for full acclimation
- **Minimum 10–14 days** for meaningful partial acclimation
- Benefits: lower core temperature, earlier sweating onset, expanded plasma volume, reduced HR at given intensity

### Protocol options (choose based on availability)

1. **Passive heat exposure (sauna):** 20–30 min post-training sauna, 3–4×/week for 3–4 weeks. Start at 15 min, build gradually. Hydrate before and after.
2. **Overdressing for easy sessions:** Extra layers during easy runs/rides in cool weather. Only on easy sessions — never during key workouts.
3. **Hot bath protocol:** 30–40 min hot bath (40°C) post-training. Similar effect to sauna.

### Integration with training load

- Heat exposure adds physiological stress — treat it as training load
- Never combine heat protocol with key sessions or hard days
- Reduce easy session intensity slightly when adding heat exposure
- If fatigue scores rise, reduce heat exposure frequency before reducing training
- Stop heat protocol 5–7 days before race day (acclimation is retained for ~2 weeks)

### Race-day heat strategy seeds

Track and refine during build/peak phase:
- **Pre-cooling:** ice slurry or cold towel before start
- **Hydration plan:** sodium loading 24h before; electrolyte-heavy during race; aim for individualized fluid intake (not "drink as much as possible")
- **Pacing adjustment:** if race-day temp >28°C, plan for 3–5% slower pace targets
- **Cooling opportunities:** ice in cap/suit at aid stations, cold sponges, water dousing
- **Warning signs:** stop if: confusion, stopping sweating, severe headache, nausea + dizziness (heat illness — see alerts.md)

## Race Nutrition Development Protocol

Progressive fueling practice integrated into the training plan across three phases.

### Phase 1 — Foundation (Base)
- **Target:** 30-40g carbs/h
- **Products:** familiar, easily tolerated (whatever the athlete already uses)
- **Focus:** establish the habit of eating during training. Practice the mechanics — opening gels, drinking from bottles on the bike, eating while running.
- **Sessions:** every long session >75 min

### Phase 2 — Race Candidate Testing (Build)
- **Target:** 50-60g carbs/h
- **Products:** race-candidate products (what will be available on course, or athlete's preferred race fuel)
- **Timing:** every 20-25 min
- **Focus:** test specific products, practice race timing, note GI response
- **Sessions:** long rides, bricks, long runs >75 min

### Phase 3 — Race Rehearsal (Peak, 4-6 weeks pre-race)
- **Target:** 60-90g carbs/h at race rate
- **Products:** only race-day products (nothing new)
- **Focus:** full rehearsal including pre-race meal timing, exact products, exact intervals
- **Sessions:** race simulations, key long sessions

### Integration with `/coach:plan`

Mark fueling-eligible sessions with `[FUEL]` tag in the session name (sessions >75 min, bricks, race simulations). When generating the plan, reference the current nutrition phase and include fueling instructions:
- Check `coach-memory.md` → Race Rehearsal Log for tested products and GI outcomes
- Include specific fueling targets (g/h) in session notes
- Note which products to use

### Race-Day Nutrition Plan Template

Built from rehearsal data in `coach-memory.md` → Race Rehearsal Log during `/coach:raceweek`:

```
Pre-race: [meal], [timing before start]
Swim: nothing (triathlon)
Bike: [product] every [X min], targeting [X]g/h. [hydration plan]
Run: [product] every [X min], targeting [X]g/h. [hydration plan]
Backup: [alternative if GI issues arise]
```

**Warning:** if <3 fueling log entries in Race Rehearsal Log by race week → warn athlete "Limited fueling data — going conservative with targets."

---

**Duration estimation:** Calculate `moving_time` from the exercise list rather than using a fixed value:
- Warmup: use stated duration (e.g., 10 min)
- Per exercise: ~3 min (accounts for set execution + rest between sets; roughly 1 min/set × 3 sets)
- Cooldown: use stated duration (e.g., 5 min)
- `moving_time` = (warmup min + exercises × 3 + cooldown min) × 60

Example: 10 min warmup + 7 exercises × 3 min + 5 min cooldown = 36 min → `moving_time: 2160`

### Strength Load Estimation

Strength workouts don't produce power/HR-based training load via the API. Use this heuristic to estimate load per session:

| Phase | Intensity | Sets × Reps profile | Estimated load |
|-------|-----------|---------------------|----------------|
| Anatomical Adaptation | Light–moderate | 2–3 sets × 12–15 reps | 20–30 |
| Maximum Strength | Heavy | 3–4 sets × 6–10 reps | 35–50 |
| Power Endurance | Explosive | 2–3 sets × sport-specific | 25–40 |
| Maintenance | Light | 1–2 sets × activation | 10–20 |

Include the estimated load in the ICU event payload as `"icu_training_load": 25` when creating the calendar event (Section 7 of `.claude/services/coach/intervals-icu.md`).

### Long Run: Easy

**name:** `Long Run: Easy`
**type:** `Run`
**moving_time:** `5400` (90 min)

```
Warmup
- 10m Z1 Pace

Main set
- 70m Z1-Z2 Pace

Cooldown
- 10m Z1 Pace
```

### Long Bike: Aerobic + Race-Pace Blocks

**name:** `Long Bike: Aerobic + RP Blocks`
**type:** `Ride`
**moving_time:** `12600` (3.5 h)

```
Warmup
- 20m Z2

Main set
- 40m Z2
- 20m 85%
- 10m Z2
- 20m 85%
- 40m Z2

Cooldown
- 20m Z1
```
