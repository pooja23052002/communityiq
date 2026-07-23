"""
CommunityIQ v2
Architecture Page

Displays the architecture and technology stack
used by CommunityIQ.
"""

import streamlit as st


def show_architecture():
    """Render Architecture Page"""

    st.header("☁️ CommunityIQ Architecture")

    st.caption(
        "AI-powered Decision Intelligence Platform built using a modular multi-agent architecture."
    )

    st.divider()

    # ==========================================================
    # High-Level Architecture
    # ==========================================================

    st.subheader("🏗 High-Level System Architecture")

    architecture = """
                    Citizens / Decision Makers
                              │
                              ▼
                  Streamlit Web Application
                              │
         ┌────────────────────┴────────────────────┐
         │                                         │
         ▼                                         ▼
 Decision Intelligence Engine              AI Assistant
         │
         ▼
 Multi-Agent Orchestrator
         │
 ┌────────────┬────────────┬────────────┬────────────┐
 ▼            ▼            ▼            ▼
Planner     Analysis   Recommendation   Report
 Agent        Agent        Agent         Agent
         │
         ▼
 Decision Engine
         │
 ┌──────────────┬──────────────┬──────────────┐
 ▼              ▼              ▼
Traffic       Air Quality   Citizen Complaints
         │
         ▼
 Explainable AI
         │
         ▼
 Executive Dashboard / PDF Report
"""

    st.code(architecture, language="text")

    st.divider()

    # ==========================================================
    # Technology Stack
    # ==========================================================

    st.subheader("🛠 Technology Stack")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Application")

        st.success("Python")
        st.success("Streamlit")
        st.success("Pandas")
        st.success("ReportLab")

    with col2:

        st.markdown("### AI Components")

        st.success("Multi-Agent Workflow")
        st.success("Decision Engine")
        st.success("Explainable AI")
        st.success("Forecasting Engine")

    st.divider()

    # ==========================================================
    # Google Cloud Stack
    # ==========================================================

    st.subheader("☁️ Google Cloud Technologies")

    st.info(
        """
**Current / Planned Google AI Stack**

• Google Gemini

• Vertex AI

• Google Cloud

• BigQuery

• Cloud Run

• Streamlit Deployment
"""
    )

    st.divider()

    # ==========================================================
    # Multi-Agent Workflow
    # ==========================================================

    st.subheader("🤖 Multi-Agent Workflow")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Planner", "✓")
        st.caption("Intent Detection")

    with c2:
        st.metric("Analysis", "✓")
        st.caption("Risk Analysis")

    with c3:
        st.metric("Recommendation", "✓")
        st.caption("Decision Support")

    with c4:
        st.metric("Report", "✓")
        st.caption("Executive Report")

    st.divider()

    # ==========================================================
    # Platform Capabilities
    # ==========================================================

    st.subheader("🚀 Platform Capabilities")

    capabilities = [
        "Community Risk Ranking",
        "Explainable AI",
        "AI Decision Support",
        "Forecasting",
        "Intervention Simulation",
        "Interactive Risk Map",
        "Executive Reports",
        "Multi-Agent Workflow",
        "AI Assistant",
    ]

    for capability in capabilities:
        st.success(f"✔ {capability}")

    st.divider()

    # ==========================================================
    # Explainable AI
    # ==========================================================

    st.subheader("🔍 Explainable AI")

    st.write(
        """
CommunityIQ combines multiple signals to generate transparent recommendations:

- Traffic congestion
- Air Quality Index (AQI)
- Citizen complaints
- Historical trends
- Forecasting
- AI reasoning

Every recommendation includes an explanation so that city administrators can understand why a decision was suggested.
"""
    )

    st.divider()

    # ==========================================================
    # Future Roadmap
    # ==========================================================

    st.subheader("🔮 Future Enhancements")

    roadmap = [
        "Vertex AI Agent Engine",
        "Gemini API Integration",
        "BigQuery Data Warehouse",
        "Cloud Run Deployment",
        "Cloud Functions",
        "Looker Studio Dashboards",
        "Real-time IoT Sensor Integration",
    ]

    for item in roadmap:
        st.write(f"• {item}")

    st.divider()

    # ==========================================================
    # Footer
    # ==========================================================

    st.success(
        """
CommunityIQ demonstrates how AI, predictive analytics,
and a modular multi-agent architecture can help
city administrators make faster, explainable,
and data-driven decisions.
"""
    )


if __name__ == "__main__":
    show_architecture()