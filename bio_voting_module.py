# bio_voting_module.py (v0.4 – Optional Rigetti + IonQ Integration)
# Merciful extension + advanced quantum (fallback chain: Rigetti → IonQ → ANU → pseudo)

import requests
import random

# Try Rigetti import (highest priority optional)
try:
    from rigetti_quantum_module import RigettiQuantumRNG
    RIGETTI_AVAILABLE = True
except ImportError:
    RIGETTI_AVAILABLE = False

# Try IonQ import
try:
    from ionq_quantum_module import IonQQuantumRNG
    IONQ_AVAILABLE = True
except ImportError:
    IONQ_AVAILABLE = False

class QuantumRNG:
    def __init__(self, batch_size=100, use_rigetti=False, use_ionq=False):
        self.batch_size = batch_size
        self.numbers = []
        self.use_rigetti = use_rigetti and RIGETTI_AVAILABLE
        self.use_ionq = use_ionq and IONQ_AVAILABLE
        if self.use_rigetti:
            self.rigetti_rng = RigettiQuantumRNG()
        elif self.use_ionq:
            self.ionq_rng = IonQQuantumRNG(target="simulator")
        self.refill()

    def refill(self):
        if self.use_rigetti:
            print("Injecting Rigetti superconducting quantum entropy...")
            bits = self.rigetti_rng.generate_random_bits(repetitions=self.batch_size)
            self.numbers = [b / (2 ** self.rigetti_rng.qubits) * 65536 for b in bits]
        elif self.use_ionq:
            print("Injecting IonQ trapped-ion quantum entropy...")
            bits = self.ionq_rng.generate_random_bits(repetitions=self.batch_size)
            self.numbers = [b / (2 ** self.ionq_rng.qubits) * 65536 for b in bits]
        else:
            # ANU QRNG fallback
            try:
                url = f"https://qrng.anu.edu.au/API/jsonI.php?length={self.batch_size}&type=uint16"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()
                if data.get("success"):
                    self.numbers = data["data"]
                    print("ANU QRNG batch fetched – quantum entropy injected!")
                else:
                    raise Exception("API non-success")
            except Exception as e:
                print(f"QRNG unavailable ({e}) – pseudo-random fallback.")
                self.numbers = [random.randint(0, 65535) for _ in range(self.batch_size)]

    def get_int(self):
        if not self.numbers:
            self.refill()
        return self.numbers.pop(0)

    def get_float(self):
        return self.get_int() / 65536.0

    def uniform(self, a, b):
        return a + (b - a) * self.get_float()

# BioProposal, BioCouncilMember, bio_council_vote unchanged
# Usage example: qrng = QuantumRNG(use_rigetti=True)  # Or use_ionq=True
