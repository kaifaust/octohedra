import math

from euclid3 import Vector3

from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs
from printing.utils.OctoUtil import X, Y, Z, p2
from printing.utils.RenderUtils import render_grid

INF = 100


# class Growth(Enum):
#     N = (0, 1  # Unused
#     S = 2
#     E = 3
#     W = 4
#
#     ALL = {
#         Growth.NW: (-1, 1),
#         Growth.NE: (1, 1),
#         Growth.SE: (1, -1),
#         Growth.SW: (-1, -1),
#         }
#
#     @staticmethod
#     def ALL():
#         return {
#             Growth.NW: (-1, 1),
#             Growth.NE: (1, 1),
#             Growth.SE: (1, -1),
#             Growth.SW: (-1, -1),
#         }


# class OctoTowerConfig:
#
#     def __init__(self,
#                  base_i,
#                  min_i=0,
#                  center=None,
#                  max_evil=math.inf,
#                  min_evil=1
#                  ):
#         self.base_i = base_i
#         self.min_i = min_i
#         self.center = center
#         self.max_evil = max_evil
#         self.min_evil = min_evil


class Tower(OctoBuilder):

    def __init__(self, iteration: int, center=OctoVector(), min_iteration: int = 1):
        super().__init__()
        for i in range(iteration, min_iteration - 1, -1):
            self.add_child(FlakeBuilder(i, center))
            center += Z * p2(i + 1)


class HollowTower(OctoBuilder):

    def __init__(self, iteration: int, center=OctoVector(), min_iteration: int = 1,
                 elevate_base=False,
                 contact_patch_i_offset=2
                 ):
        super().__init__()

        if elevate_base:
            center = center + Z * (p2(iteration + 1) - p2(iteration + 1 - contact_patch_i_offset))

        for i in range(iteration, min_iteration - 1, -1):
            self.add_child(FlakeBuilder(i, center, i))
            center += Z * p2(i + 1)


class EvilTower(OctoBuilder):

    def __init__(self,
                 base_i,
                 center=OctoVector(),
                 min_i=1,
                 max_evil=math.inf,
                 min_evil=1,
                 elevate_base=False,
                 contact_patch_i_offset=2
                 ):

        super().__init__()

        if elevate_base:
            center = center + Z * (p2(base_i + 1) - p2(base_i + 1 - contact_patch_i_offset))
        c = center

        for i in range(base_i, min_i - 1, -1):
            self.add_child(FlakeBuilder(i, c, i))
            c = c + Z * p2(i + 1)
            if min_evil <= i <= max_evil:
                t_i = i - 1
                t_o = p2(i) + p2(i - 1)  # p2(i + 1)
                t_z = Z * (-p2(t_i + 1) - p2(t_i))
                self.add_child(Tower(i - 1, c + X * t_o + t_z, min_i))
                self.add_child(Tower(i - 1, c - X * t_o + t_z, min_i))
                self.add_child(Tower(i - 1, c + Y * t_o + t_z, min_i))
                self.add_child(Tower(i - 1, c - Y * t_o + t_z, min_i))


class FlowerTower(OctoBuilder):

    def __init__(self,
                 base_i,
                 center=OctoVector(),
                 growth_dirs=None,
                 min_i=1,
                 max_evil=math.inf,
                 min_evil=3,
                 elevate_base=True,
                 contact_patch_i_offset=1
                 ):
        super(FlowerTower, self).__init__()
        all_dirs = {(1, 0), (-1, 0), (0, 1), (0, -1)}
        growth_dirs = growth_dirs if growth_dirs is not None else all_dirs.copy()
        if elevate_base:
            center = center + Z * (p2(base_i + 1) - p2(base_i + 1 - contact_patch_i_offset))
        c = center
        for i in range(base_i, min_i - 1, -1):
            self.add_child(FlakeBuilder(i, c))
            c += Z * p2(i + 1)
            if min_evil <= i <= max_evil or True:
                t_i = i - 1
                t_o = p2(i + 1)
                t_z = -p2(t_i + 1)
                for x, y in growth_dirs:
                    next_dirs = all_dirs.copy()
                    next_dirs.remove((-x, -y))
                    next_c = c + (t_o * x, t_o * y, t_z)
                    self.add_child(FlowerTower(i - 1,
                                               next_c,
                                               next_dirs,
                                               min_i,
                                               max_evil,
                                               min_evil,
                                               False))


# def test():
#     i = 4
#     # # tower.evil_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3, min_i=2)
#     grid = FlowerTower(i, min_evil=1).materialize()
#     # # tower.simple_tower(i, center=(0, 0, p2(i) - p2(i, - 2)))
#     # grid = OctoGrid()
#     # tower.materialize(grid)
#     # grid = EvilTower(5, elevate_base=True, contact_patch_i_offset=1).materialize()
#     # grid = HollowTower(3, min_iteration=1, elevate_base=True,
#     # contact_patch_i_offset=1).materialize()
#     config = OctoConfigs.config_25_15
#     # config.absolute_layers_per_cell = 8
#     # config.derive()
#     grid.compute_trimming()
#
#     render_grid(grid, config=config)
#     config.print_settings()


def test():
    for i in (3, 4):
        for levels in (5, 6, 7, 8):
            # # tower.evil_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3, min_i=2)
            grid = FlowerTower(i, min_evil=1).materialize()
            # # tower.simple_tower(i, center=(0, 0, p2(i) - p2(i, - 2)))
            # grid = OctoGrid()
            # tower.materialize(grid)
            # grid = EvilTower(5, elevate_base=True, contact_patch_i_offset=1).materialize()
            # grid = HollowTower(3, min_iteration=1, elevate_base=True,
            # contact_patch_i_offset=1).materialize()
            config = OctoConfigs.config_25_26
            config.absolute_layers_per_cell = levels
            config.derive()
            grid.compute_trimming()

            render_grid(grid,
                        config=config,
                        i=i,
                        levels=levels,
                        width=config.line_width,
                        height=config.layer_height)
            config.print_settings()


if __name__ == "__main__":
    test()
