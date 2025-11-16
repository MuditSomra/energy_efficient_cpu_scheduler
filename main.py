# main.py
from scheduler import RoundRobinScheduler
from visualization import Visualizer
import pandas as pd
import random

# Input data (could also be read from CSV)
process_data = [{"pid": f"P{i+1}", "arrival": i, "burst": random.randint(2, 8)} for i in range(8)]




# Run schedulers
rr = RoundRobinScheduler(process_data, quantum=2, energy_aware=False)
earr = RoundRobinScheduler(process_data, quantum=2, energy_aware=True)

completed_rr = rr.simulate()
completed_earr = earr.simulate()

# Visualization
Visualizer.plot_power_trace(rr.power_trace, earr.power_trace)
Visualizer.plot_energy_bar(rr.energy, earr.energy)
Visualizer.plot_gantt_chart(rr.gantt, "Traditional RR")
Visualizer.plot_gantt_chart(earr.gantt, "Energy-Aware RR")
Visualizer.generate_dashboard(rr, earr, completed_rr,completed_earr)

# Summary table
summary = pd.DataFrame({
    "Process": [p.pid for p in completed_earr],
    "Arrival": [p.arrival for p in completed_earr],
    "Burst": [p.burst for p in completed_earr],
    "Completion": [round(p.completion, 2) for p in completed_earr],
    "Waiting": [round(p.waiting, 2) for p in completed_earr],
    "Turnaround": [round(p.turnaround, 2) for p in completed_earr],
})
summary.loc[len(summary.index)] = ["Total Energy (J)", "-", "-", "-", "-", f"{earr.energy:.2f}"]

print(summary)
