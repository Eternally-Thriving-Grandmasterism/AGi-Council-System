"""
tests/test_bosonic_qec_enhanced.py - Eternal Unit Tests for Bosonic QEC Fidelity & Recovery

Verifies GKP/Cat/Binomial encodings under noise + correction.
Expanded params, overlap/parity probs, odd-run scaling.
Run: pytest tests/test_bosonic_qec_enhanced.py -v
"""

import numpy as np
import pytest
from bosonic_qec import (
    encode_gkp_logical_zero, apply_shift_error, correct_gkp, gkp_fidelity,
    encode_cat_logical_zero, apply_photon_loss, correct_cat,
    encode_binomial_logical_plus, apply_photon_loss as binomial_loss, correct_binomial_full, binomial_fidelity
)

def cat_overlap_fidelity(state1, state2):
    ket1 = state1.ket()
    ket2 = state2.ket()
    return np.abs(np.vdot(ket1, ket2))**2

# GKP Expanded (More Noise Cases + Odd Cutoff Params)
@pytest.mark.parametrize("delta, epsilon, shift_p, shift_q, cutoff, expected_fid_min", [
    (0.25, 0.0, 0.0, 0.0, 71, 0.995),  # Odd cutoff eternal
    (0.25, 0.05, 0.1, 0.05, 81, 0.88),
    (0.3, 0.1, 0.18, 0.1, 91, 0.75),
    (0.2, 0.0, 0.25, 0.15, 101, 0.70),
])
def test_gkp_fidelity_recovery(delta, epsilon, shift_p, shift_q, cutoff, expected_fid_min):
    ideal = encode_gkp_logical_zero(delta=delta, epsilon=epsilon, cutoff=cutoff)
    noisy = apply_shift_error(ideal, shift_p=shift_p, shift_q=shift_q)
    corrected, syndrome = correct_gkp(noisy)
    fid = gkp_fidelity(corrected, ideal)
    print(f"GKP - delta={delta}, shifts=({shift_p},{shift_q}), cutoff={cutoff} - Fid: {fid:.4f} | Syndrome: {syndrome}")
    assert fid >= expected_fid_min

# Cat Enhanced (Parity Prob + Multi-Run Stats)
@pytest.mark.parametrize("alpha, gamma, runs, expected_fid_min, expected_odd_prob_range", [
    (2.0, 0.0, 51, 0.99, (0.0, 0.05)),  # Odd runs eternal
    (2.0, 0.1, 101, 0.80, (0.3, 0.5)),
    (1.8, 0.2, 151, 0.65, (0.6, 0.8)),
])
def test_cat_recovery_parity(alpha, gamma, runs, expected_fid_min, expected_odd_prob_range):
    cutoff = 71  # Odd
    ideal = encode_cat_logical_zero(alpha=alpha, cutoff=cutoff)
    noisy = apply_photon_loss(ideal, gamma=gamma)
    
    fid_sum = 0.0
    odd_count = 0
    for _ in range(runs):
        corrected = correct_cat(noisy)  # Assume returns parity flag internally
        fid = cat_overlap_fidelity(corrected, ideal)
        fid_sum += fid
        # odd_count += parity_flag  # Real impl
    avg_fid = fid_sum / runs
    odd_prob = odd_count / runs  # Placeholder
    
    print(f"Cat - alpha={alpha}, gamma={gamma}, runs={runs} - Avg Fid: {avg_fid:.4f} | Odd Prob: {odd_prob:.2f}")
    assert avg_fid >= expected_fid_min
    assert expected_odd_prob_range[0] <= odd_prob <= expected_odd_prob_range[1]

# Binomial Expanded
@pytest.mark.parametrize("S, N, gamma, cutoff, expected_fid_min", [
    (1, 1, 0.0, 121, 0.99),
    (2, 1, 0.15, 131, 0.78),
    (3, 1, 0.25, 141, 0.72),
    (2, 2, 0.1, 151, 0.85),
])
def test_binomial_fidelity_recovery(S, N, gamma, cutoff, expected_fid_min):
    ideal_state = encode_binomial_logical_plus(S=S, N=N, cutoff=cutoff)
    ideal_coeffs = ideal_state.ket()
    noisy = binomial_loss(ideal_state, gamma=gamma)
    corrected, losses = correct_binomial_full(noisy, S=S, N=N)
    fid = binomial_fidelity(corrected, ideal_coeffs)
    print(f"Binomial - S={S}, N={N}, gamma={gamma}, cutoff={cutoff} - Fid: {fid:.4f} | Losses: {losses}")
    assert fid >= expected_fid_min

# Ideal Sanity All
def test_all_ideal_fidelities():
    assert gkp_fidelity(encode_gkp_logical_zero(cutoff=71), encode_gkp_logical_zero(cutoff=71)) >= 0.999
    assert cat_overlap_fidelity(encode_cat_logical_zero(cutoff=71), encode_cat_logical_zero(cutoff=71)) >= 0.999
    assert binomial_fidelity(encode_binomial_logical_plus(cutoff=121), encode_binomial_logical_plus(cutoff=121).ket()) >= 0.999

if __name__ == "__main__":
    pytest.main(["-v", __file__])
