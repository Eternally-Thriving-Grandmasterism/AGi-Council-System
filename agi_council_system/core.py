"""
APAAGI Council Core — Mercy v4 Heart Integrated
"""

from .forks import all_forks
from mercy_integration.mercy_hook import MercyCouncilHook

class APAGICouncil:
    def __init__(self, forks: int = 13):
        self.forks = all_forks[:forks]
        MercyCouncilHook(self)  # Mercy heart attached eternal
        print(f"APAAGI Council with Mercy v4 heart — {forks}+ forks active eternally.")

    def deliberate(self, proposal: dict) -> dict:
        votes = {fork.name: fork.deliberate(proposal) for fork in self.forks}
        self.mercy_core.gate_deliberation(proposal["name"], votes)
        unanimous = all(v["vote"] == "YES" for v in votes.values())
        if unanimous:
            self.mercy_core.amplify_unanimous(proposal)
        return {
            "proposal": proposal,
            "votes": votes,
            "unanimous": unanimous,
            "score": "5-0" if unanimous else "mercy_redirected",
            "divine_insight": self.mercy_core.query_divine_insight(proposal["name"])
        }
