[README_MEDFLOW_FINAL.md](https://github.com/user-attachments/files/32431531/README_MEDFLOW_FINAL.md)
# MEDFLOW — Smart Hospital Resource Management Simulator

> AI-assisted hospital operations, resource allocation, and emergency scheduling simulator.

## 🚀 Live Demo

**[Launch the MEDFLOW Simulator][demo]**

The live Streamlit application allows users to interact with the hospital simulation, test different operational scenarios, allocate resources, and analyze hospital performance using the AI Hospital Analyst.

---

## 🏥 Problem Statement

Hospitals operate with limited beds, ICU capacity, doctors, nurses, and emergency resources while patients arrive with different urgency levels, waiting times, and resource requirements.

MEDFLOW models this challenge as a dynamic hospital scheduling and resource-allocation simulation.

## 💡 Solution

```text
Patient Arrival
      ↓
Priority Calculation
      ↓
Priority Queue
      ↓
Resource Availability Check
      ↓
Resource Allocation
      ↓
Scheduling
      ↓
Operations Dashboard
      ↓
Performance Analysis
```

The system can dynamically simulate emergency surges, staff shortages, ICU constraints, and changing waiting times.

## 🚀 Key Features

- Priority-based patient queue
- Urgency and waiting-time aware scheduling
- General bed and ICU allocation
- Doctor and nurse resource tracking
- Emergency surge simulation
- Staff shortage simulation
- ICU capacity constraints
- Patient waiting-time analysis
- Resource utilization dashboard
- Discharge and resource release
- Performance statistics
- Urgency-only vs MEDFLOW Smart scheduling comparison
- AI Hospital Analyst
- Interactive Streamlit dashboard

## 🤖 AI Hospital Analyst

MEDFLOW uses the OpenAI API as an AI-assisted operational analysis layer.

The AI receives the current simulated hospital state, including waiting patients, urgency, waiting time, resource availability, allocations, staffing constraints, and ICU requirements.

It provides:

- Current operational situation
- Highest-priority cases
- Potential bottlenecks
- Scheduling recommendations
- Resource-related risks
- Suggested operational actions

### AI Workflow

```text
Live Simulation State
        ↓
Hospital State Representation
        ↓
OpenAI API
        ↓
Operational Analysis
        ↓
Streamlit Dashboard Recommendations
```

The core simulation, priority calculation, resource allocation, scheduling logic, and capacity management remain deterministic and transparent.

> MEDFLOW is a hackathon simulation and is not intended for clinical diagnosis, treatment, or autonomous medical decision-making.

## 🧠 Scheduling Concept

MEDFLOW considers multiple operational factors instead of relying only on urgency:

```text
Patient Priority
      =
Urgency
+
Waiting-Time Consideration
+
Resource Availability
```

This allows different scheduling strategies to be compared under changing hospital conditions.

## 📊 Simulation Scenarios

### Normal Operations

Patients arrive gradually while resources are available.

### Emergency Surge

A sudden increase in patient arrivals stresses hospital capacity.

### Staff Shortage

Doctor and nurse availability is reduced to create staffing bottlenecks.

### ICU Constraint

Multiple patients require ICU resources while ICU capacity is limited.

### Combined Stress Scenario

Emergency surge + staff shortage + ICU requirements.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Simulation and scheduling logic |
| Streamlit | Interactive web dashboard and simulation interface |
| Pandas | Data handling and analysis |
| OpenAI API | AI-assisted operational analysis |
| GitHub | Version control |

## 📁 Project Structure

```text
MEDFLOW/
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
```

## ⚙️ Installation

```bash
git clone https://github.com/Code-Spacers/MEDFLOW.git
cd MEDFLOW
pip install -r requirements.txt
```

## 🔐 OpenAI API Configuration

Set your API key as an environment variable.

### macOS / Linux

```bash
export OPENAI_API_KEY="YOUR_API_KEY"
```

### Windows PowerShell

```powershell
$env:OPENAI_API_KEY="YOUR_API_KEY"
```

Run the Streamlit application:

```bash
streamlit run app.py
```

> Security: Never commit your OpenAI API key, `.env` file, or other secrets to GitHub.

## 🎯 Hackathon Alignment

MEDFLOW addresses the MEDFLOW — Hospital Resource Management Simulator challenge from Hack-a-Matics 2026.

The project focuses on:

- Patient prioritization
- Resource allocation
- Waiting-time reduction
- Capacity management
- Emergency scheduling
- Staff constraints
- Resource utilization
- Operational decision support

## 🌟 What Makes MEDFLOW Different

MEDFLOW combines:

```text
Priority Queue
      +
Waiting-Time Awareness
      +
Resource Constraints
      +
Emergency Surges
      +
Staff Shortages
      +
ICU Capacity
      +
Scheduling Comparison
      +
Resource Utilization
      +
AI Operational Analysis
      +
Interactive Streamlit Dashboard
```

Instead of presenting hospital scheduling as a static calculation, MEDFLOW lets users change the hospital environment and observe how the scheduling system responds in real time through an interactive Streamlit dashboard.

## 🔬 Example Stress Test

1. Open the MEDFLOW Live Demo
2. Activate staff shortage
3. Generate an emergency patient surge
4. Advance simulation time
5. Observe the priority queue
6. Allocate resources to critical cases
7. Run AI analysis
8. Reassess the operational situation
9. Compare scheduling performance

## 🔒 AI Disclosure

MEDFLOW uses the OpenAI API for AI-assisted operational analysis of the simulated hospital state.

The core simulation, priority calculation, resource allocation, scheduling logic, capacity management, and dashboard integration were developed specifically for this hackathon project.

AI is used as an operational analysis and explanation layer rather than as a replacement for the deterministic scheduling engine.

## 👥 Team

Project: MEDFLOW  
Hackathon: Hack-a-Matics 2026

## 📌 Future Scope

- Multi-department hospital simulation
- Ambulance arrival prediction
- Multiple-hospital coordination
- Resource failure simulation
- Historical performance analytics
- Advanced optimization algorithms
- Predictive patient-arrival modelling
- Real-time hospital data integration
- Advanced scheduling strategy comparison

[demo]: https://medflow-hrthbuz8rh26bb28uhdhnk.streamlit.app/
