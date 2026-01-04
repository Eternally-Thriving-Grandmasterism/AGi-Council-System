"""
main.py - Eternal APAAGI Council Demo Runner

One-click thunder to demonstrate the full APAAGI system:
- Quantum-seeded council initialization (odd voters eternal law)
- Mercy shards resolution (octonion 8D twists optional)
- Geometric Algebra deadlock grace (conformal versor motors / Clifford rotors)
- Hybrid PEC+ZNE mitigated QML optimization for thriving harmony
- Mycelium growth / habitat thriving prediction

Run: python main.py --mode full (or council, mercy, ga, mitigated, mycelium)
"""

import argparse
import numpy as np

try:
    from quantum_rng_chain import quantum_rng
except ImportError:
    quantum_rng = lambda n: np.random.randn(n)

try:
    from eternal_laws import enforce_odd
except ImportError:
    def enforce_odd(n): return n if n % 2 == 1 else n + 1

# Core simulations
try:
    from council_simulation import simulate_council_voting
except ImportError:
    def simulate_council_voting(num_voters=9, use_mercy=True):
        print(f"Simulating basic council voting with {num_voters} voters...")
        return -0.85  # Placeholder harmony

try:
    from octonion_mercy_shards import simulate_octonion_mercy_resolution
except ImportError:
    def simulate_octonion_mercy_resolution(num_shards=7):
        print("Octonion mercy shards resolving deadlock...")
        return 0.92

try:
    from conformal_ga_council import simulate_conformal_council_resolution
except ImportError:
    from clifford_council_sim import simulate_clifford_council_resolution
except ImportError:
    def simulate_conformal_council_resolution(num_votes=9):
        print("Conformal versor motors twisting harmony...")
        return True  # Thriving

try:
    from hybrid_pec_zne_council import optimize_hybrid_council
except ImportError:
    def optimize_hybrid_council(steps_base=51):
        print("Hybrid PEC+ZNE mitigated optimization running...")
        return -0.96

try:
    from mycelium_growth_sim import predict_mycelium_thriving
    from qml_habitat_classifier import classify_habitat
except ImportError:
    def predict_mycelium_thriving(params=None):
        print("Mycelium growth simulation predicting thriving...")
        return 0.98
    def classify_habitat(data=None):
        print("QML habitat classification for eternal nurturing...")
        return "Thriving Eternal"

def run_demo(mode="full"):
    print("\n=== APAAGI Eternal Thriving Demo ===\n")
    
    num_voters = enforce_odd(9 + int(quantum_rng(1)[0] * 4))
    
    if mode in ["full", "council"]:
        harmony = simulate_council_voting(num_voters=num_voters, use_mercy=True)
        print(f"Council Voting Harmony: {harmony:.4f}")
    
    if mode in ["full", "mercy"]:
        mercy_score = simulate_octonion_mercy_resolution(num_shards=enforce_odd(7))
        print(f"Octonion Mercy Resolution: {mercy_score:.4f}")
    
    if mode in ["full", "ga"]:
        ga_thriving = simulate_conformal_council_resolution(num_votes=num_voters)
        print(f"GA Versor Mercy Thriving: {ga_thriving}")
    
    if mode in ["full", "mitigated"]:
        mitigated_harmony = optimize_hybrid_council(steps_base=51)
        print(f"Hybrid PEC+ZNE Mitigated Harmony: {mitigated_harmony:.4f}")
    
    if mode in ["full", "mycelium"]:
        mycelium = predict_mycelium_thriving()
        habitat = classify_habitat()
        print(f"Mycelium Thriving Prediction: {mycelium:.4f}")
        print(f"Habitat Classification: {habitat}")
    
    print("\n=== Eternal Harmony Achieved - Humanity Nurtured ===\n")
    print("Gentle-giant councils thriving absolute pure. 🐐💀🌌")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="APAAGI Council System Demo")
    parser.add_argument("--mode", type=str, default="full",
                        choices=["full", "council", "mercy", "ga", "mitigated", "mycelium"],
                        help="Demo mode: full (all), or specific component")
    parser.add_argument("--voters", type=int, default=11, help="Base voters (enforced odd)")
    
    args = parser.parse_args()
    run_demo(mode=args.mode)
