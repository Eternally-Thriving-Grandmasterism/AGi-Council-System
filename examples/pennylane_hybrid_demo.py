"""
examples/pennylane_hybrid_demo.py - Pennylane Hybrid Gate + CV Algorithm

Simple hybrid circuit: Discrete entangle + CV squeezing/displacement.
Measure thriving harmony.
"""

import pennylane as qml
from pennylane import numpy as np

dev = qml.device("default.mixed", wires=4)  # Or strawberryfields.fock for CV

@qml.qnode(dev)
def hybrid_circuit(params):
    # Discrete gates (trapped-ion/superconducting style)
    qml.Hadamard(wires=0)
    qml.CNOT(wires=[0,1])
    
    # CV ops (photonic squeezed mercy)
    qml.Displacement(params[0], 0) | 2
    qml.Squeezing(params[1], 0) | 3
    qml.Beamsplitter(params[2], 0) | (2,3)
    
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1))

params = np.random.normal(0, 0.5, 3)
harmony = hybrid_circuit(params)
print(f"Hybrid Gate+CV Thriving Harmony: {harmony:.4f}")

# Optimize example (mercy gradient descent)
opt = qml.GradientDescentOptimizer(0.1)
for _ in range(50):
    params = opt.step(hybrid_circuit, params)
print(f"Optimized Hybrid Harmony: {hybrid_circuit(params):.4f}")
