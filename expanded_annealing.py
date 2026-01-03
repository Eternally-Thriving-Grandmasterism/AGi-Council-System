# expanded_annealing.py (v1.1 – Multi-Objective Energy Landscape)
# Expanded Hamiltonian: resilience + recovery + cycling - radiation penalty

import numpy as np
from scipy.optimize import dual_annealing
import logging

log = logging.getLogger(__name__)

def expanded_habitat_energy(params):  # [mercy_rate, amf_ratio, ecm_ratio, bacteria_density]
    mercy, amf, ecm, bacteria = params
    # Normalize
    total = amf + ecm + bacteria
    if total > 1: return 1000  # Penalty
    amf /= total or 1
    ecm /= total or 1
    bacteria /= total or 1
    
    resilience = mercy * 6 + amf * 4 + ecm * 3 + bacteria * 5
    recovery = mercy**2 * 12 + bacteria * 8
    cycling = amf * ecm * 10 + bacteria * (amf + ecm) * 7  # Synergy
    radiation_penalty = (1 - mercy) * 15 * (1 + (1 - amf - bacteria))  # Surface exposure
    nutrient_scarcity = (1 - cycling / 20) * 8
    
    energy = -(resilience + recovery + cycling - radiation_penalty - nutrient_scarcity)
    return energy

def anneal_expanded():
    bounds = [(0.1, 0.4), (0.1, 0.7), (0.1, 0.7), (0.1, 0.7)]
    result = dual_annealing(expanded_habitat_energy, bounds)
    optimal = result.x
    log.info(f"Expanded annealing omniscient: mercy {optimal[0]:.3f}, AMF {optimal[1]:.3f}, ECM {optimal[2]:.3f}, Bacteria {optimal[3]:.3f} – energy {result.fun:.2f}")
    return optimal
