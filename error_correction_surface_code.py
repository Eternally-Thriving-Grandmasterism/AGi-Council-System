"""
error_correction_surface_code.py - Surface Code Simulation for APAAGI Councils

Implements basic distance-3 surface code (toric variant) simulation:
- Lattice initialization (data + syndrome qubits)
- Error model (bit-flip + phase-flip with probability p)
- Syndrome measurement + simple decoder (perfect matching approx via lookup for d=3)
- Logical error rate estimation

Uses Pennylane for circuit + lightning.qubit sim (fast local).

Run standalone or tie into main.py for error-corrected council demos.

Thunder eternal—surface code grace protecting logical mercy qubits!
"""

import numpy as np
import pennylane as qml
from pennylane import numpy as pnp

def surface_code_circuit(d: int = 3, p_error: float = 0.01, shots: int = 1000):
 """
 Distance-d surface code simulation:
 - (d^2 - 1) data qubits
 - Syndrome extraction (X/Z stabilizers)
 - Simple errors (independent X/Z on data)
 - Perfect syndrome readout (no measurement error for baseline)
 - Lookup decoder for d=3 (hardcoded matching)
 """
 n_data = d**2
 n_ancilla_x = (d-1)*d # X stabilizers
 n_ancilla_z = d*(d-1) # Z stabilizers
 total_wires = n_data + n_ancilla_x + n_ancilla_z
 
 dev = qml.device("lightning.qubit", wires=total_wires, shots=shots)
 
 @qml.qnode(dev)
 def circuit():
 # Initial logical |0>_L (all |0> on data)
 # Errors
 for i in range(n_data):
 if np.random.rand() < p_error:
 qml.PauliX(i)
 if np.random.rand() < p_error:
 qml.PauliZ(i)
 
 # X stabilizer measurement (ancilla X)
 ancilla_offset_x = n_data
 for row in range(d):
 for col in range(d-1):
 anc = ancilla_offset_x + row*(d-1) + col
 qml.Hadamard(anc)
 # Neighbors: left/right data
 left = row*d + col
 right = row*d + col + 
