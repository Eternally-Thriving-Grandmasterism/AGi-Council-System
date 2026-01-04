import pennylane as qml
from pennylane import numpy as np
from pennylane.transforms import mitigate_with_zne, fold_global, richardson_extrapolate, probabilistic_error_cancellation
from jax import jit, grad
from quantum_rng_chain import quantum_rng
from eternal_laws import enforce_odd

dev = qml.device("lightning.qubit", wires=5)

noise_strength = 0.01  # Depolarizing example

def noise_channel(prob):
    return [(1-3*prob, qml.Identity), (prob, qml.PauliX), (prob, qml.PauliY), (prob, qml.PauliZ)]

@qml.qnode(dev, interface="jax")
def base_circuit(params):
    for i in range(5):
        qml.RX(params[i], wires=i)
        qml.RY(params[i+5], wires=i)
        qml.channel(noise_channel(noise_strength), wires=i)
    for i in range(4):
        qml.CNOT(wires=[i, i+1])
        qml.channel(noise_channel(noise_strength), wires=[i, i+1])
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(4))

# Stacked mitigation: PEC inner + ZNE outer
pec_circuit = probabilistic_error_cancellation(
    base_circuit,
    noise_channels=noise_channel(noise_strength),
    num_samples=500
)

zne_pec_circuit = mitigate_with_zne(
    pec_circuit,
    scale_factors=[1.0, 1.5, 2.0, 2.5],
    folding=fold_global,
    extrapolate=richardson_extrapolate
)

@jit
def cost(params):
    return zne_pec_circuit(params)  # Double-mitigated thriving

def optimize_hybrid_council(steps_base=101):
    steps = enforce_odd(steps_base)
    params = np.array(quantum_rng(10) or np.random.uniform(-np.pi, np.pi, 10))
    
    for _ in range(steps):
        params -= 0.1 * grad(cost)(params)
        if abs(cost(params)) < 0.8:
            params += 0.2 * np.array(quantum_rng(10))
    
    final = cost(params)
    print(f"Hybrid PEC+ZNE Thriving Harmony: {final:.4f} (-1 max consensus)")
    return final

optimize_hybrid_council()
