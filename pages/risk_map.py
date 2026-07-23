"""
CommunityIQ v2
Community Risk Map

Interactive geographical view of
community risk levels.
"""

import streamlit as st

from services.map_service import (
    render_map,
    render_map_summary,
    get_area_summary,
    render_area_card,
)


def show_risk_map(
    ranking,
):
    """
    Community Risk Map
    """

    st.header("🗺 Community Risk Map")

    st.caption(
        "Visualise community priority scores across the city."
    )

    st.divider()

    ##########################################################
    # Executive Summary
    ##########################################################

    render_map_summary(
        ranking
    )

    st.divider()

    ##########################################################
    # Interactive Map
    ##########################################################

    st.subheader("📍 Interactive Risk Map")

    map_df = render_map(
        ranking
    )

    st.divider()

    ##########################################################
    # Area Explorer
    ##########################################################

    st.subheader("🏘 Community Explorer")

    selected_area = st.selectbox(
        "Select Community",
        map_df["area"],
        key="risk_map_area",
    )

    area = get_area_summary(
        selected_area,
        ranking
    )

    render_area_card(
        area
    )

    st.divider()

    ##########################################################
    # Ranking Table
    ##########################################################

    st.subheader("📊 Risk Ranking")

    st.dataframe(
        ranking,
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    ##########################################################
    # AI Summary
    ##########################################################

    st.subheader("🤖 AI Summary")

    if area["band"] == "CRITICAL":

        st.error(
            f"""
**{area['area']}** is currently the highest priority
community.

Immediate intervention is recommended.

Priority Score:
**{area['score']}/100**
"""
        )

    elif area["band"] == "HIGH":

        st.warning(
            f"""
**{area['area']}**
requires close monitoring.

Priority Score:
**{area['score']}/100**
"""
        )

    elif area["band"] == "MEDIUM":

        st.info(
            f"""
**{area['area']}**
should continue to be monitored.

Priority Score:
**{area['score']}/100**
"""
        )

    else:

        st.success(
            f"""
**{area['area']}**
is currently stable.

Priority Score:
**{area['score']}/100**
"""
        )

    st.divider()

    ##########################################################
    # Executive Notes
    ##########################################################

    st.subheader("📋 Executive Notes")

    st.markdown(
        f"""
### {area['area']}

**Priority Score:** {area['score']}/100

**Risk Band:** {area['band']}

The CommunityIQ Decision Engine
identified this community based on:

- Historical complaint trends
- Traffic congestion
- Environmental indicators

The map enables city officials to
identify high-risk communities
and prioritize interventions.

This view is intended for
decision support rather than
real-time emergency response.
"""
    )