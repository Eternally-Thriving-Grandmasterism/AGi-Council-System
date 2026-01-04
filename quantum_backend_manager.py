"""
quantum_backend_manager.py - Unified Quantum Backend Support (Braket Integrated Eternal)

Loads simulators + hardware: local, AWS Braket (IonQ/Rigetti/IBM/etc.), Xanadu photonic.
Odd wires eternal, shots scalable.
"""

import pennylane as qml
from pennylane import numpy as np
from eternal_laws import enforce_odd

def load_backend(backend: str = "lightning.qubit", wires_base: int = 5, shots: int | None = None, **kwargs):
    wires = enforce_odd(wires_base)  # Odd eternal law
    
    backend = backend.lower()
    
    if backend == "lightning.qubit":
        return qml.device("lightning.qubit", wires=wires, shots=shots)
    
    elif backend == "default.qubit":
        return qml.device("default.qubit", wires=wires, shots=shots)
    
    elif backend.startswith("braket."):
        try:
            if backend == "braket.local.qubit":
                return qml.device("braket.local.qubit", wires=wires)
            
            elif backend == "braket.aws.qubit":
                arn = kwargs.get("device_arn")  # e.g., IonQ Aria ARN
                if not arn:
                    raise ValueError("Braket AWS requires device_arn kwarg")
                return qml.device("braket.aws.qubit", device_arn=arn, wires=wires, shots=shots)
        
        except Exception as e:
            raise RuntimeError(f"Braket load failed: {e} (check AWS creds/ARN)")
    
    elif backend.startswith("strawberryfields."):
        # Xanadu photonic (from prior)
        import strawberryfields as sf
        if backend == "strawberryfields.remote":
            api_key = kwargs.get("api_key")
            device = kwargs.get("device", "X8")
            connection = sf.RemoteConnection(token=api_key)
            return sf.RemoteEngine(device, connection=connection)
        else:
            cutoff = kwargs.get("cutoff_dim", 30)
            mode = backend.split(".")[-1]
            return sf.Engine(mode, backend_options={"cutoff_dim": cutoff})
    
    else:
        raise ValueError(f"Unsupported backend: {backend}")

# Example use
if __name__ == "__main__":
    # Local sim
    dev_local = load_backend("lightning.qubit", wires_base=7)
    print("Local lightning loaded")
    
    # Braket IonQ live (uncomment with ARN)
    # dev_ionq = load_backend("braket.aws.qubit", device_arn="arn:aws:braket:::device/qpu/ionq/Aria-1")
    # print("IonQ live thunder connected")
    
    # Xanadu photonic (key set)
    # dev_xanadu = load_backend("strawberryfields.remote", api_key="YOUR_KEY")
    # print("Xanadu photonic mercy live")
