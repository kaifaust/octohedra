import math

import numpy as np
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

    def __init__(self,
                 base_i: int,
                 center=OctoVector(),
                 min_iteration: int = 1,
                 elevate_base=False,
                 contact_patch_i_offset=1
                 ):
        super().__init__()
        if elevate_base:
            center = center + Z * (p2(base_i + 1) - p2(base_i + 1 - contact_patch_i_offset))
        for i in range(base_i, min_iteration - 1, -1):
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
                 contact_patch_i_offset=1
                 ):

        super().__init__()

        if elevate_base:
            center = center + Z * (p2(base_i + 1) - p2(base_i + 1 - contact_patch_i_offset))
        c = center

        for i in range(base_i, min_i - 1, -1):
            self.add_child(FlakeBuilder(i, c))
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
                                               # {(x, y)},
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
    # i = 7
    # layers = 5
    # config = OctoConfigs.config_25_big
    # config = OctoConfigs.config_2_small
    # config.absolute_layers_per_cell = layers
    # config.print_settings()
    # config.print_derived_values()
    #
    # # for width in (.24,):
    # #     config.absolute_line_width = width
    # # FlowerTower(i).render(config, i=i, layers=layers, filename="flower",
    # width=config.line_width)
    # # EvilTower(i, elevate_base=True).render(config, i=i, layers=layers, filename="evil")
    # Tower(i, elevate_base=True).render(config, i=i, layers=layers, filename="regular")

    # exit()
    for i in (4,):
         # for width in (0.17, .18, .19, .2, .21, .22, .23, .24, .25):
             # for height in np.arange(0.05, 0.12, 0.01):
        #  for layers in (5, 6, 7, 10, 15):
        # for overlap in np.linspace(.99, .0, 9):

                # config = OctoConfigs.config_25
                config = OctoConfigs.config_20_thin
                # config.line_overlap = overlap
                # config = OctoConfigs.config_2_small
                # config.absolute_layers_per_cell = 8
                # config.absolute_layers_per_cell = layers
                # config.target_overlap_cell_ratio = 5
                # config.absolute_line_width = width
                # height = width/2
                # config.absolute_layer_height = height

                # floor = 1.5 * height if 1.5 * height > 0.15 else 1.5 * height
                # config.absolute_floor_height = floor

                config.print_settings()
                config.print_derived_values()

                # for width in (.24,):
                #     config.absolute_line_width = width
                # FlowerTower(i).render(config, i=i, layers=layers, filename="flowerprocess")
                FlowerTower(i, elevate_base=True).render(config, #f=config.floor_height,  h=config.layer_height,
                                                         # w=config.line_width,
                                                         filename="e")
                # EvilTower(i, elevate_base=True).render(config, w=width, h=height, f=floor, filename="e")
                # Tower(i, elevate_base=True).render(config, i=i, layers=layers, filename="regular")


if __name__ == "__main__":
    test()
