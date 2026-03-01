# Intervals.icu API Service

API integration for pulling training data, wellness metrics, and fitness trends from intervals.icu. Used by the coach agent to replace manual data entry with real data.

## Authentication

Uses HTTP Basic Auth with API key. Credentials stored in `config/intervals-icu.json`:

```json
{
  "athleteId": "i12345",
  "apiKey": "your-api-key-here",
  "baseUrl": "https://intervals.icu/api/v1"
}
```

**Setup:** Go to https://intervals.icu/settings → scroll to "Developer Settings" → generate API key. Your athlete ID is shown in the URL when you're on your profile (e.g., `i12345`).

**Important — curl command format:** All curl commands MUST start with `curl` as the very first word. Do not use variable assignments, subshells, or pipes in the command. Read `config/intervals-icu.json` first with the Read tool, then inline the athlete ID and API key directly into the curl command. This ensures the command matches the `Bash(curl:*)` permission pattern.

```bash
# Read config/intervals-icu.json first, then use values directly:
curl -s -u "API_KEY:<apiKey>" "https://intervals.icu/api/v1/athlete/<athleteId>/..."
```

## Available Endpoints

### 1. Recent Activities (completed workouts)

**Use in:** `/coach:debrief` (auto-fill session data), `/coach:review` (weekly volume/load)

```bash
# Last 7 days of activities (inline athlete ID and API key from config)
curl -s -u "API_KEY:<apiKey>" "https://intervals.icu/api/v1/athlete/<athleteId>/activities?oldest=YYYY-MM-DD&newest=YYYY-MM-DD"
```

**Key fields returned per activity:**
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
curl -s -u "API_KEY:<apiKey>" "https://intervals.icu/api/v1/activity/<activityId>"
```

Returns full activity with intervals detected, zone time distribution, and all metrics.

**Additional useful fields:**
- `icu_intervals` — detected intervals with avg HR, power, pace per interval
- `icu_zone_times` — time spent in each HR/power zone
- `pace` — formatted pace string
- `gap` — grade-adjusted pace (for hilly runs)

### 3. Wellness Data (readiness metrics)

**Use in:** `/coach:checkin` (auto-populate sleep, HRV, resting HR), `/coach:review` (trends)

```bash
# Last 7 days of wellness
curl -s -u "API_KEY:<apiKey>" "https://intervals.icu/api/v1/athlete/<athleteId>/wellness?oldest=YYYY-MM-DD&newest=YYYY-MM-DD"
```

**Key fields returned per day:**
- `id` — date (YYYY-MM-DD)
- `restingHR` — resting heart rate
- `hrv` — heart rate variability
- `hrvSDNN` — HRV SDNN value
- `sleep` — sleep duration (hours, decimal)
- `sleepQuality` — sleep quality score
- `fatigue` — fatigue rating
- `soreness` — soreness rating
- `stress` — stress rating
- `mood` — mood rating
- `motivation` — motivation rating
- `weight` — body weight (kg)
- `steps` — daily steps
- `spO2` — blood oxygen

### 4. Write Wellness Data (push subjective scores)

**Use in:** `/coach:checkin` (write readiness scores to intervals.icu)

```bash
# Update today's wellness
curl -s -X PUT -u "API_KEY:<apiKey>" -H 'Content-Type: application/json' "https://intervals.icu/api/v1/athlete/<athleteId>/wellness/YYYY-MM-DD" -d '{"soreness": 3, "fatigue": 4, "stress": 5, "mood": 7}'
```

### 5. Fitness / Fatigue Trends (CTL/ATL/TSB)

**Use in:** `/coach:review` (training load trends), `/coach:plan` (load targets)

```bash
# Athlete summary with fitness data
curl -s -u "API_KEY:<apiKey>" "https://intervals.icu/api/v1/athlete/<athleteId>"
```

Returns athlete profile including current CTL (fitness), ATL (fatigue), TSB (form).

### 6. Calendar Events (planned workouts)

**Use in:** `/coach:plan` (sync planned workouts to intervals.icu calendar)

```bash
# Read planned events
curl -s -u "API_KEY:<apiKey>" "https://intervals.icu/api/v1/athlete/<athleteId>/events?oldest=YYYY-MM-DD&newest=YYYY-MM-DD"
```

### 7. Create Calendar Events (structured workouts)

**Use in:** `/coach:plan` (push structured workouts to intervals.icu calendar → Garmin sync)

```bash
# Create a workout event
curl -s -X POST -u "API_KEY:<apiKey>" -H 'Content-Type: application/json' "https://intervals.icu/api/v1/athlete/<athleteId>/events" -d '{"start_date_local":"2026-03-02","category":"WORKOUT","name":"Tempo Run","type":"Run","description":"Warmup\n- 15m Z1 Pace\nMain set\n3x\n- 10m 85% Pace\n- 3m Z1 Pace\nCooldown\n- 10m Z1 Pace","moving_time":3600}'
```

**Payload fields:**

| Field | Type | Description |
|-------|------|-------------|
| `start_date_local` | string | Date in `YYYY-MM-DD` format |
| `category` | string | Always `"WORKOUT"` for planned workouts |
| `name` | string | Session title shown on calendar |
| `type` | string | Sport type (see mapping below) |
| `description` | string | Workout steps in ICU syntax (see Section 8) |
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
curl -s -X PUT -u "API_KEY:<apiKey>" -H 'Content-Type: application/json' "https://intervals.icu/api/v1/athlete/<athleteId>/events/<eventId>" -d '{"name":"Updated Session","description":"...","moving_time":3000}'
```

**Delete an event:**

```bash
curl -s -X DELETE -u "API_KEY:<apiKey>" "https://intervals.icu/api/v1/athlete/<athleteId>/events/<eventId>"
```

The API returns the created/updated event with its `id` — store this in `current-plan.md` so mid-week adjustments can use PUT/DELETE.

### 8. Workout Description Syntax

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
1. Pull today's wellness data (sleep, HRV, resting HR from device sync)
2. Show athlete what's already recorded — ask only for missing fields (subjective stress, soreness, pain)
3. Optionally write subjective scores back to intervals.icu
4. Pull yesterday's activity if not yet debriefed

### `/coach:debrief`
1. Pull today's most recent activity — auto-fill duration, distance, HR, TSS, pace/power
2. Show the athlete a summary: "You ran 10.2 km in 58 min, avg HR 148, TSS 72"
3. Ask only for subjective data the API can't provide: RPE feel, pain, fueling details, learnings
4. Compare against the planned session from `current-plan.md`

### `/coach:review`
1. Pull last 7 days of activities — compute weekly volume, intensity distribution, load
2. Pull last 7 days of wellness — trend sleep, fatigue, soreness, HRV
3. Pull athlete summary for current CTL/ATL/TSB
4. Compare planned vs. actual from `current-plan.md`
5. Use all of this to write the weekly review

### `/coach:plan`
1. Pull current CTL/ATL/TSB to gauge fitness/fatigue state
2. Pull last 2–4 weeks of activity data for load trend context
3. Reference the original plan from `plans/` for what's prescribed
4. Adjust based on real data and write to `current-plan.md`
5. After athlete approves the plan, POST each session as a structured workout event (Section 7) with ICU workout syntax (Section 8) so workouts sync to Garmin

## Error Handling

- If the API returns 401: credentials are wrong — tell the athlete to check `config/intervals-icu.json`
- If the API returns 400: bad workout syntax in description — check ICU syntax (Section 8) and fix
- If the API returns 409: duplicate event on that date — use PUT to update the existing event instead
- If the API returns empty data: the athlete may not have synced their device — fall back to manual input
- If the API is unreachable: proceed with manual input, note that data is self-reported

## Notes

- All times from the API are local to the athlete's timezone setting in intervals.icu
- Distances are in meters — convert to km for display
- Durations are in seconds — convert to minutes/hours
- The API returns a lot of fields — only extract what's needed, don't overwhelm the athlete
- Wellness data syncs from connected devices (Garmin, Oura, etc.) — it may not be available until the device syncs
