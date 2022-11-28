import math

from printing.builders.FlakeBuilder import FlakeBuilder
from printing.builders.OctoBuilder import OctoBuilder
from printing.grid.OctoVector import OctoVector
from printing.utils import OctoConfigs
from printing.utils.OctoUtil import X, Y, Z, p2

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
            self.add_child(FlakeBuilder(base_i - 1, center))
            center = center + Z * (p2(base_i + 1))  # - p2(base_i + 1 - contact_patch_i_offset))

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
            # self.add_child(FlakeBuilder(base_i - 1, center))
            # center = center + Z * (p2(base_i + 1))  # - p2(base_i + 1 - contact_patch_i_offset))
            center = center + Z * (p2(base_i + 1) - p2(base_i + 1 - contact_patch_i_offset))
        # center = center -  Z
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


def test():

    def get_target_width(nozzle_diameter, layer_height):
        nozzle_radius = nozzle_diameter / 2
        area = math.pi * (nozzle_radius ** 2)
        h = layer_height

        return area / h + h - math.pi * h / 4

    # exit()
    for i in (2,):
        # for layers in range(2, 15):
        # for overlap in (0, 0.25, 0.5, 0.75, 1):
        # for width in (.1, .12, .14, .16, .18, .2):
        # for width in (.2, 22, .24, .26, .28, .3, 0.32, 0.34, 0.36):
        # for width in (.1, .12, .14, .16, .18, .2):
        # config = OctoConfigs.config_20_rainbow_gem
        config = OctoConfigs.config_20_rainbow_speed
        # config.absolute_layers_per_cell = layers
        # config.line_overlap = overlap
        # config.absolute_line_width = width
        config.print_settings()
        config.print_derived_values()

        # Tower(i).render(config,filename="Tower")

        FlowerTower(i, elevate_base=True).render(config,
                                                 # layers=layers,
                                                 # overlap=overlap,
                                                 # width=width,
                                                 filename="Flower")
        EvilTower(i, elevate_base=True).render(config,
                                               # overlap=overlap,
                                               filename="Evil")


if __name__ == "__main__":
    test()
