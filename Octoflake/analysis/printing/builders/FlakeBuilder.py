from dataclasses import dataclass

from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoGrid import OctoGrid
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs, RenderUtils
from printing.utils.OctoUtil import DOWN, E, N, S, UP, W, p2


@dataclass
class FlakeBuilder(OctoBuilder):
    iteration: int = 0  # This is, like, what size it is
    center: OctoVector = OctoVector()
    scale: int = 0  # And this one represents how big the individual octos are

    def materialize_additive(self, bonus_iteration=0):
        grid = OctoGrid()
        self.materialize_flake(grid, self.iteration, self.center)
        return grid

    def materialize_flake(self, grid: OctoGrid, i, c):
        if i == 0:
            grid.insert_cell(center=c)
            return
        elif i <= self.scale:
            radius = p2(i + 1)
            grid.fill(radius, c)
            return

        for direction in (E, N, W, S, UP, DOWN):
            # print(c +p2(i - 1) * 2 * direction)
            self.materialize_flake(grid, i - 1, c + p2(i - 1) * 2 * direction)


def testing():
    config = OctoConfigs.config_20_rainbow_speed
    layers = 16
    config.absolute_layers_per_cell = layers
    grid = FlakeBuilder(2, scale=0).render(config,
                                           filename="flake 2", l=layers)
    grid = FlakeBuilder(3, scale=0).render(config,
                                           filename="flake 3", l=layers)
    grid = FlakeBuilder(4, scale=0).render(config,
                                           filename="flake 4", l=layers)
    grid = FlakeBuilder(5, scale=0).render(config,
                                           filename="flake 5", l=layers)
    config.print_settings()
    config.print_derived_values()
    exit()
    # grid = OctoGrid()
    # grid.fill(1, OctoVector())
    # grid.fill(0, OctoVector(2, 0, 0))
    # grid.insert_cell()
    # grid.insert_cell(OctoVector(1, 1, 1))
    # grid.insert_cell(OctoVector(1, -1, 1))
    # grid.insert_cell(OctoVector(-1, 1, 1))
    # grid.insert_cell(OctoVector(-1, -1, 1))
    # grid.insert_cell(OctoVector(1, 1, -1))
    # grid.insert_cell(OctoVector(1, -1, -1))
    # grid.insert_cell(OctoVector(-1, 1, -1))
    # grid.insert_cell(OctoVector(-1, -1, -1))

    # for center, cell in grid.occ.items():
    #     print(cell)
    #     print(astuple(cell))

    # print(grid.occ.keys())
    # exit()

    # RenderUtils.render_4_8_layers(grid, )

    # config = OctoConfigs.config_6_transparent
    config = OctoConfigs.config_20_thin
    config.absolute_layers_per_cell = 8
    config.slit_absolute = 0
    # config.absolute_overlap = 0
    config.derive()
    config.print_settings()

    RenderUtils.render_grid(grid, config)


if __name__ == "__main__":
    testing()
