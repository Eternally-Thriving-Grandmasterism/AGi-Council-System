# mycelium_growth_sim.py (v1.1 – Ultimate Symbiotic 3D Prototype + Visualization Clarity)
# Enhanced clarity: custom colormap, legend/colorbar, cross-sections, metrics trend plot

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import logging
from bio_voting_module import QuantumRNG, BioProposal, bio_council_vote
from matplotlib.colors import ListedColormap

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
        self.grid = np.zeros(self.shape, dtype=int)  # 0=empty, 1=nutrient, 2=hyphae, 3=bound, 4=algal, 5=lichen
        
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

    # _get_neighbors, _random, step unchanged for brevity (same as v1.0)

    def run(self):
        metrics_history = []
        for step in range(self.steps):
            self.step(step)
            binding = np.mean(self.grid >= 3)
            symbiosis = np.mean(self.grid == 5)
            algal = np.mean(self.grid == 4)
            metrics_history.append((binding, symbiosis, algal))
        final_binding = metrics_history[-1][0]
        final_symbiosis = metrics_history[-1][1]
        min_binding = min(m[0] for m in metrics_history)
        recovery = final_binding - min_binding
        log.info(f"Run complete – Binding: {final_binding:.2f}, Lichen Symbiosis: {final_symbiosis:.2f}, Recovery: {recovery:.2f}")
        return metrics_history

    def visualize(self, metrics_history=None):
        # Custom colormap for clarity
        colors = ['#333333', '#FFFF00', '#66B2FF', '#8B4513', '#00FF00', '#006400']  # Gray, Yellow, LightBlue, Brown, BrightGreen, DarkGreen
        cmap = ListedColormap(colors)
        bounds = [0, 1, 2, 3, 4, 5, 6]
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)
        
        fig = plt.figure(figsize=(18, 10))
        
        if self.depth <= 1:
            ax = fig.add_subplot(111)
            im = ax.imshow(self.grid[0], cmap=cmap, norm=norm)
            ax.set_title("Final 2D Symbiotic Habitat (Crystal Clear Layers)")
        else:
            # Cross-section slices (surface, mid, deep)
            slice_positions = [0, self.depth // 3, 2 * self.depth // 3, self.depth - 1]
            for i, z in enumerate(slice_positions):
                ax = fig.add_subplot(2, 4, i+1)
                im = ax.imshow(self.grid[z], cmap=cmap, norm=norm)
                ax.set_title(f"Cross-Section z={z} (Depth Layer)")
                ax.grid(False)
            
            # 3D voxel view
            ax3d = fig.add_subplot(2, 4, (5,8), projection='3d')
            bound_mask = self.grid >= 3
            x, y, z = np.indices(self.shape)
            colors_3d = np.empty(self.shape + (4,), dtype=float)
            colors_3d[self.grid == 0] = [0.2, 0.2, 0.2, 0.1]   # Transparent empty
            colors_3d[self.grid == 1] = [1.0, 1.0, 0.0, 0.5]   # Yellow nutrients
            colors_3d[self.grid == 2] = [0.4, 0.7, 1.0, 0.7]   # Light blue hyphae
            colors_3d[self.grid == 3] = [0.5, 0.3, 0.1, 0.9]   # Brown bound
            colors_3d[self.grid == 4] = [0.0, 1.0, 0.0, 0.8]   # Bright green algal
            colors_3d[self.grid == 5] = [0.0, 0.4, 0.0, 1.0]   # Dark green lichen shield
            ax3d.voxels(bound_mask, facecolors=colors_3d[bound_mask], edgecolor='k', alpha=0.8)
            ax3d.set_title("3D Eternal Habitat (Lichen Shield Prominent)")
            ax3d.set_xlabel('X'); ax3d.set_ylabel('Y'); ax3d.set_zlabel('Depth')
        
        # Legend/Colorbar
        cbar = fig.colorbar(im or plt.cm.ScalarMappable(norm=norm, cmap=cmap), ax=fig.axes, shrink=0.6)
        cbar.set_ticks([0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
        cbar.set_ticklabels(['Empty Regolith', 'Nutrients', 'Hyphae', 'Bound Mycelium', 'Algal Layer', 'Lichen Shield'])
        cbar.ax.set_title('Biological States')
        
        # Metrics trend if available
        if metrics_history:
            ax_metrics = fig.add_subplot(2, 4, 4 if self.depth > 1 else None)
            steps = range(len(metrics_history))
            binding = [m[0] for m in metrics_history]
            symbiosis = [m[1] for m in metrics_history]
            algal = [m[2] for m in metrics_history]
            ax_metrics.plot(steps, binding, label='Binding Density', color='brown')
            ax_metrics.plot(steps, symbiosis, label='Lichen Symbiosis', color='darkgreen')
            ax_metrics.plot(steps, algal, label='Algal Coverage', color='lime')
            ax_metrics.set_title('Eternal Growth Metrics')
            ax_metrics.set_xlabel('Steps')
            ax_metrics.legend()
            if self.radiation_events:
                for event in self.radiation_events:
                    ax_metrics.axvline(event, color='red', linestyle='--', alpha=0.5)
        
        plt.suptitle("Absolute Pure Truth: Symbiotic Myco-Lichen Habitat (Quantum Mercy Optimized)", fontsize=16)
        plt.tight_layout()
        plt.show()

# Run examples unchanged – now with crystal clarity
# sim = MyceliumGrowthSim(...)
# metrics = sim.run()
# sim.visualize(metrics)
