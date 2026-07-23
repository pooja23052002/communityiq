# CommunityIQ — AI Decision Intelligence Platform

A focused decision-intelligence demo for a Google Cloud AI hackathon. It ingests
three city data streams (traffic, air quality, citizen complaints), produces an
**explainable priority score** per area, forecasts the dominant signal, and —
the differentiator — **simulates acting now vs doing nothing** so a decision-maker
can see the payoff of intervening before they commit.

Demo city: **Chennai**, 5 areas, 30 days of data.

---

## What this is (and what it deliberately is NOT)

The brief tempts you toward a 7-module, 5-agent, digital-twin platform. That is
a slide deck, not a hackathon build. This repo builds **one vertical that
actually runs**, and frames the platform vision in the pitch.

Kept (the spine): three domains → priority score → explainability → forecast →
recommendation → two-tier agents → intervention simulation.

Cut on purpose (say "future work" in the pitch): five domain agents (we use two
tiers, honestly), live data ingestion (synthetic, seeded), a full digital twin
(the simulation IS the scoped version of that idea), and heavyweight ML
(a naive trend baseline you are honest about beats a RandomForest trained on a
handful of rows — and survives a judge's questioning).

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

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python generate_data.py     # writes the three CSVs with the seeded anomaly
python demo.py              # CLI: full decision loop end to end
streamlit run app.py        # dashboard: map, forecast, simulation, chat
```

Optional Gemini narrative:

```bash
pip install google-cloud-aiplatform
export GOOGLE_CLOUD_PROJECT=your-project
export GOOGLE_CLOUD_REGION=us-central1
gcloud auth application-default login
export USE_GEMINI=1
python demo.py
```

Without `USE_GEMINI`, everything still works via the rule-based fallback — so you
can develop and demo with no network and no quota burn.

---

## Demo script (what to click / say, in order)

1. **Ranking.** "CommunityIQ scores every area each day. T Nagar is CRITICAL at
   86.6." — establishes it's a decision tool, not a chatbot.
2. **Explainability.** "It's not a black box — 40 of those points come from
   complaints running 5x the area's own baseline, plus AQI at 200." — open the
   contribution breakdown. This is your responsible-AI beat.
3. **Anomaly framing.** "Notice we flagged this from a *spike vs baseline*, not a
   raw count — we'd catch a water-main failure before a formal report exists."
4. **Forecast.** "Left alone, complaints trend to ~22/day in three days."
5. **Simulation (the moment).** "Dispatch tankers now and priority falls from
   CRITICAL to MEDIUM over four days, avoiding ~37 priority points. Wait, and it
   stays CRITICAL. That's the decision." — this is the line that wins the room.
6. **Agents + action.** Show the three agent findings combining into one
   recommendation. Mention ADK as the production path.
7. **Close on vision.** *Now* show the CommunityIQ platform slide (health, waste,
   disaster) as "where this goes" — one working vertical, a credible roadmap.

---

## Honesty notes (so you don't get caught out)

- The data is **synthetic and seeded** — say so plainly; it's normal for a demo.
- The forecast is a **naive linear trend**, presented as a baseline, not a deep
  model. Don't overclaim.
- Intervention effects are **transparent modelled multipliers**, not learned —
  good enough to demonstrate the decision loop; flag it as a modelling choice.
- The priority score is **deterministic and rule-based**; Gemini only narrates
  it. That separation is a feature, not a limitation — it's your explainability
  and responsible-AI story.

---

## Dashboard (`app.py`)

Four tabs, all wired to the engine:
- **Overview & Map** — priority ranking + a colour-coded Chennai risk map.
- **Area Detail & Forecast** — explainability bar chart, metrics, forecast chart,
  agent findings + recommendation.
- **Simulation** — pick an area + intervention + horizon; watch the do-nothing vs
  act-now priority paths diverge live.
- **Ask City AI** — chat box; questions route to the engine (Gemini if enabled,
  keyword router offline).

## Next (optional, if time allows)

- CRITICAL-band auto-alert via Cloud Functions + Gmail (the automation beat).
- Swap CSVs for BigQuery and deploy `app.py` on Cloud Run for the live story.
