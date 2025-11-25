import streamlit as st

st.set_page_config(page_title="CPU Scheduler", layout="wide")

# Load custom CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------- HEADER --------------------------
st.title("⚙️ CPU Scheduler Simulation Suite")
st.markdown("### A Modern Interactive Visualization of Round Robin & Energy-Aware Scheduling")
st.write("---")

# ---------------------- INTRO ---------------------------
st.markdown("""
## 👋 Welcome!

This platform helps you **visualize, compare, and understand**  
how CPU scheduling works when we introduce **energy-saving techniques like DVFS**.

Use the sidebar to explore:
- 🎛 **Simulator** — Run RR & Energy-Aware RR  
- 📊 **Dashboard** — Compare performance & energy usage  
- 📘 **About** — Documentation  
""")

st.write("---")

# ============================================================
#                   EXPLANATION SECTION
# ============================================================

st.markdown("""
# 🧠 What Problem Are We Solving?

Traditional Round Robin (RR) scheduling always runs the CPU at **full speed**.  
But modern processors don't work like that — they **dynamically change CPU frequency**  
to save energy when workload is low.

This technique is called:

## ⚡ Dynamic Voltage & Frequency Scaling (DVFS)

Our project shows:

- How changing CPU frequency affects execution time  
- How energy consumption changes  
- What trade-off exists between speed & battery life  
- How Round Robin behaves under realistic CPU conditions  
""")

st.markdown("---")

# ------------------------------------------------------------
st.markdown("""
# 🛠 How Our Simulator Works

### ✔ 1. Each process has:
- Arrival time  
- Burst time (in **CPU cycles**)  
- Remaining cycles  

### ✔ 2. CPU gives a fixed **time quantum** (like Round Robin)

### ✔ 3. CPU frequency changes based on queue size:
- **More processes → HIGH freq (fast but high power)**  
- **Few processes → LOW freq (slow but energy-saving)**  

### ✔ 4. Frequency decides how many cycles CPU can finish per quantum.

Example (Quantum = 2 ms):

| Mode | Frequency | Cycles per ms | Work done in quantum |
|------|-----------|----------------|----------------------|
| HIGH | 2 cycles/ms | 2 | **4 cycles** |
| LOW  | 1 cycle/ms  | 1 | **2 cycles** |

Faster CPU → finishes earlier but wastes more energy  
Slower CPU → finishes later but saves energy
""")

# ------------------------------------------------------------
st.markdown("""
# 🔍 Key Formulas Used in the Simulation

### **1. Maximum cycles CPU can execute in one quantum:**
            max_cycles = quantum × frequency

### **2. Actual execution time**
            exec_time = cycles_done / frequency

### **3. Energy consumed**
            energy = power × exec_time

### **4. Power follows real DVFS physics (approximation)**
            power = k * frequency³ + P_IDLE

*Higher frequency → exponentially higher power consumption.*
""")



            
        
