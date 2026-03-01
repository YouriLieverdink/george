# /coach:help — Coach Commands

An evidence-based AI endurance coach for IRONMAN 70.3, marathon, and ultra events.

## Commands

| Command | Description | When to use |
|---------|-------------|-------------|
| `/coach:onboard` | Athlete intake — collect profile, goals, constraints | First time setup |
| `/coach:checkin` | Daily readiness check (<30 sec) → adapted session | Before every training session |
| `/coach:plan` | Generate next week's training plan | Weekly (usually Sunday/Monday) |
| `/coach:debrief` | Post-session logging + brief feedback | After every training session |
| `/coach:review` | Weekly/monthly trend analysis + plan adaptation | End of each week; monthly for deeper review |

## Typical Daily Flow

```
Morning:  /coach:checkin  → get today's session (adapted to readiness)
Training: do the session
After:    /coach:debrief  → log what happened, get feedback
```

## Typical Weekly Flow

```
Sunday:   /coach:review   → analyze the past week
          /coach:plan     → generate next week
Mon–Sat:  /coach:checkin  → /coach:debrief (daily cycle)
```

## Data

**Local files (repo):**
- `data/coach/references/events.md` — Race calendar with dates, distances, goals
- `data/coach/references/athlete-profile.md` — Your intake profile
- `data/coach/plans/current-plan.md` — Active macrocycle / training plan
- `data/coach/plans/archive/` — Past plans

**Google Sheet** (configured in `config/sheets.json` → `coach`):
- Tabs: Daily Log, Weekly Review, Zones

Edit `events.md` and `current-plan.md` directly when things change — the coach reads them before every decision.

## Safety

The coach will automatically flag red flags and recommend modification or medical referral. It will never push through pain, illness, or overtraining signals. See `agents/coach/alerts.md` for the full decision tree.
