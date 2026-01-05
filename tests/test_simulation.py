from agi_council_system import APAGICouncil

def test_deliberation():
    council = APAGICouncil(forks=3)  # Test base
    proposal = {"name": "Test"}
    result = council.deliberate(proposal)
    assert result["unanimous"]
