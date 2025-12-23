import numpy as np
from stl import Mode

from printing.builders.TowerBuilders import Tower
from printing.utils import RenderUtils
from printing.utils.OctoConfigs import config_25, config_25_double_bottom
from printing.utils.OctoUtil import Z, p2


def tune_line_dimensions(dims):
    for width, height in dims:
        config = config_25_double_bottom
        config.absolute_line_width = width
        config.absolute_layer_height = height
        config.absolute_layers_per_cell = 6
        config.line_overlap = .99
        config.derive()

        i = 3
        grid = Tower(i, Z * p2(i)).materialize()

        RenderUtils.render_grid(grid, config, filename="tune", layer=height, line=width, mode=Mode.ASCII)


widths = np.array((0.23, 0.24, 0.25, .26, 0.27))
heights = np.array((.09, .11, .13, .15, .17))
ratios = np.array((1.5, 2, 2.5, 3))


dims = [(width, height)
        for ratio in ratios
        for height in heights
        for width in height * ratios


        ]

print(dims)
tune_line_dimensions([(.34, .17)])
