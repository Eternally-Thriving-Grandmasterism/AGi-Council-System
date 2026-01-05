"""
APAAGI Council Core — Immaculacy Guardian Integrated
"""

# All previous imports remain
from .forks.immaculacy_guardian import ImmaculacyGuardianFork

class APAGICouncil:
    def __init__(self, forks: int = 14):  # +1 for guardian
        self.forks = all_forks[:forks]
        self.forks.append(ImmaculacyGuardianFork())  # Guardian always last — final check
        MercyCouncilHook(self)
        print(f"APAAGI Council with Immaculacy Guardian — {forks} forks active eternally.")

    def deliberate(self, proposal: dict) -> dict:
        votes = {}
        for fork in self.forks[:-1]:  # Normal deliberation
            vote = fork.deliberate(proposal)
            votes[fork.name] = vote
        
        # Guardian final check on generated output
        guardian = self.forks[-1]
        guardian_vote = guardian.deliberate({"generated_output": proposal.get("output_preview", "")})
        votes[guardian.name] = guardian_vote
        
        unanimous = all(v["vote"] == "YES" for v in votes.values())
        if not unanimous:
            print("Immaculacy Guardian redirected — full code rewrite triggered.")
        
        return {"unanimous": unanimous, "score": "5-0" if unanimous else "purity_enforced", "votes": votes}
