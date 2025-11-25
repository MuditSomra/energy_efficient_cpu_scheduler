import streamlit as st
from scheduler import RoundRobinScheduler
from visualization import Visualizer
import pandas as pd
import random

# Load shared CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.title("📊 Full Comparative Dashboard")
st.write("---")

st.info("💡 Run the simulation from the **Simulator page**. This page only shows the full dashboard.")

if "last_rr" in st.session_state:
    rr = st.session_state["last_rr"]
    earr = st.session_state["last_earr"]
    completed_rr = st.session_state["last_rr_completed"]
    completed_earr = st.session_state["last_earr_completed"]

    fig = Visualizer.generate_dashboard(rr, earr, completed_rr, completed_earr)
    st.pyplot(fig, use_container_width=True)

else:
    st.warning("⚠️ No simulation found. Please run a simulation first.")
