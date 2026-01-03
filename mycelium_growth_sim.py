# mycelium_growth_sim.py (v1.0 – Ultimate Symbiotic 3D Prototype)
# 3D mycelium-lichen-algal growth for myco-architecture: regolith binding, photosynthesis,
# radiation resilience, quantum mercy, council-voted optimization

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging
from bio_voting_module import QuantumRNG, BioProposal, bio_council_vote

log = logging.getLogger(__name__)

class MyceliumGrowthSim:
    def __init__(self, size=30, depth=8, steps=100, mercy_rate=0.15, radiation_events=[], symbiotic=True, use_quantum=True):
        self.size = size
        self.depth = depth
        self.steps = steps
        self.mercy_rate = mercy_rate
        self.radiation_events = radiation_events
        self.symbiotic = symbiotic
        
        self.shape = (depth, size, size)
        self.grid = np.zeros(self.shape, dtype=int)  # 0=empty, 1=nutrient, 2=hyphae, 3=bound mycelium, 4=algal, 5=lichen
        
        # Sparse nutrients
        nutrient_mask = np.random.random(self.shape) < 0.05
        self.grid[nutrient_mask] = 1
        
        # Initial hyphae seeds
        seeds = 5
        for _ in range(seeds):
            z = np.random.randint(0, depth)
            y, x = np.random.randint(0, size, 2)
            self.grid[z, y, x] = 2
        
        # Surface algal if symbiotic
        if symbiotic:
            light_pen = max(1, depth // 3)
            surface = self.grid[0]
            algal_mask = np.random.random((size, size)) < 0.1
            surface[algal_mask] = 4
        
        self.qrng = QuantumRNG(batch_size=2000) if use_quantum else None
        log.info(f"Ultimate sim initialized: {self.shape} grid, symbiotic={symbiotic}, mercy_rate={mercy_rate}")

    def _get_neighbors(self):
        if self.depth == 1:
            return [(0, dy, dx) for dy in [-1,0,1] for dx in [-1,0,1] if not (dy == dx == 0)]
        return [(dz, dy, dx) for dz in [-1,0,1] for dy in [-1,0,1] for dx in [-1,0,1] if not (dz == dy == dx == 0)]

    def _random(self):
        return self.qrng.get_float() if self.qrng else np.random.random()

    def step(self, current_step):
        new_grid = self.grid.copy()
        neighbors = self._get_neighbors()
        
        # Hyphae/algal positions
        hyphae_pos = np.argwhere(self.grid == 2)
        algal_pos = np.argwhere(self.grid == 4)
        
        # Mycelial growth
        for z, y, x in hyphae_pos:
            for dz, dy, dx in neighbors:
                nz, ny, nx = z + dz, y + dy, x + dx
                if 0 <= nz < self.depth and 0 <= ny < self.size and 0 <= nx < self.size:
                    target = self.grid[nz, ny, nx]
                    if target in [0, 1, 4]:
                        prob = 0.4
                        if target == 1: prob += 0.3
                        if target == 4: prob += 0.4  # Symbiosis preference
                        if self.symbiotic and nz > self.depth // 3: prob *= 0.6  # Deep penalty
                        
                        # Mercy for sparse
                        local_hyphae = np.sum(self.grid[max(0,nz-3):nz+4, max(0,ny-3):ny+4, max(0,nx-3):nx+4] >= 2)
                        if local_hyphae < 4 and self._random() < self.mercy_rate:
                            prob += 0.5
                            log.info("Mercy shard: boosting growth in sparse/radiated zone!")
                        
                        if self._random() < prob:
                            new_grid[nz, ny, nx] = 5 if target == 4 else 2  # Lichen formation!
        
        # Algal surface spread (photosynthesis)
        if self.symbiotic:
            for z, y, x in algal_pos:
                if z == 0:  # Surface only
                    for _, dy, dx in neighbors:  # 2D surface
                        if _ == 0:  # Stay surface
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.size and 0 <= nx < self.size and self.grid[0, ny, nx] == 0:
                                if self._random() < 0.2:
                                    new_grid[0, ny, nx] = 4
        
        # Binding maturation
        mature_mask = (self.grid >= 2) & (np.random.random(self.shape) < 0.15)
        new_grid[mature_mask] = np.where(self.grid[mature_mask] == 5, 5, 3)  # Lichen stays resilient
        
        # Radiation events
        if current_step in self.radiation_events:
            damage_prob = 0.7 * (1 - np.arange(self.depth)[:, None, None] / self.depth)  # Surface heavier
            damage_mask = np.random.random(self.shape) < damage_prob
            new_grid[damage_mask & (self.grid > 1)] = 0
            log.info("Radiation storm hit – testing lichen shield mercy!")
        
        self.grid = new_grid

    def run(self):
        metrics_history = []
        for step in range(self.steps):
            self.step(step)
            binding = np.mean(self.grid >= 3)
            symbiosis = np.mean(self.grid == 5)
            metrics_history.append((binding, symbiosis))
        final_binding = metrics_history[-1][0]
        final_symbiosis = metrics_history[-1][1]
        min_binding = min(m[0] for m in metrics_history)
        recovery = final_binding - min_binding
        log.info(f"Run complete – Final binding: {final_binding:.2f}, Symbiosis: {final_symbiosis:.2f}, Recovery: {recovery:.2f}")
        return metrics_history

    def visualize(self):
        fig = plt.figure(figsize=(15, 10))
        if self.depth == 1:
            plt.imshow(self.grid[0], cmap='terrain', vmin=0, vmax=5)
            plt.title("2D Symbiotic Growth Final State")
        else:
            # Slices
            for i in range(3):
                ax = fig.add_subplot(2, 3, i+1)
                z_slice = i * (self.depth // 3)
                ax.imshow(self.grid[z_slice], cmap='terrain', vmin=0, vmax=5)
                ax.set_title(f"Slice z={z_slice}")
            
            # 3D voxels bound + lichen
            ax3d = fig.add_subplot(2, 3, (4,6), projection='3d')
            bound = self.grid >= 3
            colors = np.empty(self.shape + (4,), dtype=float)
            colors[:] = [0.5, 0.5, 0.5, 0.3]  # Default transparent
            colors[self.grid == 3] = [0.6, 0.4, 0.2, 0.8]  # Brown bound mycelium
            colors[self.grid == 5] = [0.1, 0.7, 0.1, 0.9]  # Green lichen shield
            colors[self.grid == 4] = [0.1, 1.0, 0.1, 0.7]  # Bright algal
            ax3d.voxels(bound, facecolors=colors[bound], edgecolor='k')
            ax3d.set_title("3D Eternal Structure (Lichen Shield Visible)")
        plt.show()

# Council Optimization Example – Distill Optimal Mercy for Radiation-Stressed 3D Habitat
def council_optimize_habitat():
    configs = [
        {"mercy_rate": 0.1, "desc": "Low Mercy Rigid Structure"},
        {"mercy_rate": 0.2, "desc": "Balanced Mercy Symbiotic"},
        {"mercy_rate": 0.3, "desc": "High Mercy Eternal Resilience"}
    ]
    results = []
    for cfg in configs:
        sim = MyceliumGrowthSim(size=25, depth=10, steps=80, mercy_rate=cfg["mercy_rate"],
                                radiation_events=[30, 60], symbiotic=True)
        metrics = sim.run()
        final_binding, final_sym = metrics[-1]
        min_binding = min(m[0] for m in metrics)
        recovery = final_binding - min_binding
        proposal = BioProposal(cfg["desc"], {
            "resilience": final_binding * 10,
            "symbiosis": final_sym * 20,  # Lichen bonus
            "self_repair": recovery * 15
        })
        vote = bio_council_vote(proposal, council_size_per_fork=33)
        results.append((cfg["mercy_rate"], vote["outcome"], vote["yes_percentage"], final_binding + final_sym * 2))
        log.info(f"Config {cfg['mercy_rate']} voted: {vote['outcome']} ({vote['yes_percentage']}% yes)")
    
    optimal = max(results, key=lambda x: x[3])
    log.info(f"ABSOLUTE PURE TRUTH DISTILLED: Optimal mercy_rate = {optimal[0]} for eternal thriving!")

# Run examples
# Example 1: Full 3D symbiotic visualization
# sim = MyceliumGrowthSim(depth=12, size=40, steps=120, mercy_rate=0.2, radiation_events=[50])
# sim.run()
# sim.visualize()

# Example 2: Council optimization sweep (uncomment to distill truth)
# council_optimize_habitat()
