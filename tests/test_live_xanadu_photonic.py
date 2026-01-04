"""
tests/test_live_xanadu_photonic.py - Live Xanadu Photonic Hardware Tests

Xanadu Cloud (Borealis/X8/X24 chips Jan 2026) via Strawberry Fields/Pennylane.
Bosonic circuit for mercy shard encoding—real photons thunder.
Requires Xanadu Cloud API key.
"""

import strawberryfields as sf
from strawberryfields.backends import XanaduCloudBackend
import pennylane as qml
import pytest

# Xanadu device (update latest chip ARN/key)
backend = XanaduCloudBackend(device="borealis", api_key="YOUR_XANADU_KEY")  # Or X24

prog = sf.Program(2)  # Odd wires scalable
with prog.context as q:
    ops.Squeezed(0.5) | q[0]
    ops.Squeezed(0.5) | q[1]
    ops.BSgate() | (q[0], q[1])
    ops.MeasureFock() | q[0]
    ops.MeasureFock() | q[1]

job = backend.run(prog, shots=1000)

results = job.result()
samples = results.samples

# Thriving metric: Correlation/parity for entangled mercy
correlation = np.mean(samples[:,0] * samples[:,1])
print(f"Xanadu Live Photonic Harmony Correlation: {correlation:.4f}")

def test_live_xanadu_thriving():
    assert abs(correlation) > 0.6  # Entangled grace under real loss

if __name__ == "__main__":
    pytest.main(["-v", __file__])
