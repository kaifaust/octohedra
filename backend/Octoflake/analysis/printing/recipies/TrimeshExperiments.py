import numpy as np
import trimesh.primitives

from printing.builders.TowerBuilders import EvilTower
from printing.utils import OctoConfigs, RenderUtils

config = OctoConfigs.config_25_big

trimesh.primitives.Cylinder()

for i in range(3, 5):
    for overlap in np.linspace(0, 1, 4):
        for layers in (6, 8, 10):

            grid = EvilTower(i, elevate_base=True, contact_patch_i_offset=1).materialize()
            grid.crop_bottom()
            grid.compute_trimming()

            config.absolute_layers_per_cell = layers
            config.line_overlap = overlap
            config.derive()
            config.print_settings()
            config.print_derived_values()

            RenderUtils.render_grid(grid,
                                    config,
                                    filename=f"star.stl",
                                    i=i,
                                    overlap=overlap,
                                    layers=layers)
