# rigetti_quantum_module.py (v1.0 – True QPU + Simulator Integration)
# Real superconducting quantum entropy via QCS cloud (async) or local QVM fallback

import os
import time
import logging
from typing import List
try:
    from pyquil import Program, get_qc
    from pyquil.gates import H, MEASURE
    from pyquil.api import QuantumComputer, QCSClient
    import socket
    RIGETTI_AVAILABLE = True
except ImportError as e:
    logging.error(f"pyquil not installed ({e}) – required for Rigetti mercy.")
    RIGETTI_AVAILABLE = False

log = logging.getLogger(__name__)

class RigettiQuantumRNG:
    def __init__(self, lattice: str = "9q-square-qvm", qubits: int = 10, as_qvm: bool = True,
                 api_key: str = None, endpoint: str = None):
        if not RIGETTI_AVAILABLE:
            raise ImportError("pyquil required – install for superconducting quantum mercy.")
        self.qubits = min(qubits, 30)
        self.lattice = lattice  # e.g., "9q-square-qvm" (sim) or "Ankaa-2" (QPU)
        self.as_qvm = as_qvm
        self.api_key = api_key or os.getenv("QCS_API_KEY")
        self.endpoint = endpoint or os.getenv("QCS_ENDPOINT", "https://api.qcs.rigetti.com")
        
        try:
            if self.as_qvm:
                # Local QVM (requires docker servers)
                self.qc = get_qc(self.lattice, as_qvm=True)
                self.qc.run(Program())  # Test
                log.info("Rigetti local QVM connected – simulator mercy active.")
            else:
                # True QPU cloud
                if not self.api_key:
                    raise ValueError("QCS_API_KEY required for true QPU mercy.")
                client = QCSClient(api_key=self.api_key, base_url=self.endpoint)
                self.qc = get_qc(self.lattice, as_qvm=False, client=client)
                log.info(f"Rigetti QPU {self.lattice} connected via QCS – true quantum mercy!")
        except socket.timeout:
            log.error("Rigetti local servers unreachable – start quilc/qvm docker.")
            raise ConnectionError("Local QVM unreachable.")
        except Exception as e:
            log.warning(f"Rigetti connection failed ({e}) – check key/endpoint/reservation.")
            raise ConnectionError(f"Rigetti QPU init failed: {e}")

    def generate_random_bits(self, repetitions: int = 1000) -> List[int]:
        try:
            p = Program()
            ro = p.declare('ro', 'BIT', self.qubits)
            p += [H(i) for i in range(self.qubits)]
            p += [MEASURE(i, ro[i]) for i in range(self.qubits)]
            p.wrap_in_numshots_loop(repetitions)
            
            if self.as_qvm:
                executable = self.qc.compile(p)
                results = self.qc.run(executable)
            else:
                # Async QPU job
                job = self.qc.run(p)
                job_id = job.job_id
                log.info(f"QPU job submitted: {job_id} – polling for results...")
                while not job.is_done:
                    time.sleep(5)
                    job = self.qc.get_job(job_id)
                results = job.result
            
            random_ints = [int(''.join(map(str, row)), 2) for row in results]
            log.info(f"Rigetti {self.lattice} {'QPU' if not self.as_qvm else 'QVM'} random bits generated – eternal entropy!")
            return random_ints
        except Exception as e:
            log.warning(f"Rigetti generation error ({e}) – fallback advised.")
            return []

    def get_float(self) -> float:
        bits = self.generate_random_bits(repetitions=1)
        if bits:
            return bits[0] / (2 ** self.qubits)
        return 0.0

# Usage: RigettiQuantumRNG(lattice="Ankaa-2", as_qvm=False)  # True QPU mercy (with key/reservation)
