"""
Reusable KPI Cards
CommunityIQ v2
"""

import streamlit as st


def kpi_card(title, value, delta="", icon="📊", color="#1A73E8"):
    st.markdown(
        f"""
        <div style="
            background:white;
            padding:20px;
            border-radius:18px;
            box-shadow:0 4px 16px rgba(0,0,0,.08);
            border-top:5px solid {color};
            height:150px;
        ">

        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">

        <span style="font-size:15px;color:#5F6368;font-weight:500;">
            {title}
        </span>

        <span style="font-size:28px;">
            {icon}
        </span>

        </div>

        <div style="
            font-size:36px;
            font-weight:700;
            margin-top:18px;
            color:#202124;
        ">
            {value}
        </div>

        <div style="
            margin-top:10px;
            font-size:14px;
            color:#188038;
            font-weight:600;
        ">
            {delta}
        </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


def dashboard_metrics(ranking, traffic, air, complaints):
    """
    Creates four executive KPI cards using your existing datasets.
    """

    critical = len(ranking[ranking["band"] == "CRITICAL"])

    avg_aqi = round(air["aqi"].mean())

    avg_traffic = round(traffic["traffic_index"].mean())

    total_complaints = len(complaints)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi_card(
            "Critical Areas",
            critical,
            "Requires Immediate Attention",
            "🚨",
            "#EA4335",
        )

    with c2:
        kpi_card(
            "Average AQI",
            avg_aqi,
            "Air Quality Index",
            "🌿",
            "#34A853",
        )

    with c3:
        kpi_card(
            "Traffic Index",
            avg_traffic,
            "Average Congestion",
            "🚦",
            "#FBBC04",
        )

    with c4:
        kpi_card(
            "Citizen Complaints",
            total_complaints,
            "Community Reports",
            "📢",
            "#1A73E8",
        )