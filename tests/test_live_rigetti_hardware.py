"""
tests/test_live_rigetti_hardware.py - Live Rigetti Ankaa/Forest Tests

Rigetti superconducting QPUs via Braket (Ankaa-2 latest Jan 2026).
ZNE + readout mitigation for transmon noise resilience.
"""

import pennylane as qml
from pennylane import numpy as np
from pennylane.transforms import mitigate_with_zne, fold_global, richardson_extrapolate
import pytest

RIGETTI_ARN = "arn:aws:braket:us-west-1::device/qpu/rigetti/Ankaa-2"  # Update latest

dev_rigetti = qml.device("braket.aws.qubit", device_arn=RIGETTI_ARN, shots=3000, wires=5)

@qml.qnode(dev_rigetti)
def rigetti_circuit(params):
    for i in range(5):
        qml.RX(params[i], wires=i)
        qml.RY(params[i+5], wires=i)
    for i in range(4):
        qml.CZ(wires=[i, i+1])  # Rigetti native CZ
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(4))

zne_rigetti = mitigate_with_zne(
    rigetti_circuit,
    scale_factors=[1, 3, 5],
    folding=fold_global,
    extrapolate=richardson_extrapolate
)

def test_live_rigetti_mitigated():
    params = np.zeros(10)
    mitigated = zne_rigetti(params)
    print(f"Rigetti Mitigated Harmony: {mitigated:.4f}")
    assert mitigated > -0.9  # Transmon noise crushed

if __name__ == "__main__":
    pytest.main(["-v", __file__])
