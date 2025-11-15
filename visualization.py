# visualization.py
import matplotlib.pyplot as plt
import pandas as pd

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

   
