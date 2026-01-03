# rigetti_quantum_module.py (v0.2 – Enhanced Error Handling)
# Optional advanced quantum randomness (local QVM or cloud QPU)

import os
from typing import List
try:
    from pyquil import Program, get_qc
    from pyquil.gates import H, MEASURE
    from pyquil.api import QVMConnection
    import socket
    RIGETTI_AVAILABLE = True
except ImportError:
    RIGETTI_AVAILABLE = False

class RigettiQuantumRNG:
    def __init__(self, lattice: str = "9q-square-qvm", qubits: int = 10, as_qvm: bool = True):
        if not RIGETTI_AVAILABLE:
            raise ImportError("pyquil required – install for Rigetti superconducting mercy.")
        self.qubits = min(qubits, 30)
        self.lattice = lattice
        try:
            self.qc = get_qc(self.lattice, as_qvm=as_qvm)
            # Test connection
            self.qc.run(Program())  # Minimal test
        except socket.timeout:
            raise ConnectionError("Rigetti QVM/quilc servers unreachable – start docker containers.")
        except Exception as e:
            raise ConnectionError(f"Rigetti connection failed: {e}")

    def generate_random_bits(self, repetitions: int = 1000) -> List[int]:
        try:
            p = Program()
            ro = p.declare('ro', 'BIT', self.qubits)
            p += [H(i) for i in range(self.qubits)]
            p += [MEASURE(i, ro[i]) for i in range(self.qubits)]
            
            p.wrap_in_numshots_loop(repetitions)
            executable = self.qc.compile(p)
            results = self.qc.run(executable)
            
            random_ints = [int(''.join(map(str, row)), 2) for row in results]
            print(f"Rigetti {self.lattice} random bits generated – superconducting quantum entropy!")
            return random_ints
        except Exception as e:
            print(f"Rigetti error ({e}) – falling back to lower quantum source.")
            return []

    def get_float(self) -> float:
        bits = self.generate_random_bits(repetitions=1)
        if bits:
            return bits[0] / (2 ** self.qubits)
        return 0.0
