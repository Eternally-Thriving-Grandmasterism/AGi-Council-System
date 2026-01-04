"""
examples/photonic_xanadu_demo.py - Live Xanadu Photonic Run Demo (Bosonic QEC on Remote)

Run GKP/cat/binomial on Xanadu Cloud (set API key).
Fallback local sim if no key.
"""

import strawberryfields as sf
from strawberryfields.ops import GKP, Catstate, Dgate, LossChannel
from bosonic_qec import correct_gkp, gkp_fidelity  # Reuse metrics

api_key = None  # Set your Xanadu Cloud key here or env

if api_key:
    connection = sf.RemoteConnection(token=api_key)
    eng = sf.RemoteEngine("X8", connection=connection)  # Or latest device
    print("Connected to Xanadu Cloud remote photonic hardware!")
else:
    eng = sf.Engine("fock", backend_options={"cutoff_dim": 60})
    print("Running local photonic simulation (set api_key for real hardware)")

prog = sf.Program(1)

with prog.context as q:
    GKP(state="0", delta=0.25) | q[0]
    Dgate(0.18) | q[0]  # Shift error
    # LossChannel(0.15) for cat/binomial test

state = eng.run(prog).state

# Correction + fidelity (reuse from bosonic_qec)
ideal = sf.Engine("fock", backend_options={"cutoff_dim": 60})
ideal_prog = sf.Program(1)
with ideal_prog.context as q:
    GKP(state="0", delta=0.25) | q[0]
ideal_state = ideal.run(ideal_prog).state

corrected, syndrome = correct_gkp(state)
fid = gkp_fidelity(corrected, ideal_state)

print(f"Photonic GKP demo complete - Fidelity: {fid:.4f} | Syndrome: {syndrome}")

print("Xanadu photonic thunder eternal - bosonic grace on real squeezed light!")
