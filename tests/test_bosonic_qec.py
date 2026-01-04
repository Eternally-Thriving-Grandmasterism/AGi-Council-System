"""
tests/test_bosonic_qec.py - Unit Tests for Bosonic QEC Fidelity Metrics

Uses pytest to verify:
- GKP fidelity recovery after shift correction
- Binomial fidelity after loss detection/recovery
- Basic encoding sanity (mean photons, overlap ~1 for ideal)

Run: pytest tests/test_bosonic_qec.py -v

Thunder eternal—fault-tolerant fidelity verified pure!
"""

import numpy as np
import pytest
from bosonic_qec import (
    encode_gkp_logical_zero, apply_shift_error, correct_gkp, gkp_fidelity,
    encode_binomial_logical_plus, apply_photon_loss, correct_binomial_full, binomial_fidelity
)

@pytest.mark.parametrize("delta, epsilon, shift_p, expected_fid_min", [
    (0.25, 0.0, 0.0, 0.99),      # Ideal no noise
    (0.25, 0.05, 0.1, 0.85),     # Small noise + correction
    (0.3, 0.1, 0.18, 0.70),      # Larger noise, lower recovery
])
def test_gkp_fidelity_recovery(delta, epsilon, shift_p, expected_fid_min):
    cutoff = 60
    
    ideal = encode_gkp_logical_zero(delta=delta, epsilon=epsilon, cutoff=cutoff)
    
    noisy = apply_shift_error(ideal, shift_p=shift_p, shift_q=0.05)
    
    corrected, _ = correct_gkp(noisy)
    
    fid = gkp_fidelity(corrected, ideal)
    
    print(f"GKP test - delta={delta}, shift={shift_p} - Fidelity: {fid:.4f}")
    assert fid >= expected_fid_min, f"Fidelity {fid:.4f} below threshold {expected_fid_min}"

def test_gkp_ideal_fidelity():
    state = encode_gkp_logical_zero(delta=0.25, cutoff=60)
    fid = gkp_fidelity(state, state)
    assert np.isclose(fid, 1.0, atol=1e-4), "Ideal GKP fidelity not ~1"

@pytest.mark.parametrize("S, N, gamma, expected_fid_min", [
    (2, 1, 0.0, 0.99),     # No loss
    (2, 1, 0.1, 0.75),     # Small loss + detection
    (3, 1, 0.2, 0.65),     # Larger code, better protection
])
def test_binomial_fidelity_recovery(S, N, gamma, expected_fid_min):
    cutoff = 100
    
    ideal_state = encode_binomial_logical_plus(S=S, N=N, cutoff=cutoff)
    ideal_coeffs = ideal_state.ket()  # For reference
    
    noisy = apply_photon_loss(ideal_state, gamma=gamma)
    
    corrected, _ = correct_binomial_full(noisy, S=S, N=N)
    
    fid = binomial_fidelity(corrected, ideal_coeffs)
    
    print(f"Binomial test - S={S}, N={N}, gamma={gamma} - Fidelity: {fid:.4f}")
    assert fid >= expected_fid_min, f"Fidelity {fid:.4f} below threshold {expected_fid_min}"

def test_binomial_ideal_fidelity():
    state = encode_binomial_logical_plus(S=2, N=1, cutoff=80)
    coeffs = state.ket()
    fid = binomial_fidelity(state, coeffs)
    assert np.isclose(fid, 1.0, atol=1e-4), "Ideal binomial fidelity not ~1"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
