"""
CommunityIQ v2
Report Agent

Responsibilities
----------------
- Build executive report
- Consolidate agent outputs
- Prepare report for PDF export
- Produce decision summary
"""

from datetime import datetime
from typing import Dict


class ReportAgent:
    """
    Report Agent

    Creates a structured executive report
    from the outputs of previous AI agents.
    """

    def generate(
        self,
        planner: Dict,
        analysis: Dict,
        recommendation: Dict,
    ) -> Dict:

        report = {

            ########################################################
            # Metadata
            ########################################################

            "generated_at": datetime.now().strftime(
                "%d %b %Y %H:%M"
            ),

            "status": "Completed",

            ########################################################
            # Planner Output
            ########################################################

            "planner": {

                "query": planner["query"],

                "intent": planner["intent"],

                "workflow": planner["workflow"],

                "datasets": planner["datasets"],

            },

            ########################################################
            # Analysis Output
            ########################################################

            "analysis": {

                "area": analysis["area"],

                "priority_score":
                    analysis["priority_score"],

                "risk_band":
                    analysis["risk_band"],

                "top_driver":
                    analysis["top_driver"],

                "forecast":
                    analysis["forecast"],

                "forecast_metric":
                    analysis["forecast_metric"],

                "contribution":
                    analysis["contribution"],

                "explanation":
                    analysis["explanation"],

            },

            ########################################################
            # Recommendation Output
            ########################################################

            "recommendation": {

                "priority":
                    recommendation["priority"],

                "expected_impact":
                    recommendation["expected_impact"],

                "recommended_actions":
                    recommendation["recommended_actions"],

                "agent_findings":
                    recommendation["agent_findings"],

                "executive_summary":
                    recommendation["executive_summary"],

            },

            ########################################################
            # Executive Summary
            ########################################################

            "executive_report":

                f"""
CommunityIQ Executive Decision Report

Area:
{analysis['area']}

Priority Score:
{analysis['priority_score']}/100

Risk Band:
{analysis['risk_band']}

Primary Driver:
{analysis['top_driver']}

Priority Level:
{recommendation['priority']}

Expected Impact:
{recommendation['expected_impact']}

--------------------------------------------------

Recommended Actions

{chr(10).join(
f"- {a}" for a in recommendation["recommended_actions"]
)}

--------------------------------------------------

Agent Findings

{chr(10).join(
f"- {a}" for a in recommendation["agent_findings"]
)}

--------------------------------------------------

Summary

{recommendation["executive_summary"]}

--------------------------------------------------

Generated automatically by
CommunityIQ Multi-Agent Decision Intelligence Platform.

Powered by Google Gemini,
Vertex AI,
BigQuery,
Streamlit.
""",

        }

        return report


report_agent = ReportAgent()