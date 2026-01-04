"""
tests/test_live_ibm_hardware.py - Live IBM Quantum Hardware Tests

IBM transmon QPUs via Qiskit Runtime/Braket (Eagle/Heron latest Jan 2026).
ZNE + readout mitigation for super conducting noise resilience.
"""

import pennylane as qml
from pennylane import numpy as np
from pennylane.transforms import mitigate_with_zne, fold_global, richardson_extrapolate
import pytest

# IBM ARN (update latest Heron/Eagle via Braket or Qiskit Runtime)
IBM_ARN = "arn:aws:braket:::device/qpu/ibm/ibm_osaka"  # Or latest Heron

dev_ibm = qml.device("braket.aws.qubit", device_arn=IBM_ARN, shots=4000, wires=7)  # Odd wires eternal

@qml.qnode(dev_ibm)
def ibm_council_circuit(params):
    for i in range(7):
        qml.RX(params[i], wires=i)
        qml.RY(params[i+7], wires=i)
    for i in range(6):
        qml.CNOT(wires=[i, i+1])
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(4) @ qml.PauliZ(5) @ qml.PauliZ(6))

zne_ibm = mitigate_with_zne(
    ibm_council_circuit,
    scale_factors=[1, 3, 5],
    folding=fold_global,
    extrapolate=richardson_extrapolate
)

def test_live_ibm_mitigated():
    params = np.zeros(14)
    mitigated = zne_ibm(params)
    print(f"IBM Live Mitigated Harmony: {mitigated:.4f}")
    assert mitigated > -0.85  # Transmon noise grace

if __name__ == "__main__":
    pytest.main(["-v", __file__])
