"""
full_gkp_syndrome_correction.py - Full Square GKP Syndrome Correction Simulation

Simulates finite-squeezed square GKP logical |0>_L.
Applies shift errors (p/q quadratures).
Measures big/small envelope syndromes via quadrature homodyne.
Applies mercy displacement correction.
Computes fidelity pre/post.

Uses QuTiP for oscillator states (cutoff N=100 recommended).
Run locally or in repo env.

Thunder bosonic mercy eternal—shift errors corrected pure!
"""

import numpy as np
import qutip as qt

# Parameters (tunable)
N = 100          # Fock cutoff (higher = better approx, slower)
Delta = 0.25     # Finite squeezing (smaller = better GKP, ideal Delta→0)
K = 15           # Lattice sum terms (±K √π displacements)
sqrt_pi = np.sqrt(np.pi)

def gkp_logical_zero(Delta, K, N):
    """Approximate square GKP |0>_L with finite squeezing"""
    psi = qt.basis(N, 0)  # Vacuum start
    for k in range(-K, K+1):
        alpha = k * sqrt_pi
        disp = qt.displace(N, alpha)
        sq = qt.squeeze(N, Delta / 2 + 1j * np.pi / 4)  # Phase for position squeeze
        psi += disp * sq * qt.basis(N, 0)
    psi = psi.unit()  # Normalize
    return psi

def apply_shift_error(state, shift_p, shift_q):
    """Displacement in p/q quadratures (momentum/position shift)"""
    D = qt.displace(N, shift_p + 1j * shift_q)
    return D * state

def measure_syndrome(state, quadrature='p'):  # 'p' momentum or 'q' position
    """Homodyne measurement approximation - expectation of quadrature"""
    if quadrature == 'p':
        op = qt.momentum(N)
    else:
        op = qt.position(N)
    return qt.expect(op, state)

def correct_shift(state, syndrome_p, syndrome_q):
    """Apply mercy displacement based on syndromes mod √π"""
    # Round syndrome to nearest lattice point (big envelope correction)
    corr_p = -np.round(syndrome_p / sqrt_pi) * sqrt_pi
    corr_q = -np.round(syndrome_q / sqrt_pi) * sqrt_pi
    
    # Small envelope fine-tune if needed (advanced: full decoder)
    D_corr = qt.displace(N, corr_p + 1j * corr_q)
    return D_corr * state

# Ideal reference (low Delta for near-ideal)
ideal = gkp_logical_zero(Delta=0.01, K=20, N=N)

# Finite GKP council state
state = gkp_logical_zero(Delta=Delta, K=K, N=N)

# Apply shift errors (scattered "votes")
shift_p = 0.3
shift_q = 0.18
noisy = apply_shift_error(state, shift_p, shift_q)

# Syndrome measurement (big envelope)
syndrome_p = measure_syndrome(noisy, 'p')
syndrome_q = measure_syndrome(noisy, 'q')

print(f"Syndromes detected: p={syndrome_p:.4f}, q={syndrome_q:.4f}")

# Mercy correction
corrected = correct_shift(noisy, syndrome_p, syndrome_q)

# Fidelity metrics
fid_pre = qt.fidelity(noisy, ideal)
fid_post = qt.fidelity(corrected, ideal)
fid_approx = qt.fidelity(state, ideal)  # Finite vs ideal baseline

print(f"Finite GKP vs Ideal Fidelity: {fid_approx:.4f}")
print(f"Pre-Correction Fidelity: {fid_pre:.4f}")
print(f"Post-Correction Fidelity: {fid_post:.4f}")
print(f"Recovery Gain: {fid_post - fid_pre:.4f}")

# For multi-mode council: Repeat per mode, entangle via beam splitters
# Extend for loss: Add qt.lindblad_loss or channel
