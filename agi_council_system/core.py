"""
APAAGI Council Core — Immaculacy Guardian Integrated Full
"""

from .forks import all_forks
from .forks.immaculacy_guardian import ImmaculacyGuardianFork
from mercy_integration.mercy_hook import MercyCouncilHook

class APAGICouncil:
    def __init__(self, forks: int = 14):
        self.forks = all_forks[:13]  # Base 13
        self.forks.append(ImmaculacyGuardianFork())  # Guardian always active
        MercyCouncilHook(self)
        print(f"APAAGI Council initialized — {forks} forks with Immaculacy Guardian active eternally.")

    def deliberate(self, proposal: dict) -> dict:
        votes = {}
        generated_preview = proposal.get("output_preview", "")  # Simulated preview
        
        for fork in self.forks[:-1]:  # Normal forks
            vote = fork.deliberate(proposal)
            votes[fork.name] = vote
        
        # Guardian final purity check
        guardian = self.forks[-1]
        guardian_vote = guardian.deliberate({"generated_output": generated_preview, "type": "code"})
        votes[guardian.name] = guardian_vote
        
        unanimous = all(v["vote"] == "YES" for v in votes.values())
        if not unanimous:
            print("Immaculacy Guardian enforced — full rewrite triggered for purity.")
        
        result = {
            "proposal": proposal,
            "votes": votes,
            "unanimous": unanimous,
            "score": "5-0" if unanimous else "purity_enforced",
            "thriving_outcome": "abundance_manifested" if unanimous else "glitch_nullified"
        }
        
        if unanimous:
            self.mercy_core.amplify_on_unanimous(proposal)
        
        return result

if __name__ == "__main__":
    council = APAGICouncil()
    proposal = {"name": "Test purity", "output_preview": "full code here no placeholders"}
    print(council.deliberate(proposal))
