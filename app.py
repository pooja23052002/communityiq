"""
CommunityIQ - Streamlit dashboard
=================================
The demo surface. Run with:

    pip install -r requirements.txt
    python generate_data.py        # if you haven't already
    streamlit run app.py

Optional Gemini narrative/chat: set USE_GEMINI=1 plus GOOGLE_CLOUD_PROJECT and
authenticate (see README). Without it, everything still works offline.
"""

import pandas as pd
import streamlit as st
from components.styles import load_css
from components.sidebar import render_sidebar
from pages.dashboard import show_dashboard
from pages.decision_explorer import show_decision_explorer
from pages.simulation import show_simulation
from pages.risk_map import show_risk_map
from pages.agents import show_agents
from pages.reports import show_reports
from pages.architecture import show_architecture

from engine.decision import (
    load_data,
    rank_areas,
)
from engine.assistant import answer_question

st.set_page_config(
    page_title="CommunityIQ",
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()
#render_sidebar()


@st.cache_data
def get_data():
    return load_data()


try:
    traffic, air, complaints = get_data()
except FileNotFoundError:
    st.error("No data found. Run `python generate_data.py` first, then reload.")
    st.stop()

areas = sorted(traffic["area"].unique())

ranking = rank_areas(
    traffic,
    air,
    complaints,
)

st.markdown("""
<div class="hero">
<h1>🏙️ CommunityIQ</h1>
<h3>AI Powered Decision Intelligence Platform</h3>

<p>
Built using Google Gemini, Vertex AI,
BigQuery and Explainable AI.
</p>
</div>
""", unsafe_allow_html=True)

st.caption("Chennai · explainable priority scoring · forecast · act-now-vs-wait simulation")

(
    tab_dashboard,
    tab_detail,
    tab_sim,
    tab_map,
    tab_agents,
    tab_reports,
    tab_architecture,
    tab_chat,
) = st.tabs(
    [
        "📊 Executive Dashboard",
        "🔎 Decision Explorer",
        "🧪 AI Simulator",
        "🗺 Risk Map",
        "🤖 AI Agents",
        "📄 Reports",
        "☁️ Architecture",
        "💬 Ask City AI",
    ]
)

# ============================================================ OVERVIEW + MAP ==
with tab_dashboard:
    show_dashboard(
        traffic,
        air,
        complaints,
    )

# ==================================================== AREA DETAIL + FORECAST ==
with tab_detail:

    show_decision_explorer(
        traffic,
        air,
        complaints,
        areas,
    )

# ================================================================ SIMULATION ==
with tab_sim:

    show_simulation(
        traffic,
        air,
        complaints,
        ranking,
    )
# ================================================================== TAB MAP ==
with tab_map:

    show_risk_map(
        ranking,
    )
# ==========================================================
# AI AGENTS
# ==========================================================

with tab_agents:

    show_agents(
        traffic,
        air,
        complaints,
    )

# ==========================================================
# REPORTS
# ==========================================================
with tab_reports:

    show_reports(
        traffic,
        air,
        complaints,
    )

# ==========================================================
# ARCHITECTURE
# ==========================================================

with tab_architecture:

    show_architecture()
# ================================================================== ASK CHAT ==
with tab_chat:
    st.subheader("Ask the City AI")
    st.caption("e.g. \"Which area needs attention?\" · \"Predict T Nagar\" · "
               "\"What if we act in Velachery?\"")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    for role, msg in st.session_state.chat:
        st.chat_message(role).write(msg)

    if q := st.chat_input("Ask about the city…"):
        st.session_state.chat.append(("user", q))
        st.chat_message("user").write(q)
        ans = answer_question(q, traffic, air, complaints)
        st.session_state.chat.append(("assistant", ans))
        st.chat_message("assistant").write(ans)
