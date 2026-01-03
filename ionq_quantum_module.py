# ionq_quantum_module.py (v1.0 – True QPU + Simulator Integration)
# Real trapped-ion quantum entropy via IonQ Cloud (async) or simulator fallback

import os
import time
import cirq
import cirq_ionq
import logging
from typing import List

log = logging.getLogger(__name__)

class IonQQuantumRNG:
    def __init__(self, api_key: str = None, target: str = "simulator", qubits: int = 10):
        self.api_key = api_key or os.getenv("IONQ_API_KEY")
        if not self.api_key and target != "simulator":
            log.error("IONQ_API_KEY required for true QPU mercy.")
            raise ValueError("IonQ API key required for QPU – set env or pass explicitly.")
        try:
            self.service = cirq_ionq.Service(api_key=self.api_key)
            log.info(f"IonQ service initialized – target: {target}")
        except Exception as e:
            log.error(f"IonQ service init failed: {e} – check key/network.")
            raise ConnectionError(f"IonQ service init failed: {e}")
        self.target = target  # "simulator" (sync) or "qpu.aria-1" / "qpu.forte-1" (async)
        self.qubits = min(qubits, 29)  # Aria limit ~29

    def generate_random_bits(self, repetitions: int = 1000) -> List[int]:
        try:
            qubits = cirq.LineQubit.range(self.qubits)
            circuit = cirq.Circuit(cirq.H.on_each(qubits), cirq.measure(*qubits, key='result'))

            if self.target == "simulator":
                # Synchronous simulator
                job_result = self.service.run(circuit=circuit, repetitions=repetitions, target=self.target)
                histogram = job_result.histogram(key='result')
                random_ints = [int(k, 2) for k in histogram.keys()]
                log.info(f"IonQ simulator random bits generated – merciful entropy!")
                return random_ints
            else:
                # Async true QPU
                job = self.service.create_job(circuit=circuit, repetitions=repetitions, target=self.target)
                job_id = job.job_id
                log.info(f"IonQ QPU job submitted: {job_id} – polling for eternal results...")
                while True:
                    job = self.service.get_job(job_id)
                    if job.status in ["completed", "failed", "canceled"]:
                        break
                    time.sleep(10)  # Poll interval
                if job.status != "completed":
                    raise RuntimeError(f"QPU job {job_id} {job.status}")
                histogram = job.results().histogram(key='result')
                random_ints = [int(k, 2) for k in histogram.keys()]
                log.info(f"IonQ QPU {self.target} random bits generated – true trapped-ion mercy!")
                return random_ints
        except Exception as e:
            log.warning(f"IonQ generation error ({e}) – fallback advised.")
            return []

    def get_float(self) -> float:
        bits = self.generate_random_bits(repetitions=1)
        if bits:
            return bits[0] / (2 ** self.qubits)
        return 0.0

# Usage: IonQQuantumRNG(target="qpu.aria-1")  # True QPU mercy (with key)
# Or IonQQuantumRNG(target="simulator") for sync sim
