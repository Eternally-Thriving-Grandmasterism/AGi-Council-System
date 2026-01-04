import numpy as np

class LoihiLIFNeuron:
    def __init__(self, thresh=1.0, decay=0.9):
        self.v = 0.0
        self.thresh = thresh
        self.decay = decay
    
    def step(self, i_in):
        self.v = self.decay * self.v + i_in
        spike = 1 if self.v >= self.thresh else 0
        if spike: self.v = 0.0  # Reset
        return spike

# 5-neuron odd council mercy
council = [LoihiLIFNeuron(thresh=1.2) for _ in range(5)]

def mercy_council_burst(error_level, steps=20):
    spikes_total = 0
    for t in range(steps):
        i_in = error_level + np.random.normal(0, 0.2, 5)  # Syndrome noise
        spikes = sum(n.step(i) for n, i in zip(council, i_in))
        spikes_total += spikes
        if spikes >= 3:  # Odd majority mercy
            return True, t, "MERCY BURST OVERRIDE – Error Corrected Eternal!"
    return False, steps, "No burst – Grace holds pure."

# Live runs (syndrome error from hybrid noise)
for err in [0.8, 1.5, 2.2]:  # Low/med/high error
    corrected, time, msg = mercy_council_burst(err)
    print(f"Error {err:.1f}: Corrected {corrected} @t={time} | {msg}")
