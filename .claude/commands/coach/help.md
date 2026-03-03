---
model: haiku
---

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
| `/coach:raceweek` | Race week prep — schedule, logistics, pacing, mental prep | 7 days before a race |
| `/coach:postrace` | Post-race debrief — race report, insights, recovery plan | After a race |
| `/coach:status` | Quick dashboard — week, phase, fitness, next session, countdown | Anytime (no logging) |
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
- `data/memory/coach-memory.md` — **Coaching memory:** patterns, injury history, follow-ups, learnings, zones, fitness tests
- `data/logs/daily-log.md` — Daily check-in and debrief log
- `data/logs/weekly-reviews.md` — Weekly review summaries
- `data/archive/` — Completed weeks (`weekly/`) and race reports (`races/`)

**Intervals.icu API** — objective training data (activities, wellness, fitness/fatigue/form)

The coach reads `current-plan.md` and `coach-memory.md` before every decision. Edit `events.md` when races change. Original plans in `plans/` stay unchanged — all modifications are tracked in `current-plan.md`.

## Safety

The coach will automatically flag red flags and recommend modification or medical referral. It will never push through pain, illness, or overtraining signals. See `.claude/agents/alerts.md` for the full decision tree.
