"""Python wrapper around scripts/icu CLI (subprocess --json)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ICU_SCRIPT = str(Path(__file__).resolve().parent.parent / "scripts" / "icu")


class ICUError(Exception):
    """Raised when scripts/icu returns a non-zero exit code."""
    pass


def _run(*args: str) -> dict | list | None:
    """Run scripts/icu with --json and return parsed output."""
    cmd = ["python3", ICU_SCRIPT, *args, "--json"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired:
        raise ICUError("ICU API call timed out")

    if result.returncode != 0:
        raise ICUError(result.stderr.strip() or f"icu exited with code {result.returncode}")

    stdout = result.stdout.strip()
    if not stdout:
        return None
    return json.loads(stdout)


# --- Wellness ---

def wellness(oldest: str, newest: str) -> list[dict]:
    data = _run("wellness", "get", "--oldest", oldest, "--newest", newest)
    return data if isinstance(data, list) else []


def wellness_put(date: str, data: dict) -> None:
    _run("wellness", "put", "--date", date, "--data", json.dumps(data))


# --- Activities ---

def activities(oldest: str, newest: str) -> list[dict]:
    data = _run("activities", "list", "--oldest", oldest, "--newest", newest)
    return data if isinstance(data, list) else []


def activity(activity_id: str) -> dict:
    data = _run("activities", "get", "--id", activity_id)
    return data if isinstance(data, dict) else {}


# --- Athlete ---

def athlete_summary() -> dict:
    data = _run("athlete", "get")
    if isinstance(data, list) and data:
        return data[-1]
    return data if isinstance(data, dict) else {}


# --- Events ---

def events(oldest: str, newest: str) -> list[dict]:
    data = _run("events", "list", "--oldest", oldest, "--newest", newest)
    return data if isinstance(data, list) else []


def event_create(data: dict) -> dict:
    result = _run("events", "create", "--data", json.dumps(data))
    return result if isinstance(result, dict) else {}


def event_update(event_id: str, data: dict) -> dict:
    result = _run("events", "update", "--id", str(event_id), "--data", json.dumps(data))
    return result if isinstance(result, dict) else {}


def event_delete(event_id: str) -> None:
    _run("events", "delete", "--id", str(event_id))


def events_apply_plan(folder_id: str, start_date: str) -> list[dict]:
    data = _run("events", "apply-plan", "--folder-id", str(folder_id), "--start-date", start_date)
    return data if isinstance(data, list) else []


# --- Folders ---

def folders_create(name: str, folder_type: str = "PLAN", duration_weeks: int | None = None) -> dict:
    args = ["folders", "create", "--name", name, "--type", folder_type]
    if duration_weeks is not None:
        args.extend(["--duration-weeks", str(duration_weeks)])
    result = _run(*args)
    return result if isinstance(result, dict) else {}


def folders_delete(folder_id: str) -> None:
    _run("folders", "delete", "--id", str(folder_id))


# --- Workouts ---

def workouts(folder_id: str) -> list[dict]:
    data = _run("workouts", "list", "--folder-id", str(folder_id))
    return data if isinstance(data, list) else []


def workout_create(data: dict) -> dict:
    result = _run("workouts", "create", "--data", json.dumps(data))
    return result if isinstance(result, dict) else {}


def workout_delete(workout_id: str) -> None:
    _run("workouts", "delete", "--id", str(workout_id))
