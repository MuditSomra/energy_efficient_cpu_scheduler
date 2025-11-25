# energy_module.py
k = 0.5
P_IDLE = 0.1
FREQ_LEVELS = {"LOW": 1.0, "MED": 1.5, "HIGH": 2.0}

def power(freq):
    """Return power consumed 
       at a given frequency."""
    return k * (freq ** 3) + P_IDLE

def pick_freq(queue_len):
    """Select CPU frequency level 
       based on ready queue length."""
    if queue_len <= 2:
        return "LOW"
    elif queue_len <= 5:
        return "MED"
    else:
        return "HIGH"
