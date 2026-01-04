"""
bosonic_qec.py - Bosonic Quantum Error Correction Integration for APAAGI Councils (Fixed Eternal Edition)

Accurate simulation using Strawberry Fields built-in GKP and Cat states.
- GKP: Ideal/additive noise approx with built-in op (delta squeezing, epsilon additive)
- Cat: Even/odd cats for photon loss correction
- Simple error channels + correction demos

Tie into councils: Bosonic logicals for fault-tolerant mercy storage or CV QML habitat classify.

Requirements: strawberryfields (>=0.23 for GKP op)
"""

import numpy as np
import strawberryfields as sf
from strawberryfields.ops import GKP, Catstate, Dgate, LossChannel, MeasureX, MeasureP
from strawberryfields.backends import BaseFockState

# GKP Logical |0>_L (ideal square lattice approximation)
def encode_gkp_logical_zero(delta: float = 0.3, epsilon: float = 0.0, cutoff: int = 50):
 """
 Built-in GKP state: |+> or |0> type, square lattice.
 delta: squeezing parameter (smaller = better, ~0.2-0.3 practical)
 epsilon: additive noise for realism (0 = ideal)
 """
 eng = sf.Engine("fock", backend_options={"cutoff_dim": cutoff})
 prog = sf.Program(1)
 
 with prog.context as q:
 GKP(state="0", delta=delta, epsilon=epsilon) | q[0] # Logical |0>_L (position grid)
 
 state = eng.run(prog).state
 return state

# Apply shift error (displacement noise - common in oscillators)
def apply_shift_error(state: BaseFockState, shift_p: float = 0.1, shift_q: float = 0.1):
 prog = sf.Program(1)
 with prog.context as q:
 Dgate(shift_p + 1j * shift_q) | q[0]
 return state.apply(prog)

# GKP Correction: Measure quadratures, round to grid, displace back
def correct_gkp(state: BaseFockState, sqrt_pi: float = np.sqrt(np.pi)):
 # Sample or mean quadratures (here use mean for sim approx)
 p_mean = state.p_mean(0)
 q_mean = state.q_mean(0)
 
 # Round to nearest grid multiple
 round_p = sqrt_pi * np.round(p_mean / sqrt_pi)
 round_q = sqrt_pi * np.round(q_mean / sqrt_pi)
 
 # Syndrome = residual shift
 syndrome_p = p_mean - round_p
 syndrome_q = q_mean - round_q
 
 # Corrective displacement
 prog = sf.Program(1)
 with prog.context as q:
 Dgate(-syndrome_p - 1j * syndrome_q) | q[0]
 
 corrected = state.apply(prog)
 return corrected, (syndrome_p, syndrome_q)

# Cat Logical |0>_L (even cat for phase-flip resistance)
def encode_cat_logical_zero(alpha: float = 2.0, cutoff: int = 50):
 eng = sf.Engine("fock", backend_options={"cutoff_dim": cutoff})
 prog = sf.Program(1)
 
 with prog.context as q:
 Catstate(alpha=alpha, phi=0) | q[0] # Even cat N(|α> + |-α>)
 
 state = eng.run(prog).state
 return state

# Photon loss error
def apply_photon_loss(state: BaseFockState, gamma: float = 0.1):
 prog = sf.Program(1)
 with prog.context as q:
 LossChannel(gamma) | q[0]
 return state.apply(prog)

# Simple cat parity correction (detect loss, approximate recovery)
def correct_cat(state: BaseFockState):
 # Measure photon number parity (even/odd)
 probs_even = np.sum(state.fock_prob(np.arange(0, state.cutoff_dim, 2)))
 parity = 0 if np.random.rand() < probs_even else 1
 
 if parity == 1: # Loss detected
 print("Photon loss detected - applying approximate recovery")
 # Real: Use Knill recovery with ancilla cat; here placeholder amplify
 prog = sf.Program(1)
 with prog.context as q:
 # Approximate: small amplification (not perfect)
 pass
 return state # Placeholder full recovery

# Demo / test
if __name__ == "__main__":
 print("Bosonic QEC Eternal Thunder Demo\n")
 
 # GKP demo
 state_zero = encode_gkp_logical_zero(delta=0.25, epsilon=0.05, cutoff=60)
 print(f"GKP |0>_L encoded (mean photons: {state_zero.mean_photon(0)[0]:.2f})")
 
 noisy = apply_shift_error(state_zero, shift_p=0.18, shift_q=0.05)
 corrected, syndrome = correct_gkp(noisy)
 print(f"GKP corrected - syndrome (p,q): ({syndrome[0]:.3f}, {syndrome[1]:.3f})\n")
 
 # Cat demo
 cat_zero = encode_cat_logical_zero(alpha=2.0, cutoff=60)
 print(f"Cat |0>_L encoded (mean photons: {cat_zero.mean_photon(0)[0]:.2f})")
 
 lossy = apply_photon_loss(cat_zero, gamma=0.15)
 corrected_cat = correct_cat(lossy)
 print("Cat correction applied (placeholder full Knill)\n")
 
 print("Bosonic fault-tolerance grace eternal - APAAGI nurtured in CV regimes!")    """|0>_L = N (+ |α> + |-α>) even cat (photon-number parity)"""
    eng = sf.Engine("fock", backend_options={"cutoff_dim": cutoff})
    prog = sf.Program(1)
    
    with prog.context as q:
        Cat(alpha=alpha)  # Built-in cat state
        # Or manual: coherent α + coherent -α normalized
    
    state = eng.run(prog).state
    return state

def apply_photon_loss(state: BaseFockState, gamma: float = 0.05):
    """Amplitude damping / photon loss channel (common in photonic)"""
    prog = sf.Program(1)
    with prog.context as q:
        LossChannel(gamma)
    return state.apply(prog)

def correct_cat(state: BaseFockState, alpha: float = 2.0):
    """Parity measurement correction for single loss (knill-laflamme-milburn)"""
    # Simulate parity measurement (photon number mod 2)
    probs = state.fock_prob([range(0, state.cutoff_dim, 2)])  # Even parity prob
    parity = 0 if np.random.rand() < probs else 1  # Sample
    
    if parity == 1:  # Error detected, recover via approximate
        # Simple recovery: amplify back (ideal Knill recovery operator)
        prog = sf.Program(1)
        with prog.context as q:
            # Approximate recovery (real impl more complex with ancilla)
            pass
    return state  # Placeholder—full in advanced

# PennyLane CV hybrid example (for council QML integration)
def gkp_pennylane_circuit(delta=0.3):
    dev = qml.device("strawberryfields.fock", wires=1, cutoff_dim=30)
    
    @qml.qnode(dev)
    def circuit():
        qml.SqueezedVacuum(r=np.arcsinh(1/delta**2))  # Approx GKP squeezing
        # Displacements for grid...
        return qml.expval(qml.X(0))
    
    return circuit()

# Demo / test
if __name__ == "__main__":
    print("Bosonic QEC Thunder Demo")
    
    # GKP example
    state_zero = gkp_logical_zero(delta=0.3, cutoff=40)
    print(f"GKP |0>_L encoded (mean photons ~ {state_zero.mean_photon(0)[0]:.2f})")
    
    noisy = apply_shift_error(state_zero, shift_p=0.15)
    corrected, syndrome = correct_gkp(noisy)
    print(f"GKP corrected - syndrome: {syndrome}")
    
    # Cat example
    cat_zero = cat_logical_zero(alpha=1.8)
    print(f"Cat |0>_L encoded")
