"""
CommunityIQ v2
Multi-Agent Orchestrator

Coordinates the complete AI workflow:

User Query
      │
      ▼
Planner Agent
      │
      ▼
Analysis Agent
      │
      ▼
Recommendation Agent
      │
      ▼
Report Agent
"""

from typing import Dict

from agents.planner_agent import planner_agent
from agents.analysis_agent import analysis_agent
from agents.recommendation_agent import recommendation_agent
from agents.report_agent import report_agent


class MultiAgentOrchestrator:
    """
    Coordinates all CommunityIQ AI agents.
    """

    def execute(
        self,
        query: str,
        traffic,
        air,
        complaints,
        default_area: str = None,
    ) -> Dict:

        ###########################################################
        # Planner Agent
        ###########################################################

        planner = planner_agent.plan(query)

        ###########################################################
        # Resolve Area
        ###########################################################

        area = planner["area"]

        if area is None:

            if default_area is not None:

                area = default_area

            else:

                area = sorted(
                    traffic["area"].unique()
                )[0]

        ###########################################################
        # Analysis Agent
        ###########################################################

        analysis = analysis_agent.analyse(
            area,
            traffic,
            air,
            complaints,
        )

        ###########################################################
        # Recommendation Agent
        ###########################################################

        recommendation = recommendation_agent.recommend(
            analysis,
            complaints,
        )

        ###########################################################
        # Report Agent
        ###########################################################

        report = report_agent.generate(
            planner,
            analysis,
            recommendation,
        )

        ###########################################################
        # Final Response
        ###########################################################

        return {

            "planner": planner,

            "analysis": analysis,

            "recommendation": recommendation,

            "report": report,

            "workflow": planner["workflow"],

            "status": "Completed",

        }


orchestrator = MultiAgentOrchestrator()