import random

class BioProposal:
    def __init__(self, description, metrics):
        self.description = description
        self.metrics = metrics  # e.g., {'resilience': 9, 'symbiosis': 10, ...}

    def average_score(self):
        return sum(self.metrics.values()) / len(self.metrics) if self.metrics else 0

class BioCouncilMember:
    def __init__(self, name, fork):
        self.name = name
        self.fork = fork

    def vote(self, proposal, mercy_active=False):
        base_score = proposal.average_score()
        
        if self.fork == "Quantum Cosmos":
            base_score += random.gauss(0, 1.5)
        elif self.fork == "Gaming Forge":
            base_score += 1 if 'self_repair' in proposal.metrics else -1
        elif self.fork == "Powrush Divine":
            base_score += 2 if 'symbiosis' in proposal.metrics else 0
        
        if mercy_active and random.random() < 0.1:
            base_score += random.uniform(1, 4)
            return "MERCY_YES"
        
        if base_score > 8:
            return "YES"
        elif base_score < 6:
            return "NO"
        else:
            return "ABSTAIN"

def bio_council_vote(proposal, council_size_per_fork=3, mercy_rate=0.15):
    forks = ["Quantum Cosmos", "Gaming Forge", "Powrush Divine"]
    members = [BioCouncilMember(f"{fork}_Member_{i}", fork) 
               for fork in forks for i in range(council_size_per_fork)]
    
    votes = [(member.name, member.vote(proposal, random.random() < mercy_rate)) 
             for member in members]
    
    yes_count = sum(1 for _, v in votes if v in ["YES", "MERCY_YES"])
    total = len(votes)
    consensus = yes_count > total * 0.7
    
    return {
        "proposal": proposal.description,
        "votes": votes,
        "yes_percentage": (yes_count / total) * 100 if total else 0,
        "outcome": "APPROVED (Eternal Thriving)" if consensus else "RECONSIDER (More Diplomacy Needed)"
    }
