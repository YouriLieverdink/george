# AI Endurance Coach

An evidence-based personal endurance coach for IRONMAN 70.3, marathon, and ultra events. Built as a Claude Code agent with structured commands, safety-first decision logic, and periodized training planning.

## Commands

| Command | Description | When |
|---------|-------------|------|
| `/coach:onboard` | Athlete intake — collect profile, goals, constraints | First time setup |
| `/coach:checkin` | Daily readiness check → adapted session | Before every session |
| `/coach:plan` | Generate next week's training plan | Weekly (Sunday/Monday) |
| `/coach:debrief` | Post-session logging + feedback | After every session |
| `/coach:review` | Weekly/monthly trend analysis + plan adaptation | End of each week |
| `/coach:raceweek` | Race week prep — schedule, logistics, pacing, mental prep | 7 days before a race |
| `/coach:postrace` | Post-race debrief — race report, insights, recovery plan | After a race |
| `/coach:status` | Quick dashboard — week, phase, fitness, next session, race countdown | Anytime |
| `/coach:chat` | Freeform conversation — ask anything training-related | Anytime |
| `/coach:help` | Show all commands and data locations | Anytime |

## Daily Flow

```
Morning:   /coach:checkin   → readiness scores → adapted session for today
Training:  do the session
After:     /coach:debrief   → log RPE, pain, fueling, learnings
```

## Weekly Flow

```
Sunday:    /coach:review    → analyze the past week's trends
           /coach:plan      → generate next week based on review
Mon–Sat:   /coach:checkin + /coach:debrief daily cycle
```

## Data

### Local Files (version-controlled context the coach reads)

| File | Purpose | Who updates it |
|------|---------|----------------|
| `data/references/events.md` | Race calendar — dates, distances, priorities, goals | You, when events change |
| `data/references/athlete-profile.md` | Intake profile — history, constraints, equipment, health | `/coach:onboard`, then you as needed |
| `data/current-plan.md` | **Operational state** — current week/phase, rationale, goals, decisions, agreements. Does NOT contain the session schedule (that's on the intervals.icu calendar) | Coach maintains this via commands |
| `data/plans/` | Training plan library — original plans as reference | You add plans; coach reads them |
| `data/memory/coach-memory.md` | **Coaching memory** — patterns, injury history, follow-ups, learnings, preferences, zones, fitness tests | Coach writes via commands; accumulates over time |
| `data/logs/conversations.md` | Conversation log — summary of every coach interaction | All commands append; coach reads for context |
| `data/logs/daily-log.md` | Daily check-in + debrief log | `/coach:checkin`, `/coach:debrief` |
| `data/logs/weekly-reviews.md` | Weekly review summaries | `/coach:review` |
| `data/archive/weekly/` | Completed week archives (one file per week) | `/coach:review` |
| `data/archive/races/` | Race reports | `/coach:postrace` |
| `data/archive/logs/` | Monthly daily-log archives (one file per month, e.g. `2026-02.md`) | `/coach:review` (auto-rotates when new month starts) |

### How the data works together

- **`plans/`** holds the original training plans as-is (e.g. `ironman-70.3.md`, `marathon-sub345.md`). These are reference documents that don't change.
- **`current-plan.md`** is the operational state: which plan is active, what week you're in, rationale, goals, and decisions. Does NOT contain the session schedule — that lives on the intervals.icu calendar as the single source of truth. Completed weeks are archived to `data/archive/weekly/`.
- **`coach-memory.md`** is accumulated coaching intelligence: what the coach has learned about you over time. Every command reads it for context; checkin, debrief, review, and chat write to it.
- **`conversations.md`** is an append-only log of every coach interaction. It ensures nothing discussed is lost between sessions. The coach reads recent entries before every interaction for continuity.
- **`daily-log.md`** and **`weekly-reviews.md`** are append-only logs replacing the Google Sheets tabs.

The coach reads `current-plan.md` for phase/context and `coach-memory.md` for accumulated intelligence before every decision. For today's planned session, it reads from the intervals.icu calendar. It references the original plan from `plans/` and checks `events.md` for what's coming.

### Intervals.icu API (objective training data — coach reads and writes)

Configured in `config/intervals-icu.json` with your athlete ID and API key. See `.claude/services/coach/intervals-icu.md` for full API reference.

**All API calls must go through `./scripts/icu`.** Never use `curl` or raw HTTP requests. The CLI handles authentication, formatting, and error handling automatically. See the API reference for all available subcommands.

**Before making any `./scripts/icu` calls, always read `.claude/services/coach/intervals-icu.md` first** to verify the correct resource, action, and flag syntax. Do not guess at CLI syntax from memory.

| Data | What the coach pulls | Used by |
|------|---------------------|---------|
| Calendar events | **Single source of truth for the session schedule.** Planned workouts (WORKOUT), coaching notes (NOTE), illness markers (SICKNESS) | `/coach:checkin`, `/coach:debrief`, `/coach:plan`, `/coach:review`, `/coach:status` |
| Activities | Completed workouts: distance, duration, HR, pace, power, training load, zones | `/coach:debrief`, `/coach:review` |
| Wellness | Garmin-synced: sleep (duration, score, quality), HRV, resting HR, weight, SpO2, VO2 max, steps. Subjective (1–4 scale): soreness, fatigue, stress, mood, motivation, injury, hydration | `/coach:checkin`, `/coach:review` |
| Athlete summary | Current CTL (fitness), ATL (fatigue), TSB (form) | `/coach:review`, `/coach:plan` |

The coach pulls objective data from intervals.icu first, then asks you only for what the API can't provide (RPE feel, pain location, fueling details, learnings).

## Agent & Service Files

| File | Role |
|------|------|
| `.claude/agents/coach.md` | Core system prompt — operating rules, knowledge base, communication style |
| `.claude/agents/alerts.md` | Safety decision tree — red flags, alert triggers, referral protocol |
| `.claude/agents/periodization.md` | Macrocycle templates, sample weeks, session library |
| `.claude/services/coach/intervals-icu.md` | Intervals.icu API reference — CLI wrapper usage, endpoints, per-command patterns |

## Core Principles

1. **Safety first** — red flags always override training optimization. Pain, illness, and overtraining signals trigger automatic modification or referral. See `.claude/agents/alerts.md`.
2. **Evidence-based** — training decisions grounded in sports science (intensity distribution, load management, periodization, tapering). Not dogmatic — acknowledges uncertainty.
3. **Collaborative** — ask before advising, summarize inputs, propose options, confirm commitment. Uses motivational interviewing style (OARS: Open questions, Affirmations, Reflections, Summaries).
4. **You stay in control** — the coach drafts and suggests. It never commits to changes without your approval.
5. **Metrics are decision aids, not truth** — TSS/CTL/ATL/TSB, TRIMP, HRV, and ACWR are tools to inform judgment, not rules to follow blindly.

## Getting Started

1. Fill in `data/references/events.md` with your race calendar
2. Add your training plans to `data/plans/` (one file per plan, e.g. `ironman-70.3.md`, `marathon-sub345.md`)
3. Set up intervals.icu API access: go to https://intervals.icu/settings → "Developer Settings" → generate API key. Add your athlete ID and key to `config/intervals-icu.json`
4. Run `/coach:onboard` to complete your athlete profile — this also creates `data/current-plan.md`
5. Start the daily cycle: `/coach:checkin` → train → `/coach:debrief`
