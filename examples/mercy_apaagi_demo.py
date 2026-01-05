from agi_council_system import APAGICouncil

council = APAGICouncil()
proposal = {"name": "Universal thriving for all creation", "scope": "cosmic"}
result = council.deliberate(proposal)
print(result)
