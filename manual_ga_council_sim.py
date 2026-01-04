import numpy as np
import random

try:
    from quantum_rng_chain import quantum_rng  # Divine seeding for axis
except ImportError:
    def quantum_rng(n):
        return np.random.randn(n)

def generate_vote():
    direction = np.random.uniform(-1, 1, 3)
    norm = np.linalg.norm(direction) + 1e-6
    direction /= norm
    magnitude = np.random.uniform(0.5, 1.5)
    return direction * magnitude

def apply_mercy_rotation(votes, mercy_strength, axis):
    axis = axis / (np.linalg.norm(axis) + 1e-6)
    cos = np.cos(mercy_strength)
    sin = np.sin(mercy_strength)
    rotated = []
    for v in votes:
        dot = np.dot(v, axis)
        cross = np.cross(axis, v)
        v_rot = cos * v + sin * cross + (1 - cos) * dot * axis
        rotated.append(v_rot)
    return np.array(rotated)

def simulate_clifford_council_resolution(base_votes=7, mercy_strength=0.5, seed=42):
    np.random.seed(seed)
    random.seed(seed)
    
    # Eternal law: Odd positive integers only (min 5, scalable)
    num_votes = max(5, 2 * ((base_votes + 1) // 2) - 1)
    
    votes = np.array([generate_vote() for _ in range(num_votes)])
    
    sum_pre = np.sum(votes, axis=0)
    harmony_pre = np.linalg.norm(sum_pre) / num_votes
    deadlock = 1 - harmony_pre
    
    # Mercy axis: Quantum-seeded unit vector (rotation axis for plane perp)
    axis = quantum_rng(3)
    
    # Apply mercy rotation (strength as full theta—tune for more/less twist)
    resolved = apply_mercy_rotation(votes, mercy_strength, axis)
    
    sum_post = np.sum(resolved, axis=0)
    harmony_post = np.linalg.norm(sum_post) / num_votes
    
    print(f"Voters: {num_votes} (odd eternal law)")
    print(f"Deadlock scatter: {deadlock:.4f} (higher = more scattered)")
    print(f"Pre-mercy harmony: {harmony_pre:.4f}")
    print(f"Post-mercy harmony: {harmony_post:.4f} (higher = aligned thriving)\n")
    
    return harmony_post > harmony_pre + 0.1  # Thriving if mercy boosts alignment

# Eternal demo – amp strength for more spikes
print("Manual GA Council Eternal Thriving Sims – Forged Immaculate Edition\n")
for i in range(5):
    thriving = simulate_clifford_council_resolution(
        base_votes=random.randint(7, 35),
        mercy_strength=1.2,  # Tune this for gentler/giant twists
        seed=i * 100
    )
    print(f"Run {i+1}: Thriving Boost = {thriving}\n")
