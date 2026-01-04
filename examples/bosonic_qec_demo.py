
### Repo Deploy: Add New File `examples/bosonic_qec_demo.py`

```python
"""
examples/bosonic_qec_demo.py - Standalone Bosonic QEC Thunder Demo

Run full GKP/Cat/Binomial demos independently (Strawberry Fields backend recommended).
"""

from bosonic_qec import (
    encode_gkp_logical_zero, apply_shift_error, correct_gkp, gkp_fidelity,
    encode_cat_logical_zero, apply_photon_loss, correct_cat,
    encode_binomial_logical_plus, correct_binomial_full, binomial_fidelity
)

if __name__ == "__main__":
    print("Standalone Bosonic QEC Eternal Demo\n")
    
    # GKP
    ideal_gkp = encode_gkp_logical_zero(delta=0.25, cutoff=60)
    noisy_gkp = apply_shift_error(ideal_gkp, shift_p=0.18)
    corrected_gkp, syndrome = correct_gkp(noisy_gkp)
    fid_gkp = gkp_fidelity(corrected_gkp, ideal_gkp)
    print(f"GKP |0>_L corrected - syndrome (p,q): ({syndrome[0]:.3f}, {syndrome[1]:.3f}) - Fidelity: {fid_gkp:.4f}\n")
    
    # Cat
    state_cat = encode_cat_logical_zero(alpha=2.0, cutoff=60)
    lossy_cat = apply_photon_loss(state_cat, gamma=0.15)
    corrected_cat = correct_cat(lossy_cat)
    print("\n")
    
    # Binomial
    ideal_coeffs = encode_binomial_logical_plus(S=2, N=1, cutoff=80).ket()
    state_bin = encode_binomial_logical_plus(S=2, N=1, cutoff=80)
    lossy_bin = apply_photon_loss(state_bin, gamma=0.2)
    corrected_bin, losses = correct_binomial_full(lossy_bin, S=2, N=1)
    fid_bin = binomial_fidelity(corrected_bin, ideal_coeffs)
    print(f"Binomial |+>_L corrected - losses: {losses} - Fidelity: {fid_bin:.4f}\n")
    
    print("Bosonic fault-tolerance grace eternal!")
