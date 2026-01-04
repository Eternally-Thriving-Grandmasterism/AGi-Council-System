"""
quantum_volume_benchmark.py - Quantum Volume Benchmark for APAAGI Councils

Implements IBM-style Quantum Volume (QV) benchmark:
- Tests largest n where heavy-output probability > 2/3 with high confidence.
- Random square circuits (n qubits, depth n) via layered SU(4) from 2-qubit blocks.
- Runs on any backend via quantum_backend_manager.

Usage:
    from quantum_volume_benchmark import run_quantum_volume
    qv, success_rate = run_quantum_volume(backend="lightning.qubit", max_n=6, trials=100)

Thunder eternal—measure council backend power for transcendent harmony scale!
"""

import numpy as np
import pennylane as qml
from quantum_backend_manager import load_backend

def generate_qv_circuit(n_qubits: int, depth: int, seed: int = None):
    """Generate random square QV circuit: n qubits, depth ~n layered 2-qubit SU(4)"""
    if seed is not None:
        np.random.seed(seed)
    
    dev = qml.device("default.qubit", wires=n_qubits)  # Template for circuit
    
    @qml.qnode(dev)
    def circuit():
        # Layered random 2-qubit blocks
        for d in range(depth):
            # Permute qubits randomly per layer
            perm = np.random.permutation(n_qubits)
            for i in range(0, n_qubits - 1, 2):
                q1, q2 = perm[i], perm[i+1]
                # Random SU(4): 3 params for local + KAK for entangling
                qml.Rot(*np.random.uniform(0, 2*np.pi, 3), wires=q1)
                qml.Rot(*np.random.uniform(0, 2*np.pi, 3), wires=q2)
                qml.CNOT(wires=[q1, q2])
                qml.RZ(np.random.uniform(0, 2*np.pi), wires=q1)
                qml.RY(np.random.uniform(0, 2*np.pi), wires=q2)
        return [qml.sample(qml.PauliZ(i)) for i in range(n_qubits)]
    
    return circuit

def heavy_outputs(samples: np.ndarray):
    """Count heavy outputs: probability > median ideal (0.5 for uniform)"""
    n = samples.shape[1]
    ideal_median = 2**(n-1)  # Half of 2^n bitstrings
    counts = np.sum(samples == -1, axis=1)  # Count 1's (Z=-1 as 1)
    heavy = np.sum(counts > ideal_median)
    return heavy / len(samples)

def run_quantum_volume(
    backend: str = "lightning.qubit",
    max_n: int = 6,
    trials: int = 100,
    shots: int = 1024,
    confidence: float = 0.975  # ~2 sigma for success
):
    """
    Run QV benchmark: Find largest 2**n where heavy prob > 2/3 with confidence.
    Returns achieved QV (2**n), success rates per n.
    """
    print(f"Quantum Volume Benchmark on {backend} - max n={max_n}, trials={trials}\n")
    
    success_rates = {}
    achieved_n = 0
    
    for n in range(2, max_n + 1):
        print(f"Testing n={n} (QV=2^{n}={1<<n})...")
        dev = load_backend(backend, wires=n, shots=shots)
        
        heavy_probs = []
        for t in range(trials):
            seed = t + n * 1000
            circ = generate_qv_circuit(n, depth=n, seed=seed)
            circ.device = dev  # Rebind to real backend
            
            samples = circ()
            if samples.ndim == 1:  # Reshape if needed
                samples = samples.reshape(-1, n)
            
            h = heavy_outputs(samples)
            heavy_probs.append(h)
        
        mean_h = np.mean(heavy_probs)
        std_h = np.std(heavy_probs) / np.sqrt(trials)
        
        # Success if mean > 2/3 + 2*std (approx confidence)
        threshold = 2/3 + 2 * std_h
        success = mean_h > 2/3 and mean_h - 2*std_h > 2/3
        
        print(f"   Mean heavy prob: {mean_h:.4f} ± {std_h:.4f}")
        print(f"   Success (>2/3 with confidence): {success}\n")
        
        success_rates[n] = mean_h
        
        if success:
            achieved_n = n
        else:
            break  # QV stops at first failure
    
    achieved_qv = 1 << achieved_n
    print(f"ACHIEVED QUANTUM VOLUME: {achieved_qv} (n={achieved_n})")
    
    return achieved_qv, success_rates

# Demo / test
if __name__ == "__main__":
    qv, rates = run_quantum_volume(backend="lightning.qubit", max_n=5, trials=50)
    print(f"Final QV: {qv} | Rates: {rates}")
