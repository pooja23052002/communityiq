"""
CommunityIQ v2
Professional Sidebar
"""

import streamlit as st


def render_sidebar():
    with st.sidebar:

        st.markdown(
            """
            <div style="text-align:center;padding:10px;">
                <h2 style="margin-bottom:0;color:#1A73E8;">
                    🏙️ CommunityIQ
                </h2>

                <p style="color:#5F6368;margin-top:4px;">
                    AI Decision Intelligence
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        st.markdown("### 🚀 Google AI Stack")

        st.success("Gemini 2.5")

        st.info("Vertex AI")

        st.info("BigQuery")

        st.info("Cloud Run")

        st.info("Streamlit")

        st.divider()

        st.markdown("### 📌 Platform Features")

        st.markdown("✅ Executive Dashboard")

        st.markdown("✅ Explainable AI")

        st.markdown("✅ Risk Forecasting")

        st.markdown("✅ Decision Engine")

        st.markdown("✅ AI Recommendations")

        st.markdown("✅ Intervention Simulation")

        st.markdown("✅ Community Intelligence")

        st.divider()

        st.markdown("### 🤖 AI Workflow")

        st.markdown("""
```text
Planner
   ↓
Analysis
   ↓
Recommendation
   ↓
Report

""")