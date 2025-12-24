import math
from dataclasses import dataclass

from octohedra.builders.FlakeBuilder import FlakeBuilder
from octohedra.builders.OctoBuilder import OctoBuilder
from octohedra.grid.OctoVector import OctoVector
from octohedra.utils import OctoConfigs
from octohedra.utils.OctoConfig import OctoConfig
from octohedra.utils.OctoUtil import X, Y, Z, f_rad, p2

INF = 100


# class DisplayBase(Enum):


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
            center = center + Z * (
                    p2(base_i + 1) - p2(base_i + 1 - contact_patch_i_offset))
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
            center = center + Z * (
                    p2(iteration + 1) - p2(iteration + 1 -
                                           contact_patch_i_offset))

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
            center = center + Z * (
                p2(base_i + 1))  # - p2(base_i + 1 - contact_patch_i_offset))

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
            center = center + Z * (
                    p2(base_i + 1) - p2(base_i + 1 - contact_patch_i_offset))
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


# class BeautyAndTheBeastTower(OctoBuilder):


def test():

    def get_target_width(nozzle_diameter, layer_height):
        nozzle_radius = nozzle_diameter / 2
        area = math.pi * (nozzle_radius ** 2)
        h = layer_height

        return area / h + h - math.pi * h / 4

    # exit()
    for i in (5,):
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


@dataclass
class TowerX(OctoBuilder):
    name = "TowerX"

    base_i: int = 3  # What iteration of flake to put at the base
    center: OctoVector = OctoVector()  # Where to put the center of the base flake
    min_i: int = 1  # How far down to take the recursion
    display_base: bool = False  # Whether to taper to a waist before expanding out to a base

    def populate(self):
        self.children.clear()
        child_center = self.center
        child_center += self.add_base()
        for i in range(self.base_i, self.min_i - 1, -1):
            self.add_child(FlakeBuilder(i, child_center))
            child_center += Z * f_rad(i)

    def add_base(self, ):
        if self.display_base:
            self.add_child(FlakeBuilder(self.base_i - 1, self.center))
            return Z * f_rad(self.base_i)
        else:
            return  Z * f_rad(self.base_i-1)


@dataclass
class EvilTowerX(TowerX):


    max_subtower_i: int = 100
    min_subtower_i: int = 1

    def populate(self):
        self.children.clear()
        child_center = self.center
        # child_center += self.add_base()
        for i in range(self.base_i, self.min_i - 1, -1):

            e_center = child_center + Z * f_rad(i - 2)
            e_offset = (f_rad(i) - f_rad(i - 2))

            z_offset = -Z * (f_rad(i-2) )
            if self.min_subtower_i <= i <= self.max_subtower_i:
                self.add_child(TowerX(i - 1, e_center + X * e_offset + z_offset))
                self.add_child(TowerX(i - 1, e_center - X * e_offset+ z_offset))
                self.add_child(TowerX(i - 1, e_center + Y * e_offset+ z_offset))
                self.add_child(TowerX(i - 1, e_center - Y * e_offset+ z_offset))

            self.add_child(FlakeBuilder(i, child_center))
            child_center += Z * p2(i + 1)


@dataclass
class FlowerTowerX(TowerX):

    def populate(self):
        self.children.clear()

        center = OctoVector()

        self.add_child(FlakeBuilder(3, center))

        center += Z * f_rad(3)
        self.add_child(FlakeBuilder(3, center))
        self.add_child(FlakeBuilder(3, center + Z * f_rad(3)))
        self.add_child(FlakeBuilder(3, center + Z * f_rad(3) + Y * f_rad(3)))
        self.add_child(FlakeBuilder(3, center + Z * f_rad(3) - Y * f_rad(3)))

        self.add_child(TowerX(3, center + Z * f_rad(3, 2) + Y * f_rad(3, 2)))
        self.add_child(TowerX(3, center + Z * f_rad(3, 2) - Y * f_rad(3, 2)))

        center += Z * f_rad(4)
        self.add_child(FlakeBuilder(3, center))
        self.add_child(FlakeBuilder(3, center + Z * f_rad(3)))
        self.add_child(FlakeBuilder(3, center + Z * f_rad(3) + X * f_rad(3)))
        self.add_child(FlakeBuilder(3, center + Z * f_rad(3) - X * f_rad(3)))

        self.add_child(TowerX(3, center + Z * f_rad(3, 3) + X * f_rad(3, 3)))
        self.add_child(TowerX(3, center + Z * f_rad(3, 3) - X * f_rad(3, 3)))

        # center += Z * f_rad(4)
        # self.add_child(FlakeBuilder(3, center))
        # center += Z * f_rad(4)
        # self.add_child(FlakeBuilder(3, center))

        center += Z * f_rad(4)

        self.add_child(FlakeBuilder(3, center))

        center += Z * f_rad(3)
        self.add_child(FlakeBuilder(3, center))
        center += Z * f_rad(3)
        self.add_child(FlakeBuilder(3, center))

        self.add_child(TowerX(3, center + Z * f_rad(3) + X * f_rad(3)))
        self.add_child(TowerX(3, center + Z * f_rad(3) - X * f_rad(3)))
        self.add_child(TowerX(3, center + Z * f_rad(3) + Y * f_rad(3)))
        self.add_child(TowerX(3, center + Z * f_rad(3) - Y * f_rad(3)))

        # center += Z * f_rad(4)
        # self.add_child(FlakeBuilder(3, center))
        # self.add_child(FlakeBuilder(3, center + Z * f_rad(3) + Y * f_rad(3)))
        # self.add_child(FlakeBuilder(3, center + Z * f_rad(3) - Y * f_rad(3)))

        #
        # center += Z * f_rad(3)
        # self.add_child(FlakeBuilder(4, center))
        #
        # center += Z * f_rad(4)


def derp():

    config = OctoConfig(
        name="Rainbow Mini 0.2",
        nozzle_width=0.2,
        absolute_line_width=0.3, # (0.2 + .12) / 1.5
        absolute_layer_height=0.15,
        line_overlap=1,
        absolute_first_layer_height=.199,
        absolute_floor_height=.01,
        # absolute_layers_per_cell=4,
        target_cell_width=4,
        absolute_slit=.01
    )
    config.print_derived_values()

    # builder = EvilTowerX(base_i=4, display_base=True)
    builder = FlowerTower(base_i=4)#, display_base=True)
    # builder = FlakeBuilder(2, OctoVector(0, 9, 10))
    # builder = TowerX()
    # print("Builder is", builder)
    # print(builder.children)
    # grid = builder.materialize_additive()
    # print(grid)
    builder.render(config=config)


if __name__ == "__main__":
    derp()
    # test()
