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
            self.add_child(FlakeBuilder(i, c))
            c = c + Z * p2(i + 1)
            if min_evil <= i <= max_evil:
                t_i = i - 1
                t_o = p2(i + 1)
                t_z = Z * -p2(t_i + 1)
                self.add_child(Tower(i - 1, c + X * t_o + t_z, min_i))
                self.add_child(Tower(i - 1, c - X * t_o + t_z, min_i))
                self.add_child(Tower(i - 1, c + Y * t_o + t_z, min_i))
                self.add_child(Tower(i - 1, c - Y * t_o + t_z, min_i))


class FlowerTower(OctoBuilder):

    def flower_tower(self,
                     base_i,
                     center=None,
                     growth_dirs=None,
                     min_i=1,
                     max_evil=math.inf,
                     min_evil=3,
                     elevate_base=False,
                     contact_patch_i_offset=-2
                     ):
        all_dirs = {(1, 1), (1, -1), (-1, 1), (-1, -1)}
        growth_dirs = growth_dirs if growth_dirs is not None else all_dirs.copy()
        # print("Making a flower tower that grows in: ", growth_dirs)
        c = center if center is not None else Vector3(0, 0, 0)
        for i in range(base_i, min_i - 1, -1):
            self.add_child(FlakeBuilder(i, c))
            c += Z * p2(i)
            if min_evil <= i <= max_evil:
                t_i = i - 1
                t_o = p2(i)
                t_z = -p2(t_i)
                for x, y in growth_dirs:
                    # print(x, y)
                    next_dirs = all_dirs.copy()
                    next_dirs.remove((-x, -y))
                    next_dirs = {(x, y)}
                    print(next_dirs)

                    self.flower_tower(i - 1, next_dirs, c + (t_o * x, t_o * y, t_z))
                    # self.flower_tower(i-1, c + (t_o, -t_o, t_z))
                    # self.flower_tower(i-1, c + (-t_o, t_o, t_z))
                    # self.flower_tower(i-1, c + (-t_o, -t_o, t_z))

            # if i in evil or (full_evil and iteration >= i > 1):
            #     exy = 2 ** (i) - 2 ** (i - 2) if not thin_evil else p2(i)
            #     ez = z + 2 ** (i - 2) if not thin_evil else z +  p2(i, -1)
            #     sub_evil = full_evil
            #     OctoBuilder.tower(grid, i - 1, center + (exy, exy, ez), full_evil=sub_evil)
            #     OctoBuilder.tower(grid, i - 1, center + (exy, -exy, ez), full_evil=sub_evil)
            #     OctoBuilder.tower(grid, i - 1, center + (-exy, exy, ez), full_evil=sub_evil)
            #     OctoBuilder.tower(grid, i - 1, center + (-exy, -exy, ez), full_evil=sub_evil)

            # grid.make_flake(i-1, center +  (exy, exy, ez))
            # grid.make_flake(i-1, center +  (exy, -exy, ez))
            # grid.make_flake(i-1, center +  (-exy, exy, ez))
            # grid.make_flake(i-1, center + (-exy, -exy, ez))


def test():
    # i = 3
    # # tower.evil_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3, min_i=2)
    # tower.flower_tower(i, center=(0, 0, p2(i) - p2(i, - 2)), min_evil=3)
    # # tower.simple_tower(i, center=(0, 0, p2(i) - p2(i, - 2)))
    # grid = OctoGrid()
    # tower.materialize(grid)
    # grid = EvilTower(5, elevate_base=True).materialize()
    grid = Tower(3, min_iteration=1).materialize()
    config = OctoConfigs.config_25_double_bottom
    # config.absolute_layers_per_cell = 16
    config.derive()

    render_grid(grid, config=config)
    config.print_settings()


if __name__ == "__main__":
    test()
