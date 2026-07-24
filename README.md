# CommunityIQ — AI Decision Intelligence Platform

A focused decision-intelligence project for a Google Cloud AI hackathon. It ingests
three city data streams (traffic, air quality, citizen complaints), produces an
**explainable priority score** per area, forecasts the dominant signal, and —
the differentiator — **simulates acting now vs doing nothing** so a decision-maker
can see the payoff of intervening before they commit.

Demo city: **Chennai**, 5 areas, 30 days of data.
---

## Architecture

```
  traffic.csv   air_quality.csv   complaints.csv      (synthetic, seeded anomaly)
        \              |                /
         \             |               /
          v            v              v
        ┌──────────────────────────────────┐
        │  engine/decision.py               │   component risk (0-100 each):
        │   - aqi_to_risk (real AQI bands)  │     traffic / environment / complaints
        │   - traffic_to_risk               │   weighted -> PRIORITY SCORE + band
        │   - complaint_risk (anomaly vs    │   + per-component contribution
        │     own baseline)                 │     = full explainability
        │   - forecast_series (trend)       │
        │   - simulate_intervention  <-- differentiator
        └──────────────────────────────────┘
                         │
        ┌──────────────────────────────────┐
        │  engine/recommend.py              │   domain agents -> findings
        │   - domain_agent  (per domain)    │   coordinating agent -> actions
        │   - decision_brief (coordinator)  │   narrative: rule-based OR Gemini
        │   - gemini_brief  (optional LLM)  │   (LLM explains the numbers, does
        └──────────────────────────────────┘    not invent them)
                         │
              demo.py (CLI)   +   [next: Streamlit UI + map + chat]
```

**Mapping to the Google Cloud stack (for the pitch + production path):**

| Layer | This repo | Production on GCP |
|---|---|---|
| Data | local CSVs | BigQuery |
| Decision engine | `engine/decision.py` | same logic, Cloud Run service |
| LLM narrative / chat | `gemini_brief()` | Gemini 2.5 via Vertex AI |
| RAG over policy docs | (next) | Vertex AI Search + Vector Search |
| Agents | two-tier in `recommend.py` | ADK |
| Automation (alert on CRITICAL) | (next) | Cloud Functions + Gmail API |
| Dashboard | (next: Streamlit) | Looker Studio / Cloud Run |

---

## Demo Link:
https://communityiq-d7hsctrt6gb6x4lsmpnba5.streamlit.app/

```
