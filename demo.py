"""
CommunityIQ - end-to-end CLI demo
=================================
Runs the whole decision-intelligence loop on the seeded data and prints it.
This is a working, demoable artifact on its own (before the Streamlit UI).

    python generate_data.py     # once, to create the CSVs
    python demo.py
"""

from engine.decision import (load_data, rank_areas, compute_priority,
                              forecast_series, daily_complaint_counts,
                              simulate_intervention)
from engine.recommend import decision_brief


def hr(c="-"):
    print(c * 64)


def main():
    traffic, air, complaints = load_data()

    hr("=")
    print("COMMUNITYIQ  -  Chennai  -  decision intelligence run")
    hr("=")

    # 1. Rank every area by priority.
    print("\n[1] PRIORITY RANKING (latest day)")
    print(rank_areas(traffic, air, complaints).to_string(index=False))

    # 2. Drill into the top area with full explainability.
    top_area = rank_areas(traffic, air, complaints).iloc[0]["area"]
    d = compute_priority(top_area, traffic, air, complaints)
    print(f"\n[2] WHY {top_area.upper()} SCORED {d['score']}/100  ({d['band']})")
    for line in d["explanation"]:
        print(f"    - {line}")
    print(f"    contribution -> {d['contribution']}")

    # 3. Forecast the dominant signal.
    print(f"\n[3] 3-DAY FORECAST for {top_area} (top driver: {d['top_driver']})")
    if d["top_driver"] == "complaints":
        fc = forecast_series(daily_complaint_counts(complaints, top_area))
        unit = "complaints/day"
    elif d["top_driver"] == "environment":
        fc = forecast_series(air[air["area"] == top_area].set_index("date")["aqi"])
        unit = "AQI"
    else:
        fc = forecast_series(traffic[traffic["area"] == top_area].set_index("date")["traffic_index"])
        unit = "congestion index"
    print(f"    trend: {fc['direction']} (slope {fc['slope']}) -> next 3 days "
          f"{fc['projection']} {unit}")

    # 4. Recommendation + agent findings.
    top_complaint = (complaints[complaints["area"] == top_area]["complaint"]
                     .value_counts().idxmax())
    brief = decision_brief(d, top_complaint=top_complaint)
    print(f"\n[4] AGENT FINDINGS + RECOMMENDATION")
    for f in brief["agent_findings"]:
        print(f"    {f}")
    for i, a in enumerate(brief["actions"], 1):
        print(f"    action {i}: {a}")
    print(f"\n    BRIEF: {brief['narrative']}")

    # 5. The differentiator: simulate acting now vs doing nothing.
    print(f"\n[5] SIMULATION  -  act now vs do nothing  ({top_area})")
    sim = simulate_intervention(top_area, traffic, air, complaints,
                                "dispatch_water_tanker", horizon=4)
    print(f"    intervention : {sim['intervention']}")
    print(f"    current score: {sim['current_score']}")
    print(f"    do nothing   : priority {sim['do_nothing']['priority_path']} "
          f"-> ends {sim['do_nothing']['final_band']}")
    print(f"    with action  : priority {sim['with_action']['priority_path']} "
          f"-> ends {sim['with_action']['final_band']}")
    print(f"    >> acting now avoids ~{sim['score_avoided']} priority points "
          f"by day {sim['horizon_days']}")
    hr("=")


if __name__ == "__main__":
    main()
