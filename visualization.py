# visualization.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

class Visualizer:
    @staticmethod
    def plot_power_trace(power_trace_rr, power_trace_earr):
        df_rr = pd.DataFrame(power_trace_rr, columns=["time", "power"])
        df_earr = pd.DataFrame(power_trace_earr, columns=["time", "power"])
        plt.figure(figsize=(8, 4))
        plt.plot(df_rr["time"], df_rr["power"], label="Traditional RR", linestyle="--")
        plt.plot(df_earr["time"], df_earr["power"], label="Energy-Aware RR")
        plt.xlabel("Time (ms)")
        plt.ylabel("Power (W)")
        plt.title("Power Consumption Over Time")
        plt.legend()
        plt.show()

    @staticmethod
    def plot_energy_bar(energy_rr, energy_earr):
        plt.figure(figsize=(5, 4))
        plt.bar(["Traditional RR", "Energy-Aware RR"], [energy_rr, energy_earr], color=["red", "green"])
        plt.title("Total Energy Consumption Comparison")
        plt.ylabel("Energy (Joules)")
        plt.show()

    @staticmethod
    def plot_gantt_chart(gantt, title):
        plt.figure(figsize=(8, 2))
        colors = {"LOW": "green", "MED": "orange", "HIGH": "red"}
        for start, pid, freq in gantt:
            plt.barh(y=pid, width=1, left=start, color=colors.get(freq, "blue"))
        plt.title(f"Gantt Chart - {title}")
        plt.xlabel("Time (ms)")
        plt.ylabel("Process ID")
        plt.show()

    def generate_dashboard(rr, earr, completed_rr, completed_earr):
    # Compute averages
        def avg_metrics(completed):
            avg_wait = sum(p.waiting for p in completed) / len(completed)
            avg_turn = sum(p.turnaround for p in completed) / len(completed)
            return avg_wait, avg_turn

        avg_wait_rr, avg_turn_rr = avg_metrics(completed_rr)
        avg_wait_earr, avg_turn_earr = avg_metrics(completed_earr)

        # Comparison DataFrame
        comparison_df = pd.DataFrame({
            "Metric": ["Avg Waiting Time", "Avg Turnaround Time", "Total Energy (J)"],
            "Traditional RR": [round(avg_wait_rr, 2), round(avg_turn_rr, 2), round(rr.energy, 2)],
            "Energy-Aware RR": [round(avg_wait_earr, 2), round(avg_turn_earr, 2), round(earr.energy, 2)]
        })

        # 2x2 Dashboard Layout
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Energy-Aware Round Robin vs Traditional Round Robin - Dashboard", fontsize=16, fontweight='bold')

        # 1️⃣ POWER vs TIME (Top-left)
        df_rr = pd.DataFrame(rr.power_trace, columns=["time", "power"])
        df_earr = pd.DataFrame(earr.power_trace, columns=["time", "power"])

        axs[0, 0].plot(df_rr["time"], df_rr["power"], linestyle="--", label="Traditional RR")
        axs[0, 0].plot(df_earr["time"], df_earr["power"], label="EARR")
        axs[0, 0].set_title("Power Consumption Over Time")
        axs[0, 0].set_xlabel("Time (ms)")
        axs[0, 0].set_ylabel("Power (W)")
        axs[0, 0].legend()

        # 2️⃣ ENERGY BAR (Top-right)
        axs[0, 1].bar(["Traditional RR", "EARR"], [rr.energy, earr.energy], color=["red", "green"])
        axs[0, 1].set_title("Total Energy Consumption")
        axs[0, 1].set_ylabel("Energy (J)")

        # 3️⃣ PERFORMANCE COMPARISON (Bottom-left)
        labels = ["Avg Waiting", "Avg Turnaround"]
        rr_values = [avg_wait_rr, avg_turn_rr]
        earr_values = [avg_wait_earr, avg_turn_earr]

        x = np.arange(len(labels))
        width = 0.35

        axs[1, 0].bar(x - width/2, rr_values, width, label='Traditional RR')
        axs[1, 0].bar(x + width/2, earr_values, width, label='EARR')
        axs[1, 0].set_xticks(x)
        axs[1, 0].set_xticklabels(labels)
        axs[1, 0].set_title("Performance Comparison")
        axs[1, 0].set_ylabel("Time (ms)")
        axs[1, 0].legend()

        # 4️⃣ SUMMARY TABLE (Bottom-right)
        axs[1, 1].axis('off')
        table = axs[1, 1].table(
            cellText=comparison_df.values,
            colLabels=comparison_df.columns,
            cellLoc='center',
            loc='center'
        )
        table.scale(1, 2)
        axs[1, 1].set_title("Summary Table")

        plt.tight_layout()
        plt.show()


# Call the dashboard function