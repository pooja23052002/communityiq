"""
CommunityIQ - synthetic data generator
=======================================
Produces 30 days of realistic-looking city data for 5 Chennai areas across
three domains: traffic, air quality, and citizen complaints.

A deliberate ANOMALY is seeded into one area (T Nagar) over the final days so
that the demo always fires the same way: a complaint spike + rising AQI that
the engine flags as HIGH priority, forecasts as escalating, and that the
simulation can then "fix". Seeded RNG => reproducible demo every run.

Synthetic data is fine for a hackathon as long as you SAY SO. Do not claim it
is live municipal data.
"""

import numpy as np
import pandas as pd

SEED = 42
rng = np.random.default_rng(SEED)

# End the window on the project's "today" so the anomaly sits at the edge.
END_DATE = pd.Timestamp("2026-06-24")
DAYS = 30
dates = pd.date_range(END_DATE - pd.Timedelta(days=DAYS - 1), END_DATE, freq="D")

# Per-area baselines: (traffic congestion index 0-100, baseline AQI, daily complaint rate)
AREAS = {
    "Anna Nagar": dict(traffic=58, aqi=95,  complaints=1.5),
    "T Nagar":    dict(traffic=72, aqi=120, complaints=2.0),   # anomaly target
    "Velachery":  dict(traffic=65, aqi=105, complaints=1.8),
    "Adyar":      dict(traffic=48, aqi=80,  complaints=1.2),
    "Mylapore":   dict(traffic=55, aqi=90,  complaints=1.4),
}

COMPLAINT_TYPES = [
    "Garbage not collected", "Water leakage", "No water supply",
    "Heavy traffic", "Streetlight not working", "Open drainage",
    "Road damage", "Noise pollution",
]

ANOMALY_AREA = "T Nagar"
ANOMALY_DAYS = 5          # last N days carry the spike
ANOMALY_TYPES = ["No water supply", "Water leakage", "Garbage not collected"]


def _weekly_factor(d: pd.Timestamp) -> float:
    # Weekdays busier than weekends for traffic.
    return 1.12 if d.dayofweek < 5 else 0.85


def build_traffic() -> pd.DataFrame:
    rows = []
    for area, base in AREAS.items():
        for d in dates:
            val = base["traffic"] * _weekly_factor(d) + rng.normal(0, 5)
            rows.append((area, d.date().isoformat(), round(float(np.clip(val, 5, 100)), 1)))
    return pd.DataFrame(rows, columns=["area", "date", "traffic_index"])


def build_air_quality() -> pd.DataFrame:
    rows = []
    for area, base in AREAS.items():
        for i, d in enumerate(dates):
            val = base["aqi"] + rng.normal(0, 8)
            # Seeded anomaly: AQI climbs over the final days in T Nagar.
            if area == ANOMALY_AREA:
                days_from_end = (END_DATE - d).days
                if days_from_end < ANOMALY_DAYS:
                    val += (ANOMALY_DAYS - days_from_end) * 16  # ramp up
            pm25 = max(2.0, val * 0.4 + rng.normal(0, 3))
            rows.append((area, d.date().isoformat(),
                         round(float(pm25), 1), int(np.clip(val, 10, 400))))
    return pd.DataFrame(rows, columns=["area", "date", "pm25", "aqi"])


def build_complaints() -> pd.DataFrame:
    rows = []
    for area, base in AREAS.items():
        for d in dates:
            rate = base["complaints"]
            types = COMPLAINT_TYPES
            # Seeded anomaly: complaint surge concentrated on water/garbage.
            if area == ANOMALY_AREA:
                days_from_end = (END_DATE - d).days
                if days_from_end < ANOMALY_DAYS:
                    rate += (ANOMALY_DAYS - days_from_end) * 2.2
                    types = ANOMALY_TYPES
            n = rng.poisson(rate)
            for _ in range(n):
                rows.append((area, d.date().isoformat(), str(rng.choice(types))))
    return pd.DataFrame(rows, columns=["area", "date", "complaint"])


def main():
    build_traffic().to_csv("data/traffic_data.csv", index=False)
    build_air_quality().to_csv("data/air_quality.csv", index=False)
    build_complaints().to_csv("data/citizen_complaints.csv", index=False)
    print("Wrote data/traffic_data.csv, data/air_quality.csv, data/citizen_complaints.csv")
    print(f"Seeded anomaly: {ANOMALY_AREA} (last {ANOMALY_DAYS} days, "
          f"water+garbage spike + rising AQI)")


if __name__ == "__main__":
    main()
