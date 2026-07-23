"""
CommunityIQ - natural-language assistant
========================================
Answers free-text questions ("which area needs attention?", "predict T Nagar")
by grounding on the engine's computed decisions.

  * With Gemini (USE_GEMINI=1): the ranked decisions are passed in as context and
    the model answers using ONLY those numbers. Grounded => it explains the
    engine, it does not hallucinate civic data.
  * Offline: a keyword router produces a sensible answer straight from the
    computed decisions. Works with no network, so the chat is always live.
"""

from __future__ import annotations
import os
from engine.decision import (rank_areas, compute_priority, forecast_series,
                             daily_complaint_counts)

AREAS_HINT = None  # filled lazily


def build_context(traffic, air, complaints) -> str:
    """Compact, model-friendly snapshot of every area's decision."""
    lines = ["City decision snapshot (latest day):"]
    for a in sorted(traffic["area"].unique()):
        d = compute_priority(a, traffic, air, complaints)
        lines.append(
            f"- {a}: priority {d['score']}/100 ({d['band']}), top driver "
            f"{d['top_driver']}; AQI {d['raw']['aqi']}, "
            f"complaints {d['raw']['complaints_recent']}/day vs "
            f"{d['raw']['complaints_baseline']}/day baseline, "
            f"traffic {d['raw']['traffic_index']}/100.")
    return "\n".join(lines)


def _find_area(question: str, areas) -> str | None:
    q = question.lower()
    for a in areas:
        if a.lower() in q:
            return a
    return None


def _offline_answer(question: str, traffic, air, complaints) -> str:
    q = question.lower()
    areas = sorted(traffic["area"].unique())
    ranking = rank_areas(traffic, air, complaints)
    mentioned = _find_area(question, areas)

    # forecast intent
    if any(k in q for k in ("predict", "forecast", "tomorrow", "next", "trend")):
        area = mentioned or ranking.iloc[0]["area"]
        d = compute_priority(area, traffic, air, complaints)
        drv = d["top_driver"]
        if drv == "complaints":
            fc = forecast_series(daily_complaint_counts(complaints, area)); unit = "complaints/day"
        elif drv == "environment":
            fc = forecast_series(air[air["area"] == area].set_index("date")["aqi"]); unit = "AQI"
        else:
            fc = forecast_series(traffic[traffic["area"] == area].set_index("date")["traffic_index"]); unit = "congestion index"
        return (f"{area}: its top driver is {drv}, trending {fc['direction']}. "
                f"Next 3 days projected at {fc['projection']} {unit} (naive trend baseline).")

    # simulation intent
    if any(k in q for k in ("what if", "simulate", "if i", "act now", "do nothing")):
        area = mentioned or ranking.iloc[0]["area"]
        return (f"Open the Simulation tab for {area} to compare acting now vs "
                f"doing nothing — it projects the priority path under each choice.")

    # specific area
    if mentioned:
        d = compute_priority(mentioned, traffic, air, complaints)
        return (f"{mentioned} is {d['band']} priority ({d['score']}/100). "
                f"Main reason: {d['explanation'][0]}.")

    # default: urgency / ranking
    top = ranking.iloc[0]
    d = compute_priority(top["area"], traffic, air, complaints)
    return (f"{top['area']} needs attention first — {top['band']} at "
            f"{top['score']}/100, driven by {d['explanation'][0]}. "
            f"Full ranking: " +
            ", ".join(f"{r.area} {r.score}" for r in ranking.itertuples()))


def answer_question(question: str, traffic, air, complaints) -> str:
    if os.environ.get("USE_GEMINI") == "1":
        try:
            from vertexai.generative_models import GenerativeModel
            import vertexai
            vertexai.init(project=os.environ["GOOGLE_CLOUD_PROJECT"],
                          location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"))
            ctx = build_context(traffic, air, complaints)
            prompt = (f"You are a city operations assistant. Answer the question "
                      f"using ONLY this data; do not invent figures.\n\n{ctx}\n\n"
                      f"Question: {question}")
            return GenerativeModel("gemini-2.5-pro").generate_content(prompt).text
        except Exception as e:
            return f"[offline fallback - {e}] " + _offline_answer(question, traffic, air, complaints)
    return _offline_answer(question, traffic, air, complaints)
