"""
CommunityIQ - decision intelligence engine
===========================================
This is the brain. It turns three raw data streams into a single, explainable
priority decision per area, then lets you forecast and SIMULATE interventions.

Design choices that matter for the demo:

1. Every risk component maps to a 0-100 scale using a transparent rule, so the
   final priority score is fully explainable (no black box). AQI uses the real
   CPCB/EPA-style band cutoffs.
2. Complaint risk is an ANOMALY measure: how far above an area's own recent
   baseline today's volume sits. A spike matters more than a high steady state.
3. The forecast is a deliberately simple linear trend. It is honest, fast, and
   defensible. Tell judges it is a baseline, not a deep model.
4. simulate_intervention() is the differentiator: project "do nothing" vs
   "act now" and show the priority trajectory diverge.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

# Weighting of the three domains in the final priority score. Tunable + visible.
WEIGHTS = {"traffic": 0.25, "environment": 0.35, "complaints": 0.40}

BANDS = [(80, "CRITICAL"), (60, "HIGH"), (40, "MEDIUM"), (0, "LOW")]


def band(score: float) -> str:
    for cutoff, label in BANDS:
        if score >= cutoff:
            return label
    return "LOW"


# ---------------------------------------------------------------- loaders ----
def load_data(folder: str = "data"):
    traffic = pd.read_csv(f"{folder}/traffic_data.csv", parse_dates=["date"])
    air = pd.read_csv(f"{folder}/air_quality.csv", parse_dates=["date"])
    complaints = pd.read_csv(f"{folder}/citizen_complaints.csv", parse_dates=["date"])
    return traffic, air, complaints


# ------------------------------------------------ component risk functions ----
def aqi_to_risk(aqi: float) -> float:
    """Map AQI to a 0-100 risk using standard band cutoffs (piecewise linear)."""
    pts = [(0, 0), (50, 15), (100, 35), (150, 55), (200, 75), (300, 90), (400, 100)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if aqi <= x1:
            return float(y0 + (y1 - y0) * (aqi - x0) / (x1 - x0))
    return 100.0


def traffic_to_risk(idx: float) -> float:
    """Congestion index is already 0-100; emphasise the painful high end."""
    return float(np.clip((idx / 100) ** 1.3 * 100, 0, 100))


def complaint_risk(area_series: pd.Series, baseline_days: int = 21,
                   recent_days: int = 3) -> tuple[float, float, float]:
    """
    Anomaly-based complaint risk for one area.
    Returns (risk_0_100, recent_daily_avg, baseline_daily_avg).
    """
    s = area_series.sort_index()
    if len(s) == 0:
        return 0.0, 0.0, 0.0
    recent = s.tail(recent_days).mean()
    base = s.tail(baseline_days).head(max(baseline_days - recent_days, 1)).mean()
    base = max(base, 0.5)                      # floor avoids divide-by-zero blow-ups
    ratio = recent / base                      # 1.0 = normal, >1 = spike
    risk = float(np.clip((ratio - 1) * 55, 0, 100))
    return risk, float(recent), float(base)


# --------------------------------------------- per-area daily complaint count -
def daily_complaint_counts(complaints: pd.DataFrame, area: str) -> pd.Series:
    sub = complaints[complaints["area"] == area]
    counts = sub.groupby("date").size()
    full = pd.Series(0, index=pd.date_range(complaints["date"].min(),
                                            complaints["date"].max(), freq="D"))
    full.update(counts)
    return full


# ----------------------------------------------------------- priority score --
def compute_priority(area: str, traffic, air, complaints) -> dict:
    """Full explainable priority decision for one area, evaluated at latest date."""
    t_latest = traffic[traffic["area"] == area].sort_values("date")["traffic_index"].iloc[-1]
    a_latest = air[air["area"] == area].sort_values("date")["aqi"].iloc[-1]
    c_series = daily_complaint_counts(complaints, area)

    t_risk = traffic_to_risk(t_latest)
    a_risk = aqi_to_risk(a_latest)
    c_risk, c_recent, c_base = complaint_risk(c_series)

    contrib = {
        "traffic": t_risk * WEIGHTS["traffic"],
        "environment": a_risk * WEIGHTS["environment"],
        "complaints": c_risk * WEIGHTS["complaints"],
    }
    score = round(sum(contrib.values()), 1)

    # Plain-language explanation = the dominant contributor first.
    drivers = sorted(contrib.items(), key=lambda kv: kv[1], reverse=True)
    top = drivers[0][0]
    reason_bits = {
        "traffic": f"congestion index {t_latest:.0f}/100",
        "environment": f"AQI {a_latest:.0f} ({band(a_risk).lower()} health risk)",
        "complaints": (f"complaints running {c_recent:.1f}/day vs {c_base:.1f}/day "
                       f"baseline ({c_recent / max(c_base,0.5):.1f}x)"),
    }

    return {
        "area": area,
        "score": score,
        "band": band(score),
        "raw": {"traffic_index": round(float(t_latest), 1),
                "aqi": int(a_latest),
                "complaints_recent": round(c_recent, 2),
                "complaints_baseline": round(c_base, 2)},
        "component_risk": {"traffic": round(t_risk, 1),
                           "environment": round(a_risk, 1),
                           "complaints": round(c_risk, 1)},
        "contribution": {k: round(v, 1) for k, v in contrib.items()},
        "top_driver": top,
        "explanation": [f"{k}: {reason_bits[k]}" for k, _ in drivers],
    }


def rank_areas(traffic, air, complaints) -> pd.DataFrame:
    rows = [compute_priority(a, traffic, air, complaints)
            for a in sorted(traffic["area"].unique())]
    df = pd.DataFrame([{"area": r["area"], "score": r["score"], "band": r["band"],
                        "top_driver": r["top_driver"]} for r in rows])
    return df.sort_values("score", ascending=False).reset_index(drop=True)


# ----------------------------------------------------------------- forecast --
def forecast_series(series: pd.Series, horizon: int = 3, window: int = 7) -> dict:
    """Naive linear-trend forecast. Honest baseline, not a deep model."""
    s = series.dropna().astype(float).tail(window)
    if len(s) < 2:
        last = float(s.iloc[-1]) if len(s) else 0.0
        return {"projection": [last] * horizon, "slope": 0.0, "direction": "flat"}
    x = np.arange(len(s))
    slope, intercept = np.polyfit(x, s.values, 1)
    future_x = np.arange(len(s), len(s) + horizon)
    proj = [float(slope * fx + intercept) for fx in future_x]
    direction = "rising" if slope > 0.5 else "falling" if slope < -0.5 else "flat"
    return {"projection": [round(p, 1) for p in proj],
            "slope": round(float(slope), 2), "direction": direction}


# ------------------------------------------------- intervention simulation ----
# Modelled effect of each intervention on a domain. Transparent multipliers:
# value at each future step is multiplied toward (1 - effect) with a daily decay.
INTERVENTIONS = {
    "dispatch_water_tanker":   {"domain": "complaints", "effect": 0.55,
                                "label": "Dispatch water tankers + repair crew"},
    "deploy_waste_collection": {"domain": "complaints", "effect": 0.45,
                                "label": "Deploy extra waste collection"},
    "reroute_traffic":         {"domain": "traffic", "effect": 0.30,
                                "label": "Reroute traffic + signal retiming"},
    "street_cleaning_water":   {"domain": "environment", "effect": 0.20,
                                "label": "Water-spray dust suppression"},
}


def simulate_intervention(area, traffic, air, complaints,
                          intervention: str, horizon: int = 4) -> dict:
    """
    Compare two futures for one area:
      - do_nothing : project the current trend forward (problem persists/worsens)
      - with_action: the intervention resolves the root cause, so the affected
                     signal decays back toward its healthy baseline
    Each projected value is converted back into a priority score, so the two
    paths diverge in decision terms. This is the act-now-vs-wait payoff.
    """
    if intervention not in INTERVENTIONS:
        raise ValueError(f"Unknown intervention. Options: {list(INTERVENTIONS)}")
    spec = INTERVENTIONS[intervention]
    domain = spec["domain"]
    eff = spec["effect"]

    base = compute_priority(area, traffic, air, complaints)

    # Current value + a "healthy" target the intervention recovers toward.
    if domain == "complaints":
        series = daily_complaint_counts(complaints, area)
        start = float(series.tail(3).mean())
        target = max(float(series.tail(21).head(18).mean()), 0.5)   # pre-spike norm
        base_avg = target
    elif domain == "environment":
        series = air[air["area"] == area].set_index("date")["aqi"]
        start = float(series.tail(3).mean())
        target = float(series.head(len(series) - 5).mean())          # pre-ramp norm
    else:
        series = traffic[traffic["area"] == area].set_index("date")["traffic_index"]
        start = float(series.tail(3).mean())
        target = float(series.median())

    # do-nothing: continue the recent trend forward.
    fc = forecast_series(series, horizon=horizon)
    nothing_vals = fc["projection"]

    # with-action: decay from current value toward the healthy target.
    action_vals = []
    for i in range(horizon):
        frac = (1 - eff) ** (i + 1)               # share of the gap still remaining
        action_vals.append(round(target + (start - target) * frac, 1))

    # Convert a projected domain value back into a full priority score.
    def priority_with(domain_value):
        cr = dict(base["component_risk"])
        if domain == "environment":
            cr["environment"] = aqi_to_risk(domain_value)
        elif domain == "traffic":
            cr["traffic"] = traffic_to_risk(domain_value)
        else:
            cr["complaints"] = float(np.clip((domain_value / base_avg - 1) * 55, 0, 100))
        return round(sum(cr[k] * WEIGHTS[k] for k in WEIGHTS), 1)

    nothing_scores = [priority_with(v) for v in nothing_vals]
    action_scores = [priority_with(v) for v in action_vals]

    return {
        "area": area,
        "intervention": spec["label"],
        "affected_domain": domain,
        "current_score": base["score"],
        "horizon_days": horizon,
        "do_nothing": {"domain_projection": nothing_vals, "priority_path": nothing_scores,
                       "final_band": band(nothing_scores[-1])},
        "with_action": {"domain_projection": action_vals, "priority_path": action_scores,
                        "final_band": band(action_scores[-1])},
        "score_avoided": round(nothing_scores[-1] - action_scores[-1], 1),
    }
