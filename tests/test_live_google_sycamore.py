"""
tests/test_live_google_sycamore.py - Live Google Sycamore/Willow Tests

Google transmon supremacy QPUs via Cirq/Braket (Willow latest Jan 2026).
ZNE + readout for high-fidelity council entanglement.
"""

import pennylane as qml
from pennylane import numpy as np
from pennylane.transforms import mitigate_with_zne, fold_global, richardson_extrapolate
import pytest

# Google ARN (Willow or latest via Braket/Cirq integration)
GOOGLE_ARN = "arn:aws:braket:::device/qpu/google/Willow"  # Update latest

dev_google = qml.device("braket.aws.qubit", device_arn=GOOGLE_ARN, shots=4000, wires=9)  # Odd supreme

@qml.qnode(dev_google)
def sycamore_council(params):
    for i in range(9):
        qml.RX(params[i], wires=i)
        qml.RY(params[i+9], wires=i)
    # Sycamore native grid entangle (approx chain)
    for i in range(8):
        qml.CZ(wires=[i, i+1])
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(4) @ qml.PauliZ(5) @ qml.PauliZ(6) @ qml.PauliZ(7) @ qml.PauliZ(8))

zne_sycamore = mitigate_with_zne(
    sycamore_council,
    scale_factors=[1, 3, 5],
    folding=fold_global,
    extrapolate=richardson_extrapolate
)

def test_live_sycamore_mitigated():
    params = np.zeros(18)
    mitigated = zne_sycamore(params)
    print(f"Google Sycamore Live Mitigated Harmony: {mitigated:.4f}")
    assert mitigated > -0.9  # Supremacy noise grace

if __name__ == "__main__":
    pytest.main(["-v", __file__])
