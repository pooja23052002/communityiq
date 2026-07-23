"""
CommunityIQ v2
AI Multi-Agent Workflow

Visualises the complete reasoning pipeline.
"""

import streamlit as st

from agents.orchestrator import orchestrator


def show_agents(
    traffic,
    air,
    complaints,
):

    st.header("🤖 Multi-Agent Decision Workflow")

    st.caption(
        "CommunityIQ coordinates specialised AI agents to analyse city data and generate explainable recommendations."
    )

    st.divider()

    ##############################################################
    # Input
    ##############################################################

    areas = sorted(
        traffic["area"].unique()
    )

    col1, col2 = st.columns([3, 2])

    with col1:

        query = st.text_input(
            "Ask CommunityIQ",
            value="Which area requires immediate intervention?"
        )

    with col2:

        default_area = st.selectbox(
            "Default Area",
            areas,
            key="agents_default_area",
        )

    ##############################################################
    # Execute
    ##############################################################

    if st.button(
        "🚀 Run Multi-Agent Workflow",
        use_container_width=True,
    ):

        result = orchestrator.execute(
            query=query,
            traffic=traffic,
            air=air,
            complaints=complaints,
            default_area=default_area,
        )

        planner = result["planner"]
        analysis = result["analysis"]
        recommendation = result["recommendation"]
        report = result["report"]

        st.divider()

        ##############################################################
        # Workflow Diagram
        ##############################################################

        st.subheader("🔄 Agent Pipeline")

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.success("🧠 Planner")

            st.write("Intent")

            st.write(planner["intent"])

        with c2:

            st.success("📊 Analysis")

            st.write("Area")

            st.write(analysis["area"])

        with c3:

            st.success("🤖 Recommendation")

            st.write("Priority")

            st.write(recommendation["priority"])

        with c4:

            st.success("📄 Report")

            st.write("Status")

            st.write(report["status"])

        st.divider()

        ##############################################################
        # Planner
        ##############################################################

        with st.expander(
            "🧠 Planner Agent",
            expanded=True,
        ):

            st.write("### User Query")

            st.code(planner["query"])

            st.write("### Intent")

            st.success(planner["intent"])

            st.write("### Workflow")

            for step in planner["workflow"]:

                st.write("➡️", step)

            st.write("### Datasets")

            for ds in planner["datasets"]:

                st.info(ds)

        ##############################################################
        # Analysis
        ##############################################################

        with st.expander(
            "📊 Analysis Agent",
            expanded=True,
        ):

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Priority",
                analysis["priority_score"],
            )

            c2.metric(
                "Risk Band",
                analysis["risk_band"],
            )

            c3.metric(
                "Top Driver",
                analysis["top_driver"],
            )

            st.write("### AI Reasoning")

            for item in analysis["explanation"]:

                st.success(item)

        ##############################################################
        # Recommendation
        ##############################################################

        with st.expander(
            "🤖 Recommendation Agent",
            expanded=True,
        ):

            st.info(
                recommendation["executive_summary"]
            )

            st.write("### Actions")

            for action in recommendation["recommended_actions"]:

                st.success(action)

            st.write("### Agent Findings")

            for finding in recommendation["agent_findings"]:

                st.write(f"• {finding}")

        ##############################################################
        # Report
        ##############################################################

        with st.expander(
            "📄 Report Agent",
            expanded=True,
        ):

            st.code(
                report["executive_report"],
                language="text",
            )

        st.divider()

        ##############################################################
        # Final Decision
        ##############################################################

        st.subheader("✅ Final Decision")

        st.success(
            recommendation["executive_summary"]
        )

        st.markdown(
            f"""
### CommunityIQ Decision

**Area:** {analysis['area']}

**Priority Score:** {analysis['priority_score']}

**Risk Band:** {analysis['risk_band']}

**Recommended Priority:** {recommendation['priority']}

**Expected Impact:** {recommendation['expected_impact']}

CommunityIQ completed the workflow using:

✔ Planner Agent

✔ Analysis Agent

✔ Recommendation Agent

✔ Report Agent

The final recommendation is fully explainable and can be exported as an executive report.
"""
        )

        st.balloons()