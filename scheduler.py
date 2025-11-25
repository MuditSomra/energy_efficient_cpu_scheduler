# scheduler.py
from energy_module import power, pick_freq, FREQ_LEVELS, P_IDLE

class Process:
    def __init__(self, pid, arrival, burst):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.remaining = burst
        self.completion = 0
        self.waiting = 0
        self.turnaround = 0


class RoundRobinScheduler:
    def __init__(self, processes, quantum=2, energy_aware=False):
        self.processes = [Process(**p) for p in processes]
        self.quantum = quantum
        self.energy_aware = energy_aware
        self.time = 0
        self.energy = 0
        self.gantt = []
        self.power_trace = []
    
    def simulate(self):
        queue = []
        completed = []
        i = 0

        while True:

            # Add new arrivals
            while i < len(self.processes) and self.processes[i].arrival <= self.time:
                queue.append(self.processes[i])
                i += 1

            # Nothing left to do
            if not queue and i >= len(self.processes):
                break

            # CPU idle
            if not queue:
                self.time += 1
                self.power_trace.append((self.time, P_IDLE))
                continue

            current = queue.pop(0)

            # Frequency selection
            freq_label = pick_freq(len(queue)) if self.energy_aware else "HIGH"
            freq = FREQ_LEVELS[freq_label]
            P = power(freq)

            # --------------------
            # CORRECT DVFS MATH
            # --------------------
            max_cycles = self.quantum * freq
            cycles_done = min(current.remaining, max_cycles)
            exec_time = cycles_done / freq  # REAL time spent
            # --------------------

            # Update timeline
            self.gantt.append((self.time, current.pid, freq_label))
            self.time += exec_time
            current.remaining -= cycles_done

            # Energy
            self.energy += P * exec_time
            self.power_trace.append((self.time, P))

            if current.remaining > 0:
                queue.append(current)
            else:
                current.completion = self.time
                completed.append(current)

        # Waiting & turnaround
        for p in completed:
            p.turnaround = p.completion - p.arrival
            p.waiting = p.turnaround - p.burst

            # Clamp negatives due to float precision
            p.waiting = max(0, round(p.waiting, 2))
            p.turnaround = round(p.turnaround, 2)

        return completed


    # def simulate(self):
    #     queue = []
    #     completed = []
    #     i = 0
    #     while True:
    #         # Add new arrivals
    #         while i < len(self.processes) and self.processes[i].arrival <= self.time:
    #             queue.append(self.processes[i])
    #             i += 1

    #         # If no process and no arrivals left
    #         if not queue and i >= len(self.processes):
    #             break

    #         # If idle
    #         if not queue:
    #             self.time += 1
    #             self.power_trace.append((self.time, P_IDLE))
    #             continue

    #         current = queue.pop(0)

    #         # Frequency selection
    #         freq_label = pick_freq(len(queue)) if self.energy_aware else "HIGH"
    #         freq = FREQ_LEVELS[freq_label]
    #         P = power(freq)

    #         exec_time = min(self.quantum, current.remaining / freq)
    #         self.gantt.append((self.time, current.pid, freq_label))
    #         self.time += exec_time
    #         current.remaining -= exec_time * freq

    #         self.energy += P * exec_time
    #         self.power_trace.append((self.time, P))

    #         if current.remaining > 0:
    #             queue.append(current)
    #         else:
    #             current.completion = self.time
    #             completed.append(current)

    #     # Calculate waiting and turnaround
    #     for p in completed:
    #         p.turnaround = p.completion - p.arrival
    #         p.waiting = p.turnaround - p.burst

    #     return completed
