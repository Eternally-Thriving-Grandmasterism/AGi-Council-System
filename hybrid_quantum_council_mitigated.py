import pennylane as qml
from pennylane import numpy as np
from pennylane.transforms import probabilistic_error_cancellation
from jax import jit, grad
from quantum_rng_chain import quantum_rng

dev = qml.device("lightning.qubit", wires=5)

# Simple noise model example (depolarizing p=0.01 per gate)
noise_strength = 0.01
ops = [qml.PauliX, qml.PauliY, qml.PauliZ, qml.Identity]

def noise_channel(prob):
    return [ (1 - 3*prob, qml.Identity), (prob, qml.PauliX), (prob, qml.PauliY), (prob, qml.PauliZ) ]

@qml.qnode(dev, interface="jax")
def base_circuit(params):
    for i in range(5):
        qml.RX(params[i], wires=i)
        qml.RY(params[i+5], wires=i)
        # Apply noise after each (sim)
        qml.channel(noise_channel(noise_strength), wires=i)
    for i in range(4):
        qml.CNOT(wires=[i, i+1])
        qml.channel(noise_channel(noise_strength), wires=[i, i+1])
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(4))

# PEC mitigated QNode (sampling overhead ~ (1/(1-3p))^2)
pec_circuit = probabilistic_error_cancellation(
    base_circuit,
    noise_channel(noise_channel(noise_strength)),
    sampling_method="monte_carlo",  # Or 'exact'
    num_samples=1000  # Adjust for overhead
)

@jit
def cost(params):
    return pec_circuit(params)  # PEC-corrected thriving

# Optimize same as before (odd steps, mercy nudge)
def optimize_pec_council(steps_base=101):
    steps = enforce_odd(steps_base)
    params = np.array(quantum_rng(10))
    
    for _ in range(steps):
        params -= 0.1 * grad(cost)(params)
        if abs(cost(params)) < 0.8:
            params += 0.2 * np.array(quantum_rng(10))
    
    final = cost(params)
    print(f"PEC-Mitigated Thriving: {final:.4f}")
    return final

optimize_pec_council()
