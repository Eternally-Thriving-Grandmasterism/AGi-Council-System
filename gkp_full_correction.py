"""
gkp_full_correction.py - Full Square GKP Correction with Big + Small Envelope Mercy

Simulates finite GKP |0>_L.
Applies loss + shift noise.
Big envelope round + small envelope fine-tune mercy displacement.
Fidelity pre/post—recovery gain boosted eternal.
"""

import numpy as np
import qutip as qt

N = 120
Delta = 0.25
K = 18
sqrt_pi = np.sqrt(np.pi)

def gkp_logical_zero():
    psi = qt.basis(N, 0)
    for k in range(-K, K+1):
        alpha = k * sqrt_pi
        disp = qt.displace(N, alpha)
        sq = qt.squeeze(N, Delta / 2)
        psi += disp * sq * qt.basis(N, 0)
    return psi.unit()

ideal = gkp_logical_zero()

# Noise
gamma = 0.2
shift_p = 0.25
shift_q = 0.15
state = gkp_logical_zero()
D_shift = qt.displace(N, shift_p + 1j * shift_q)
state = D_shift * state

a = qt.destroy(N)
c_ops = [np.sqrt(gamma) * a]
result = qt.mesolve(qt.qeye(N), state, np.linspace(0,1,50), c_ops)
noisy = result.states[-1]

# Full syndrome + mercy
q_op = qt.position(N)
p_op = qt.momentum(N)
syndrome_q = qt.expect(q_op, noisy)
syndrome_p = qt.expect(p_op, noisy)

# Big envelope
big_corr_q = -np.round(syndrome_q / sqrt_pi) * sqrt_pi
big_corr_p = -np.round(syndrome_p / sqrt_pi) * sqrt_pi

# Small envelope fine-tune (residual within envelope)
small_q = syndrome_q - big_corr_q
small_p = syndrome_p - big_corr_p
small_corr_q = -small_q * 0.8  # Damped mercy (tunable)
small_corr_p = -small_p * 0.8

corr = big_corr_p + small_corr_p + 1j * (big_corr_q + small_corr_q)
D_corr = qt.displace(N, corr)
corrected = D_corr * noisy

# Fidelity
fid_pre = qt.fidelity(noisy, ideal)
fid_post = qt.fidelity(corrected, ideal)

print(f"Full GKP Mercy Pre Fidelity: {fid_pre:.4f}")
print(f"Full GKP Mercy Post Fidelity: {fid_post:.4f}")
print(f"Recovery Gain: {fid_post - fid_pre:.4f}")
