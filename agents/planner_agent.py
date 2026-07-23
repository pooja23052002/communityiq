"""
CommunityIQ v2
Planner Agent

Determines:
- User Intent
- Target Area
- Required Datasets
- Agent Workflow

This is the first agent in the multi-agent pipeline.
"""

from typing import Dict, List


class PlannerAgent:
    """
    Planner Agent

    Understands the user request and
    generates an execution plan for
    downstream AI agents.
    """

    def __init__(self):

        self.available_areas = [
            "Anna Nagar",
            "T Nagar",
            "Velachery",
            "Adyar",
            "Mylapore",
        ]

    ###########################################################

    def detect_area(
        self,
        query: str,
    ) -> str | None:

        query = query.lower()

        for area in self.available_areas:

            if area.lower() in query:
                return area

        return None

    ###########################################################

    def detect_intent(
        self,
        query: str,
    ) -> str:

        q = query.lower()

        if any(
            word in q
            for word in [
                "forecast",
                "predict",
                "future",
                "next",
            ]
        ):
            return "forecast"

        if any(
            word in q
            for word in [
                "simulate",
                "what if",
                "intervention",
            ]
        ):
            return "simulation"

        if any(
            word in q
            for word in [
                "risk",
                "priority",
                "danger",
            ]
        ):
            return "risk_assessment"

        if any(
            word in q
            for word in [
                "report",
                "summary",
                "pdf",
            ]
        ):
            return "report"

        return "general"

    ###########################################################

    def required_data(
        self,
        intent: str,
    ) -> List[str]:

        mapping = {

            "forecast": [
                "traffic",
                "air",
                "complaints",
            ],

            "simulation": [
                "traffic",
                "air",
                "complaints",
            ],

            "risk_assessment": [
                "traffic",
                "air",
                "complaints",
            ],

            "report": [
                "traffic",
                "air",
                "complaints",
            ],

            "general": [
                "traffic",
                "air",
                "complaints",
            ],
        }

        return mapping[intent]

    ###########################################################

    def execution_plan(
        self,
        intent: str,
    ) -> List[str]:

        if intent == "forecast":

            return [
                "Analysis Agent",
                "Recommendation Agent",
            ]

        if intent == "simulation":

            return [
                "Analysis Agent",
                "Recommendation Agent",
                "Report Agent",
            ]

        if intent == "risk_assessment":

            return [
                "Analysis Agent",
                "Recommendation Agent",
            ]

        if intent == "report":

            return [
                "Analysis Agent",
                "Recommendation Agent",
                "Report Agent",
            ]

        return [
            "Analysis Agent",
        ]

    ###########################################################

    def plan(
        self,
        query: str,
    ) -> Dict:

        intent = self.detect_intent(query)

        area = self.detect_area(query)

        datasets = self.required_data(intent)

        workflow = self.execution_plan(intent)

        return {

            "query": query,

            "intent": intent,

            "area": area,

            "datasets": datasets,

            "workflow": workflow,

            "status": "Planned",

        }


planner_agent = PlannerAgent()