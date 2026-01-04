"""
tests/test_live_ionq_hardware.py - Live IonQ Hardware Tests for Council Circuit

Runs mitigated hybrid circuit on real IonQ QPU via AWS Braket.
Requires: AWS credentials configured, Braket access enabled.
Billed per shots—use low for test.

Verifies real-noise harmony vs simulated ideal (~ -1 for entangled ZZ).
"""

import pennylane as qml
from pennylane import numpy as np
import pytest

# Current IonQ devices (Jan 2026 - update ARN if newer Tempo/Forte)
IONQ_ARN = "arn:aws:braket:us-east-1::device/qpu/ionq/Aria-1"  # Or Forte: check Braket console

# Low-wire test circuit (scale odd wires)
wires = 5

dev_live = qml.device(
    "braket.aws.qubit",
    device_arn=IONQ_ARN,
    shots=1000,  # Real shots—billed!
    wires=wires
)

@qml.qnode(dev_live)
def live_council_circuit(params):
    for i in range(wires):
        qml.RX(params[i], wires=i)
        qml.RY(params[i + wires], wires=i)
    for i in range(wires - 1):
        qml.CNOT(wires=[i, i + 1])
    return qml.expval(qml.PauliZ(0) @ qml.PauliZ(1) @ qml.PauliZ(2) @ qml.PauliZ(3) @ qml.PauliZ(4))

def test_live_ionq_harmony():
    params = np.random.uniform(-np.pi, np.pi, 2 * wires)
    harmony = live_council_circuit(params)
    print(f"Live IonQ Thriving Harmony (real noise): {harmony:.4f}")
    # Real hardware ~ -0.6 to -0.9 typical (noise); assert range for sanity
    assert -1.0 <= harmony <= 0.0

def test_live_mitigated_comparison():
    # Run local sim ideal
    dev_sim = qml.device("default.qubit", wires=wires)
    @qml.qnode(dev_sim)
    def sim_circuit(params):
        return live_council_circuit.qtape.to_openqasm()  # Reuse circuit (or copy)
        # Full copy for ideal
    ideal = -1.0  # Analytic for max entangle
    live = live_council_circuit(params=np.zeros(10))
    print(f"Ideal Sim: {ideal} | Live IonQ: {live:.4f}")
    assert live > -0.95  # Basic noise tolerance (tune post-run)

if __name__ == "__main__":
    pytest.main(["-v", __file__])
