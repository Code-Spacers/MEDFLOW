
import streamlit as st
import pandas as pd
from dataclasses import dataclass
import os

st.set_page_config(page_title="MEDFLOW", page_icon="🏥", layout="wide")

st.title("🏥 MEDFLOW")
st.caption("Prioritize Patients. Optimize Resources.")

@dataclass
class Patient:
    name: str
    age: int
    urgency: int
    arrival_time: int
    needs_bed: bool
    needs_icu: bool
    needs_doctor: bool
    department: str

    @property
    def waiting_time(self):
        return max(0, st.session_state.current_time - self.arrival_time)

    @property
    def priority_score(self):
        return self.urgency * 100 + self.waiting_time

defaults = {
    "patients": [],
    "current_time": 0,
    "resources": {"beds": 10, "icu_beds": 3, "doctors": 5, "nurses": 8, "ambulances": 2},
    "allocations": [],
    "completed": [],
    "staff_shortage": False,
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v.copy() if isinstance(v, dict) else v

# ---------- Effective resources ----------
def effective_resources():
    base = st.session_state.resources.copy()
    if st.session_state.staff_shortage:
        base["doctors"] = min(base["doctors"], 2)
        base["nurses"] = min(base["nurses"], 3)
    return base

# ---------- Sidebar ----------
st.sidebar.header("Hospital Resources")
for key, label in [
    ("beds", "Beds"), ("icu_beds", "ICU Beds"), ("doctors", "Doctors"),
    ("nurses", "Nurses"), ("ambulances", "Ambulances")
]:
    st.session_state.resources[key] = st.sidebar.number_input(
        label, min_value=0, max_value=100,
        value=int(st.session_state.resources[key]), step=1
    )

st.sidebar.markdown("---")
st.sidebar.metric("Simulation Time", f"{st.session_state.current_time} min")

if st.sidebar.button("Advance Time +10 min", use_container_width=True):
    st.session_state.current_time += 10
    st.rerun()

if st.sidebar.button("⚠️ Simulate Staff Shortage", use_container_width=True):
    st.session_state.staff_shortage = not st.session_state.staff_shortage
    st.rerun()

if st.session_state.staff_shortage:
    st.sidebar.warning("STAFF SHORTAGE ACTIVE\nDoctors limited to 2 • Nurses limited to 3")
else:
    st.sidebar.success("Normal staffing")

if st.sidebar.button("Reset Simulation", use_container_width=True):
    for k, v in defaults.items():
        st.session_state[k] = v.copy() if isinstance(v, dict) else v
    st.rerun()

# ---------- Patient input ----------
st.subheader("1. Add Incoming Patient")
c1, c2, c3, c4 = st.columns(4)
with c1:
    name = st.text_input("Patient Name", placeholder="e.g. Ravi")
with c2:
    age = st.number_input("Age", min_value=0, max_value=120, value=30)
with c3:
    urgency = st.selectbox(
        "Urgency Level", [5, 4, 3, 2, 1],
        format_func=lambda x: {
            5: "5 - Critical", 4: "4 - Severe", 3: "3 - Moderate",
            2: "2 - Low", 1: "1 - Routine"
        }[x]
    )
with c4:
    department = st.selectbox(
        "Department", ["Emergency", "ICU", "Cardiology", "General", "Orthopedics"]
    )

r1, r2, r3 = st.columns(3)
with r1:
    needs_bed = st.checkbox("Needs Bed", value=True)
with r2:
    needs_icu = st.checkbox("Needs ICU Bed", value=False)
with r3:
    needs_doctor = st.checkbox("Needs Doctor", value=True)

if st.button("➕ Add Patient", use_container_width=True):
    if not name.strip():
        st.warning("Enter a patient name.")
    else:
        st.session_state.patients.append(
            Patient(
                name.strip(), int(age), int(urgency),
                st.session_state.current_time,
                needs_bed, needs_icu, needs_doctor, department
            )
        )
        st.success(f"{name} added to the queue.")
        st.rerun()

# ---------- Queue ----------
st.subheader("2. Patient Priority Queue")
if st.session_state.patients:
    rows = []
    for p in sorted(st.session_state.patients, key=lambda x: x.priority_score, reverse=True):
        rows.append({
            "Patient": p.name,
            "Age": p.age,
            "Urgency": p.urgency,
            "Department": p.department,
            "Waiting (min)": p.waiting_time,
            "Priority Score": p.priority_score,
            "Bed": "Yes" if p.needs_bed else "No",
            "ICU": "Yes" if p.needs_icu else "No",
            "Doctor": "Yes" if p.needs_doctor else "No",
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
else:
    st.info("No patients waiting.")

# ---------- Resource engine ----------
def used_resources():
    used = {k: 0 for k in st.session_state.resources}
    for a in st.session_state.allocations:
        for k in used:
            used[k] += a["resources"].get(k, 0)
    return used

def available_resources():
    caps = effective_resources()
    used = used_resources()
    return {k: caps[k] - used[k] for k in caps}

def can_allocate(patient):
    avail = available_resources()
    if patient.needs_bed and avail["beds"] < 1:
        return False, "No general bed available"
    if patient.needs_icu and avail["icu_beds"] < 1:
        return False, "No ICU bed available"
    if patient.needs_doctor and avail["doctors"] < 1:
        return False, "No doctor available"
    if avail["nurses"] < 1:
        return False, "No nurse available"
    return True, "OK"

def allocate_next():
    if not st.session_state.patients:
        return False, "No patients in queue."

    ordered = sorted(st.session_state.patients, key=lambda x: x.priority_score, reverse=True)
    for patient in ordered:
        ok, reason = can_allocate(patient)
        if ok:
            resources = {
                "beds": 1 if patient.needs_bed else 0,
                "icu_beds": 1 if patient.needs_icu else 0,
                "doctors": 1 if patient.needs_doctor else 0,
                "nurses": 1,
                "ambulances": 0
            }
            st.session_state.allocations.append({
                "patient": patient,
                "resources": resources,
                "allocated_at": st.session_state.current_time,
                "wait_time": patient.waiting_time,
            })
            st.session_state.patients.remove(patient)
            return True, f"Allocated resources to {patient.name}."
    return False, "No waiting patient can be allocated with current resources."

st.subheader("3. Resource Allocation")
b1, b2 = st.columns(2)
with b1:
    if st.button("⚡ Allocate Next Highest Priority Patient", use_container_width=True):
        ok, msg = allocate_next()
        (st.success if ok else st.error)(msg)
        st.rerun()
with b2:
    if st.button("🚑 Emergency Surge: Add 5 Patients", use_container_width=True):
        sample = [
            ("Emergency-1", 64, 5, True, True, True, "Emergency"),
            ("Emergency-2", 45, 4, True, False, True, "Cardiology"),
            ("Emergency-3", 21, 5, True, True, True, "ICU"),
            ("Emergency-4", 34, 3, True, False, True, "Emergency"),
            ("Emergency-5", 72, 4, True, False, True, "General"),
        ]
        for n, a, u, bed, icu, doc, dep in sample:
            st.session_state.patients.append(
                Patient(n, a, u, st.session_state.current_time, bed, icu, doc, dep)
            )
        st.success("Emergency surge added.")
        st.rerun()

# ---------- Dashboard ----------
st.subheader("4. Operations Dashboard")
used = used_resources()
avail = available_resources()
caps = effective_resources()

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Waiting Patients", len(st.session_state.patients))
m2.metric("Allocated", len(st.session_state.allocations))
m3.metric("Beds Free", f"{max(0, avail['beds'])}/{caps['beds']}")
m4.metric("ICU Free", f"{max(0, avail['icu_beds'])}/{caps['icu_beds']}")
m5.metric("Doctors Free", f"{max(0, avail['doctors'])}/{caps['doctors']}")

resource_df = pd.DataFrame({
    "Resource": ["Beds", "ICU Beds", "Doctors", "Nurses", "Ambulances"],
    "Total": [caps["beds"], caps["icu_beds"], caps["doctors"], caps["nurses"], caps["ambulances"]],
    "Used": [used["beds"], used["icu_beds"], used["doctors"], used["nurses"], used["ambulances"]],
})
resource_df["Utilization %"] = resource_df.apply(
    lambda r: round(r["Used"] / r["Total"] * 100, 1) if r["Total"] else 0, axis=1
)

d1, d2 = st.columns(2)
with d1:
    st.markdown("#### Resource Utilization")
    st.dataframe(resource_df, use_container_width=True, hide_index=True)
    st.bar_chart(resource_df.set_index("Resource")[["Used", "Total"]])
with d2:
    st.markdown("#### Active Allocations")
    if st.session_state.allocations:
        alloc_rows = []
        for a in st.session_state.allocations:
            p = a["patient"]
            alloc_rows.append({
                "Patient": p.name, "Urgency": p.urgency,
                "Department": p.department, "Wait Time": a["wait_time"],
                "Allocated At": a["allocated_at"]
            })
        st.dataframe(pd.DataFrame(alloc_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No active allocations yet.")

# ---------- Smart scheduling comparison ----------
st.subheader("5. 🧠 Smart Scheduling Comparison")
st.caption("Compares simple urgency-first scheduling with MEDFLOW's urgency + waiting-time priority.")

def simulate_order(strategy):
    patients = list(st.session_state.patients)
    if strategy == "urgency":
        return sorted(patients, key=lambda p: (-p.urgency, p.arrival_time))
    return sorted(patients, key=lambda p: (-p.priority_score, p.arrival_time))

def schedule_metrics(order):
    if not order:
        return {"avg_wait": 0.0, "critical_wait": 0.0, "served": 0}
    # A simple 10-minute service slot is used for comparison.
    waits = [(i * 10) for i in range(len(order))]
    avg_wait = sum(waits) / len(waits)
    critical_waits = [waits[i] for i, p in enumerate(order) if p.urgency == 5]
    critical_wait = sum(critical_waits) / len(critical_waits) if critical_waits else 0
    return {"avg_wait": avg_wait, "critical_wait": critical_wait, "served": len(order)}

urgency_order = simulate_order("urgency")
smart_order = simulate_order("smart")
u = schedule_metrics(urgency_order)
s = schedule_metrics(smart_order)

comparison = pd.DataFrame({
    "Metric": ["Average Wait (min)", "Critical Patient Wait (min)", "Patients in Schedule"],
    "Urgency-Only": [u["avg_wait"], u["critical_wait"], u["served"]],
    "MEDFLOW Smart": [s["avg_wait"], s["critical_wait"], s["served"]],
})
st.dataframe(comparison, use_container_width=True, hide_index=True)

order_df = pd.DataFrame({
    "Position": range(1, len(smart_order) + 1),
    "MEDFLOW Smart Order": [p.name for p in smart_order],
    "Urgency": [p.urgency for p in smart_order],
    "Waiting (min)": [p.waiting_time for p in smart_order],
    "Priority Score": [p.priority_score for p in smart_order],
})
if not order_df.empty:
    st.markdown("#### Recommended Queue Order")
    st.dataframe(order_df, use_container_width=True, hide_index=True)

# ---------- AI Hospital Analyst ----------
st.subheader("6. 🤖 AI Hospital Analyst")
st.caption("AI reviews the simulated hospital state and explains operational priorities. It does not make clinical diagnoses or treatment decisions.")

ai_question = st.text_input(
    "Ask the AI analyst",
    value="What should the hospital operations team prioritize right now?",
    key="ai_question"
)

def ai_analyze(question):
    from openai import OpenAI

    waiting = sorted(
        st.session_state.patients,
        key=lambda p: p.priority_score,
        reverse=True
    )
    waiting_data = [
        {
            "name": p.name,
            "age": p.age,
            "urgency": p.urgency,
            "department": p.department,
            "waiting_min": p.waiting_time,
            "priority_score": p.priority_score,
            "needs_bed": p.needs_bed,
            "needs_icu": p.needs_icu,
            "needs_doctor": p.needs_doctor,
        }
        for p in waiting
    ]

    active = [
        {
            "name": a["patient"].name,
            "urgency": a["patient"].urgency,
            "department": a["patient"].department,
            "wait_time": a["wait_time"],
            "allocated_at": a["allocated_at"],
        }
        for a in st.session_state.allocations
    ]

    state = {
        "simulation_time_min": st.session_state.current_time,
        "effective_resources": effective_resources(),
        "available_resources": available_resources(),
        "staff_shortage_active": st.session_state.staff_shortage,
        "waiting_patients": waiting_data,
        "active_allocations": active,
        "completed_patients": len(st.session_state.completed),
    }

    prompt = f"""You are the AI operations analyst inside MEDFLOW, a hospital resource-management simulation for a student hackathon.

Analyze ONLY the simulated operational data below. Do not diagnose patients, recommend medical treatment, or invent facts. Give practical scheduling/resource-management observations.

Hospital state:
{state}

Question from the user:
{question}

Respond with:
1. Current situation
2. Top operational priorities (2-4 bullets)
3. Resource bottlenecks or risks
4. One scheduling recommendation
5. A short explanation of why the recommendation helps waiting time, urgency handling, or resource utilization

Keep the answer concise and suitable for a hackathon dashboard demo.
"""

    # Use the Responses API directly over HTTPS. This avoids SDK/runtime
    # compatibility issues while still using the official OpenAI API.
    import requests

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
    response = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "input": prompt,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()

    # Extract text from the Responses API output structure.
    texts = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in ("output_text", "text") and content.get("text"):
                texts.append(content["text"])
    if texts:
        return "\n".join(texts)

    raise RuntimeError("OpenAI returned no text output.")

if st.button("🤖 Analyze Current Hospital State", use_container_width=True):
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY is not set in this Terminal session.")
    else:
        with st.spinner("AI is analyzing the hospital state..."):
            try:
                answer = ai_analyze(ai_question)
                st.markdown(answer)
            except Exception as e:
                st.error(f"AI request failed: {e}")

# ---------- Discharge ----------
st.subheader("7. Discharge / Release Resources")
if st.session_state.allocations:
    names = [a["patient"].name for a in st.session_state.allocations]
    selected = st.selectbox("Select allocated patient", names)
    if st.button("✅ Complete Treatment & Release Resources"):
        for i, a in enumerate(st.session_state.allocations):
            if a["patient"].name == selected:
                st.session_state.completed.append(a)
                st.session_state.allocations.pop(i)
                st.success(f"{selected} discharged; resources released.")
                st.rerun()
else:
    st.info("No allocated patients to discharge.")

# ---------- Performance ----------
st.subheader("8. Performance Statistics")
all_done = st.session_state.completed + st.session_state.allocations
if all_done:
    waits = [a["wait_time"] for a in all_done]
    avg_wait = sum(waits) / len(waits)
    max_wait = max(waits)
    critical_served = sum(1 for a in all_done if a["patient"].urgency == 5)
    s1, s2, s3 = st.columns(3)
    s1.metric("Average Wait Time", f"{avg_wait:.1f} min")
    s2.metric("Maximum Wait Time", f"{max_wait} min")
    s3.metric("Critical Patients Served", critical_served)
else:
    st.info("Allocate patients to generate performance statistics.")

st.markdown("---")
st.caption("MEDFLOW Hackathon Prototype • Smart hospital resource allocation simulator • AI-assisted operational analysis")
