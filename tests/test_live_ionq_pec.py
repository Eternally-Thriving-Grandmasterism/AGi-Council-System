"""
tests/test_live_ionq_pec.py - Live IonQ PEC Mitigation Tests

Probabilistic Error Cancellation on real IonQ QPU.
Requires noise channel cal (depolarizing approx or full tomography—run separate cal job).
High sampling overhead—start low shots.
"""

import pennylane as qml
from pennylane import numpy as np
from pennylane.transforms import probabilistic_error_cancellation
import pytest

IONQ_ARN = "arn:aws:braket:us-east-1::device/qpu/ionq/Aria-1"

dev_live = qml.device("braket.aws.qubit", device_arn=IONQ_ARN, shots=5000, wires=5)  # Higher for PEC variance

# Approx depolarizing channel (real: learn from cal data)
noise_p = 0.02
def ionq_noise(prob):
    return [(1-3*prob, qml.Identity), (prob, qml.PauliX), (prob, qml.PauliY), (prob, qml.PauliZ)]

@qml.qnode(dev_live)
def base_circuit(params):
    for i in range(5):
        qml.RX(params[i], wires=i)
        qml.RY(params[i+5], wires=i)
    for i in range(4):
        qml.CNOT(wires=[i, i+1])
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(4))

pec_circuit = probabilistic_error_cancellation(
    base_circuit,
    noise_channels=ionq_noise(noise_p),
    num_samples=2000  # Overhead control—scale odd
)

def test_live_ionq_pec_harmony():
    params = np.random.uniform(-np.pi, np.pi, 10)
    raw = base_circuit(params)
    pec = pec_circuit(params)
    print(f"Raw IonQ: {raw:.4f} | PEC Mitigated: {pec:.4f}")
    assert pec > raw + 0.05  # Cancellation grace

if __name__ == "__main__":
    pytest.main(["-v", __file__])
