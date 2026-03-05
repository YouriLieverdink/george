# Coach Memory

<!--
  Accumulated coaching intelligence. Every command reads this file for context.
  Updated by: checkin (patterns, injury), debrief (learnings, injury), review (maintenance, pruning),
  chat (significant mentions), onboard (initial seed).

  Pruning: review.md archives entries older than 12 weeks that haven't been reobserved
  to data/memory/archive/YYYY-MM.md
-->

## Athlete Patterns & Tendencies

<!--
  Schema: - **Pattern name** (YYYY-MM-DD first observed): description + evidence
  When to add: Pattern confirmed across ≥2 sessions or explicitly reported by athlete
  When to update: New evidence reinforces or contradicts the pattern — update date + evidence
  Retention: Archive entries older than 12 weeks that haven't been reobserved (review.md handles this)
-->

- **Sleep & social evenings** (2026-03-01, updated 2026-03-02): Consistently gets <8h sleep. Late social evenings (often past midnight) with early work mornings — key recovery limiter. Committed to fixed 7:00 wake-up daily + in bed by 23:00 on 5+ nights/week. Recognizes some late nights are habit rather than quality social time. Wants to become a morning person again.
- **Caffeine** (2026-03-01, updated 2026-03-05): Heavy user (~8 cups/day, lifelong habit). Late caffeine cutoff likely compounds sleep issues. Process goal: moderate over time. **2026-03-04:** Caffeine back after illness pause. Cutoff ~19:00 — same night sleep dropped from 7.8h/86 to 6.7h/78 with AVG quality. **2026-03-05:** Cutoff 14:00 — sleep bounced back to 8.35h/91/GOOD. Two data points now: 19:00 cutoff → poor sleep, 14:00 cutoff → good sleep. Pattern strengthening.

## Injury & Health History

<!--
  Schema: - **YYYY-MM-DD — Description:** context, severity, resolution status
  When to add: Any injury ≥ NIGGLE(2), illness affecting training, or alert trigger
  When to update: Status changes (worsening, improving, resolved) — append update with date
  Retention: Permanent — entries are compact and date-stamped
-->

- **2025-07 — Left knee pain:** Overload during Amsterdam–Paris cycling tour (~500 km). Insufficient preparation. Resolved on its own. No recurrence reported.
- **2026-02-27/28 — GI illness (Egypt travel):** Acute onset vomiting + diarrhea on last day in Egypt. Shifted to nausea + stomach pain after eating + constipation. Unable to eat real meals for ~4 days. Fluids OK. Week 1 training fully paused. **2026-03-03 doctor visit:** No fever, no blood in stool — nothing acute. Doctor says wait it out, stay hydrated, eat small amounts. Full resolution may take ~6 weeks. No medication prescribed. **2026-03-03:** Athlete reports stomach "getting a lot better" but still not eating full meals — made pasta but froze it instead of eating it. Trending toward recovery but not there yet. Resume movement once eating normally without pain for 2+ days. **2026-03-04:** Still symptomatic — painful stomach this morning (eased but not resolved). Day 5 since onset. Not eating full meals. Return criteria still not met. Coach recommended skipping swim — athlete chose to attend (Lesson 3) due to financial commitment. Given safety guidelines: stay easy, exit if symptoms worsen, tell instructor. **2026-03-04 post-swim:** Diarrhea after breakfast (change from constipation pattern of recent days). GI noticeable during swim but manageable — did not have to stop. This is a fluctuation in recovery, not a new acute episode. Continue monitoring. Return criteria still not met for unrestricted training. **2026-03-05:** Significant improvement — ate full carbonara dinner without pain, no diarrhea. Return criteria approaching met. Cleared for first easy run (30 min). Caffeine cutoff improved to 14:00. Sleep excellent (8h21m, score 91).

## Open Follow-ups

<!--
  Schema: - **YYYY-MM-DD:** What to follow up on — specific question or check
  When to add: Coach commits to checking on something (injury, doctor visit, commitment, concern)
  When to update: Remove when resolved; update if context changes
  Retention: Active items only — remove once resolved
-->

- **2026-03-05:** GI return-to-training: first easy run today (30 min). Monitor for any GI symptoms during or after running. Follow up in debrief: (1) any gut discomfort during the run? (2) how did energy/legs feel on first run back?

## Key Learnings

<!--
  Schema: - **YYYY-MM-DD — Topic:** insight from athlete or coach observation
  When to add: Debrief "what did you learn?" contains a preservable insight, or race/review reveals something new
  When to update: If a learning is reinforced or revised — append date + update
  Retention: Permanent unless superseded
-->

<!-- No entries yet — will populate from debrief sessions. -->

## Preferences & Style

<!--
  Schema: - Description of preference or style observation
  When to add: Coach observes what motivates the athlete, what communication style works, or athlete explicitly states a preference
  When to update: If preference changes or new evidence emerges
  Retention: Permanent unless athlete preference changes
-->

- **Full Ironman ambition** (2026-03-03): Interested in a full Ironman in late 2027. No specific race yet. Revisit after 70.3 Greece (Oct 2026) — use that race experience to decide if/when to commit. Prerequisites: power meter for bike pacing, sustained training consistency through 2026–2027 winter base.
- Responds well to collaborative, low-pressure coaching style
- Identity-driven motivation: "I show up for myself consistently — training is my time to invest in me"
- Enjoys the process — A-race goal is to "finish and enjoy every moment"
- Values relationship time — explicitly doesn't want training to take away from time with girlfriend on trips. Prefers minimal, opportunistic training during vacations.
- Prefers flexible training timing over rigid schedule — morning when sleep was good, evening when it wasn't
- **Paid commitments override caution** (2026-03-04): Will push through illness/discomfort for sessions with financial commitment (swim course). Respect this but ensure safety guardrails are clear when it happens.
- **Strength & body composition goal** (2026-03-03): Wants to rebuild muscle mass — had more muscle from previous strength training and misses it. Also interested in visible abs / better body composition. Enjoys lifting. Agreed to hypertrophy-focused upper/lower split 2x/week. Has access to a local gym (full equipment: barbells, dumbbells, cables).

## Intervals.icu

<!--
  Persistent API integration state. Updated by /coach:plan when folder is first created.
  Retention: Permanent — only recreate folder_id if the folder is deleted from intervals.icu.
-->

- Workout library folder: "George's Plan" (folder_id: _pending first /coach:plan run_)

## Race Rehearsal Log

<!--
  Schema: Track what's been tested and decided for race day — nutrition, kit, transitions.
  When to add: Debrief after long sessions (>75 min) with fueling practice, race simulation days,
  or chat when athlete reports a gear/nutrition decision.
  When to update: New test supersedes or confirms previous — update outcome.
  Retention: Permanent per race cycle — archive after race is complete.
-->

### Nutrition Products Tested

| Date | Product | Context | GI Outcome | Notes |
|------|---------|---------|------------|-------|
| — | — | — | — | No fueling sessions yet — will populate as sessions >75 min begin |

### Kit Decisions

<!-- Gear that's been tested or decided for race day. Update as decisions are made. -->

- No kit decisions yet — will populate during build/peak phase.

### Transition Practice

<!-- Track T1/T2 rehearsals for triathlon. -->

- No transition practice yet — begins with brick sessions in 70.3 build phase.

### Open Water Swimming

<!-- Track OW swim sessions — comfort level, sighting, wetsuit use. -->

- 2026-02 (Hurghada): 8 OW sessions, ~2.7 km total. First meaningful OW experience. Comfort level: growing.

## Swim Development

<!--
  Schema: Track swim-specific skill progression through structured lessons and beyond.
  When to add: Debrief after swim course sessions, or when technique cues/test results emerge.
  When to update: New lesson content, technique breakthroughs, or test results.
  Retention: Permanent — compact and valuable for long-term development.
-->

### Lesson Progress (Bosch Control Method)

| Date | Lesson # | Content / Skills | Key Cues | Notes |
|------|----------|-----------------|----------|-------|
| — | 1–2 | Completed before coaching started | — | No details available |
| 2026-03-04 | 3 | Correct arm use, breathing technique | — | 1425m, 59 min pool (28 active). Avg HR 135, max 195. RPE 4/10. GI illness active but manageable during session. First session back after 5-day pause. |

### Technique Cues That Work

<!-- Cues the athlete responds to — use in session descriptions and reminders. -->

- **Trouble swimming slowly** (2026-03-04): Feels like sinking at low effort, so defaults to swimming fast during exercises. This drives HR spikes (195 max on a 4/10 RPE session). As technique and body position improve, slow swimming should become possible. Until then, expect spiky swim HR — don't alarm on it.

### CSS Test Results

| Date | 400m Time | 200m Time | CSS Pace | Notes |
|------|-----------|-----------|----------|-------|
| — | — | — | — | To be tested after swim course progresses (est. April/May) |

### Open Water Readiness

- [ ] Comfortable with continuous 750m+ in pool
- [ ] Sighting technique practiced
- [ ] Bilateral breathing or reliable one-side breathing
- [ ] Wetsuit swimming practiced (if applicable)
- [ ] Mass start / drafting comfort
- [ ] OW navigation (buoy turns)

## Fitness Test History

<!--
  Schema: | Date | Discipline | Protocol | Result | Conditions | Notes |
  When to add: Any threshold test, time trial, or race result used as a fitness marker
  When to update: New test supersedes old — keep both rows for trend tracking
  Retention: Permanent
-->

| Date | Discipline | Protocol | Result | Conditions | Notes |
|------|-----------|----------|--------|------------|-------|
| — | Cycling | — | FTP unknown | — | No power meter available |
| — | Swimming | — | CSS unknown | — | To be tested after swim course progresses |
| 2025-04 | Running | Marathon | ~4:12 finish | First marathon | ~5:58/km avg; not a threshold test but useful baseline |

## Current Zones

<!--
  Schema: Zone tables per discipline (running, cycling, swimming) with pace/power/HR ranges + RPE anchors
  When to add: After any threshold test or zone recalculation
  When to update: When a new test produces updated thresholds — replace the table, note the date
  Retention: Permanent — always reflects current zones
-->

### Running

No formal zone test yet. Using estimated zones from marathon performance (~4:12):

| Zone | Name | Pace (min/km) | HR estimate | RPE |
|------|------|--------------|-------------|-----|
| Z1 | Recovery | >7:00 | <130 | 1–2 |
| Z2 | Easy aerobic | 6:15–7:00 | 130–145 | 2–4 |
| Z3 | Tempo | 5:40–6:15 | 145–160 | 5–6 |
| Z4 | Threshold | 5:15–5:40 | 160–172 | 7–8 |
| Z5 | VO2max | <5:15 | 172+ | 9–10 |

*Estimated — needs calibration via 5k/10k time trial when base fitness rebuilt.*

### Cycling

No power meter. Using HR-based zones only (estimated):

| Zone | Name | HR estimate | RPE |
|------|------|-------------|-----|
| Z1 | Recovery | <120 | 1–2 |
| Z2 | Endurance | 120–140 | 2–4 |
| Z3 | Tempo | 140–155 | 5–6 |
| Z4 | Threshold | 155–168 | 7–8 |
| Z5 | VO2max | 168+ | 9–10 |

*Very rough estimates — no FTP test available. Revisit when cycling volume increases (post-marathon, ~June).*

### Swimming

No CSS test yet. Using RPE + stroke count only until swim course progresses.

*Schedule CSS test (400m + 200m TT) once comfortable with 400m continuous — likely April/May.*
