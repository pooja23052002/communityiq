"""
CommunityIQ v2
Analysis Agent
"""

from typing import Dict

from engine.decision import (
    compute_priority,
    forecast_series,
    daily_complaint_counts,
)


class AnalysisAgent:

    def analyse(
        self,
        area,
        traffic,
        air,
        complaints,
    ) -> Dict:

        detail = compute_priority(
            area,
            traffic,
            air,
            complaints,
        )

        ####################################################
        # Forecast
        ####################################################

        if detail["top_driver"] == "complaints":

            history = daily_complaint_counts(
                complaints,
                area,
            )

            metric = "Complaints / Day"

        elif detail["top_driver"] == "environment":

            history = (
                air[air["area"] == area]
                .set_index("date")["aqi"]
            )

            metric = "AQI"

        else:

            history = (
                traffic[traffic["area"] == area]
                .set_index("date")["traffic_index"]
            )

            metric = "Traffic Index"

        forecast = forecast_series(
            history,
            horizon=3,
        )

        ####################################################
        # IMPORTANT:
        # Preserve original decision output
        ####################################################

        return {

            "area": area,

            "decision": detail,

            "priority_score": detail["score"],

            "risk_band": detail["band"],

            "top_driver": detail["top_driver"],

            "forecast": forecast,

            "forecast_metric": metric,

            "raw_metrics": detail["raw"],

            "contribution": detail["contribution"],

            "explanation": detail["explanation"],

            "status": "Analysed",

        }


analysis_agent = AnalysisAgent()