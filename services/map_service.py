"""
CommunityIQ v2
Map Service

Creates interactive risk maps and
community location datasets.
"""

import pandas as pd
import streamlit as st


# --------------------------------------------------------
# Chennai Coordinates
# --------------------------------------------------------

COORDS = {
    "Anna Nagar": (13.0850, 80.2101),
    "T Nagar": (13.0418, 80.2341),
    "Velachery": (12.9755, 80.2207),
    "Adyar": (13.0012, 80.2565),
    "Mylapore": (13.0339, 80.2619),
}


# --------------------------------------------------------
# Risk Colors
# --------------------------------------------------------

RISK_COLORS = {
    "CRITICAL": "#C62828",
    "HIGH": "#EF6C00",
    "MEDIUM": "#F9A825",
    "LOW": "#2E7D32",
}


# --------------------------------------------------------
# Build Map Data
# --------------------------------------------------------

def create_map_dataframe(ranking):
    """
    Converts ranked communities into
    a Streamlit/PyDeck compatible dataframe.
    """

    rows = []

    for _, row in ranking.iterrows():

        lat, lon = COORDS[row["area"]]

        rows.append(
            {
                "area": row["area"],
                "lat": lat,
                "lon": lon,
                "score": row["score"],
                "band": row["band"],
                "color": RISK_COLORS[row["band"]],
                "size": 120 + row["score"] * 6,
            }
        )

    return pd.DataFrame(rows)


# --------------------------------------------------------
# Render Streamlit Map
# --------------------------------------------------------

def render_map(ranking):
    """
    Displays community risk map.
    """

    map_df = create_map_dataframe(ranking)

    st.map(
        map_df,
        latitude="lat",
        longitude="lon",
        size="size",
        color="color",
    )

    st.caption(
        "🔴 Critical    🟠 High    🟡 Medium    🟢 Low"
    )

    return map_df


# --------------------------------------------------------
# Area Information
# --------------------------------------------------------

def get_area_summary(area, ranking):
    """
    Returns summary for a selected area.
    """

    row = ranking[
        ranking["area"] == area
    ].iloc[0]

    return {
        "area": row["area"],
        "score": row["score"],
        "band": row["band"],
        "lat": COORDS[row["area"]][0],
        "lon": COORDS[row["area"]][1],
    }


# --------------------------------------------------------
# Dashboard Cards
# --------------------------------------------------------

def render_area_card(area_info):

    color = RISK_COLORS[area_info["band"]]

    st.markdown(
        f"""
<div style="
background:white;
padding:18px;
border-radius:15px;
border-left:8px solid {color};
box-shadow:0px 4px 12px rgba(0,0,0,.08);
">

<h3>{area_info['area']}</h3>

<p>

<b>Priority Score:</b>
{area_info['score']}/100

</p>

<p>

<b>Risk Band:</b>
{area_info['band']}

</p>

<p>

<b>Coordinates:</b>

{area_info['lat']:.4f},
{area_info['lon']:.4f}

</p>

</div>
""",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------
# Executive Summary
# --------------------------------------------------------

def render_map_summary(ranking):

    critical = len(
        ranking[
            ranking["band"] == "CRITICAL"
        ]
    )

    high = len(
        ranking[
            ranking["band"] == "HIGH"
        ]
    )

    medium = len(
        ranking[
            ranking["band"] == "MEDIUM"
        ]
    )

    low = len(
        ranking[
            ranking["band"] == "LOW"
        ]
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Critical",
        critical,
    )

    c2.metric(
        "High",
        high,
    )

    c3.metric(
        "Medium",
        medium,
    )

    c4.metric(
        "Low",
        low,
    )