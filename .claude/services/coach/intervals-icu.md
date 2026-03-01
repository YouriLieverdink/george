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

All curl calls use:
```bash
curl -s -u "API_KEY:$(jq -r .apiKey config/intervals-icu.json)" \
  "https://intervals.icu/api/v1/athlete/$(jq -r .athleteId config/intervals-icu.json)/..."
```

## Available Endpoints

### 1. Recent Activities (completed workouts)

**Use in:** `/coach:debrief` (auto-fill session data), `/coach:review` (weekly volume/load)

```bash
# Last 7 days of activities
ATHLETE_ID=$(jq -r .athleteId config/intervals-icu.json)
API_KEY=$(jq -r .apiKey config/intervals-icu.json)

curl -s -u "API_KEY:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/activities?oldest=$(date -d '7 days ago' +%Y-%m-%d)&newest=$(date +%Y-%m-%d)"
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
curl -s -u "API_KEY:$API_KEY" \
  "https://intervals.icu/api/v1/activity/$ACTIVITY_ID"
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
curl -s -u "API_KEY:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/wellness?oldest=$(date -d '7 days ago' +%Y-%m-%d)&newest=$(date +%Y-%m-%d)"
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
curl -s -X PUT -u "API_KEY:$API_KEY" \
  -H 'Content-Type: application/json' \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/wellness/$TODAY" \
  -d '{"soreness": 3, "fatigue": 4, "stress": 5, "mood": 7}'
```

### 5. Fitness / Fatigue Trends (CTL/ATL/TSB)

**Use in:** `/coach:review` (training load trends), `/coach:plan` (load targets)

```bash
# Athlete summary with fitness data
curl -s -u "API_KEY:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID"
```

Returns athlete profile including current CTL (fitness), ATL (fatigue), TSB (form).

### 6. Calendar Events (planned workouts)

**Use in:** `/coach:plan` (sync planned workouts to intervals.icu calendar)

```bash
# Read planned events
curl -s -u "API_KEY:$API_KEY" \
  "https://intervals.icu/api/v1/athlete/$ATHLETE_ID/events?oldest=$(date +%Y-%m-%d)&newest=$(date -d '7 days' +%Y-%m-%d)"
```

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

## Error Handling

- If the API returns 401: credentials are wrong — tell the athlete to check `config/intervals-icu.json`
- If the API returns empty data: the athlete may not have synced their device — fall back to manual input
- If the API is unreachable: proceed with manual input, note that data is self-reported

## Notes

- All times from the API are local to the athlete's timezone setting in intervals.icu
- Distances are in meters — convert to km for display
- Durations are in seconds — convert to minutes/hours
- The API returns a lot of fields — only extract what's needed, don't overwhelm the athlete
- Wellness data syncs from connected devices (Garmin, Oura, etc.) — it may not be available until the device syncs
