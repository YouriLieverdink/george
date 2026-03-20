"""Deterministic readiness score computation from alerts.md algorithm."""

from __future__ import annotations

from dataclasses import dataclass, field


# Subjective score mapping: 1=100, 2=70, 3=35, 4=0
SUBJECTIVE_MAP = {1: 100, 2: 70, 3: 35, 4: 0}


@dataclass
class Component:
    name: str
    weight: float
    score: float  # 0-100
    raw_value: str = ""  # human-readable raw value


@dataclass
class Modifier:
    name: str
    penalty: int
    reason: str = ""


@dataclass
class ReadinessResult:
    score: int  # 0-100 (clamped)
    band: str  # GREEN, AMBER, YELLOW, ORANGE, RED
    band_color: str  # for rich display
    components: list[Component] = field(default_factory=list)
    modifiers: list[Modifier] = field(default_factory=list)
    red_flag: bool = False
    missing: list[str] = field(default_factory=list)

    @property
    def action(self) -> str:
        actions = {
            "GREEN": "Execute as planned",
            "AMBER": "Cap top-end intensity; easy sessions proceed normally",
            "YELLOW": "Easy aerobic only, or shorten 30-50%. No key session work",
            "ORANGE": "Active recovery only (20-30 min easy walk/mobility)",
            "RED": "Full rest. If red flag: medical evaluation",
        }
        return actions.get(self.band, "")


def _score_band(score: int) -> tuple[str, str]:
    if score >= 80:
        return "GREEN", "green"
    if score >= 60:
        return "AMBER", "yellow"
    if score >= 40:
        return "YELLOW", "bright_yellow"
    if score >= 20:
        return "ORANGE", "dark_orange"
    return "RED", "red"


def _score_sleep(wellness: dict) -> Component | None:
    """Score sleep: use Garmin sleep score if available, fallback to hours."""
    sleep_score = wellness.get("sleepScore")
    sleep_hours = wellness.get("sleep")

    if sleep_score is not None:
        return Component("Sleep", 0.25, float(sleep_score), f"score {sleep_score}")

    if sleep_hours is not None:
        h = float(sleep_hours)
        if h >= 8:
            s = 95
        elif h >= 7:
            s = 80
        elif h >= 6:
            s = 60
        elif h >= 5:
            s = 40
        else:
            s = 20
        return Component("Sleep", 0.25, s, f"{h:.1f}h")

    return None


def _score_hrv(wellness: dict, hrv_baseline: float | None = None) -> Component | None:
    """Score HRV: % of 30-day baseline. Each 1% below = -2 pts from 100."""
    hrv = wellness.get("hrv")
    if hrv is None:
        return None
    if hrv_baseline is None or hrv_baseline <= 0:
        # No baseline — can't score meaningfully
        return None

    pct_of_baseline = (float(hrv) / hrv_baseline) * 100
    score = max(0, 100 - 2 * max(0, 100 - pct_of_baseline))
    return Component("HRV", 0.20, score, f"{int(hrv)} (baseline {int(hrv_baseline)})")


def _score_resting_hr(wellness: dict, rhr_baseline: float | None = None) -> Component | None:
    """Score resting HR: inverse — each 1% above baseline = -2.5 pts from 100."""
    rhr = wellness.get("restingHR")
    if rhr is None:
        return None
    if rhr_baseline is None or rhr_baseline <= 0:
        return None

    pct_above = ((float(rhr) - rhr_baseline) / rhr_baseline) * 100
    score = max(0, 100 - 2.5 * max(0, pct_above))
    return Component("Resting HR", 0.10, score, f"{int(rhr)} (baseline {int(rhr_baseline)})")


def _score_subjective(wellness: dict, field_name: str, weight: float) -> Component | None:
    """Score a subjective field (1-4 scale)."""
    val = wellness.get(field_name)
    if val is None:
        return None
    score = SUBJECTIVE_MAP.get(int(val), 50)
    labels = {
        "fatigue": {1: "LOW", 2: "AVG", 3: "HIGH", 4: "EXTREME"},
        "soreness": {1: "LOW", 2: "AVG", 3: "HIGH", 4: "EXTREME"},
        "mood": {1: "GREAT", 2: "GOOD", 3: "OK", 4: "GRUMPY"},
        "motivation": {1: "EXTREME", 2: "HIGH", 3: "AVG", 4: "LOW"},
    }
    label = labels.get(field_name, {}).get(int(val), str(val))
    return Component(field_name.capitalize(), weight, score, label)


def _score_mood_motivation(wellness: dict) -> Component | None:
    """Score mood + motivation combined (average of both)."""
    mood = wellness.get("mood")
    motivation = wellness.get("motivation")
    if mood is None and motivation is None:
        return None

    scores = []
    parts = []
    if mood is not None:
        scores.append(SUBJECTIVE_MAP.get(int(mood), 50))
        mood_labels = {1: "GREAT", 2: "GOOD", 3: "OK", 4: "GRUMPY"}
        parts.append(f"mood {mood_labels.get(int(mood), str(mood))}")
    if motivation is not None:
        scores.append(SUBJECTIVE_MAP.get(int(motivation), 50))
        mot_labels = {1: "EXTREME", 2: "HIGH", 3: "AVG", 4: "LOW"}
        parts.append(f"motivation {mot_labels.get(int(motivation), str(motivation))}")

    avg = sum(scores) / len(scores)
    return Component("Mood+Motivation", 0.15, avg, ", ".join(parts))


def compute_modifiers(
    wellness: dict,
    alcohol_drinks: int = 0,
    spo2_baseline: float | None = None,
    consecutive_low_days: int = 0,
) -> list[Modifier]:
    """Compute additive penalty modifiers."""
    mods = []

    # Alcohol
    if alcohol_drinks >= 3:
        mods.append(Modifier("Alcohol", -10, f"{alcohol_drinks} drinks (3+)"))
    elif alcohol_drinks >= 1:
        mods.append(Modifier("Alcohol", -5, f"{alcohol_drinks} drinks"))

    # SpO2
    spo2 = wellness.get("spO2")
    if spo2 is not None and spo2_baseline is not None and float(spo2) < spo2_baseline:
        mods.append(Modifier("SpO2", -10, f"{spo2}% (below baseline {spo2_baseline}%)"))

    # Injury
    injury = wellness.get("injury")
    if injury is not None:
        injury = int(injury)
        if injury == 2:
            mods.append(Modifier("Injury", -5, "NIGGLE"))
        elif injury == 3:
            mods.append(Modifier("Injury", -20, "POOR"))
        elif injury == 4:
            mods.append(Modifier("Injury", -40, "INJURED"))

    # Stress
    stress = wellness.get("stress")
    if stress is not None and int(stress) >= 3:
        labels = {3: "HIGH", 4: "EXTREME"}
        mods.append(Modifier("Stress", -5, labels.get(int(stress), "HIGH+")))

    # Consecutive low days
    if consecutive_low_days >= 3:
        mods.append(Modifier("Consecutive low days", -10, f"{consecutive_low_days} days <50"))

    return mods


def compute(
    wellness: dict,
    hrv_baseline: float | None = None,
    rhr_baseline: float | None = None,
    spo2_baseline: float | None = None,
    alcohol_drinks: int = 0,
    consecutive_low_days: int = 0,
    red_flag: bool = False,
) -> ReadinessResult:
    """Compute the readiness score from wellness data and baselines.

    wellness: dict with keys from intervals.icu wellness API (sleep, sleepScore,
              hrv, restingHR, fatigue, soreness, mood, motivation, injury, stress, spO2)
    """
    # Red flag override
    if red_flag:
        return ReadinessResult(
            score=0, band="RED", band_color="red", red_flag=True,
            components=[], modifiers=[], missing=["Red flag override"],
        )

    # Collect available components
    all_components = [
        _score_sleep(wellness),
        _score_hrv(wellness, hrv_baseline),
        _score_resting_hr(wellness, rhr_baseline),
        _score_subjective(wellness, "fatigue", 0.15),
        _score_subjective(wellness, "soreness", 0.15),
        _score_mood_motivation(wellness),
    ]

    component_names = ["Sleep", "HRV", "Resting HR", "Fatigue", "Soreness", "Mood+Motivation"]
    available = []
    missing = []

    for comp, name in zip(all_components, component_names):
        if comp is not None:
            available.append(comp)
        else:
            missing.append(name)

    # Need minimum 2 components
    if len(available) < 2:
        return ReadinessResult(
            score=-1, band="UNKNOWN", band_color="dim",
            components=available, modifiers=[], missing=missing,
        )

    # Redistribute weights proportionally
    total_weight = sum(c.weight for c in available)
    weighted_score = sum((c.weight / total_weight) * c.score for c in available)

    # Apply modifiers
    modifiers = compute_modifiers(
        wellness, alcohol_drinks, spo2_baseline, consecutive_low_days,
    )
    modifier_total = sum(m.penalty for m in modifiers)

    raw_score = weighted_score + modifier_total
    final_score = max(0, min(100, int(round(raw_score))))

    band, band_color = _score_band(final_score)

    return ReadinessResult(
        score=final_score,
        band=band,
        band_color=band_color,
        components=available,
        modifiers=modifiers,
        missing=missing,
    )
