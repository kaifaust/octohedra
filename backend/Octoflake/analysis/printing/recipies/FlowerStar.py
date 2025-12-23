from functools import reduce

from euclid3 import Vector3

from printing.builders.FlakeBuilder import FlakeBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.utils import RenderUtils
from printing.utils.OctoConfigs import config_25
from printing.utils.OctoUtil import X, Z, p2

flakes = set()


i = 4

# flakes.add(OctoFlake.make_flake(i))
# flakes.add(OctoFlake.make_flake(i - 1, p2(i) * Z))

flakes.add(FlakeBuilder.make_flake(i - 1, Vector3(p2(i), 0, (p2(i) + p2(i)))))



grids = [flake.materialize() for flake in flakes]

grid = reduce(OctoGrid.merge, grids)
grid.four_way()
grid.six_way()

RenderUtils.render_grid(grid, config_25)
