"""
cat_codes_photonic_mercy.py - Cat Code Mercy for Loss-Tolerant Council

Cat logical |+> (even/odd parity cats).
Photon loss shifts parity—syndrome detects, mercy rotates back.
Multi-mode entangle for council.
"""

import qutip as qt
import numpy as np

alpha = 2.0
cutoff = 80

def cat_plus(alpha):
    coh_plus = qt.coherent(cutoff, alpha)
    coh_minus = qt.coherent(cutoff, -alpha)
    cat = (coh_plus + coh_minus).unit()
    return cat

def apply_loss(cat, gamma=0.15):
    a = qt.destroy(cutoff)
    c_ops = [np.sqrt(gamma) * a]
    result = qt.mesolve(qt.qeye(cutoff), cat, np.linspace(0,1,50), c_ops)
    return result.states[-1]

def parity_syndrome(state):
    # Project even/odd parity
    even = qt.projection(cutoff, range(0,cutoff,2), range(0,cutoff,2))
    odd = qt.projection(cutoff, range(1,cutoff,2), range(1,cutoff,2))
    p_even = qt.expect(even, state)
    return 'even' if p_even > 0.5 else 'odd'

def correct_cat(state, syndrome):
    if syndrome == 'odd':
        # Mercy rotation to even parity
        return qt.phase_gate(np.pi) * state  # Or bit-flip analog
    return state

# Demo
ideal = cat_plus(alpha)
noisy = apply_loss(ideal)
synd = parity_syndrome(noisy)
corrected = correct_cat(noisy, synd)
fid_pre = qt.fidelity(noisy, ideal)
fid_post = qt.fidelity(corrected, ideal)

print(f"Cat Mercy: Pre Fid {fid_pre:.4f} | Post Fid {fid_post:.4f} | Syndrome {synd}")
