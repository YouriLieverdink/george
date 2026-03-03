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
- **Caffeine** (2026-03-01): Heavy user (~8 cups/day, lifelong habit). Late caffeine cutoff likely compounds sleep issues. Process goal: moderate over time.

## Injury & Health History

<!--
  Schema: - **YYYY-MM-DD — Description:** context, severity, resolution status
  When to add: Any injury ≥ NIGGLE(2), illness affecting training, or alert trigger
  When to update: Status changes (worsening, improving, resolved) — append update with date
  Retention: Permanent — entries are compact and date-stamped
-->

- **2025-07 — Left knee pain:** Overload during Amsterdam–Paris cycling tour (~500 km). Insufficient preparation. Resolved on its own. No recurrence reported.
- **2026-02-27/28 — GI illness (Egypt travel):** Acute onset vomiting + diarrhea on last day in Egypt. Shifted to nausea + stomach pain after eating + constipation. Unable to eat real meals for ~4 days. Fluids OK. Week 1 training fully paused. **2026-03-03 doctor visit:** No fever, no blood in stool — nothing acute. Doctor says wait it out, stay hydrated, eat small amounts. Full resolution may take ~6 weeks. No medication prescribed.

## Open Follow-ups

<!--
  Schema: - **YYYY-MM-DD:** What to follow up on — specific question or check
  When to add: Coach commits to checking on something (injury, doctor visit, commitment, concern)
  When to update: Remove when resolved; update if context changes
  Retention: Active items only — remove once resolved
-->

- **2026-03-03:** Doctor visit done — no acute findings. Monitor return to eating and energy. Follow up on readiness to resume easy movement (walk first, then run) once eating small meals without pain for 2+ days.

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

- Responds well to collaborative, low-pressure coaching style
- Identity-driven motivation: "I show up for myself consistently — training is my time to invest in me"
- Enjoys the process — A-race goal is to "finish and enjoy every moment"
- Values relationship time — explicitly doesn't want training to take away from time with girlfriend on trips. Prefers minimal, opportunistic training during vacations.
- Prefers flexible training timing over rigid schedule — morning when sleep was good, evening when it wasn't

## Intervals.icu

<!--
  Persistent API integration state. Updated by /coach:plan when folder is first created.
  Retention: Permanent — only recreate folder_id if the folder is deleted from intervals.icu.
-->

- Workout library folder: "George's Plan" (folder_id: _pending first /coach:plan run_)

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
