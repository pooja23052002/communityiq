"""
CommunityIQ
Confidence Estimation Service

Provides a simple confidence score for AI recommendations.
"""

from typing import Dict


def calculate_confidence(priority: Dict) -> Dict:
    """
    Estimate confidence based on consistency of signals.

    Returns
    -------
    {
        "score": 92,
        "label": "High",
        "color": "#34A853"
    }
    """

    contribution = priority["contribution"]

    values = [
        abs(v)
        for v in contribution.values()
    ]

    dominant = max(values)
    total = sum(values)

    if total == 0:
        confidence = 50
    else:
        confidence = int(
            60 + (dominant / total) * 40
        )

    confidence = min(confidence, 99)

    if confidence >= 90:
        label = "High"
        color = "#34A853"

    elif confidence >= 75:
        label = "Medium"
        color = "#FBBC04"

    else:
        label = "Low"
        color = "#EA4335"

    return {
        "score": confidence,
        "label": label,
        "color": color,
    }