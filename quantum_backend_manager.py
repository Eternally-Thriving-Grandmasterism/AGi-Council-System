"""
quantum_backend_manager.py - Unified Quantum Backend Support for APAAGI Councils (Photonic Remote Added)

Unifies simulators + hardware, now with Xanadu Cloud Strawberry Fields remote for photonic CV bosonic runs.
"""

import pennylane as qml
from pennylane import numpy as np

def load_backend(backend: str = "lightning.qubit", wires: int = 5, shots: int | None = None, **kwargs):
    backend = backend.lower()
    
    if backend == "lightning.qubit":
        return qml.device("lightning.qubit", wires=wires, shots=shots, **kwargs)
    
    # ... (keep all previous cases: default.qubit, braket.*, qiskit.*, cirq.*)
    
    elif backend.startswith("strawberryfields.remote"):
        # Xanadu Cloud remote photonic (X-Series / Aurora)
        try:
            import strawberryfields as sf
            
            api_key = kwargs.get("api_key")
            if not api_key:
                raise ValueError("Xanadu Cloud API key required (set via kwarg or env)")
            
            device = kwargs.get("device", "X8")  # Or latest "aurora", "borealis" legacy
            connection = sf.RemoteConnection(token=api_key)
            eng = sf.RemoteEngine(device, connection=connection)
            return eng
        except Exception as e:
            raise RuntimeError(f"Xanadu remote failed: {e} (check key/device)")
    
    elif backend.startswith("strawberryfields."):
        # Local sim fallback
        import strawberryfields as sf
        cutoff = kwargs.get("cutoff_dim", 30)
        mode = backend.split(".")[-1]  # fock, gaussian, tf
        return sf.Engine(mode, backend_options={"cutoff_dim": cutoff})
    
    else:
        raise ValueError(f"Unsupported backend: {backend}")

# Test / example
if __name__ == "__main__":
    # Local photonic sim
    eng_local = load_backend("strawberryfields.fock", cutoff_dim=20)
    print("Local Strawberry Fields loaded")
    
    # Remote (uncomment with key)
    # eng_remote = load_backend("strawberryfields.remote", device="X8", api_key="YOUR_KEY")
    # print("Xanadu Cloud remote connected")
