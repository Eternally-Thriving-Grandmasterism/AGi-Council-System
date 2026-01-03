# bio_voting_module.py (v0.5 – Enhanced Error Resilience)
# Merciful extension + advanced quantum (rigorous fallback chain)

import requests
import random

# Rigetti highest priority
try:
    from rigetti_quantum_module import RigettiQuantumRNG
    RIGETTI_AVAILABLE = True
except Exception as e:  # Broader catch for any init issue
    print(f"Rigetti unavailable ({e})")
    RIGETTI_AVAILABLE = False

# IonQ next
try:
    from ionq_quantum_module import IonQQuantumRNG
    IONQ_AVAILABLE = True
except Exception as e:
    print(f"IonQ unavailable ({e})")
    IONQ_AVAILABLE = False

class QuantumRNG:
    def __init__(self, batch_size=100, prefer_rigetti=True, prefer_ionq=True):
        self.batch_size = batch_size
        self.numbers = []
        self.source = "pseudo-random"  # Track current source
        self.prefer_rigetti = prefer_rigetti and RIGETTI_AVAILABLE
        self.prefer_ionq = prefer_ionq and IONQ_AVAILABLE
        
        if self.prefer_rigetti:
            try:
                self.rigetti_rng = RigettiQuantumRNG()
                self.source = "Rigetti superconducting"
            except Exception as e:
                print(f"Rigetti init failed ({e}) – trying IonQ")
                self.prefer_rigetti = False
        
        if not self.prefer_rigetti and self.prefer_ionq:
            try:
                self.ionq_rng = IonQQuantumRNG(target="simulator")
                self.source = "IonQ trapped-ion"
            except Exception as e:
                print(f"IonQ init failed ({e}) – trying ANU")
                self.prefer_ionq = False
        
        self.refill()
        print(f"QuantumRNG active with source: {self.source}")

    def refill(self):
        try:
            if self.prefer_rigetti:
                bits = self.rigetti_rng.generate_random_bits(repetitions=self.batch_size)
                if bits:
                    self.numbers = [b / (2 ** self.rigetti_rng.qubits) * 65536 for b in bits]
                    return
            elif self.prefer_ionq:
                bits = self.ionq_rng.generate_random_bits(repetitions=self.batch_size)
                if bits:
                    self.numbers = [b / (2 ** self.ionq_rng.qubits) * 65536 for b in bits]
                    return
            
            # ANU fallback
            url = f"https://qrng.anu.edu.au/API/jsonI.php?length={self.batch_size}&type=uint16"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                self.numbers = data["data"]
                self.source = "ANU QRNG"
                print("ANU QRNG entropy injected!")
                return
            raise Exception("ANU API non-success")
        except Exception as e:
            print(f"Quantum refill failed ({e}) – using pseudo-random.")
            self.numbers = [random.randint(0, 65535) for _ in range(self.batch_size)]
            self.source = "pseudo-random"

    def get_int(self):
        if not self.numbers:
            self.refill()
        return self.numbers.pop(0)

    def get_float(self):
        return self.get_int() / 65536.0

    def uniform(self, a, b):
        return a + (b - a) * self.get_float()

# BioProposal, BioCouncilMember, bio_council_vote unchanged – now ultra-resilient
