# Intervals.icu API Service

API integration for pulling training data, wellness metrics, and fitness trends from intervals.icu. Used by the coach agent to replace manual data entry with real data.

## Authentication

Handled automatically by the `./scripts/icu` CLI wrapper. Credentials stored in `config/intervals-icu.json`:

```json
{
  "athleteId": "i12345",
  "apiKey": "your-api-key-here",
  "baseUrl": "https://intervals.icu/api/v1"
}
```

**Setup:** Go to https://intervals.icu/settings → scroll to "Developer Settings" → generate API key. Your athlete ID is shown in the URL when you're on your profile (e.g., `i12345`).

## CLI Invocation

All API calls go through `./scripts/icu`. It reads config automatically, formats output for readability, and prints errors to stderr.

```bash
# Any subcommand supports --json for raw JSON output
./scripts/icu <resource> <action> [--flags]
./scripts/icu <resource> <action> --json   # raw JSON
```

## Available Endpoints

### 1. Recent Activities (completed workouts)

**Use in:** `/coach:debrief` (auto-fill session data), `/coach:review` (weekly volume/load)

```bash
./scripts/icu activities list --oldest YYYY-MM-DD --newest YYYY-MM-DD
```

Output: one line per activity with date, type, name, duration, distance, HR, load, power.

**Key fields (available via `--json`):**
- `id` — activity ID (use for detail queries)
- `start_date_local` — when it happened
- `type` — Run, Ride, Swim, WeightTraining, etc.
- `moving_time`, `elapsed_time` — duration in seconds
- `distance` — meters
- `average_heartrate`, `max_heartrate`
- `average_speed` — m/s
- `icu_training_load` — intervals.icu's computed training load (similar to TSS)
- `icu_intensity` — intensity factor
- `icu_average_watts`, `icu_weighted_avg_watts` — power (cycling)
- `average_cadence`
- `suffer_score` — relative effort
- `name` — activity title
- `description` — athlete notes

### 2. Activity Details (single workout deep dive)

**Use in:** `/coach:debrief` (detailed interval analysis)

```bash
./scripts/icu activities get --id <activityId>
```

Output: multi-line detail with duration, distance, HR, pace, power, intervals, and zone times.

**Additional useful fields (via `--json`):**
- `icu_intervals` — detected intervals with avg HR, power, pace per interval
- `icu_zone_times` — time spent in each HR/power zone
- `pace` — formatted pace string
- `gap` — grade-adjusted pace (for hilly runs)

### 3. Wellness Data (readiness metrics)

**Use in:** `/coach:checkin` (auto-populate Garmin-synced fields + write subjective scores), `/coach:review` (trends)

```bash
./scripts/icu wellness get --oldest YYYY-MM-DD --newest YYYY-MM-DD
```

Output: one line per day with sleep, HRV, rHR, weight, SpO2, steps, and subjective scores.

**Key fields returned per day:**

Auto-synced from Garmin (numeric — don't ask the athlete for these):
- `id` — date (YYYY-MM-DD)
- `weight` — body weight (kg)
- `bodyFat` — body fat %
- `restingHR` — resting heart rate
- `sleep` — sleep duration (hours, decimal)
- `sleepScore` — Garmin sleep score
- `sleepQuality` — subjective sleep quality (1–4: GREAT/GOOD/AVG/POOR) — auto from Garmin
- `hrv` — HRV rMSSD
- `vo2Max` — VO2 max estimate
- `spO2` — blood oxygen saturation
- `steps` — daily steps
- `kcalConsumed` — daily kCal

Subjective fields (athlete fills in, coach writes via PUT — 1–4 scale, 1=best, 4=worst):
- `soreness` — LOW(1) / AVG(2) / HIGH(3) / EXTREME(4)
- `fatigue` — LOW(1) / AVG(2) / HIGH(3) / EXTREME(4)
- `stress` — LOW(1) / AVG(2) / HIGH(3) / EXTREME(4)
- `mood` — GREAT(1) / GOOD(2) / OK(3) / GRUMPY(4)
- `motivation` — EXTREME(1) / HIGH(2) / AVG(3) / LOW(4)
- `injury` — NONE(1) / NIGGLE(2) / POOR(3) / INJURED(4)
- `hydration` — GOOD(1) / OK(2) / POOR(3) / BAD(4)

### 4. Write Wellness Data (push subjective scores)

**Use in:** `/coach:checkin` (write readiness scores to intervals.icu)

```bash
./scripts/icu wellness put --date YYYY-MM-DD --data '{"soreness": 2, "fatigue": 3, "stress": 2, "mood": 2, "motivation": 2, "injury": 1, "hydration": 1}'
```

### 5. Fitness / Fatigue Trends (CTL/ATL/TSB)

**Use in:** `/coach:review` (training load trends), `/coach:plan` (load targets)

```bash
./scripts/icu athlete get
```

Output: current CTL (fitness), ATL (fatigue), TSB (form).

### 6. Calendar Events (planned workouts, notes, sickness)

**Use in:** `/coach:checkin` (read today's planned session), `/coach:debrief` (compare plan vs actual), `/coach:plan` (sync planned workouts), `/coach:review` (week's planned vs actual), `/coach:status` (today's session)

**Reading the schedule (single source of truth for all planned sessions):**

```bash
./scripts/icu events list --oldest YYYY-MM-DD --newest YYYY-MM-DD
```

Output: one line per event with date, weekday, category, name, type, duration.

Every command that needs to know "what's planned today/this week" reads from this endpoint — NOT from `current-plan.md`. The calendar is the single source of truth for the session schedule.

**Event categories:**

| Category | Purpose | Example |
|----------|---------|---------|
| `WORKOUT` | Planned training session | Tempo run, swim technique, strength |
| `NOTE` | Coaching notes — session modifications, week rationale, key session notes | "Session modified: easy run → rest (GI illness)" |
| `SICKNESS` | Illness period marker | "GI illness — unable to train" |

**Creating events (NOTE, SICKNESS, WORKOUT):**

```bash
# Note on a specific date
./scripts/icu events create --data '{"start_date_local":"2026-03-02","category":"NOTE","name":"Session modified","description":"Easy run cancelled — GI illness"}'

# Sickness marker
./scripts/icu events create --data '{"start_date_local":"2026-03-02","category":"SICKNESS","name":"GI illness","description":"Acute onset vomiting + diarrhea"}'

# Week rationale NOTE (posted on Monday by /coach:plan)
./scripts/icu events create --data '{"start_date_local":"2026-03-09","category":"NOTE","name":"Week 2 — Rebuild","description":"Rationale: ...\n\nKey sessions:\n1. ...\n2. ..."}'
```

### 7. Create Calendar Events (structured workouts)

**Use in:** `/coach:plan` (push structured workouts to intervals.icu calendar → Garmin sync)

```bash
./scripts/icu events create --data '{"start_date_local":"2026-03-02","category":"WORKOUT","name":"Tempo Run","type":"Run","description":"Warmup\n- 15m Z1 HR\nMain set\n3x\n- 10m 85% Pace\n- 3m Z1 HR\nCooldown\n- 10m Z1 HR","moving_time":3600}'
```

**Payload fields:**

| Field | Type | Description |
|-------|------|-------------|
| `start_date_local` | string | Date in `YYYY-MM-DD` format |
| `category` | string | Always `"WORKOUT"` for planned workouts |
| `name` | string | Session title shown on calendar |
| `type` | string | Sport type (see mapping below) |
| `description` | string | Workout steps in ICU syntax (see Section 11) |
| `moving_time` | integer | Planned duration in seconds |
| `icu_training_load` | integer | Estimated training load (optional — use for strength sessions where load isn't auto-calculated from HR/power) |

**Sport type mapping:**

| Session type | `type` value |
|-------------|-------------|
| Swim | `Swim` |
| Bike | `Ride` |
| Run | `Run` |
| Strength | `WeightTraining` |
| Brick (bike + run) | Split into two separate events: one `Ride`, one `Run` |

**Update an existing event:**

```bash
./scripts/icu events update --id <eventId> --data '{"name":"Updated Session","description":"...","moving_time":3000}'
```

**Delete an event:**

```bash
./scripts/icu events delete --id <eventId>
```

The API returns the created/updated event with its `id`. Mid-week adjustments query events by date range to find the event to update — no need to store IDs locally.

### 8. Create Workout Library Folder

**Use in:** `/coach:plan` (one-time setup — create a persistent folder for coach-generated workouts)

```bash
./scripts/icu folders create --name "George's Plan"
```

Returns the created folder with its `id`. Store this `folder_id` in `data/memory/coach-memory.md` — it persists across weeks and plan cycles. Only recreate if the folder is deleted.

### 9. Manage Workouts in a Folder

**Use in:** `/coach:plan` (clear old workouts, add new week's workouts to the library folder)

**List workouts in a folder:**

```bash
./scripts/icu workouts list --folder-id <folderId>
```

Returns one line per workout with day, id, name, type, duration. Use the `id` from each to delete old workouts before adding new ones.

**Create a workout in a folder:**

```bash
./scripts/icu workouts create --data '{"folder_id": 123, "name": "Tempo Run", "day": 2, "description": "Warmup\n- 15m Z1 HR\nMain set\n3x\n- 10m 85% Pace\n- 3m Z1 HR\nCooldown\n- 10m Z1 HR", "type": "Run", "moving_time": 3600}'
```

**Workout payload fields:**

| Field | Type | Description |
|-------|------|-------------|
| `folder_id` | integer | ID of the library folder (from Section 8) |
| `name` | string | Session title |
| `day` | integer | Day within the plan week: 1=Monday, 2=Tuesday, ..., 7=Sunday |
| `description` | string | ICU workout syntax (see Section 11) |
| `type` | string | Sport type (`Run`, `Ride`, `Swim`, `WeightTraining`) |
| `moving_time` | integer | Planned duration in seconds |
| `icu_training_load` | integer | Estimated training load (use for strength sessions where load isn't auto-calculated) |

**Brick sessions:** Create two separate workouts on the same `day` value (one `Ride`, one `Run`).
**Strength:** Use plain text description + `icu_training_load`.
**Rest days:** Skip — do not create workouts.

**Delete a workout from a folder:**

```bash
./scripts/icu workouts delete --id <workoutId>
```

### 10. Apply Plan to Calendar

**Use in:** `/coach:plan` (apply the folder's workouts to the calendar as events, triggering Garmin sync)

```bash
./scripts/icu events apply-plan --folder-id <folderId> --start-date YYYY-MM-DD
```

- `folder-id`: the library folder ID
- `start-date`: Monday of the target week

Returns a confirmation with the number of workouts applied and date range. Mid-week adjustments query events by date range (Section 6) to find specific events — no need to store IDs locally.

### 11. Workout Description Syntax

The `description` field in calendar events uses ICU workout syntax. When parsed correctly, these become structured workouts with targets that sync to Garmin watches.

**Structure:** Section headers on their own line, steps prefixed with `-`

```
Warmup
- 10m 60% Pace

Main set
3x
- 5m 90% Pace
- 2m Z1 Pace

Cooldown
- 10m 60% Pace
```

**Duration formats:**

| Format | Meaning | Example |
|--------|---------|---------|
| `30s` | Seconds | `- 30s 90rpm` |
| `5m` | Minutes | `- 5m Z2` |
| `1m30` | Minutes + seconds | `- 1m30 95%` |
| `400m` | Meters (distance) | `- 400m Z4` |
| `1km` | Kilometers | `- 1km 85% Pace` |
| `50mtr` | Meters (swim) | `- 50mtr Z1` |
| `50yrd` | Yards (swim) | `- 50yrd Z2` |

**Intensity targets:**

| Type | Syntax | Example |
|------|--------|---------|
| Power (% FTP) | `80%` or `100w` | `- 10m 88%` |
| Heart rate | `60% HR` or `100% LTHR` | `- 20m 75% HR` |
| Running pace | `80% Pace` or `Z2 Pace` | `- 5m 85% Pace` |
| Zone (generic) | `Z2` or `Z3 HR` | `- 10m Z2` |

**Target selection by discipline and readiness:**

| Discipline | Condition | Target type | ICU syntax |
|------------|-----------|-------------|------------|
| Running | Zones uncalibrated or returning from break | HR | `Z2 HR` |
| Running | Zones calibrated, stable fitness | Pace | `Z2 Pace` or `85% Pace` |
| Cycling | Power meter available | Power | `88%` or `Z3` |
| Cycling | No power meter | HR | `Z2 HR` |
| Swimming | No CSS test | Generic zone + RPE | `Z2` |
| Swimming | CSS tested | Pace | `Z2 Pace` |

Check `data/memory/coach-memory.md` → Current Zones before generating workouts. If a zone section says "estimated" or "needs calibration," use the uncalibrated column.

**Modifiers:**

| Modifier | Syntax | Example |
|----------|--------|---------|
| Cadence | `90rpm` | `- 5m 88% 95rpm` |
| Rest intensity | `intensity=rest` | `- 30s intensity=rest` |
| Warmup tag | `intensity=warmup` | `- 10m intensity=warmup` |
| Cooldown tag | `intensity=cooldown` | `- 10m intensity=cooldown` |
| Ramp | `ramp 60-80%` | `- 10m ramp 60-80%` |

**Repeats:** Put `Nx` on its own line before the steps to repeat:

```
4x
- 4m 92%
- 2m Z1
```

**Step naming:** Text before the duration becomes a Garmin on-wrist prompt:

```
- Build to tempo 5m 85% Pace
- Recovery jog 2m Z1 Pace
```

On the Garmin watch, "Build to tempo" and "Recovery jog" appear as step labels.

**Garmin sync notes:**
- Ramps become range targets on device (e.g., `ramp 60-80%` shows as 60–80% target range)
- Distance-based steps are supported on Garmin
- Step names display on the watch during the workout
- Ensure "Upload planned workouts" is enabled in Intervals.icu settings (Settings → Garmin)

## How Each Command Should Use the API

### `/coach:checkin`
1. Pull today's wellness data — Garmin-synced fields: sleep duration, sleep score, sleep quality, HRV, resting HR, weight, SpO2, steps, VO2 max
2. Pull today's calendar events (Section 6) — get the planned workout for today
3. Show athlete what's already recorded — ask only for subjective fields: soreness, fatigue, stress, mood, motivation, injury, hydration
4. Write subjective scores back to intervals.icu via wellness PUT (1–4 scale)
5. Pull yesterday's activity if not yet debriefed
6. After session prescription:
   - Session proceeds as planned → no calendar change needed
   - Session modified → update the event description/duration
   - Session cancelled → delete the event, create a `NOTE` event with reason
   - No event exists but session prescribed → create new `WORKOUT` event

### `/coach:debrief`
1. Pull today's calendar events (Section 6) — get the planned workout to compare against
2. Pull today's most recent activity — auto-fill duration, distance, HR, TSS, pace/power
3. Show the athlete a summary: "You ran 10.2 km in 58 min, avg HR 148, TSS 72"
4. Ask only for subjective data the API can't provide: RPE feel, pain, fueling details, learnings
5. Compare against the planned session from the ICU calendar event

### `/coach:review`
1. Pull this week's calendar events (Section 6) — planned workouts, notes, sickness markers
2. Pull last 7 days of activities — compute weekly volume, intensity distribution, load
3. Pull last 7 days of wellness — trend sleep (duration + score + quality), HRV, resting HR, fatigue, soreness, stress, mood, motivation, injury, weight, SpO2, VO2 max
4. Pull athlete summary for current CTL/ATL/TSB
5. Compare planned events vs. actual activities for the week
6. Use all of this to write the weekly review

### `/coach:plan`
1. Pull current CTL/ATL/TSB to gauge fitness/fatigue state
2. Pull last 2–4 weeks of activity data for load trend context
3. Reference the original plan from `plans/` for what's prescribed
4. Adjust based on real data and write rationale/phase/decisions to `current-plan.md`
5. After athlete approves the plan, sync to intervals.icu via the workout library:
   - Read `folder_id` from `data/memory/coach-memory.md`. If none exists, create folder via Section 8 and store the ID.
   - Clear existing workouts from the folder: list workouts (Section 9), delete each one
   - Create each session as a workout in the folder (Section 9) with ICU workout syntax (Section 11)
   - Apply plan to calendar via Section 10 (start_date = Monday of the week)
   - Create a `NOTE` event on Monday with week rationale and key session notes
6. If API is unreachable: output the plan in the conversation, note that ICU sync is pending in `current-plan.md`

## Error Handling

- If the CLI returns an error with 401: credentials are wrong — tell the athlete to check `config/intervals-icu.json`
- If the CLI returns an error with 400: bad workout syntax in description — check ICU syntax (Section 11) and fix
- If the CLI returns an error with 409: duplicate event on that date — use update to modify the existing event instead
- If the CLI returns empty data: the athlete may not have synced their device — fall back to manual input
- If the API is unreachable: proceed with manual input, note that data is self-reported

## Notes

- All times from the API are local to the athlete's timezone setting in intervals.icu
- Distances are in meters — convert to km for display (the CLI does this automatically in formatted output)
- Durations are in seconds — convert to minutes/hours (the CLI does this automatically in formatted output)
- The API returns a lot of fields — only extract what's needed, don't overwhelm the athlete
- Wellness data syncs from connected devices (Garmin, Oura, etc.) — it may not be available until the device syncs
