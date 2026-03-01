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
| `data/current-plan.md` | **Living operational state** — what we're following now, current week/phase, decisions, adjustments, agreements | Coach maintains this via commands |
| `data/plans/` | Training plan library — original plans as reference | You add plans; coach reads them |

### How the plans work together

- **`plans/`** holds the original training plans as-is (e.g. `ironman-70.3.md`, `marathon-sub345.md`). These are reference documents that don't change.
- **`current-plan.md`** is the operational state: which plan is active, what week you're in, what adjustments have been made, what decisions you and the coach agreed on. Every command reads and updates this file.

The coach reads `events.md` to know what's coming, references the original plan from `plans/`, and uses `current-plan.md` to track what's actually happening day to day.

### Intervals.icu API (objective training data — coach reads and writes)

Configured in `config/intervals-icu.json` with your athlete ID and API key. See `.claude/services/coach/intervals-icu.md` for full API reference.

| Data | What the coach pulls | Used by |
|------|---------------------|---------|
| Activities | Completed workouts: distance, duration, HR, pace, power, training load, zones | `/coach:debrief`, `/coach:review` |
| Wellness | Sleep, HRV, resting HR, weight (from wearable sync) | `/coach:checkin`, `/coach:review` |
| Athlete summary | Current CTL (fitness), ATL (fatigue), TSB (form) | `/coach:review`, `/coach:plan` |

The coach pulls objective data from intervals.icu first, then asks you only for what the API can't provide (RPE feel, pain location, fueling details, learnings).

### Google Sheets (optional structured logging — coach reads and writes)

Configured in `config/sheets.json` → `coach` key.

| Tab | Purpose |
|-----|---------|
| Daily Log | Date, sleep, stress, fatigue, soreness, pain, session, RPE, notes |
| Weekly Review | Week summary, load, readiness trends, adjustments |
| Zones | Current thresholds (FTP, run paces, CSS) with test dates |

## Agent & Service Files

| File | Role |
|------|------|
| `agents/coach/coach.md` | Core system prompt — operating rules, knowledge base, communication style |
| `agents/coach/alerts.md` | Safety decision tree — red flags, alert triggers, referral protocol |
| `agents/coach/periodization.md` | Macrocycle templates, sample weeks, session library |
| `services/intervals-icu.md` | Intervals.icu API reference — endpoints, curl patterns, per-command usage |

## Core Principles

1. **Safety first** — red flags always override training optimization. Pain, illness, and overtraining signals trigger automatic modification or referral. See `agents/coach/alerts.md`.
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
