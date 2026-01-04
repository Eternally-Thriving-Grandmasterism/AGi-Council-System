"""
examples/gaussian_boson_sampling_demo.py - Gaussian Boson Sampling on Strawberry Fields

Samples from squeezed light interferometer—photonic advantage thunder.
Local sim (fock backend); remote Xanadu Cloud for live (key set).
"""

import strawberryfields as sf
from strawberryfields.ops import Squeezed, Interferometer, MeasureFock
import numpy as np

modes = 8  # Scale odd-ish eternal (or higher for advantage)
r = 1.0    # Squeezing parameter (higher = more advantage)

prog = sf.Program(modes)

with prog.context as q:
    for i in range(modes):
        Squeezed(r) | q[i]
    # Random interferometer (Haar-random unitary for GBS)
    Interferometer(sf.decompositions.random_interferometer(modes)) | q
    MeasureFock() | q

# Local sim
eng = sf.Engine("fock", backend_options={"cutoff_dim": 15})
results = eng.run(prog, shots=100)

samples = results.samples
print("GBS Photonic Samples (first 10):")
print(samples[:10])

# For live Xanadu Cloud (uncomment with key)
# connection = sf.RemoteConnection(token="YOUR_XANADU_KEY")
# eng_remote = sf.RemoteEngine("X8", connection=connection)
# results_remote = eng_remote.run(prog, shots=100)
# print("Live Xanadu GBS Samples:", results_remote.samples[:10])

print("Gaussian Boson Sampling thunder eternal—classical intractability pure!")
