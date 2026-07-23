"""
CommunityIQ v2
Explainable AI Component

Reusable Explainability Panel
"""

import pandas as pd
import streamlit as st


def render_explainability(priority, confidence):
    """
    Render Explainable AI Panel
    """

    st.subheader("🔍 Explainable AI")

    ########################################################
    # Confidence Card
    ########################################################

    col1, col2 = st.columns([1, 2])

    with col1:

        st.metric(
            "Confidence",
            f"{confidence['score']}%",
            confidence["label"],
        )

        st.progress(confidence["score"] / 100)

        st.caption(
            "Overall confidence of the recommendation."
        )

    ########################################################
    # Signal Contributions
    ########################################################

    with col2:

        st.markdown("### 📊 Signal Contributions")

        contribution_df = pd.DataFrame(
            {
                "Contribution": priority["contribution"]
            }
        ).T

        st.bar_chart(
            contribution_df,
            use_container_width=True,
        )

    st.divider()

    ########################################################
    # Primary Driver
    ########################################################

    st.markdown("### 🚦 Primary Risk Driver")

    driver = priority["top_driver"]

    if driver == "complaints":

        st.error(
            "📢 Citizen complaints are the dominant contributor "
            "to the current risk score."
        )

    elif driver == "traffic":

        st.warning(
            "🚦 Traffic congestion is the dominant contributor "
            "to the current risk score."
        )

    else:

        st.info(
            "🌿 Environmental conditions are the dominant contributor "
            "to the current risk score."
        )

    st.divider()

    ########################################################
    # AI Reasoning
    ########################################################

    st.markdown("### 🧠 AI Reasoning")

    for item in priority["explanation"]:

        st.success(item)

    st.divider()

    ########################################################
    # Executive Summary
    ########################################################

    st.markdown("### 📋 Explainability Summary")

    st.markdown(
        f"""
CommunityIQ analysed multiple city signals including:

- 🚦 Traffic Congestion
- 🌿 Air Quality
- 📢 Citizen Complaints

The AI model determined that **{driver.title()}**
is currently the strongest contributor to the
overall community priority score.

The recommendation confidence is
**{confidence['score']}%**
(**{confidence['label']} Confidence**).

This explanation is generated to improve
decision transparency for city administrators.
"""
    )