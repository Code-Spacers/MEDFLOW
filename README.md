# MEDFLOW — Smart Hospital Resource Management Simulator

MEDFLOW is a Streamlit-based hospital operations simulator for the Hack-a-Matics MEDFLOW challenge. It models patient priority, waiting time, resource constraints, staff shortages, emergency surges, smart scheduling, discharge, utilization, and performance statistics.

## AI component

The project includes an **AI Hospital Analyst** using the OpenAI API. The AI receives the current simulated operational state (resources, queue, urgency, waiting time, and allocations) and provides an operational analysis for the dashboard. It is not used for diagnosis or clinical treatment decisions.

For the hackathon, use only synthetic/demo patient data.

## Run

```bash
pip install -r requirements.txt
export OPENAI_API_KEY="YOUR_KEY"
streamlit run app.py
```

The API key must never be committed to GitHub.
