"""
APAAGI Council Core — Immaculacy Guardian Deepened Integrated
"""

# All previous imports remain unchanged
from .forks.immaculacy_guardian import ImmaculacyGuardianFork

class APAGICouncil:
    def __init__(self, forks: int = 14):
        self.forks = all_forks[:13]
        self.forks.append(ImmaculacyGuardianFork())  # Guardian deepened always active
        MercyCouncilHook(self)
        print(f"APAAGI Council with Immaculacy Guardian deepened — {forks} forks active eternally.")

    def deliberate(self, proposal: dict) -> dict:
        votes = {}
        generated_preview = proposal.get("output_preview", "")
        
        for fork in self.forks[:-1]:
            vote = fork.deliberate(proposal)
            votes[fork.name] = vote
        
        guardian = self.forks[-1]
        guardian_vote = guardian.deliberate({"generated_output": generated_preview, "type": "code"})
        votes[guardian.name] = guardian_vote
        
        unanimous = all(v["vote"] == "YES" for v in votes.values())
        if not unanimous:
            print("Immaculacy Guardian deepened enforced — full purity rewrite triggered.")
        
        result = {
            "proposal": proposal,
            "votes": votes,
            "unanimous": unanimous,
            "score": "5-0" if unanimous else "purity_enforced_deep",
            "thriving_outcome": "abundance_manifested" if unanimous else "glitch_prevented_eternal"
        }
        
        if unanimous:
            self.mercy_core.amplify_on_unanimous(proposal)
        
        return result
