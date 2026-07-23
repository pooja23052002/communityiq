"""
CommunityIQ v2
Decision Simulation

Simulate interventions and compare outcomes.
"""

import pandas as pd
import streamlit as st

from engine.decision import (
    simulate_intervention,
    INTERVENTIONS,
    band,
)

from services.confidence import calculate_confidence


def show_simulation(
    traffic,
    air,
    complaints,
    ranking,
):

    st.header("🧪 AI Decision Simulator")

    st.caption(
        "Evaluate interventions before implementation and compare projected outcomes."
    )

    st.divider()

    ###############################################################
    # Controls
    ###############################################################

    col1, col2, col3 = st.columns(3)

    areas = sorted(traffic["area"].unique())

    with col1:

        area = st.selectbox(
            "Area",
            areas,
            index=areas.index(ranking.iloc[0]["area"]),
            key="simulation_area",
        )

    with col2:

        options = {
            v["label"]: k
            for k, v in INTERVENTIONS.items()
        }

        label = st.selectbox(
            "Intervention",
            list(options.keys()),
            key="simulation_intervention",
        )

    with col3:

        horizon = st.slider(
            "Forecast Horizon (Days)",
            2,
            10,
            5,
        )

    ###############################################################
    # Simulation
    ###############################################################

    sim = simulate_intervention(
        area,
        traffic,
        air,
        complaints,
        options[label],
        horizon=horizon,
    )

    confidence = calculate_confidence(
        {
            "contribution": {
                "impact": sim["score_avoided"],
                "priority": sim["current_score"],
            }
        }
    )

    ###############################################################
    # KPI
    ###############################################################

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Current Priority",
        f"{sim['current_score']}/100",
        band(sim["current_score"]),
    )

    c2.metric(
        "Projected (No Action)",
        f"{sim['do_nothing']['priority_path'][-1]}/100",
        sim["do_nothing"]["final_band"],
    )

    c3.metric(
        "Projected (Intervention)",
        f"{sim['with_action']['priority_path'][-1]}/100",
        sim["with_action"]["final_band"],
    )

    c4.metric(
        "Confidence",
        f"{confidence['score']}%",
        confidence["label"],
    )

    st.divider()

    ###############################################################
    # Comparison Chart
    ###############################################################

    st.subheader("📈 Scenario Comparison")

    days = list(range(horizon + 1))

    chart = pd.DataFrame(
        {
            "Do Nothing": [
                sim["current_score"]
            ]
            + sim["do_nothing"]["priority_path"],
            "Intervention": [
                sim["current_score"]
            ]
            + sim["with_action"]["priority_path"],
        },
        index=days,
    )

    st.line_chart(
        chart,
        use_container_width=True,
    )

    st.caption(
        "Comparison of projected priority scores over time."
    )

    st.divider()

    ###############################################################
    # Outcome Summary
    ###############################################################

    st.subheader("📊 Impact Assessment")

    left, right = st.columns(2)

    with left:

        st.metric(
            "Priority Points Avoided",
            sim["score_avoided"],
        )

        reduction = (
            sim["current_score"]
            - sim["with_action"]["priority_path"][-1]
        )

        st.metric(
            "Overall Reduction",
            f"{round(reduction,1)} pts",
        )

    with right:

        st.metric(
            "Final Risk Band",
            sim["with_action"]["final_band"],
        )

        st.metric(
            "Simulation Horizon",
            f"{horizon} Days",
        )

    st.divider()

    ###############################################################
    # Recommendation
    ###############################################################

    st.subheader("🤖 AI Recommendation")

    if sim["score_avoided"] >= 15:

        recommendation = "Immediate intervention is strongly recommended."

    elif sim["score_avoided"] >= 8:

        recommendation = "Intervention is recommended within the next few days."

    else:

        recommendation = "Current conditions remain relatively stable. Continue monitoring."

    st.success(recommendation)

    st.info(
        f"""
Selected Intervention:

**{sim['intervention']}**

Projected Improvement:

**{sim['score_avoided']} priority points avoided**

Risk Band:

**{sim['do_nothing']['final_band']} → {sim['with_action']['final_band']}**
"""
    )

    st.divider()

    ###############################################################
    # Executive Summary
    ###############################################################

    st.subheader("📋 Executive Summary")

    st.markdown(
        f"""
### Simulation Report

**Area:** {area}

**Intervention:** {sim['intervention']}

**Forecast Horizon:** {horizon} days

**Priority Reduction:** {round(reduction,1)} points

**Confidence:** {confidence['score']}%

CommunityIQ predicts that implementing the selected intervention
can significantly reduce community risk while improving
overall operational efficiency.

This recommendation is based on predictive simulation
using historical complaints, traffic, and environmental data.
"""
    )