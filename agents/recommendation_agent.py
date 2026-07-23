"""
CommunityIQ v2
Recommendation Agent

Responsibilities
----------------
- Generate intervention recommendations
- Prioritize actions
- Produce executive narrative
- Estimate expected impact
"""

from typing import Dict

from engine.recommend import decision_brief


class RecommendationAgent:
    """
    Recommendation Agent

    Consumes the Analysis Agent output
    and produces actionable recommendations.
    """

    def recommend(
        self,
        analysis: Dict,
        complaints,
    ) -> Dict:

        ###########################################################
        # Determine most common complaint
        ###########################################################

        area = analysis["area"]

        top_complaint = (
            complaints[
                complaints["area"] == area
            ]["complaint"]
            .value_counts()
            .idxmax()
        )

        ###########################################################
        # Convert analysis into decision format
        ###########################################################

        decision_input = analysis["decision"]

        ###########################################################
        # Existing Recommendation Engine
        ###########################################################

        brief = decision_brief(
            decision_input,
            top_complaint=top_complaint,
        )

        ###########################################################
        # Priority
        ###########################################################

        score = analysis["priority_score"]

        if score >= 85:

            priority = "Immediate"

        elif score >= 70:

            priority = "High"

        elif score >= 50:

            priority = "Medium"

        else:

            priority = "Low"

        ###########################################################
        # Estimated Impact
        ###########################################################

        if priority == "Immediate":

            impact = "Very High"

        elif priority == "High":

            impact = "High"

        elif priority == "Medium":

            impact = "Moderate"

        else:

            impact = "Low"

        ###########################################################
        # Return Recommendation
        ###########################################################

        return {

            "area": area,

            "priority": priority,

            "expected_impact": impact,

            "recommended_actions": brief["actions"],

            "agent_findings": brief["agent_findings"],

            "executive_summary": brief["narrative"],

            "status": "Recommended",

        }


recommendation_agent = RecommendationAgent()