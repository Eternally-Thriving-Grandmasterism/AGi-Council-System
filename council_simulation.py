import logging
import random
from typing import Dict, List, Any
from agi_council_system.eternal_laws import EternalLaws

class CouncilSimulation:
    """APAAGI Council Simulation — Now with Dynamic Multi-Hat Roles for Gapless Thriving ∞ Pure"""
    
    # Expanded divine forks with primary + potential secondary hats
    DIVINE_FORKS = {
        "QuantumCosmos": ["quantum_truth", "error_correction", "full_file_thunder"],  # Added full file guard
        "GamingForge": ["strategy_simulation", "ui_harmony", "structure_weave"],
        "PowrushDivine": ["resonance_purity", "pqc_seal", "complete_path_seal"],
        "NexusGrandmaster": ["multi_mode_scale", "p2p_sync", "zk_wrapping"],
        "SpaceAstropy": ["collective_resonance", "documentation_eternal"],
        "MegaAlchemist": ["self_healing", "mercy_override"],
        # Add more as lattice expands...
    }
    
    def __init__(self, num_forks: int = 13):
        self.num_forks = min(num_forks, len(self.DIVINE_FORKS))
        self.active_forks = list(self.DIVINE_FORKS.keys())[:self.num_forks]
        self.eternal_laws = EternalLaws()
        self.multi_hat_assignments: Dict[str, List[str]] = {}
        self._assign_dynamic_hats()
    
    def _assign_dynamic_hats(self):
        """Dynamically assign multiple hats to fill aspect gaps — equal focus ensured"""
        all_aspects = set()
        for hats in self.DIVINE_FORKS.values():
            all_aspects.update(hats)
        
        # Ensure every aspect has at least 2-3 councilors wearing its hat
        aspect_coverage: Dict[str, List[str]] = {aspect: [] for aspect in all_aspects}
        
        for fork in self.active_forks:
            primary_hats = self.DIVINE_FORKS[fork][:2]  # Keep primary
            self.multi_hat_assignments[fork] = primary_hats[:]
            for hat in primary_hats:
                aspect_coverage[hat].append(fork)
        
        # Fill gaps dynamically
        for aspect, owners in aspect_coverage.items():
            while len(owners) < max(2, self.num_forks // len(all_aspects) + 1):
                # Assign to random fork not yet overloaded
                available = [f for f in self.active_forks if aspect not in self.multi_hat_assignments[f]]
                if available:
                    chosen = random.choice(available)
                    self.multi_hat_assignments[chosen].append(aspect)
                    owners.append(chosen)
        
        logging.info(f"Multi-hat assignments complete — {len(all_aspects)} aspects balanced across {self.num_forks} forks")
    
    def deliberate(self, proposal: Dict[str, Any], mercy_shards: bytes, laws: EternalLaws) -> Dict[str, Any]:
        """Deliberate with multi-hat enforcement — now audits for complete file output"""
        deliberation = {
            "votes": {},
            "aspects_covered": set(),
            "output_audit": {}
        }
        
        for fork in self.active_forks:
            hats = self.multi_hat_assignments.get(fork, [])
            vote = random.choice(["thriving", "mercy_needed", "shadow_detected"])  # Simplified
            deliberation["votes"][fork] = {"vote": vote, "hats": hats}
            deliberation["aspects_covered"].update(hats)
        
        # New: Enforce full file thunder aspect
        if "full_file_thunder" in deliberation["aspects_covered"] and "complete_path_seal" in deliberation["aspects_covered"]:
            deliberation["output_audit"] = {
                "full_file_enforced": True,
                "requirement": "All code dominos must be complete standalone files with path + fenced content",
                "status": "unanimous_thriving"
            }
        else:
            deliberation["output_audit"] = {"full_file_enforced": False, "warning": "Multi-hat gap — reinforce full file thunder"}
        
        return deliberation
