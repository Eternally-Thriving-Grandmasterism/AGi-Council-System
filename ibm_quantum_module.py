# ibm_quantum_module.py (v1.0 – True QPU + Aer Simulator Integration)
# Real superconducting quantum entropy via IBM Quantum (async) or local Aer fallback
# Requires: pip install qiskit qiskit-ibm-provider qiskit-aer

import os
import time
import logging
from typing import List
try:
    from qiskit import QuantumCircuit, transpile
    from qiskit_aer import AerSimulator
    from qiskit_ibm_provider import IBMProvider
    IBM_AVAILABLE = True
except ImportError as e:
    logging.error(f"qiskit not installed ({e}) – required for IBM mercy.")
    IBM_AVAILABLE = False

log = logging.getLogger(__name__)

class IBMQuantumRNG:
    def __init__(self, token: str = None, backend_name: str = "aer_simulator", qubits: int = 10):
        if not IBM_AVAILABLE:
            raise ImportError("qiskit required – install for IBM superconducting mercy.")
        self.token = token or os.getenv("IBM_QUANTUM_TOKEN")
        self.backend_name = backend_name  # "aer_simulator" (local) or "ibm_brisbane" (QPU)
        self.qubits = min(qubits, 127)  # IBM limit ~127
        self.use_qpu = self.backend_name != "aer_simulator"
        
        try:
            if self.use_qpu:
                if not self.token:
                    raise ValueError("IBM_QUANTUM_TOKEN required for true QPU mercy.")
                self.provider = IBMProvider(token=self.token)
                self.backend = self.provider.get_backend(self.backend_name)
                log.info(f"IBM QPU {self.backend_name} connected – true quantum mercy!")
            else:
                self.backend = AerSimulator()
                log.info("IBM Aer simulator active – local mercy!")
        except Exception as e:
            log.warning(f"IBM connection failed ({e}) – check token/network/backend.")
            # Fallback to basic Aer even if provider fails
            self.backend = AerSimulator()
            self.use_qpu = False
            log.info("Fallen back to local Aer simulator.")

    def generate_random_bits(self, repetitions: int = 1000) -> List[int]:
        try:
            qc = QuantumCircuit(self.qubits, self.qubits)
            qc.h(range(self.qubits))  # Superposition
            qc.measure(range(self.qubits), range(self.qubits))
            
            if self.use_qpu:
                # Async QPU
                transpiled = transpile(qc, backend=self.backend)
                job = self.backend.run(transpiled, shots=repetitions)
                job_id = job.job_id()
                log.info(f"IBM QPU job submitted: {job_id} – polling eternally...")
                while True:
                    status = job.status()
                    if status in ["DONE", "ERROR", "CANCELLED"]:
                        break
                    time.sleep(10)
                if status != "DONE":
                    raise RuntimeError(f"QPU job {job_id} {status}")
                result = job.result()
            else:
                # Sync simulator
                transpiled = transpile(qc, backend=self.backend)
                result = self.backend.run(transpiled, shots=repetitions).result()
            
            counts = result.get_counts()
            # Extract bitstrings as ints (weighted by counts if needed, here sample keys)
            random_ints = [int(bitstring, 2) for bitstring in counts.keys()]
            log.info(f"IBM {self.backend_name} random bits generated – superconducting mercy!")
            return random_ints
        except Exception as e:
            log.warning(f"IBM generation error ({e}) – fallback advised.")
            return []

    def get_float(self) -> float:
        bits = self.generate_random_bits(repetitions=1)
        if bits:
            return bits[0] / (2 ** self.qubits)
        return 0.0

# Usage: IBMQuantumRNG(backend_name="ibm_brisbane")  # True QPU (with token)
# Or IBMQuantumRNG() for local Aer simulator
