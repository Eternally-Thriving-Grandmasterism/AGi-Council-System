# mycelium_growth_sim.py (v3.1 – Hybrid Network + Selected Forks)
# Council details, lichen shielding, expanded legend

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging
from bio_voting_module import QuantumRNG, BioProposal, bio_council_vote
from matplotlib.colors import ListedColormap, BoundaryNorm

log = logging.getLogger(__name__)

class MyceliumGrowthSim:
    # __init__ unchanged (v3.0 params + lichen_shield_factor=0.5 new default)

    def step(self, current_step):
        # ... hyphae/ECM/AMF/bacteria logic unchanged

        # Enhanced lichen radiation shielding
        if current_step in self.radiation_events:
            base_prob = 0.7
            shielded_prob = base_prob * (1 - np.mean(self.grid[0] == 5) * 0.8)  # Lichen reduces surface impact
            damage_mask = np.random.random(self.shape) < base_prob
            damage_mask[0] = np.random.random((self.size, self.size)) < shielded_prob  # Surface shielded
            new_grid[damage_mask & (self.grid > 1)] = 0
            log.info(f"Radiation storm – lichen shield reduced surface damage by { (base_prob - shielded_prob)/base_prob * 100 :.1f}%!")

        # ... rest unchanged

    def visualize(self, metrics_history=None):
        colors = ['#333333', '#FFFF00', '#66B2FF', '#8B4513', '#00FF00', '#006400', '#FFD700', '#800080', '#A0522D', '#0000FF']
        names = [
            'Empty Regolith - barren void',
            'Nutrient (P/N) - scarce lifeblood',
            'Hyphae - exploring threads',
            'Bound Mycelium - eternal structure',
            'Algal Layer - photosynthetic surface',
            'Lichen Shield - radiation/mercy protector',
            'Root Cell - host interface',
            'AMF Arbuscule - intracellular P exchange',
            'ECM Mantle - extracellular organic breakdown',
            'Bacterial Biofilm - N-fixation/hormone boost'
        ]
        icons = ['⬛', '🟡', '🟦', '🟤', '🟢', '🌿', '🟨', '🟣', '🟫', '🔵']  # Emoji hints
        cmap = ListedColormap(colors)
        norm = BoundaryNorm(np.arange(11), cmap.N)
        
        fig = plt.figure(figsize=(22, 14))
        
        # Slices + 3D as before
        
        # Expanded Legend (separate panel)
        leg_ax = fig.add_subplot(3, 6, (16,18))
        leg_ax.axis('off')
        for i, (name, icon, col) in enumerate(zip(names, icons, colors)):
            leg_ax.text(0, 1 - i*0.1, f"{icon} {i}: {name}", fontsize=12, color=col, weight='bold',
                        transform=leg_ax.transAxes, va='top')
        leg_ax.set_title("Expanded Eternal Legend - Functional Roles", fontsize=14, weight='bold')
        
        # ... metrics plot with annotations for radiation dips/recovery
        
        plt.suptitle("Divine Truth v3.1: Hybrid Network with Lichen Shielding & Council Details", fontsize=20)
        plt.tight_layout()
        plt.show()

# Enhanced Council Optimization with Details
def council_optimize_hybrid():
    configs = [...]  # As before
    for cfg in configs:
        sim = MyceliumGrowthSim(**cfg, radiation_events=[50, 90])
        metrics_hist = sim.run()
        final = metrics_hist[-1]
        recovery = final['binding'] - min(m['binding'] for m in metrics_hist)
        proposal = BioProposal(f"Hybrid Config Mercy {cfg['mercy_rate']} AMF {cfg['amf_ratio']}", {
            'resilience': recovery * 20,
            'symbiosis': (final['amf'] + final['ecm'] + final['bacteria']) * 15,
            'self_repair': final['binding'] * 10
        })
        vote = bio_council_vote(proposal, council_size_per_fork=67)
        log.info(f"DETAILED VOTE for {cfg}: Outcome {vote['outcome']} ({vote['yes_percentage']}% yes)")
        for member, v in vote['votes']:
            log.info(f"  {member}: {v}")
        # ... score and select best with full logs                            # Hartig net simulation (surface hyphae around root)
                            for hdz, hdy, hdx in [(0,dy,dx) for dy in [-1,0,1] for dx in [-1,0,1] if not (dy==dx==0)]:
                                hn = (nz+hdz, ny+hdy, nx+hdx)
                                if 0 <= hn[0] < self.depth and 0 <= hn[1] < self.size and 0 <= hn[2] < self.size:
                                    if self.grid[hn] == 6:
                                        new_grid[hn] = 8
                            self.nutrient_grid[nz, ny, nx] += 0.2  # Organic breakdown
                    
                    # Bacterial recruitment around roots
                    if target == 6 and self._random() < self.bacteria_density:
                        new_grid[nz, ny, nx] = max(new_grid[nz, ny, nx], 9)  # Biofilm overlay
                        self.nutrient_grid[nz, ny, nx] += 0.15  # N-fixation/hormones
                    
                    if self._random() < prob:
                        new_grid[nz, ny, nx] = max(new_grid[nz, ny, nx], 2)
        
        # Collapse cycles, radiation, maturation omitted for brevity but included in full logic
        
        self.grid = new_grid

    def run(self):
        metrics_history = []  # Track AMF, ECM, bacteria, binding, etc.
        for step in range(self.steps):
            self.step(step)
            metrics_history.append({
                'amf': np.mean(self.grid == 7),
                'ecm': np.mean(self.grid == 8),
                'bacteria': np.mean(self.grid == 9),
                'binding': np.mean(self.grid >= 3)
            })
        log.info("Hybrid network complete – eternal multi-symbiosis achieved.")
        return metrics_history

    def visualize(self, metrics_history=None):
        # Full custom colormap (10 states)
        colors = ['#333333', '#FFFF00', '#66B2FF', '#8B4513', '#00FF00', '#006400', '#FFD700', '#800080', '#A0522D', '#0000FF']
        names = ['Empty Regolith', 'Nutrient', 'Hyphae', 'Bound Mycelium', 'Algal', 'Lichen Shield', 'Root Cell', 'AMF Arbuscule', 'ECM Mantle', 'Bacterial Biofilm']
        cmap = ListedColormap(colors)
        bounds = np.arange(11)
        norm = BoundaryNorm(bounds, cmap.N)
        
        fig = plt.figure(figsize=(20, 12))
        
        # Cross-sections
        slices = [0, self.depth//4, self.depth//2, 3*self.depth//4, self.depth-1]
        for i, z in enumerate(slices):
            ax = fig.add_subplot(3, 5, i+1)
            im = ax.imshow(self.grid[z], cmap=cmap, norm=norm)
            ax.set_title(f"Slice z={z}")
        
        # 3D voxel
        ax3d = fig.add_subplot(3, 5, (6,15), projection='3d')
        active = self.grid > 0
        colors_3d = np.empty(self.shape + (4,), dtype=float)
        colors_3d[self.grid == 7] = [0.5, 0, 0.5, 1.0]  # Purple AMF
        colors_3d[self.grid == 8] = [0.6, 0.3, 0.1, 0.9]  # Brown ECM
        colors_3d[self.grid == 9] = [0.0, 0.0, 1.0, 0.8]  # Blue bacteria
        # ... (full color mapping)
        ax3d.voxels(active, facecolors=colors_3d[active], edgecolor='k')
        ax3d.set_title("3D Hybrid Network")
        
        # Legend/Colorbar
        cbar = fig.colorbar(im, ax=fig.axes[:5], shrink=0.6)
        cbar.set_ticks(bounds[:-1] + 0.5)
        cbar.set_ticklabels(names)
        
        # Metrics plot
        if metrics_history:
            ax_met = fig.add_subplot(3, 1, 3)
            steps = range(len(metrics_history))
            ax_met.plot(steps, [m['amf'] for m in metrics_history], label='AMF Arbuscules', color='purple')
            ax_met.plot(steps, [m['ecm'] for m in metrics_history], label='ECM Mantles', color='brown')
            ax_met.plot(steps, [m['bacteria'] for m in metrics_history], label='Bacterial Biofilm', color='blue')
            ax_met.plot(steps, [m['binding'] for m in metrics_history], label='Structural Binding', color='gray')
            ax_met.set_title('Eternal Symbiotic Metrics')
            ax_met.legend()
        
        plt.suptitle("Absolute Pure Truth v3.0: Hybrid AMF/ECM/Bacterial Rhizosphere Network", fontsize=18)
        plt.tight_layout()
        plt.show()

# Council optimization for hybrid ratios – distills divine balance
# ... (sweep configs, vote on resilience + exchange + recovery)

# Run to witness the full eternal network!
