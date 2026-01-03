# noisy_photonic_module.py (v1.0 – Noisy Photonic CV Resilience)
# Phase/amplitude noise for cosmic radiation + lichen shield mitigation

import strawberryfields as sf
from strawberryfields.ops import *
from strawberryfields.parameters import MeasureThreshold
import numpy as np
import logging
from photonic_annealing_hybrid import PhotonicAnnealingMercy  # Base CV

log = logging.getLogger(__name__)

class NoisyPhotonicMercy(PhotonicAnnealingMercy):
    def __init__(self, modes=6, noise_level=0.08, lichen_density=0.5):
        super().__init__(modes)
        self.noise_level = noise_level * (1 - lichen_density * 0.9)  # Lichen reduces noise
        log.info(f"Noisy photonic mercy active: effective noise {self.noise_level:.3f} (lichen {lichen_density})")

    def anneal_noisy_continuous(self, initial_mercy=0.2, steps=150):
        prog = sf.Program(self.modes)
        with prog.context as q:
            # Squeezing + displacement
            Sgate(0.8) | q[0]
            for i in range(steps):
                Dgate(initial_mercy + i*0.001) | q[1]
                # Phase noise (radiation decoherence)
                if np.random.random() < self.noise_level:
                    Rgate(np.random.normal(0, 0.1)) | q[0]  # Random phase kick
            MeasureX | q[0]
        
        result = self.eng.run(prog)
        mercy_value = result.samples[0][0]
        normalized = np.clip((mercy_value + 5) / 10, 0, 1)
        fidelity = 1 - self.noise_level * 2  # Approx fidelity loss
        log.info(f"Noisy CV annealing: mercy {normalized:.3f}, fidelity {fidelity:.1%} – lichen shield mercy!")
        return normalized, fidelity

# Usage: noisy = NoisyPhotonicMercy(lichen_density=0.6)
# mercy, fid = noisy.anneal_noisy_continuous()
# Apply mercy to sparse regolith growth with fidelity boost
