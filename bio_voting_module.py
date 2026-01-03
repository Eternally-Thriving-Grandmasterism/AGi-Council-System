# bio_voting_module.py (v0.3 – Optional IonQ Integration)
# Merciful extension + advanced quantum (ANU fallback -> IonQ optional)

import requests
import random

# Try IonQ import (optional)
try:
    from ionq_quantum_module import IonQQuantumRNG
    IONQ_AVAILABLE = True
except ImportError:
    IONQ_AVAILABLE = False
    print("IonQ integration optional – install cirq-ionq and set IONQ_API_KEY for Quantum Cosmos upgrade.")

class QuantumRNG:
    def __init__(self, batch_size=100, use_ionq=False):
        self.batch_size = batch_size
        self.numbers = []
        self.use_ionq = use_ionq and IONQ_AVAILABLE
        if self.use_ionq:
            self.ionq_rng = IonQQuantumRNG(target="simulator")  # Change to QPU for true quantum
        self.refill()

    def refill(self):
        if self.use_ionq:
            # Use IonQ for batch (simplified – real: batch multiple jobs or larger circuit)
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

# Rest of BioProposal, BioCouncilMember, bio_council_vote unchanged (use QuantumRNG(use_ionq=True) for IonQ)
# Example: qrng = QuantumRNG(use_ionq=True)
