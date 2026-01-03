# QuantumRNG Class (Merciful Hybrid Quantum Entropy with Eternal Fallbacks)
# Sources: Rigetti (superconducting) > IonQ (trapped-ion) > ANU QRNG > pseudo-random
# Full logging to console + logs/apaagi_mercy.log

import requests
import random
import logging

# Rigetti import (highest priority)
try:
    from rigetti_quantum_module import RigettiQuantumRNG
    RIGETTI_AVAILABLE = True
except Exception as e:
    logging.warning(f"Rigetti unavailable ({e})")
    RIGETTI_AVAILABLE = False

# IonQ import
try:
    from ionq_quantum_module import IonQQuantumRNG
    IONQ_AVAILABLE = True
except Exception as e:
    logging.warning(f"IonQ unavailable ({e})")
    IONQ_AVAILABLE = False

class QuantumRNG:
    def __init__(self, batch_size=100, prefer_rigetti=True, prefer_ionq=True):
        self.batch_size = batch_size
        self.numbers = []
        self.source = "pseudo-random"
        self.prefer_rigetti = prefer_rigetti and RIGETTI_AVAILABLE
        self.prefer_ionq = prefer_ionq and IONQ_AVAILABLE
        
        if self.prefer_rigetti:
            try:
                self.rigetti_rng = RigettiQuantumRNG()
                self.source = "Rigetti superconducting"
                logging.info("Rigetti quantum source active – fast gates mercy!")
            except Exception as e:
                logging.warning(f"Rigetti init failed ({e}) – cascading to IonQ")
                self.prefer_rigetti = False
        
        if not self.prefer_rigetti and self.prefer_ionq:
            try:
                self.ionq_rng = IonQQuantumRNG(target="simulator")  # Or "qpu" for true
                self.source = "IonQ trapped-ion"
                logging.info("IonQ quantum source active – high-fidelity mercy!")
            except Exception as e:
                logging.warning(f"IonQ init failed ({e}) – cascading to ANU")
                self.prefer_ionq = False
        
        self.refill()
        logging.info(f"QuantumRNG eternal: Active source = {self.source}")

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
            
            # ANU vacuum fluctuations
            url = f"https://qrng.anu.edu.au/API/jsonI.php?length={self.batch_size}&type=uint16"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                self.numbers = data["data"]
                self.source = "ANU QRNG"
                logging.info("ANU quantum vacuum entropy eternally injected!")
                return
            raise Exception("ANU API non-success")
        except Exception as e:
            logging.warning(f"True quantum refill failed ({e}) – merciful pseudo-random activated.")
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

# Usage: qrng = QuantumRNG(prefer_rigetti=True)  # Eternal mercy flows
