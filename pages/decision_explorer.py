"""
CommunityIQ v2
Decision Explorer

Provides detailed AI analysis for a selected community,
including explainability, forecasting, confidence score,
and AI recommendations.
"""

import pandas as pd
import streamlit as st

from engine.decision import (
    compute_priority,
    forecast_series,
    daily_complaint_counts,
)

from engine.recommend import decision_brief

from services.confidence import calculate_confidence
from components.explainability import render_explainability


def show_decision_explorer(
    traffic,
    air,
    complaints,
    areas,
):
    """
    Decision Explorer Page
    """

    st.header("📈 Decision Explorer")

    st.caption(
        "Explore community health, AI reasoning, "
        "future forecasts and recommended interventions."
    )

    st.divider()

    ####################################################
    # Area Selection
    ####################################################

    area = st.selectbox(
        "Area",
        areas,
        key="decision_area",
    )

    priority = compute_priority(
        area,
        traffic,
        air,
        complaints,
    )

    confidence = calculate_confidence(priority)

    ####################################################
    # Executive Metrics
    ####################################################

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Priority",
        f"{priority['score']}/100",
        priority["band"],
    )

    c2.metric(
        "AQI",
        priority["raw"]["aqi"],
    )

    c3.metric(
        "Complaints",
        priority["raw"]["complaints_recent"],
        f"Baseline {priority['raw']['complaints_baseline']}",
    )

    c4.metric(
        "Traffic",
        priority["raw"]["traffic_index"],
    )

    c5.metric(
        "Confidence",
        f"{confidence['score']}%",
        confidence["label"],
    )

    st.divider()

    ####################################################
    # Explainability
    ####################################################

    render_explainability(
        priority,
        confidence,
    )

    st.divider()

    ####################################################
    # Forecast
    ####################################################

    st.subheader("📈 Five Day Forecast")

    if priority["top_driver"] == "complaints":

        history = daily_complaint_counts(
            complaints,
            area,
        )

        metric_name = "Complaints"

    elif priority["top_driver"] == "environment":

        history = (
            air[
                air["area"] == area
            ]
            .set_index("date")["aqi"]
        )

        metric_name = "AQI"

    else:

        history = (
            traffic[
                traffic["area"] == area
            ]
            .set_index("date")["traffic_index"]
        )

        metric_name = "Traffic"

    forecast = forecast_series(
        history,
        horizon=5,
    )

    future_dates = pd.date_range(
        history.index[-1] + pd.Timedelta(days=1),
        periods=5,
    )

    chart = pd.DataFrame(
        {
            "History": history
        }
    )

    chart = chart.reindex(
        chart.index.union(future_dates)
    )

    chart["Forecast"] = pd.Series(
        forecast["projection"],
        index=future_dates,
    )

    chart.loc[
        history.index[-1],
        "Forecast",
    ] = float(history.iloc[-1])

    st.line_chart(
        chart,
        use_container_width=True,
    )

    st.caption(
        f"Primary Driver: **{priority['top_driver']}** | "
        f"Forecast Trend: **{forecast['direction']}**"
    )

    st.divider()

    ####################################################
    # AI Recommendation
    ####################################################

    common_issue = (
        complaints[
            complaints["area"] == area
        ]["complaint"]
        .value_counts()
        .idxmax()
    )

    brief = decision_brief(
        priority,
        top_complaint=common_issue,
    )

    st.subheader("🤖 AI Decision Summary")

    st.info(
        brief["narrative"]
    )

    st.subheader("Agent Findings")

    for finding in brief["agent_findings"]:

        st.success(
            finding
        )

    st.subheader("Recommended Actions")

    for i, action in enumerate(
        brief["actions"],
        start=1,
    ):

        st.markdown(
            f"""
<div style="
background:#E8F5E9;
padding:15px;
border-radius:10px;
margin-bottom:10px;
border-left:6px solid #34A853;
">

<b>Action {i}</b>

<br><br>

{action}

</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    ####################################################
    # Executive Summary
    ####################################################

    st.subheader("📋 Executive Summary")

    st.markdown(
        f"""
### {area}

**Priority Score:** {priority['score']}/100

**Risk Band:** {priority['band']}

**Primary Driver:** {priority['top_driver']}

**Confidence:** {confidence['score']}%

CommunityIQ recommends prioritising
**{area}**
based on explainable AI,
historical trends,
and predictive analytics.

This recommendation was generated
using CommunityIQ's Decision Intelligence Engine.
"""
    )