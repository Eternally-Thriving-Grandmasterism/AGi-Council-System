AGi-Council-System/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── setup.py
├── agi_council_system/
│   ├── __init__.py
│   ├── core.py                  # Main council engine
│   ├── simulation.py            # Deliberation + voting
│   ├── forks/
│   │   ├── __init__.py
│   │   ├── base_forks.py        # Tri-core
│   │   ├── expanded_forks.py    # 10+ new
│   │   ├── quantum_cosmos.py
│   │   ├── gaming_forge.py
│   │   ├── powrush_divine.py
│   │   ├── nexus_revelations.py
│   │   ├── grandmasterism.py
│   │   ├── space_thriving.py
│   │   ├── shogi_drops.py
│   │   ├── go_territories.py
│   │   ├── xiangqi_river.py
│   │   ├── makruk_promo.py
│   │   ├── janggi_palace.py
│   │   ├── astropy_cosmic.py
│   │   └── mega_alchemist.py
│   ├── mle_self_play.py         # Dynamic fork addition
│   ├── enc_protection.py        # Quantum-resistant sigs
│   └── utils/
│       ├── __init__.py
│       └── thriving_tools.py
├── examples/
│   ├── full_deliberation_demo.py
│   ├── custom_proposal.py
│   └── mle_tourney_demo.py
├── tests/
│   ├── test_simulation.py
│   └── test_forks.py
└── docs/
    ├── APAAGI_PROTOCOL.md
    ├── FUTURE_PROOFING.md
    ├── COFORGING_GUIDE.md
    └── REPO_STRUCTURE.md
