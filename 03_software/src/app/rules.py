"""Explainable rule engine for soil readings (INTERFACES v0.2 §4).

Each rule returns a structured finding with a rule_id, so every recommendation can be traced
back to a named threshold (explain-to-audit, D18). pH bands follow [KANANG2026] [AAR-SOIL];
moisture bands are demo calibration values (D17); TDS rules are SIMULATED agronomy against a
per-device baseline that the operator sets on the day (D25).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from . import config as C

PRIORITY = {"irrigate": 4, "drain": 4, "lime": 3, "fertilise": 2, "skip_fertiliser": 2, "watch": 1, "ok": 0}
SEVERITY_RANK = {"high": 3, "medium": 2, "low": 1, "info": 0}
LED = {"irrigate": "red", "lime": "red", "drain": "amber", "fertilise": "amber",
       "skip_fertiliser": "amber", "watch": "amber", "ok": "green"}
# Typical sensor uncertainty, used to lower confidence when a reading sits near a threshold.
SENSOR_ERR = {"soil_moisture_pct": 3.0, "soil_ph": 0.1, "tds_ratio": 0.05}


@dataclass
class Finding:
    action: str
    severity: str
    rule_id: str
    reason: str
    oled: str                     # short second OLED line (≤16 chars)
    counterfactual: str           # what would make this finding go away
    margin: float = 0.0           # distance from the threshold in sensor-error units
    simulated: bool = False

    def as_dict(self) -> dict:
        return {"action": self.action, "severity": self.severity, "rule_id": self.rule_id, "reason": self.reason}


@dataclass
class RuleResult:
    findings: list[Finding] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)       # informational (missing sensors, pH 5.5–6.5 band)
    missing: list[str] = field(default_factory=list)
    nearest_change: str = ""                               # counterfactual when everything is OK
    tds_baseline: float | None = None
    tds_margin: float | None = None


def _fmt(v: float, nd: int = 1) -> str:
    return f"{v:.{nd}f}"


def evaluate(reading: dict, tds_baseline: float | None = None, tds_margin: float | None = None) -> RuleResult:
    res = RuleResult(tds_baseline=tds_baseline, tds_margin=tds_margin)
    nearest: list[tuple[float, str]] = []   # (distance in sensor-error units, text) for OK counterfactual

    m = reading.get("soil_moisture_pct")
    if m is None:
        res.missing.append("soil_moisture_pct")
    elif m < C.MOISTURE_LOW:
        res.findings.append(Finding(
            "irrigate", "high", "MOIST_LOW",
            f"Soil moisture {_fmt(m)}% < {_fmt(C.MOISTURE_LOW, 0)}% threshold (water deficit lowers yield [CARR2011])",
            f"moist {_fmt(m, 0)}%<{_fmt(C.MOISTURE_LOW, 0)}%", f"moisture ≥ {_fmt(C.MOISTURE_LOW, 0)}%",
            (C.MOISTURE_LOW - m) / SENSOR_ERR["soil_moisture_pct"]))
    elif m > C.MOISTURE_HIGH:
        res.findings.append(Finding(
            "drain", "medium", "MOIST_HIGH",
            f"Soil moisture {_fmt(m)}% > {_fmt(C.MOISTURE_HIGH, 0)}% — waterlogging risk, check drainage [AAR-SOIL]",
            f"moist {_fmt(m, 0)}%>{_fmt(C.MOISTURE_HIGH, 0)}%", f"moisture ≤ {_fmt(C.MOISTURE_HIGH, 0)}%",
            (m - C.MOISTURE_HIGH) / SENSOR_ERR["soil_moisture_pct"]))
    else:
        d_lo, d_hi = m - C.MOISTURE_LOW, C.MOISTURE_HIGH - m
        if d_lo <= d_hi:
            nearest.append((d_lo / SENSOR_ERR["soil_moisture_pct"], f"IRRIGATE if moisture < {_fmt(C.MOISTURE_LOW, 0)}%"))
        else:
            nearest.append((d_hi / SENSOR_ERR["soil_moisture_pct"], f"DRAIN if moisture > {_fmt(C.MOISTURE_HIGH, 0)}%"))

    ph = reading.get("soil_ph")
    if ph is None:
        res.missing.append("soil_ph")
    elif ph < C.PH_LIME:
        res.findings.append(Finding(
            "lime", "high", "PH_LIME",
            f"Soil pH {_fmt(ph, 2)} < {_fmt(C.PH_LIME)} — strongly acidic, apply lime [KANANG2026]",
            f"pH {_fmt(ph, 2)}<{_fmt(C.PH_LIME, 1)}", f"pH ≥ {_fmt(C.PH_WATCH_TOP, 1)}",
            (C.PH_LIME - ph) / SENSOR_ERR["soil_ph"]))
    elif ph < C.PH_WATCH_TOP:
        res.findings.append(Finding(
            "watch", "low", "PH_LOW_WATCH",
            f"Soil pH {_fmt(ph, 2)} in {_fmt(C.PH_LIME, 1)}–{_fmt(C.PH_WATCH_TOP, 1)} watch band — re-test before next round [KANANG2026]",
            f"pH {_fmt(ph, 2)} watch", f"pH ≥ {_fmt(C.PH_WATCH_TOP, 1)}",
            min(ph - C.PH_LIME, C.PH_WATCH_TOP - ph) / SENSOR_ERR["soil_ph"]))
    elif ph > C.PH_HIGH:
        res.findings.append(Finding(
            "watch", "low", "PH_HIGH",
            f"Soil pH {_fmt(ph, 2)} > {_fmt(C.PH_HIGH, 1)} — check readings / stop liming [AAR-SOIL]",
            f"pH {_fmt(ph, 2)}>{_fmt(C.PH_HIGH, 1)}", f"pH ≤ {_fmt(C.PH_HIGH, 1)}",
            (ph - C.PH_HIGH) / SENSOR_ERR["soil_ph"]))
    else:
        if ph > C.PH_TYPICAL_TOP:
            res.notes.append(f"pH {_fmt(ph, 2)} is above the typical oil-palm band (4.2–5.5) but not harmful")
        d_lo, d_hi = ph - C.PH_WATCH_TOP, C.PH_HIGH - ph
        if d_lo <= d_hi:
            nearest.append((d_lo / SENSOR_ERR["soil_ph"], f"WATCH if pH < {_fmt(C.PH_WATCH_TOP, 1)}"))
        else:
            nearest.append((d_hi / SENSOR_ERR["soil_ph"], f"WATCH if pH > {_fmt(C.PH_HIGH, 1)}"))

    tds = reading.get("tds_ppm")
    if tds is None:
        res.missing.append("tds_ppm")
    elif not tds_baseline:
        res.notes.append("TDS baseline not calibrated yet — nutrient rules skipped")
    else:
        margin = C.TDS_DEFAULT_MARGIN if tds_margin is None else tds_margin
        lo, hi = tds_baseline * (1 - margin), tds_baseline * (1 + margin)
        ratio = tds / tds_baseline
        if tds < lo:
            res.findings.append(Finding(
                "fertilise", "medium", "TDS_LOW",
                f"TDS {_fmt(tds, 0)} ppm < {_fmt(lo, 0)} ppm (baseline {_fmt(tds_baseline, 0)} −{margin:.0%}) — "
                "nutrient level low, fertilise (SIMULATED agronomy)",
                f"TDS {_fmt(tds, 0)}<{_fmt(lo, 0)}", f"TDS ≥ {_fmt(lo, 0)} ppm",
                ((1 - margin) - ratio) / SENSOR_ERR["tds_ratio"], simulated=True))
        elif tds > hi:
            res.findings.append(Finding(
                "skip_fertiliser", "medium", "TDS_HIGH",
                f"TDS {_fmt(tds, 0)} ppm > {_fmt(hi, 0)} ppm (baseline {_fmt(tds_baseline, 0)} +{margin:.0%}) — "
                "skip this round: saves cost and N₂O/runoff (SIMULATED agronomy)",
                f"TDS {_fmt(tds, 0)}>{_fmt(hi, 0)}", f"TDS ≤ {_fmt(hi, 0)} ppm",
                (ratio - (1 + margin)) / SENSOR_ERR["tds_ratio"], simulated=True))
        else:
            d_lo, d_hi = ratio - (1 - margin), (1 + margin) - ratio
            txt = (f"FERTILISE if TDS < {_fmt(lo, 0)} ppm" if d_lo <= d_hi else f"SKIP_FERTILISER if TDS > {_fmt(hi, 0)} ppm")
            nearest.append((min(d_lo, d_hi) / SENSOR_ERR["tds_ratio"], txt))

    if res.missing:
        res.notes.append("Sensor offline (null): " + ", ".join(res.missing))
    if nearest:
        res.nearest_change = "Would change to " + min(nearest)[1]
    return res


def _confidence(findings: list[Finding], missing: int) -> float:
    """Rule confidence: high when far from thresholds, lower near them or with missing sensors."""
    if findings:
        m = max(f.margin for f in findings if PRIORITY[f.action] == max(PRIORITY[x.action] for x in findings))
    else:
        m = 3.0  # inside every band
    base = 0.6 + 0.35 * min(1.0, max(m, 0.0) / 3.0)
    return round(max(0.3, base - 0.1 * missing), 2)


def recommend(reading: dict, tds_baseline: float | None = None, tds_margin: float | None = None) -> dict:
    """Return the INTERFACES v0.2 recommendation body (minus evidence_id, added by the caller)."""
    r = evaluate(reading, tds_baseline, tds_margin)
    f_sorted = sorted(r.findings, key=lambda f: (PRIORITY[f.action], SEVERITY_RANK[f.severity], f.margin), reverse=True)

    if f_sorted:
        top = f_sorted[0]
        action, reason = top.action, top.reason
        cf = "Would be OK if " + " and ".join(f.counterfactual for f in f_sorted)
        oled = [action.upper().replace("_", " ")[:16], top.oled[:16]]
    elif len(r.missing) == 3:
        action, reason, cf = "ok", "No sensor data — all sensors returned null", ""
        oled = ["NO DATA", "check sensors"]
    else:
        action = "ok"
        reason = "All readings within thresholds"
        if r.notes:
            reason += "; " + "; ".join(r.notes)
        cf = r.nearest_change
        oled = ["OK", "all in range"] if not r.missing else ["OK (partial)", {"soil_moisture_pct": "no moisture", "soil_ph": "no pH reading", "tds_ppm": "no TDS reading"}[r.missing[0]]]

    actions = [f.as_dict() for f in f_sorted] or [{"action": "ok", "severity": "info", "rule_id": "ALL_OK", "reason": reason}]
    return {
        "action": action,
        "reason": reason,
        "confidence": _confidence(f_sorted, len(r.missing)),
        "actions": actions,
        "counterfactual": cf,
        "simulated": any(f.simulated for f in f_sorted),
        "oled": oled,
        "led": LED[action] if len(r.missing) < 3 else "amber",
        "notes": r.notes,
        "method": "rules",
    }
