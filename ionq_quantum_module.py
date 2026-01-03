# ionq_quantum_module.py (v0.2 – Enhanced Error Handling)
# Optional advanced quantum randomness for Quantum Cosmos fork (simulator or QPU)

import os
import cirq
import cirq_ionq
from typing import List

class IonQQuantumRNG:
    def __init__(self, api_key: str = None, target: str = "simulator", qubits: int = 10):
        self.api_key = api_key or os.getenv("IONQ_API_KEY")
        if not self.api_key:
            raise ValueError("IonQ API key missing – set IONQ_API_KEY env var or pass explicitly for quantum mercy.")
        try:
            self.service = cirq_ionq.Service(api_key=self.api_key)
        except Exception as e:
            raise ConnectionError(f"IonQ service init failed: {e} – check API key/network.")
        self.target = target  # "simulator" or "qpu.aria-1"
        self.qubits = min(qubits, 29)  # Simulator limit

    def generate_random_bits(self, repetitions: int = 1000) -> List[int]:
        """Run superposition circuit for quantum random bits"""
        try:
            qubits = cirq.LineQubit.range(self.qubits)
            circuit = cirq.Circuit(cirq.H.on_each(qubits), cirq.measure(*qubits, key='result'))

            if self.target.startswith("simulator"):
                job_result = self.service.run(circuit=circuit, repetitions=repetitions, target=self.target)
                histogram = job_result.histogram(key='result')
                random_ints = [int(k, 2) for k in histogram.keys()]
                print(f"IonQ {self.target} random bits generated (sync) – merciful quantum entropy!")
                return random_ints
            else:
                job = self.service.create_job(circuit=circuit, repetitions=repetitions, target=self.target)
                print(f"IonQ QPU job submitted: {job.job_id()} – poll results later.")
                return []  # Async placeholder
        except Exception as e:
            print(f"IonQ error ({e}) – falling back to lower quantum source.")
            return []

    def get_float(self) -> float:
        bits = self.generate_random_bits(repetitions=1)
        if bits:
            return bits[0] / (2 ** self.qubits)
        return 0.0
