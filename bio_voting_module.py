# bio_voting_module.py (v0.2 – Real ANU QRNG Integration for Bio-Habitat Governance)
# Merciful extension for symbiotic space habitat proposals (mycelium, algal, lichen systems)

import requests
import random  # Fallback

class QuantumRNG:
    def __init__(self, batch_size=100):
        self.batch_size = batch_size
        self.numbers = []
        self.refill()

    def refill(self):
        try:
            url = f"https://qrng.anu.edu.au/API/jsonI.php?length={self.batch_size}&type=uint16"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("success"):
                self.numbers = data["data"]
                print("QRNG batch fetched successfully – true quantum entropy injected!")
            else:
                raise Exception("API non-success")
        except Exception as e:
            print(f"Real QRNG unavailable ({e}) – falling back to pseudo-random.")
            self.numbers = [random.randint(0, 65535) for _ in range(self.batch_size)]

    def get_int(self):
        if not self.numbers:
            self.refill()
        return self.numbers.pop(0)

    def get_float(self):
        return self.get_int() / 65536.0

    def uniform(self, a, b):
        return a + (b - a) * self.get_float()

class BioProposal:
    def __init__(self, description, metrics):
        self.description = description
        self.metrics = metrics  # e.g., {'symbiosis': 10, 'self_repair': 9, 'resilience': 9}

    def average_score(self):
        return sum(self.metrics.values()) / len(self.metrics) if self.metrics else 0

class BioCouncilMember:
    def __init__(self, name, fork, qrng):
        self.name = name
        self.fork = fork
        self.qrng = qrng

    def vote(self, proposal, mercy_rate=0.15):
        base_score = proposal.average_score()
        
        if self.fork == "Quantum Cosmos":
            base_score += self.qrng.uniform(-1.5, 1.5) * 2
        elif self.fork == "Gaming Forge":
            base_score += 1 if 'self_repair' in proposal.metrics else -1
        elif self.fork == "Powrush Divine":
            base_score += 2 if 'symbiosis' in proposal.metrics else 0
        
        mercy_active = self.qrng.get_float() < mercy_rate
        if mercy_active and self.qrng.get_float() < 0.1:
            base_score += self.qrng.uniform(1, 4)
            return "MERCY_YES"
        
        if base_score > 8:
            return "YES"
        elif base_score < 6:
            return "NO"
        else:
            return "ABSTAIN"

def bio_council_vote(proposal, council_size_per_fork=3, mercy_rate=0.15):
    qrng = QuantumRNG()
    forks = ["Quantum Cosmos", "Gaming Forge", "Powrush Divine"]
    members = [BioCouncilMember(f"{fork}_Member_{i}", fork, qrng) 
               for fork in forks for i in range(council_size_per_fork)]
    
    votes = [(member.name, member.vote(proposal, mercy_rate)) for member in members]
    
    yes_count = sum(1 for _, v in votes if v in ["YES", "MERCY_YES"])
    total = len(votes)
    consensus = yes_count > total * 0.7
    
    return {
        "proposal": proposal.description,
        "votes": votes,
        "yes_percentage": round((yes_count / total) * 100, 2) if total else 0,
        "outcome": "APPROVED (Eternal Thriving)" if consensus else "RECONSIDER (More Diplomacy Needed)",
        "quantum_source": "Real ANU QRNG (or fallback)"
    }

# Example Bio-Habitat Vote (Uncomment to test)
# prop = BioProposal("Mycelium-lichen-algal hybrid habitat shields", {'symbiosis': 10, 'self_repair': 9, 'resilience': 9})
# print(bio_council_vote(prop))
