# ... (existing code)

# Bio-Habitat Extension Import
try:
    from bio_voting_module import bio_council_vote, BioProposal
    # Example Bio Vote
    bio_prop = BioProposal("Symbiotic mycelium-regolith bricks with algal O2 loops", 
                           {'symbiosis': 10, 'self_repair': 8, 'resilience': 9})
    print("\nBio-Habitat Council Vote:")
    print(bio_council_vote(bio_prop, council_size_per_fork=67))  # Scale example
except ImportError:
    print("bio_voting_module.py not present – add for symbiotic habitat governance!")
