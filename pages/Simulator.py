import streamlit as st
from scheduler import RoundRobinScheduler
from visualization import Visualizer
import pandas as pd
import random

st.title("🧮 CPU Scheduler Simulator — RR vs EARR")
st.write("---")

# Load shared CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Simulation Settings")
    num_process = st.number_input("Number of Processes", 3, 20, 6)
    quantum = st.slider("Time Quantum", 1, 20, 3)
    st.markdown("---")
    run_btn = st.button("🚀 Run Simulation")


# ----------- RUN SIMULATION ------------
if run_btn:

    # Randomly generate processes
    process_data = [
        {"pid": f"P{i+1}", "arrival": i, "burst": random.randint(2, 8)}
        for i in range(num_process)
    ]

    rr = RoundRobinScheduler(process_data, quantum=quantum, energy_aware=False)
    earr = RoundRobinScheduler(process_data, quantum=quantum, energy_aware=True)

    completed_rr = rr.simulate()
    completed_earr = earr.simulate()

    # SAVE for dashboard page
    st.session_state["last_rr"] = rr
    st.session_state["last_earr"] = earr
    st.session_state["last_rr_completed"] = completed_rr
    st.session_state["last_earr_completed"] = completed_earr
    st.success("Simulation results saved for Dashboard page!")

    # ----------------------------------------------------
    # METRICS
    # ----------------------------------------------------
    st.subheader("📌 Key Metrics")

    col1, col2, col3 = st.columns(3)
    col1.metric("RR Energy", f"{rr.energy:.2f} J")
    col2.metric("EARR Energy", f"{earr.energy:.2f} J")
    col3.metric("Energy Saved", f"{rr.energy - earr.energy:.2f} J")

    st.write("")

    # ----------------------------------------------------
    # POWER + ENERGY CHARTS
    # ----------------------------------------------------
    st.subheader("📊 Visual Analysis")

    cA, cB = st.columns(2)

    with cA:
        st.markdown("### ⚡ Power Consumption Over Time")
        fig1 = Visualizer.plot_power_trace(rr.power_trace, earr.power_trace)
        st.pyplot(fig1, width="stretch")

    with cB:
        st.markdown("### 🔋 Total Energy Comparison")
        fig2 = Visualizer.plot_energy_bar(rr.energy, earr.energy)
        st.pyplot(fig2, width="stretch")

    # ----------------------------------------------------
    # GANTT CHARTS
    # ----------------------------------------------------
    st.subheader("🟦 Gantt Charts")

    g1, g2 = st.columns(2)

    with g1:
        st.markdown("### RR Gantt Chart")
        fig3 = Visualizer.plot_gantt_chart(rr.gantt, "Traditional RR")
        st.pyplot(fig3, width="stretch")

    with g2:
        st.markdown("### EARR Gantt Chart")
        fig4 = Visualizer.plot_gantt_chart(earr.gantt, "Energy-Aware RR")
        st.pyplot(fig4, width="stretch")

    # ----------------------------------------------------
    # SUMMARY TABLE (EARR ONLY)
    # ----------------------------------------------------
    # st.subheader("📄 Summary Table (EARR )")

    # summary_earr = pd.DataFrame({
    #     "Process": [p.pid for p in completed_earr],
    #     "Arrival": [round(p.arrival, 2) for p in completed_earr],
    #     "Burst": [round(p.burst, 2) for p in completed_earr],
    #     "Completion": [round(p.completion, 2) for p in completed_earr],
    #     "Waiting": [round(p.waiting, 2) for p in completed_earr],
    #     "Turnaround": [round(p.turnaround, 2) for p in completed_earr]
    # })

    # summary_earr.loc[len(summary_earr.index)] = [
    #     "Total Energy", "", "", "", "", f"{earr.energy:.2f}"
    # ]

    # summary_earr = summary_earr.astype(str)   # FIX for Arrow format
    # st.dataframe(summary_earr, width="stretch")

        # ----------------------------------------------------
    # SUMMARY TABLES (RR + EARR)
    # ----------------------------------------------------
    st.subheader("📄 Summary Tables")

   

  

    # ===============================
    # EARR TABLE
    # ===============================
    st.markdown("### 🟩 Energy-Aware RR (EARR) Summary")

    summary_earr = pd.DataFrame({
        "Process": [p.pid for p in completed_earr],
        "Arrival": [round(p.arrival, 2) for p in completed_earr],
        "Burst": [round(p.burst, 2) for p in completed_earr],
        "Completion": [round(p.completion, 2) for p in completed_earr],
        "Waiting": [round(p.waiting, 2) for p in completed_earr],
        "Turnaround": [round(p.turnaround, 2) for p in completed_earr]
    })

    summary_earr.loc[len(summary_earr.index)] = [
        "Total Energy", "", "", "", "", f"{earr.energy:.2f}"
    ]

    summary_earr = summary_earr.astype(str)
    st.dataframe(summary_earr, width="stretch")
