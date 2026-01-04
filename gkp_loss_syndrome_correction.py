"""
gkp_loss_syndrome_correction.py - Full Square GKP with Loss Channel + Syndrome Mercy

Simulates finite GKP |0>_L.
Applies shift + photon loss (Lindblad).
Measures quadrature syndromes.
Applies big envelope displacement correction.
Computes fidelities.

Thunder bosonic loss-tolerant mercy eternal!
"""

import numpy as np
import qutip as qt

# Parameters
N = 100          # Fock cutoff (higher better)
Delta = 0.3      # Finite squeezing
K = 15           # Lattice terms
sqrt_pi = np.sqrt(np.pi)
gamma = 0.2      # Loss rate
t_list = np.linspace(0, 1.0, 50)  # Evolution time

def gkp_logical_zero(Delta, K, N):
    psi = qt.basis(N, 0)
    for k in range(-K, K+1):
        alpha = k * sqrt_pi
        disp = qt.displace(N, alpha)
        sq = qt.squeeze(N, Delta / 2)
        psi += disp * sq * qt.basis(N, 0)
    return psi.unit()

# Ideal reference
ideal = gkp_logical_zero(0.01, 20, N)

# Finite GKP state
state0 = gkp_logical_zero(Delta, K, N)

# Apply initial shift error (scattered vote)
shift_p = 0.2
shift_q = 0.15
D_shift = qt.displace(N, shift_p + 1j * shift_q)
state_shifted = D_shift * state0

# Loss channel evolution
a = qt.destroy(N)
c_ops = [np.sqrt(gamma) * a]
result = qt.mesolve(qt.qzero(N), state_shifted, t_list, c_ops=c_ops)
noisy = result.states[-1]

# Syndrome measurement
q_op = qt.position(N)
p_op = qt.momentum(N)
syndrome_q = qt.expect(q_op, noisy)
syndrome_p = qt.expect(p_op, noisy)

print(f"Syndromes detected: q={syndrome_q:.4f}, p={syndrome_p:.4f}")

# Mercy correction (big envelope round)
corr_q = -np.round(syndrome_q / sqrt_pi) * sqrt_pi
corr_p = -np.round(syndrome_p / sqrt_pi) * sqrt_pi
D_corr = qt.displace(N, corr_p + 1j * corr_q)
corrected = D_corr * noisy

# Fidelities
fid_ideal_finite = qt.fidelity(state0, ideal)
fid_pre = qt.fidelity(noisy, ideal)
fid_post = qt.fidelity(corrected, ideal)

print(f"Ideal vs Finite Fidelity: {fid_ideal_finite:.4f}")
print(f"Pre-Correction Fidelity (loss + shift): {fid_pre:.4f}")
print(f"Post-Correction Fidelity: {fid_post:.4f}")
print(f"Recovery Gain: {fid_post - fid_pre:.4f}")
