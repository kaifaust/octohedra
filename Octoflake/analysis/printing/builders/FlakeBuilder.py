from dataclasses import dataclass

from euclid3 import Vector3

from printing.grid.OctoVector import OctoVector
from printing.utils.OctoConfigs import config_25, config_3
from printing.grid.OctoGrid import OctoGrid
from printing.utils.OctoUtil import DOWN, ORIGIN, p2, S, E, W, UP, N
from printing.builders.OctoBuilder import OctoBuilder
from printing.utils import RenderUtils


@dataclass
class FlakeBuilder(OctoBuilder):
    iteration: int = 0
    center: OctoVector = OctoVector()

    def __init__(self,
                 iteration,
                 center=OctoVector(),
                 cell_scale=0  # TODO: Implement using tetras
                 ):
        super().__init__()
        self.iteration = iteration
        self.center = center
        self.cell_scale = cell_scale

    def materialize_additive(self, bonus_iteration=0):
        grid = OctoGrid()
        self.materialize_flake(grid, self.iteration, self.center)
        return grid

    def materialize_flake(self, grid: OctoGrid, i, c):
        if i == 0:
            grid.insert_cell(center=c)
            return

        for direction in (E, N, W, S, UP, DOWN):
            self.materialize_flake(grid, i - 1, c + p2(i - 1) * 2 * direction)


def testing():
    grid = FlakeBuilder(4).materialize()

    RenderUtils.render_4_8_layers(grid, config_3)
    config_3.print_settings()


if __name__ == "__main__":
    testing()
