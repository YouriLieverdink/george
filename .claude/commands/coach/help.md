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
| `/coach:chat` | Freeform conversation — ask anything training-related | Anytime |

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
- `data/current-plan.md` — **Living operational state:** active plan, current week/phase, decisions, adjustments
- `data/references/events.md` — Race calendar with dates, distances, goals
- `data/references/athlete-profile.md` — Your intake profile
- `data/plans/` — Training plan library: original plans as reference (e.g. `ironman-70.3.md`, `marathon-sub345.md`)

**Google Sheet** (configured in `config/sheets.json` → `coach`):
- Tabs: Daily Log, Weekly Review, Zones

The coach reads `current-plan.md` before every decision. Edit `events.md` when races change. Original plans in `plans/` stay unchanged — all modifications are tracked in `current-plan.md`.

## Safety

The coach will automatically flag red flags and recommend modification or medical referral. It will never push through pain, illness, or overtraining signals. See `agents/coach/alerts.md` for the full decision tree.
