"""
CommunityIQ v2
Executive Dashboard
"""

import pandas as pd
import streamlit as st

from components.styles import load_css, hero_section, section
from components.cards import dashboard_metrics

from engine.decision import (
    rank_areas,
    compute_priority,
)

from engine.recommend import decision_brief


def show_dashboard(
    traffic,
    air,
    complaints,
):
    """Render Executive Dashboard"""

    load_css()
    hero_section()

    ranking = rank_areas(
        traffic,
        air,
        complaints,
    )

    #######################################################
    # Executive Summary
    #######################################################

    section("📊 Executive Dashboard")

    dashboard_metrics(
        ranking,
        traffic,
        air,
        complaints,
    )

    st.divider()

    #######################################################
    # Risk Ranking
    #######################################################

    section("🚨 Community Risk Ranking")

    st.dataframe(
        ranking,
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    #######################################################
    # Charts
    #######################################################

    left, right = st.columns([2, 1])

    with left:

        section("📈 Risk Distribution")

        risk_chart = (
            ranking.groupby("band")
            .size()
            .reset_index(name="Areas")
        )

        st.bar_chart(
            risk_chart,
            x="band",
            y="Areas",
            use_container_width=True,
        )

    with right:

        section("🔥 Highest Priority")

        top = ranking.iloc[0]

        st.metric(
            "Area",
            top["area"],
        )

        st.metric(
            "Priority Score",
            f"{top['score']}/100",
        )

        st.metric(
            "Risk Band",
            top["band"],
        )

    st.divider()

    #######################################################
    # AI Insights
    #######################################################

    top_area = ranking.iloc[0]["area"]

    detail = compute_priority(
        top_area,
        traffic,
        air,
        complaints,
    )

    complaint = (
        complaints[
            complaints["area"] == top_area
        ]["complaint"]
        .value_counts()
        .idxmax()
    )

    brief = decision_brief(
        detail,
        top_complaint=complaint,
    )

    section("🤖 AI Decision Insights")

    st.info(brief["narrative"])

    st.subheader("Recommended Actions")

    for i, action in enumerate(
        brief["actions"],
        start=1,
    ):
        st.success(f"Action {i}: {action}")

    st.divider()

    #######################################################
    # Explainability
    #######################################################

    section("🔍 Explainable AI")

    contribution = pd.DataFrame(
        {
            "Contribution": detail["contribution"]
        }
    ).T

    st.bar_chart(
        contribution,
        use_container_width=True,
    )

    st.subheader("Reasoning")

    for item in detail["explanation"]:
        st.write(f"• {item}")

    st.divider()

    #######################################################
    # Agent Findings
    #######################################################

    section("🤖 Agent Findings")

    for finding in brief["agent_findings"]:
        st.markdown(
            f"""
<div class="ai-card">
{finding}
</div>
""",
            unsafe_allow_html=True,
        )

    st.divider()

    #######################################################
    # Footer
    #######################################################

    st.caption(
        "CommunityIQ v2 • Powered by Google Gemini • Vertex AI • BigQuery • Streamlit"
    )


if __name__ == "__main__":
    st.warning(
        "Run this page through app.py"
    )
    