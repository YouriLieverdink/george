# George — AI Endurance Coach

A TUI for personalized endurance coaching. Python scripts handle data fetching and computation, Claude handles judgment and conversation.

## Setup

Requires [Claude Code](https://claude.com/claude-code) installed and authenticated (`claude` on your PATH).

```bash
pip install prompt_toolkit rich
```

Intervals.icu credentials go in `config/intervals-icu.json`:

```json
{
  "athleteId": "i12345",
  "apiKey": "your-api-key"
}
```

## Usage

```bash
python3 -m george
```

This opens a REPL. Type freely to chat with George, or use slash commands:

| Command | What it does |
|---------|-------------|
| `/checkin` | Morning readiness check — fetches wellness data, computes readiness score, adapts today's session |
| `/debrief` | Post-session logging — matches your activity to the plan, asks for RPE/pain/fueling, writes the log |
| `/plan` | Generates next week's training plan and syncs it to your intervals.icu calendar |
| `/review` | Weekly analysis — load trends, adherence, ACWR, adaptation decision |
| `/status` | Quick dashboard — current phase, next race countdown, today's session, CTL/ATL/TSB |
| `/chat` | Freeform conversation with George (this is also the default — just type) |
| `/raceweek` | Race week prep — day-by-day schedule, pacing, nutrition, logistics, mental |
| `/postrace` | Post-race debrief — race report, recovery plan, plan updates |
| `/help` | Show all commands |
| `/quit` | Exit (saves a conversation summary automatically) |

## Daily flow

```
Morning:   /checkin   -> readiness score -> adapted session for today
Training:  do the session
After:     /debrief   -> log RPE, pain, fueling, learnings
```

## Weekly flow

```
Sunday:    /review    -> analyze the week's trends
           /plan      -> generate next week
Mon-Sat:   /checkin + /debrief daily
```

## How it works

```
You  <->  Python TUI (george)  <->  claude -p (judgment only)
               |                          ^
          scripts/icu               pre-assembled context
          data files                structured output back
```

Scripts fetch all data (intervals.icu API, local files), compute readiness scores, and assemble context **before** Claude sees anything. Claude interprets the data as George and returns structured output. Scripts then write logs, update the calendar, and sync wellness scores.

All Claude calls go through `claude -p` (Claude Code CLI in print mode) — no API key needed, just a working `claude` installation.

This means:
- Readiness scores are deterministic (not LLM-generated)
- Data fetching never gets skipped or hallucinated
- Dates are always correct
- Log entries always get written
- Claude focuses on what it's good at: coaching judgment and conversation
