# AI Endurance Coach

An evidence-based personal endurance coach for IRONMAN 70.3, marathon, and ultra events.

Two interfaces:
- **George TUI** (`python3 -m george`) — standalone app, recommended for daily use
- **Claude Code commands** (`/coach:*`) — original Claude Code agent interface

## George TUI

The TUI moves all deterministic logic (data fetching, readiness scoring, log writing) into Python, and only calls Claude for judgment and conversation. Run with `python3 -m george`.

### TUI Architecture

```
george/
├── app.py              # REPL main loop (prompt_toolkit + rich)
├── claude.py           # Claude Code CLI wrapper (claude -p), conversation management
├── persona.py          # George system prompt from .claude/agents/coach.md
├── icu.py              # Python wrapper around scripts/icu (subprocess --json)
├── readiness.py        # Deterministic readiness score (from alerts.md algorithm)
├── files.py            # Read/write all data files, log appending
├── dates.py            # Date helpers
├── commands/
│   ├── checkin.py      # /checkin — fetch → Claude → structured output → write
│   ├── debrief.py      # /debrief — match activity → Claude → write
│   ├── plan.py         # /plan — compute analytics → Claude (opus) → sync to ICU
│   ├── review.py       # /review — compute trends → Claude (opus) → archive
│   ├── status.py       # /status — pure script, no Claude call
│   ├── chat.py         # /chat — freeform multi-turn
│   ├── raceweek.py     # /raceweek — race week briefing
│   └── postrace.py     # /postrace — race report + recovery
```

### Key design decisions

- **Readiness scores are deterministic** — computed in `readiness.py`, not by the LLM
- **Data fetching happens before Claude sees anything** — scripts assemble all context
- **Claude via CLI** — all calls go through `claude -p`, no API key needed
- **Structured output via --json-schema** — Claude returns validated JSON for write operations
- **Model selection per command** — sonnet for daily commands, opus for plan/review
- **Conversation carries across commands** — one session object, full history preserved

## Claude Code Commands

The original agent interface, still available for use within Claude Code:

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
Morning:   /checkin   → readiness scores → adapted session for today
Training:  do the session
After:     /debrief   → log RPE, pain, fueling, learnings
```

## Weekly Flow

```
Sunday:    /review    → analyze the past week's trends
           /plan      → generate next week based on review
Mon–Sat:   /checkin + /debrief daily cycle
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
| `data/logs/conversations/INDEX.md` | Conversation timeline — one line per interaction (always loaded) | All commands append |
| `data/logs/conversations/*.md` | Individual conversation files with frontmatter | All commands write |
| `data/logs/daily/INDEX.md` | Daily log timeline — one line per day (always loaded) | `/checkin`, `/debrief` append |
| `data/logs/daily/*.md` | Individual day files (checkin + debrief per day) | `/checkin`, `/debrief` write |
| `data/logs/weekly-reviews.md` | Weekly review summaries | `/review` |
| `data/archive/weekly/` | Completed week archives (one file per week) | `/review` |
| `data/archive/races/` | Race reports | `/postrace` |
| `data/archive/logs/` | Monthly daily-log archives (one file per month, e.g. `2026-02.md`) | `/review` (auto-rotates when new month starts) |

### How the data works together

- **`plans/`** holds the original training plans as-is (e.g. `ironman-70.3.md`, `marathon-sub345.md`). These are reference documents that don't change.
- **`current-plan.md`** is the operational state: which plan is active, what week you're in, rationale, goals, and decisions. Does NOT contain the session schedule — that lives on the intervals.icu calendar as the single source of truth. Completed weeks are archived to `data/archive/weekly/`.
- **`coach-memory.md`** is accumulated coaching intelligence: what the coach has learned about you over time. Every command reads it for context; checkin, debrief, review, and chat write to it.
- **`logs/conversations/`** stores individual conversation files with frontmatter. `INDEX.md` is a compact timeline (one line per entry, always loaded). Individual files are only read when their content is needed.
- **`logs/daily/`** stores one file per day with checkin + debrief data. `INDEX.md` is a compact timeline (one line per day, always loaded). Individual files are read selectively (today for checkin/debrief, this week for review).
- **`weekly-reviews.md`** is an append-only log (small, infrequent).

The coach reads `current-plan.md` for phase/context and `coach-memory.md` for accumulated intelligence before every decision. For today's planned session, it reads from the intervals.icu calendar. It references the original plan from `plans/` and checks `events.md` for what's coming.

### Intervals.icu API (objective training data — coach reads and writes)

Configured in `config/intervals-icu.json` with your athlete ID and API key. See `.claude/services/coach/intervals-icu.md` for full API reference.

**In the TUI**, all API calls go through `george/icu.py` which wraps `scripts/icu` with `--json` output.

**In Claude Code commands**, all API calls must go through `./scripts/icu`. Never use `curl` or raw HTTP requests. Before making any `./scripts/icu` calls, always read `.claude/services/coach/intervals-icu.md` first to verify the correct syntax.

| Data | What the coach pulls | Used by |
|------|---------------------|---------|
| Calendar events | **Single source of truth for the session schedule.** Planned workouts (WORKOUT), coaching notes (NOTE), illness markers (SICKNESS) | `/checkin`, `/debrief`, `/plan`, `/review`, `/status` |
| Activities | Completed workouts: distance, duration, HR, pace, power, training load, zones | `/debrief`, `/review` |
| Wellness | Garmin-synced: sleep (duration, score, quality), HRV, resting HR, weight, SpO2, VO2 max, steps. Subjective (1–4 scale): soreness, fatigue, stress, mood, motivation, injury, hydration | `/checkin`, `/review` |
| Athlete summary | Current CTL (fitness), ATL (fatigue), TSB (form) | `/review`, `/plan` |

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
4. Install [Claude Code](https://claude.com/claude-code) and authenticate (`claude` must be on your PATH)
5. Install Python dependencies: `pip install prompt_toolkit rich`
6. Run `python3 -m george` and start with `/checkin`
