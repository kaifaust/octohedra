from euclid3 import Vector3

from printing.utils.OctoConfigs import config_25
from printing.grid.OctoGrid import OctoGrid
from printing.utils.OctoUtil import DOWN, ORIGIN, p2, S, E, W, UP, N
from printing.builders.OctoBuilder import OctoBuilder
from printing.utils import RenderUtils


class OctoFlake(OctoBuilder):
    def __init__(self, iteration, center: Vector3 = None, cell_scale=0):
        super().__init__()
        self.iteration = iteration
        self.center = center if center is not None else ORIGIN
        self.cell_scale = cell_scale

    def materialize_additive(self, bonus_iteration=0):

        grid = OctoGrid()
        self.materialize_flake(grid, self.iteration, self.center)
        print(grid)
        return grid

    def materialize_subtractive(self, grid, bonus_iteration=0):
        """Nothing to remove"""
        pass

    def materialize_flake(self, grid: OctoGrid, i, c):
        if i == 0:
            grid.insert_cell(c)
            return

        for direction in (E, N, W, S, UP, DOWN):
            self.materialize_flake(grid, i - 1, c + p2(i - 1) * direction)

    @classmethod
    def make_flake(cls, iteration: int, center: Vector3 = None, cell_scale=0):
        center = center if center is not None else Vector3(0, 0, 0)
        return OctoFlake(iteration, center, cell_scale)


def testing():
    builder = OctoBuilder.builder()
    builder += OctoFlake.make_flake(3)

    RenderUtils.render_grid(builder.materialize(), config_25)


if __name__ == "__main__":
    testing()
