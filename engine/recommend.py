"""
CommunityIQ - recommendation + agent layer
===========================================
Turns a priority decision into recommended actions and a natural-language brief.

Two modes:
  * Offline (default): deterministic rule-based actions. No API needed, works in
    the demo even with no network. Use this while developing so you don't burn
    quota or get blocked behind credentials.
  * Gemini: set USE_GEMINI=1 and configure Vertex AI. Produces the polished
    analyst-style narrative judges like. The structured priority decision is
    passed in as grounding, so the model EXPLAINS your numbers rather than
    inventing its own (this is your responsible-AI story: the score is
    deterministic; the LLM only narrates it).

The "agents" framing: domain_agent() produces a per-domain finding, and
decision_brief() is the coordinating agent that combines them. That is an
honest two-tier multi-agent setup you can defend, not five fictional agents.
"""

from __future__ import annotations
import os

# Map the dominant driver / data signals to concrete municipal actions.
ACTION_LIBRARY = {
    "complaints": [
        ("No water supply", "Dispatch water tankers and a leak-repair crew to affected wards"),
        ("Water leakage", "Schedule pipeline inspection and emergency repair"),
        ("Garbage not collected", "Deploy an additional waste-collection vehicle on the route"),
        ("_default", "Open a field ticket and assign the relevant department"),
    ],
    "environment": [
        ("_default", "Activate dust-suppression water spraying and issue an AQI advisory"),
    ],
    "traffic": [
        ("_default", "Retime signals at the congested junction and deploy traffic personnel"),
    ],
}


def domain_agent(domain: str, decision: dict) -> str:
    """One agent's finding for a single domain, grounded in the computed risk."""
    risk = decision["component_risk"][domain]
    verdict = "elevated" if risk >= 55 else "moderate" if risk >= 35 else "normal"
    return f"[{domain.title()} Agent] risk {risk:.0f}/100 ({verdict})."


def rule_based_actions(decision: dict, top_complaint: str | None = None) -> list[str]:
    domain = decision["top_driver"]
    actions = []
    if domain == "complaints" and top_complaint:
        for key, act in ACTION_LIBRARY["complaints"]:
            if key == top_complaint:
                actions.append(act)
                break
        else:
            actions.append(ACTION_LIBRARY["complaints"][-1][1])
    else:
        actions.append(ACTION_LIBRARY.get(domain, ACTION_LIBRARY["complaints"])[-1][1])

    # Always add the second-highest driver as a secondary action.
    second = sorted(decision["contribution"].items(),
                    key=lambda kv: kv[1], reverse=True)[1][0]
    actions.append(ACTION_LIBRARY.get(second, ACTION_LIBRARY["complaints"])[-1][1])
    return actions


def gemini_brief(decision: dict, findings: list[str], actions: list[str]) -> str:
    """
    Optional polished narrative via Vertex AI Gemini. Requires:
      pip install google-cloud-aiplatform
      GOOGLE_CLOUD_PROJECT set, and `gcloud auth application-default login`
    The model is told to explain the supplied numbers, not invent new ones.
    """
    from vertexai.generative_models import GenerativeModel
    import vertexai
    vertexai.init(project=os.environ["GOOGLE_CLOUD_PROJECT"],
                  location=os.environ.get("GOOGLE_CLOUD_REGION", "us-central1"))
    model = GenerativeModel("gemini-2.5-pro")
    prompt = f"""You are a city operations analyst. Using ONLY the data below,
write a 4-5 sentence brief for a municipal decision-maker. Do not invent figures.

PRIORITY DECISION: {decision}
AGENT FINDINGS: {findings}
RECOMMENDED ACTIONS: {actions}

Cover: what is happening, why it scored this way, and what to do first."""
    return model.generate_content(prompt).text


def decision_brief(decision: dict, top_complaint: str | None = None) -> dict:
    """Coordinating agent: gather findings, pick actions, narrate."""
    findings = [domain_agent(d, decision) for d in ("traffic", "environment", "complaints")]
    actions = rule_based_actions(decision, top_complaint)

    if os.environ.get("USE_GEMINI") == "1":
        try:
            narrative = gemini_brief(decision, findings, actions)
        except Exception as e:                       # graceful fallback
            narrative = (f"[offline fallback - Gemini unavailable: {e}] "
                         + _offline_narrative(decision, actions))
    else:
        narrative = _offline_narrative(decision, actions)

    return {"area": decision["area"], "band": decision["band"],
            "score": decision["score"], "agent_findings": findings,
            "actions": actions, "narrative": narrative}


def _offline_narrative(decision: dict, actions: list[str]) -> str:
    drv = decision["explanation"][0]
    return (f"{decision['area']} is {decision['band']} priority "
            f"({decision['score']}/100), driven mainly by {drv}. "
            f"Recommended first action: {actions[0]}.")
